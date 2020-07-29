''' import needed modules '''
from server.data_funcs import get_data, pickle_data
from server.helper_funcs import (valid_channel_name, get_user_from_token,
                                 generate_user_info, user_in_channel, get_user_from_u_id,
                                 get_channel, user_is_admin_or_owner, user_is_owner_channel,
                                 return_messages, generate_channel_info, remove_user_with_u_id,
                                 get_members)
from server.Error import ValueError, AccessError

OWNER_ID = 1
ADMIN_ID = 2
MEMBER_ID = 3

def create_channel(token, name, is_public):
    '''
    create a channel using a token, the name of the channel
    and whether the channel is public or private.
    '''
    data = get_data()
    # check if the name is valid
    if not valid_channel_name(name):
        raise ValueError('Name is too long')
    user = get_user_from_token(data, token)
    channel_id = len(data['channels'])
    user_info = generate_user_info(user)
    # create a dict for all the information of a channel
    channel_info = generate_channel_info(channel_id, name, user_info, is_public)
    data['channels'].append(channel_info)

    pickle_data(data)
    return {'channel_id': channel_id}


def list_user_channels(token):
    '''
    Given a user's token, this function will list all the channels that this user is in
    '''
    data = get_data()
    user = get_user_from_token(data, token)

    channels = []
    # loop through the channels and find if the user is either an owner or member
    for channel in data['channels']:
        if user_in_channel(user['u_id'], channel):
            user_channel = {
                'channel_id': channel['channel_id'],
                'name': channel['name']
            }
            channels.append(user_channel)

    pickle_data(data)
    return {'channels': channels}


def list_all_user_channels(token):
    '''
    Given a user's token, this function will list all the channels in slackr
    '''
    data = get_data()
    channels = []

    # loop through the channels and add them to the channels list
    for channel in data['channels']:
        user_channel = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channels.append(user_channel)

    pickle_data(data)
    return {'channels': channels}

def invite_user(token, channel_id, u_id):
    '''
    Given a user's token, channel_id, and another user's u_id,
    invite the user with the given u_id into the channel with the channel_id so long
    as the user with token has the correct permissions (is an admin or owner of channel)
    '''
    data = get_data()
    inviting_user = get_user_from_token(data, token)
    user_to_add = get_user_from_u_id(data, u_id)
    channel = get_channel(data, channel_id)
    #if channel does not exist or the user is not in the channel
    if channel is None:
        raise ValueError('invalid channel id')
    if user_to_add is None:
        raise ValueError('invalid user id')
    if not user_in_channel(inviting_user['u_id'], channel):
        raise AccessError('user not part of channel')
    # add user to the channel
    user_info = generate_user_info(user_to_add)
    channel['members'].append(user_info)

    pickle_data(data)
    return {}

def join_channel(token, channel_id):
    '''
    given a user's token and a channel_id, the user can join the channel as long as the channel
    is private or the user has permissions such as being an admin or owner of slackr
    '''
    data = get_data()
    user = get_user_from_token(data, token)
    channel = get_channel(data, channel_id)
    #print(user_in_channel(user['email'], channel))
    if channel is None or user_in_channel(user['u_id'], channel):
        raise ValueError('invalid channel id')
    if user['perm_id'] == MEMBER_ID and not channel['is_public']:
        raise AccessError('User is not an admin or owner of slackr')
    user_info = generate_user_info(user)
    channel['members'].append(user_info)
    pickle_data(data)
    return {}


def leave_channel(token, channel_id):
    '''
    given a user's token and a channel_id, the user will leave the channel with channel_id as long
    as the user is part of the channel
    '''
    data = get_data()
    user = get_user_from_token(data, token)
    channel = get_channel(data, channel_id)

    #checks if the user is in the channel
    if not user_in_channel(user['u_id'], channel):
        raise ValueError("User not part of channel")

    user_info = generate_user_info(user)

    remove_user_with_u_id(channel, user_info['u_id'])
    pickle_data(data)
    return {}


def addowner_channel(token, channel_id, u_id):
    '''
    given a token of a user and a channel_id and another user's u_id, the user with u_id is
    promoted to being an owner of the channel with channel_id as long as the user with token
    has permissions to do so (is an admin or owner)
    '''
    data = get_data()
    owner_user = get_user_from_token(data, token)
    channel = get_channel(data, channel_id)
    promoted_user = get_user_from_u_id(data, u_id)

    if channel is None:
        raise ValueError("Channel does not exist")
    if user_is_owner_channel(promoted_user, channel):
        raise ValueError("User with u_id is already owner of channel")
    if not user_is_admin_or_owner(owner_user, channel):
        raise AccessError("Not enough permissions to add user as owner")

    user_info = generate_user_info(promoted_user)
    channel['owners'].append(user_info)
    pickle_data(data)
    return {}

def details_channel(token, channel_id):
    '''
    given a token of a user and a channel_id, show the owners and members of the channel
    with channel_id as long as the user is a member of the channel
    '''
    data = get_data()
    user = get_user_from_token(data, token)
    channel = get_channel(data, channel_id)
    if channel is None:
        raise ValueError('invalid channel id')
    if not user_in_channel(user['u_id'], channel):
        raise AccessError('user not part of channel')

    pickle_data(data)
    return {
        'name': channel['name'],
        'owner_members' : get_members(channel['owners']),
        'all_members' : get_members(channel['members'])
    }

def removeowner_channel(token, channel_id, u_id):
    '''
    given a token, channel_id and a u_id, remove ownership of the user
    with u_id as long as the user was originally an owner and the user with token
    is also an owner
    '''
    data = get_data()
    owner_user = get_user_from_token(data, token)
    channel = get_channel(data, channel_id)
    removed_user = get_user_from_u_id(data, u_id)
    if channel is None or not user_in_channel(owner_user['u_id'], channel):
        raise ValueError('invalid channel id')
    if not user_is_owner_channel(removed_user, channel) or owner_user['perm_id'] != OWNER_ID:
        raise ValueError('User is not an owner of channel or slackr')
    user_info = generate_user_info(removed_user)
    #channel['owners'].remove(user_info)
    remove_user_with_u_id(channel, user_info['u_id'], mode='owners')
    pickle_data(data)
    return {}

def get_messages(token, channel_id, start):
    '''
    given a token, channel_id and the start, show all th emessages in channel with
    channel_id after the start as long as the user with token is part of the channel
    '''
    data = get_data()
    user = get_user_from_token(data, token)
    channel = get_channel(data, channel_id)
    
    if channel is None:
        raise ValueError('Channel does not exist')

    num_messages = len(channel['message_ids'])
    if start > num_messages:
        raise ValueError('Start is greater than the total number of messages')
    if not user_in_channel(user['u_id'], channel):
        raise AccessError('User is not in channel')
    end = start + 50
    if end > num_messages:
        end = -1
        messages = return_messages(data, channel['message_ids'][start:], token)
    else:
        messages = return_messages(data, channel['message_ids'][start:end], token)
    return {
        'messages': messages,
        'start': start,
        'end': end
    }
