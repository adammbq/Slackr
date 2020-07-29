''' import needed modules '''
import re
import hashlib
import time
import random
import jwt

def get_secret():
    '''
    returns the secret
    '''
    return 'comp1531'

def find_user(data, email):
    '''
    Look through the data and find user based of email
    '''
    for user in data['users']:
        if user['email'] == email:
            return user
    return None

def find_email(data, email):
    '''
    Return True if email exists
    '''
    for user in data['users']:
        if user['email'] == email:
            return True
    return False

def get_user_from_token(data, token):
    '''
    Decode the token and return the user
    '''
    decoded = jwt.decode(token, get_secret(), algorithms=['HS256'])
    return find_user(data, decoded['email'])

def check_email(email):
    '''
    Check if email is valid syntactically
    '''
    email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # pass the regualar expression
    # and the string in search() method
    if re.search(email_regex, email):
        return True
    return False

def is_email_registered(data, email):
    '''
    Check if email has been registered before
    '''
    return find_user(data, email) != None

def check_password(data, email, password):
    '''
    Check if email and password passed in matches what is in the 'database'
    '''
    for user in data['users']:
        if user['email'] == email and user['password'] == hash_password(password):
            return True
    return False

def check_name_len(name):
    '''
    Check if the name length is valid
    '''
    return len(name) <= 50

def valid_message_len(message):
    '''
    Check if the message length is valid
    '''
    return len(message) <= 1000

def generate_token(email):
    '''
    Generate token based off email and current time
    '''
    payload = {
        'email': email,
        'timestamp': time.time()
    }
    # encode using jwt
    encoded = jwt.encode(payload, get_secret(), algorithm='HS256')
    return encoded.decode('utf-8')

def generate_handle(data, name_first, name_last):
    '''
    Generate user handle
    If a handle already exists, add a number on to the end
    '''
    handle = (name_first + name_last).lower()
    count = 0
    new_handle = handle
    # loop through each user
    for index in range(len(data['users'])):
        # if same handle is found, add a number and restart loop
        if data['users'][index]['handle'] == new_handle:
            count += 1
            index = 0
            new_handle = handle + str(count)
    return new_handle

def hash_password(password):
    '''
    Return the hashed password
    '''
    return hashlib.sha256(password.encode()).hexdigest()

