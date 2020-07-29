import pytest
import time
from datetime import datetime
from server.message_funcs import *
from server.auth_funcs import *
from server.channel_funcs import *
from server.standup_funcs import *
from server.data_funcs import *

LENGTH = 1

def test_start_standup_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    create_channel(b['token'], 'another channel', 'true')
    time_inbetween = (datetime.now() + timedelta(seconds=LENGTH)).timestamp()
    # check that the standup finish is within plus minus 1 second
    assert time_inbetween - 1 <= start_standup(a['token'], 0, LENGTH)['time_finish'] <= time_inbetween + 1
    assert time_inbetween - 1 <= start_standup(b['token'], 1, LENGTH)['time_finish'] <= time_inbetween + 1

def test_start_standup_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    create_channel(b['token'], 'another channel', 'true')
    # standup already active
    start_standup(a['token'], 0, LENGTH)
    with pytest.raises(Exception):
        assert start_standup(a['token'], 0, LENGTH)

    # invalid channel
    with pytest.raises(Exception):
        assert start_standup(a['token'], 2, LENGTH)

    #user not in channel
    with pytest.raises(Exception):
        assert start_standup(a['token'], 1, LENGTH)

def test_send_standup_valid():
    time.sleep(LENGTH)
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    start_standup(a['token'], 0, LENGTH)

    assert send_standup(a['token'], 0, 'hello there') == {}
    assert send_standup(a['token'], 0, 'a' * 1000) == {}

def test_send_standup_invalid():
    time.sleep(LENGTH)
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')

    # no standup active
    with pytest.raises(Exception):
        assert send_standup(a['token'], 0, 'hello there')

    start_standup(a['token'], 0, LENGTH)
    # invalid channel
    with pytest.raises(Exception):
        assert send_standup(a['token'], 1, 'message')

    # message too long
    with pytest.raises(Exception):
        assert send_standup(a['token'], 0, 'a' * 1001)
        
    # user not in channel
    with pytest.raises(Exception):
        assert send_standup(b['token'], 0, 'i am not in channel')

def test_active_standup_valid():
    time.sleep(LENGTH)
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    t = start_standup(a['token'], 0, LENGTH)
    assert active_standup(a['token'], 0) == {'is_active': True, 'time_finish': t['time_finish']}
    
    time.sleep(LENGTH + 1) # wait for standup to finish
    assert active_standup(a['token'], 0) == {'is_active': False, 'time_finish': None}

def test_active_standup_invalid():
    time.sleep(LENGTH)
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')

    # channel does not exist
    with pytest.raises(Exception):
        assert active_standup(a['token'], 1)



