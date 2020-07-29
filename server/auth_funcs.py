'''
Auth functions including register, login, logout, password reset quest, email reset request,
and admin permission change
'''

import random
from server.data_funcs import pickle_data, get_data
from server.helper_funcs import (check_email, find_user, check_name_len, generate_token, generate_handle,
                          generate_profile, find_email, check_password, get_user_from_token,
                          get_user_from_u_id, hash_password, generate_request_code)
from server.Error import ValueError, AccessError

OWNER_ID = 1
ADMIN_ID = 2
MEMBER_ID = 3

def register(email, password, name_first, name_last):
    '''
    Registers a user using given parameters and stores in data
    (email, password, name, name_first, name_last)
    Will fail when the entered email is already in use or any of the inputs
    are invalid.
    Returns a dictionary with the users u_id and token
    '''
    data = get_data()
    if (check_email(email) and find_user(data, email) is None and len(password) > 5
            and check_name_len(name_first) and check_name_len(name_last)):
        # these functions are in the auth_helper file
        token = generate_token(email)
        handle = generate_handle(data, name_first, name_last)
        u_id = len(data['users'])
        perm_id = MEMBER_ID
        if u_id == 0:
            perm_id = OWNER_ID

        profile = generate_profile(u_id, email, password, name_first, name_last, handle, perm_id,
                                   token)
        #profile['tokens'].append(token)
        # add the profile, email and token to the "database"
        data['users'].append(profile)
        pickle_data(data)
        return {"u_id": profile['u_id'], "token": token}
    if find_email(data, email):
        raise ValueError(description="The entered email has already been registered.")
    raise ValueError(description="Invalid email, password, first name or last name")

def login(email, password):
    '''
    Given an email and a password, logs a user in with correct credentials.
    Will raise a ValueError if incorrect credentials have been inputted.
    Returns a dictionary consisting of users u_id and token.
    '''
    data = get_data()
    #print(data)
    # variables to the keep the result to reduce clutter
    email_ok = check_email(email) and find_email(data, email)
    password_ok = check_password(data, email, password)

    if not email_ok or not password_ok:
        raise ValueError(description="Invalid email or password")
    token = generate_token(email)
    user = find_user(data, email)
    # add the token to the logged in users
    user['tokens'].append(token)
    pickle_data(data)
    return {
        "u_id": user['u_id'],
        "token": token
        }

def logout(token):
    '''
    Logs user out given their token.
    Returns True if succesful and false otherwise.
    '''
    data = get_data()
    # if the user with token has logged in, log them out
    user = get_user_from_token(data, token)
    if user is not None:
        user['tokens'].remove(token)
        pickle_data(data)
        return {"is_success" : True}

    return {"is_success" : False}

def request_reset(email):
    '''
    Given an email address, if the user is registered, sends them an email
    containing a secret code, that when entered allows user to reset password
    Will return Value Errors if: email is invalid, password is invalid, code is invalid.
    Returns an empty dictionary.
    '''
    data = get_data()
    code = generate_request_code()
    data['valid_reset'][code] = email
    pickle_data(data)
    if find_user(data, email) is not None:
        return code

    raise ValueError(description='Invalid email')

def reset_reset(code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password
    provided.
    Will raise ValueErrors if: password is invalid, or code is invalid.
    Returns an empty dictionary.
    '''
    data = get_data()

    if len(new_password) < 5:
        raise ValueError(description="Invalid password")
    if code not in data['valid_reset']:
        raise ValueError(description="Invalid code")
    # get associated email and token
    email = data['valid_reset'][code]
    user = find_user(data, email)
    # set the new password
    del data['valid_reset'][code]
    user['password'] = hash_password(new_password)
    pickle_data(data)
    return {}

def permission_change(token, u_id, permission_id):
    '''
    Given a user by their u_id, set their permissions to new permissions
    described by permission_id.
    Will raise a ValueError if: u_id is invalid, permission is invalid,
    or authorized user is not an owner or admin.
    Returns an empty dictionary.
    '''
    data = get_data()
    auth_user = get_user_from_token(data, token)
    changing_user = get_user_from_u_id(data, u_id)
    if changing_user is None:
        raise ValueError(description='Invalid u_id')
    if permission_id not in [1, 2, 3]:
        raise ValueError(description='Invalid permission_id')
    if auth_user['perm_id'] == MEMBER_ID:
        raise AccessError(description='Authorised user is not an owner or admin')

    changing_user['perm_id'] = permission_id
    pickle_data(data)
    return {}
