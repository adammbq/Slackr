'''Import necessary libraries'''
import threading
from datetime import datetime, timezone
from server.data_funcs import get_data, pickle_data
from server.helper_funcs import (get_channel, get_user_from_token, get_next_message_id,
                                 valid_message_len, user_in_channel, get_msg_from_msg_id,
                                 message_contains_react, get_react_from_react_id,
                                 user_is_admin_or_owner, user_sent_message, generate_search_result,
                                 valid_react_id, generate_react_info, perm_id_is_admin_owner,
                                 generate_message_info, user_in_channel_with_msg)
from server.Error import ValueError, AccessError

def send_message(token, channel_id, message_str):
    """
    Send a message to the channel associated with channel_id
    """
    data = get_data()
    channel = get_channel(data, channel_id)
    user = get_user_from_token(data, token)
    message_id = get_next_message_id(data)

    if not valid_message_len(message_str):
        raise ValueError("Message too long")
    if not user_in_channel(user['u_id'], channel):
        raise AccessError("User is not in channel")

    # get the current time in utc
    now = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    # set up the information to save in the 'database'
    message_info = generate_message_info(channel_id, message_id, user['u_id'], message_str, now)

    # insert the message into the front of the message ids
    # stored in the channel
    channel['message_ids'].insert(0, message_id)
    # add the message object to the messages list
    data['messages'].append(message_info)
    pickle_data(data)
    return {'message_id' : message_id}

def pin_message(token, message_id):
    """
    Pin message with message_id
    """
    data = get_data()
    user = get_user_from_token(data, token)
    message = get_msg_from_msg_id(data, message_id)
    # if the message does not exist, raise error
    if message is None:
        raise ValueError("Invalid message_id")

    channel = get_channel(data, message['channel_id'])
    if not perm_id_is_admin_owner(user['perm_id']):
        raise ValueError("User is not an admin or owner")
    if message['is_pinned']:
        raise ValueError("Message is already pinned")
    if not user_in_channel(user['u_id'], channel):
        raise AccessError("User not part of channel that the message is within")
    # set the pin flag on the message to True
    message['is_pinned'] = True
    pickle_data(data)
    return {}

def unpin_message(token, message_id):
    """
    Unpin message with message_id
    """
    data = get_data()
    user = get_user_from_token(data, token)
    message = get_msg_from_msg_id(data, message_id)
    if message is None:
        raise ValueError("Invalid message_id")
    channel = get_channel(data, message['channel_id'])
    if not perm_id_is_admin_owner(user['perm_id']):
        raise ValueError("User is not an admin or owner")
    if not message['is_pinned']:
        raise ValueError("Message is not pinned")
    if not user_in_channel(user['u_id'], channel):
        raise AccessError("User not part of channel that the message is within")

    # set the pin flag on the message to False
    message['is_pinned'] = False
    pickle_data(data)
    return {}

def react_message(token, message_id, react_id):
    """
    React message with message_id with react_id
    """
    data = get_data()
    user = get_user_from_token(data, token)
    message = get_msg_from_msg_id(data, message_id)
    if message is None or not user_in_channel_with_msg(data, user['u_id'], message):
        raise ValueError('Message is not in the channel')
    if not valid_react_id(react_id):
        raise ValueError('Invalid react id')
    if message_contains_react(message, user['u_id']):
        raise ValueError('Message already has that react')

    react = get_react_from_react_id(message, react_id)
    # if there are no current reacts, create a new data structure
    # and store the information. Otherwise, add only the user id
    if react is None:
        react_info = generate_react_info(react_id, user['u_id'])
        message['reacts'].append(react_info)
    else:
        react['u_ids'].append(user['u_id'])
    pickle_data(data)
    return {}

def unreact_message(token, message_id, react_id):
    """
    Unreact message with message_id with react_id
    """
    data = get_data()
    user = get_user_from_token(data, token)
    message = get_msg_from_msg_id(data, message_id)
    if message is None or not user_in_channel_with_msg(data, user['u_id'], message):
        raise ValueError('Message is not in the channel')
    if not valid_react_id(react_id):
        raise ValueError('Invalid react id')
    if not message_contains_react(message, user['u_id']):
        raise ValueError('Message does not have that react')

    # get the react object and delete the user u_id
    react = get_react_from_react_id(message, react_id)
    react['u_ids'].remove(user['u_id'])
    react['is_this_user_reacted'] = False
    pickle_data(data)
    return {}

def remove_message(token, message_id):
    """
    Remove message with message_id from channel
    """
    data = get_data()
    user = get_user_from_token(data, token)
    message = get_msg_from_msg_id(data, message_id)
    if message is None:
        raise ValueError('Message no longer exists')

    channel = get_channel(data, message['channel_id'])
    if not user_sent_message(user['u_id'], message) and not user_is_admin_or_owner(user, channel):
        raise AccessError("User did not send message or not enough privileges")

    # remove the message object and the message_id from the 'database'
    data['messages'].remove(message)
    channel['message_ids'].remove(message_id)
    pickle_data(data)
    return {}

def edit_message(token, message_id, message_str):
    """
    Edit message with message_id with new message
    If message is empty, delete the message
    """
    if len(message_str) == 0:
        return remove_message(token, message_id)
    data = get_data()
    og_message = get_msg_from_msg_id(data, message_id)
    user = get_user_from_token(data, token)
    channel = get_channel(data, og_message['channel_id'])
    # check if user did not send original message and user is admin/owner
    if (not user_sent_message(user['u_id'], og_message) and
            not user_is_admin_or_owner(user, channel)):
        raise AccessError("User did not send message or not enough privileges")
    # edit the original message with the new message
    og_message['message'] = message_str
    pickle_data(data)
    return {}

def message_search(token, query_str):
    """
    Search the entire message history for any message containing the substring query_str
    """
    data = get_data()
    search_results = []
    # loop though every message in the 'database'
    for message in data['messages']:
        # if query_str is a substring of message, add the relevent details
        # to search_results list
        if query_str in message['message']:
            # create search_result function here
            result = generate_search_result(message)
            search_results.append(result)
    return search_results

def send_later(token, channel_id, message_str, time_sent):
    """
    Send a message to channel with channel_id at time time_sent
    """
    data = get_data()
    user = get_user_from_token(data, token)
    channel = get_channel(data, channel_id)
    now = datetime.now().timestamp()
    # get the difference between the time_sent parameter and the current time
    time_diff = time_sent - now

    if channel is None:
        raise ValueError('channel does not exist')
    if not valid_message_len(message_str):
        raise ValueError('message is too long')
    if time_diff < 0:
        # time_sent is in the past
        raise ValueError('invalid date')
    if not user_in_channel(user['u_id'], channel):
        raise ValueError('user not part of channel')
    # set a timer to call send_message once time_diff seconds are finished
    timer = threading.Timer(time_diff, send_message, [token, channel_id, message_str])
    timer.start()
