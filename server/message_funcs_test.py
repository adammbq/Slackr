import pytest
from datetime import datetime, timedelta
from server.message_funcs import *
from server.auth_funcs import *
from server.channel_funcs import *
from server.data_funcs import *

def test_message_edit():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    assert edit_message(a['token'],0, 'new_message') == {}
    assert edit_message(a['token'],1, 'new_message') == {}
    assert edit_message(a['token'], 0, '') == {}

def test_message_edit_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    join_channel(b['token'], 0)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')

    with pytest.raises(Exception):
        # user did not send message
        assert edit_message(b['token'], 0, 'new_message')

def test_react_message_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    assert pin_message(a['token'], 0) == {}
    assert pin_message(a['token'], 1) == {}

def test_react_message_invalid():
    clear_data()
    a = register("cl@c.com", "funnnny", "ma", "jauan")
    b = register("new@c.com", "funnnny", "ma", "jauan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi')

    with pytest.raises(Exception):
        # when message_id is not a valid message 
        # within a channel that the authorised user has joined
        assert pin_message(a['token'], 15)
        assert pin_message(a['token'], 40)

    with pytest.raises(Exception):
        assert pin_message(b['token'], 0)

    pin_message(a['token'], 0)
    with pytest.raises(Exception):
        # Message with ID message_id already contains an active pin with ID react_id
        assert pin_message(a['token'], 0)

    permission_change(a['token'], 0, 3)
    with pytest.raises(Exception):
        # user not owner/admin
        assert pin_message(a['token'], 0)
        assert pin_message(a['token'], 1)

def test_react_message_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    assert react_message(a['token'], 0, 1) == {}
    assert react_message(a['token'], 1, 1) == {}

def test_react_message_invalid():
    clear_data()
    a = register("cl@c.com", "funnnny", "ma", "jauan")
    b = register("new@c.com", "funnnny", "ma", "jauan")
    create_channel(a['token'], 'new channel', 'true')
    join_channel(b['token'], 0)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi')
    react_message(a['token'], 0, 1)
    react_message(b['token'], 0, 1)

    with pytest.raises(Exception):
        # when message_id is not a valid message 
        # within a channel that the authorised user has joined
        assert react_message(a['token'], 15, 1)
        assert react_message(a['token'], 40, 1)

    with pytest.raises(Exception):
        # When react_id is not a valid React ID
        assert react_message(a['token'], 0, 9)
        assert react_message(a['token'], 1, 6)

    with pytest.raises(Exception):
        # Message with ID message_id already contains an active React with ID react_id
        assert react_message(a['token'], 0, 1)



def test_remove_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    assert remove_message(a['token'],0) == {}
    assert remove_message(a['token'],1) == {}

def test_remove_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    remove_message(a['token'], 0)

    with pytest.raises(Exception):
        # user did not send message
        assert remove_message(b['token'], 1)

    with pytest.raises(Exception):
        # message no longer exists
        assert remove_message(a['token'],0)

    permission_change(a['token'], 0, 3)
    with pytest.raises(Exception):
        # When user does not have sufficient permsissions to remove message
        assert remove_message(a['token'],1)
        
ch = "a"
long_string = ch * 1001
string99 = ch * 999

def test_send_message_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    assert send_message(a['token'], 0, "message") == {'message_id': 0}
    assert send_message(a['token'], 0, " ") == {'message_id': 1}
    assert send_message(a['token'], 0, string99) == {'message_id': 2}
    assert send_message(a['token'], 0, "1") == {'message_id': 3}

def test_send_message_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    with pytest.raises(Exception):
        # string too long
        assert send_message(a['token'], 0, long_string)

    with pytest.raises(Exception):
        # user not part of channel
        assert send_message(b['token'], 0, 'hi there')

def test_message_unpin_message_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    pin_message(a['token'], 0)
    pin_message(a['token'], 1)

    assert unpin_message(a['token'], 0) == {}
    assert unpin_message(a['token'], 1) == {}


def test_message_unpin_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')

    with pytest.raises(Exception):
        # when message_id is not a valid message 
        # within a channel that the authorised user has joined
        assert unpin_message(a['token'], 5)
        assert unpin_message(a['token'], 18)

    with pytest.raises(Exception):
        # user not part of channel
        assert unpin_message(b['token'], 0)
        assert unpin_message(b['token'], 1)

    with pytest.raises(Exception):
        # Message with ID message_id does not contai an active pin with ID react_id
        assert unpin_message(a['token'], 0)
        assert unpin_message(a['token'], 1)

    permission_change(a['token'], 0, 3)
    with pytest.raises(Exception):
        # user not owner/admin
        assert unpin_message(a['token'], 0)
        assert unpin_message(a['token'], 1)


def test_message_unreact_message_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    join_channel(b['token'], 0)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    react_message(a['token'], 0, 1)
    react_message(b['token'], 1, 1)

    assert unreact_message(a['token'], 0, 1) == {}
    assert unreact_message(b['token'], 1, 1) == {}


def test_message_unreact_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', 'true')
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')

    with pytest.raises(Exception):
        # when message_id is not a valid message 
        # within a channel that the authorised user has joined
        assert unreact_message(a['token'], 5, 1)
        assert unreact_message(a['token'], 18, 1)

    with pytest.raises(Exception):
        # When react_id is not a valid React ID
        assert unreact_message(a['token'], 0, 9)
        assert unreact_message(a['token'], 1, 6)

    with pytest.raises(Exception):
        # Message with ID message_id does not contai an active React with ID react_id
        assert unreact_message(a['token'], 0, 1)
        assert unreact_message(a['token'], 1, 1)

def test_message_search():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', True)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    m = message_search(a['token'], 'there') 
    del m[0]['time_created']
    del m[1]['time_created']
    assert m == [{
                'message_id' : 0,
                'u_id' : 0,
                'message' : 'hello there',
                'reacts' : [],
                'is_pinned' : 0
            },
            {
                'message_id' : 1,
                'u_id' : 0,
                'message' : 'hi there',
                'reacts' : [],
                'is_pinned' : 0
            }]
    assert message_search(a['token'], 'noo') == []
    

def test_message_unpin_message_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', True)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    pin_message(a['token'], 0)
    pin_message(a['token'], 1)

    assert unpin_message(a['token'], 0) == {}
    assert unpin_message(a['token'], 1) == {}


def test_message_unpin_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', True)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    permission_change(a['token'], 1, 1)
    pin_message(a['token'], 0)


    with pytest.raises(Exception):
        # when message_id is not a valid message 
        # within a channel that the authorised user has joined
        assert unpin_message(a['token'], 5)
        assert unpin_message(a['token'], 18)

    with pytest.raises(Exception):
        # user not part of channel
        assert unpin_message(b['token'], 0)

    with pytest.raises(Exception):
    	# message not pinned
        assert unpin_message(b['token'], 1)

    with pytest.raises(Exception):
        # Message with ID message_id does not contai an active pin with ID react_id
        assert unpin_message(a['token'], 0)
        assert unpin_message(a['token'], 1)

    permission_change(a['token'], 0, 3)
    with pytest.raises(Exception):
        # user not owner/admin
        assert unpin_message(a['token'], 0)
        assert unpin_message(a['token'], 1)


def test_pin_message_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("m243.juan@unsw.edu.au", "123456", "m", "juan")
    create_channel(a['token'], 'new channel', True)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi there')
    assert pin_message(a['token'], 0) == {}
    assert pin_message(a['token'], 1) == {}

def test_pin_message_invalid():
    clear_data()
    a = register("cl@c.com", "funnnny", "ma", "jauan")
    b = register("new@c.com", "funnnny", "ma", "jauan")
    create_channel(a['token'], 'new channel', True)
    send_message(a['token'], 0, 'hello there')
    send_message(a['token'], 0, 'hi')
    permission_change(a['token'], 1, 1)

    with pytest.raises(Exception):
        # when message_id is not a valid message 
        # within a channel that the authorised user has joined
        assert pin_message(a['token'], 15)
        assert pin_message(a['token'], 40)

    with pytest.raises(Exception):
        assert pin_message(b['token'], 0)

    pin_message(a['token'], 0)
    with pytest.raises(Exception):
        # Message with ID message_id already contains an active pin with ID react_id
        assert pin_message(a['token'], 0)

    permission_change(a['token'], 0, 3)
    with pytest.raises(Exception):
        # user not owner/admin
        assert pin_message(a['token'], 0)
        assert pin_message(a['token'], 1)

def test_send_later_invalid():
    clear_data()
    a = register("cl@c.com", "funnnny", "ma", "jauan")
    b = register("new@c.com", "funnnny", "ma", "jauan")
    create_channel(a['token'], 'new channel', True)
    time = (datetime.now() + timedelta(seconds=60)).timestamp()

    with pytest.raises(Exception):
        # time is in the past
        assert send_later(a['token'], 0, 'aaa', (datetime.now() - timedelta(seconds=3)).timestamp())
    
    with pytest.raises(Exception):
        # invalid channel
        assert send_later(a['token'], 1, 'hello there', time)

    with pytest.raises(Exception):
        # invalid string
        assert send_later(a['token'], 0, 'a' * 1001, time)
    
    with pytest.raises(Exception):
        assert send_later(b['token'], 0, 'hi', time)
    #user is not in channel





