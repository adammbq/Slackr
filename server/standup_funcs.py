import threading
from datetime import datetime, timedelta

from server.data_funcs import get_data, pickle_data
from server.helper_funcs import (get_channel, get_user_from_token, is_standup_active,
                          user_in_channel, valid_message_len)
from server.Error import ValueError, AccessError
from server.message_funcs import send_message


'''
For a given channel, start the standup period whereby for
the next 15 minutes if someone calls "standup_send" with a message,
it is buffered during the 15 minute window then at the end of
the 15 minute window a message will be added to the message queue
in the channel from the user who started the standup.
'''
def start_standup(token, channel_id, length):
    '''
    Start a standup
    Length is in seconds
    '''
    data = get_data()
    channel = get_channel(data, channel_id)
    user = get_user_from_token(data, token)
    # If the channel is Invalid
    if channel == None:
        raise ValueError(description='Invalid Channel')
    # If the channel is alreay in stadup mode
    if is_standup_active(channel):
        raise ValueError(description='Standup is already active')
    # If the user is not in this channel
    if not user_in_channel(user['u_id'], channel):
        raise AccessError(description='User is not in channel')
    # Else start a start up session
    channel['standup_active'] = True

    # setup the timer for with the length specified
    timer = threading.Timer(length, stop_standup, [token, channel_id])
    time_finish = (datetime.now() + timedelta(seconds=length)).timestamp()
    channel['standup_finish'] = time_finish

    pickle_data(data)
    timer.start()
    return {'time_finish': time_finish}

def active_standup(token, channel_id):
    '''
    check if standup is active
    '''
    data = get_data()
    channel = get_channel(data, channel_id)
    if channel == None:
        raise ValueError(description='Invalid Channel')

    return {
        'is_active': channel['standup_active'],
        'time_finish': channel['standup_finish']
    }

def send_standup(token, channel_id, message_str):
    '''
    Send message to standup
    '''
    data = get_data()
    channel = get_channel(data, channel_id)
    user = get_user_from_token(data, token)
    # If the channel is invalid
    if channel == None:
        raise ValueError(description='Invalid Channel')
    # If the message is too long
    if not valid_message_len(message_str):
        raise ValueError(description='Invalid Channel') 
    # If the channel is already in stand up mode
    if not is_standup_active(channel):
        raise ValueError(description='No active standup')
    # If the curret user is not in the channel
    if not user_in_channel(user['u_id'], channel):
        raise AccessError(description='User is not in channel')

    user_message = f"{user['name_first']}: {message_str}"
    channel['standup_messages'].append(user_message)
    pickle_data(data)
    return {}

def stop_standup(token, channel_id):
    '''
    stop current standup
    '''
    data = get_data()
    channel = get_channel(data, channel_id)
    
    channel['standup_active'] = False
    channel['standup_finish'] = None
    message = ' '.join(channel['standup_messages'])
    channel['standup_messages'] = []
    pickle_data(data)
    send_message(token, channel['channel_id'], message)