def generate_profile(u_id, email, password, name_first, name_last, handle, perm_id, token):
    '''
    Return a profile dictionary
    '''
    return {
        'u_id': u_id,
        'email': email,
        'password': hash_password(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle': handle,
        'perm_id': perm_id,
        'tokens': [token],
        'profile_img_url': ""
        }

def valid_channel_name(name):
    '''
    Check if channel name is valid
    '''
    return len(name) <= 20

def user_in_channel(u_id, channel):
    '''
    Return True if the user with u_id is in channel
    '''
    for user in channel['members']:
        if user['u_id'] == u_id:
            return True
    return False

def get_channel(data, channel_id):
    '''
    Return the channel with channel_id
    '''
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return None

def get_user_from_u_id(data, u_id):
    '''
    Return the user with u_id
    '''
    for user in data['users']:
        if user['u_id'] == u_id:
            return user
    return None

def get_next_message_id(data):
    '''
    Get the next message_id based off how many messages have been sent
    '''
    if len(data['messages']) >= 1:
        return data['messages'][-1]['message_id'] + 1
    return 0

def get_msg_from_msg_id(data, message_id):
    '''
    Get message with message_id
    '''
    for message in data['messages']:
        if message['message_id'] == message_id:
            return message
    return None

def get_react_from_react_id(message, react_id):
    '''
    Get react with react_id from message
    '''
    for react in message['reacts']:
        if react['react_id'] == react_id:
            return react
    return None

def user_sent_message(u_id, message):
    '''
    Return True if message was sent by user with u_id
    '''
    if u_id == message['u_id']:
        return True
    return False

def message_contains_react(message, u_id):
    '''
    Return 1 if the user with u_id has reacted to the message
    '''
    for react in message['reacts']:
        if u_id in react['u_ids']:
            return True
    return False

def perm_id_is_admin_owner(perm_id):
    '''
    Return whether a permission id represents a member
    '''
    member_perm_id = 3
    return perm_id != member_perm_id

def user_is_admin_or_owner(user, channel):
    '''
    Return 1 if the user is an admin/owner of slakr or owner of channel
    '''
    return (user_is_owner_channel(user, channel) or
            perm_id_is_admin_owner(user['perm_id']))

def user_is_owner_channel(user, channel):
    '''
    Return 1 if user is the owner of channel
    '''
    for user_info in channel['owners']:
        if user['u_id'] == user_info['u_id']:
            return True
    return False

def return_messages(data, message_ids, token):
    '''
    Return a list with the message info of messages with ids in message_ids
    '''
    messages = []
    user = get_user_from_token(data, token)
    for message in data['messages']:
        if message['message_id'] in message_ids:
            message = user_reacted(user, message)
            message_info = {
                'message_id' : message['message_id'],
                'u_id' : message['u_id'],
                'message' : message['message'],
                'reacts' : message['reacts'],
                'time_created' : message['time_created'],
                'is_pinned' : message['is_pinned']
            }
            messages.insert(0, message_info)
    return messages

def user_reacted(user, message):
    '''
    For each react, set the is_this_user_reacted variable to True or False
    based off if the user has reacted to the message
    '''
    for react in message['reacts']:
        if user['u_id'] in react['u_ids']:
            react['is_this_user_reacted'] = True
        else:
            react['is_this_user_reacted'] = False
    return message

def generate_user_info(user):
    '''
    Return the user info
    '''
    return {
        'u_id': user['u_id'],
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle'],
        'profile_img_url': user['profile_img_url']
    }

def generate_member_info(member):
    '''
    Return member info
    '''
    return {
        'u_id': member['u_id'],
        'name_first': member['name_first'],
        'name_last': member['name_last'],
        'profile_img_url': member['profile_img_url']
    }

def get_members(members):
    '''
    Return list of members info
    '''
    members_info = []
    for member in members:
        member_info = generate_member_info(member)
        members_info.append(member_info)
    return members_info

def is_standup_active(channel):
    '''
    Return 1 if channel has a current standup
    '''
    return channel['standup_active']

def generate_search_result(message):
    '''
    Generate the search result dictionary
    '''
    return {
        'message_id' : message['message_id'],
        'u_id' : message['u_id'],
        'message' : message['message'],
        'reacts' : message['reacts'],
        'time_created' : message['time_created'],
        'is_pinned' : message['is_pinned']
        }

def valid_react_id(react_id):
    '''
    Return True if react id is valid else False
    '''
    return react_id == 1

def generate_react_info(react_id, u_id):
    '''
    Generate react info dictionary
    '''
    return {
        'react_id': react_id,
        'u_ids': [u_id],
        'is_this_user_reacted': True
        }

def generate_message_info(channel_id, message_id, user_id, message_str, now):
    '''
    Generate message info dictionary
    '''
    return {
        'channel_id' : channel_id,
        'message_id' : message_id,
        'u_id' : user_id,
        'message' : message_str,
        'reacts' : [],
        'time_created' : now,
        'is_pinned' : False
    }

def generate_channel_info(channel_id, name, user_info, is_public):
    '''
    Generate channel info dictionary
    '''
    return {
        'channel_id': channel_id,
        'name': name,
        'owners': [user_info],
        'members': [user_info],
        'message_ids': [],
        'is_public': True if is_public == 'true' else False,
        'standup_active': False,
        'standup_finish': None,
        'standup_messages': []
    }

def user_in_channel_with_msg(data, user_id, message):
    '''
    Return True if the user is in the channel a message is sent in
    '''
    channel = get_channel(data, message['channel_id'])
    for member in channel['members']:
        if member['u_id'] == user_id:
            return True
    return False

def valid_image_coords(x_start, y_start, x_end, y_end, width, height):
    '''
    Return True if the x and y coordinates are within proper boundaries
    '''
    return (0 <= x_start < x_end <= width  and
            0 <= y_start < y_end <= height)

def generate_request_code():
    '''
    Genearte a random 5 digit string for the reset code
    '''
    split_code = [str(random.randint(0, 9)) for i in range(5)]
    return ''.join(split_code)

def remove_user_with_u_id(channel, u_id, mode='all'):
    '''
    Remove a user from the channel based off what mode
    modes: owners, all
    '''
    for owner in channel['owners']:
        if owner['u_id'] == u_id:
            channel['owners'].remove(owner)
            break

    if mode == 'all':
        for member in channel['members']:
            if member['u_id'] == u_id:
                channel['members'].remove(member)
                break
