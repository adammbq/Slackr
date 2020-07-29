''' import needed modules '''
import urllib.request
import imghdr
from PIL import Image

from server.data_funcs import get_data, pickle_data
from server.helper_funcs import (get_user_from_u_id, get_user_from_token,
                                 check_email, generate_user_info,
                                 valid_image_coords)
from server.Error import ValueError

def get_user_profile(token, u_id):
    '''
    set_get_profile
    For a valid user, returns information about their
    email, first name, last name, and handle
    '''
    data = get_data()
    user = get_user_from_u_id(data, u_id)
    # If the user is not valid
    if user == None:
        raise ValueError(description="User with u_id is not a valid user")
    # If the user is valid
    user_profile = generate_user_info(user)
    #pickle_data(data)
    return user_profile

def set_user_email(token, email):
    '''
    set_user_email
    Update the authorised user's email
    '''
    data = get_data()
    user = get_user_from_token(data, token)

    if not check_email(email):
        raise ValueError("Email entered is not a valid email")
    for index in data['users']:
        if email in index['email']:
            raise ValueError(description="Email address is already being used by another user")
    user['email'] = email
    pickle_data(data)
    return {}

def set_user_name(token, name_first, name_last):
    '''
    set_user_name
    Update the authorised user's first and last name
    '''
    data = get_data()
    user = get_user_from_token(data, token)

    # If the name is not valid
    if len(name_first) > 50:
        raise ValueError(description="First name too long")
    if len(name_last) > 50:
        raise ValueError(description="Last name too long")
    # Else update the name
    user['name_first'] = name_first
    user['name_last'] = name_last
    pickle_data(data)
    return {}

def set_user_handle(token, handle_str):
    '''
    set_user_handle
    Update the authorised user's handel
    '''
    data = get_data()
    user = get_user_from_token(data, token)
    # If the size of the token is out of range
    if not (3 <= len(handle_str) <= 20):
        raise ValueError(description="Handle must be between 3 and 20 characters")
    # If the handle is registered under a different user
    for index in data['users']:
        if handle_str in index['handle']:
            raise ValueError(description="Handle is already used by another user")
    # Else set current user's handle to the new handle
    user['handle'] = handle_str
    pickle_data(data)
    return {}

def get_all_users(token):
    '''
    Get all user information
    '''
    data = get_data()
    user = get_user_from_token(data, token)
    users = []
    for user in data['users']:
        users.append(generate_user_info(user))

    return {'users': users}


def upload_photo(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Upload a photo for the user's profile
    '''
    data = get_data()
    user = get_user_from_token(data, token)

    tmp_file_name = f"./frontend/prebundle/images/tmp.jpg"
    save_file_name = f"./frontend/prebundle/images/{user['u_id']}.jpg"

    # save the url under the temp file name if the url is valid
    try:
        urllib.request.urlretrieve(img_url, tmp_file_name)
    except:
        raise ValueError(description='Invalid Image Url')

    image = Image.open(tmp_file_name)
    width, height = image.size
    # check the boundaries of the image
    if not valid_image_coords(x_start, y_start, x_end, y_end, width, height):
        raise ValueError(description='Cropping values are out of bounds')

    # check for invalid image type

    if imghdr.what(tmp_file_name) != 'jpeg':
        raise ValueError(description='Image is not a JPEG')

    # crop the image and save under the save file name
    cropped = image.crop((x_start, y_start, x_end, y_end))
    cropped.save(save_file_name)

    user['profile_img_url'] = f"/images/{user['u_id']}.jpg"
    pickle_data(data)
    return {}
