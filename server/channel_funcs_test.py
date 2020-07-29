import pytest
from server.auth_funcs import *
from server.channel_funcs import *
from server.message_funcs import *
from server.data_funcs import *

def test_channel_invite(): #Testing all valid cases
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")
    c = register("matt@mail.com", "password", "matt", "juan")
    create_channel(a['token'], 'new channel', 'true')
    assert invite_user(a['token'], 0, b['u_id']) == {}

 
def test_channel_invite_exceptions(): 
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")
    c = register("matt@mail.com", "password", "matt", "juan")

    create_channel(a['token'], 'new channel', 'true')
    create_channel(b['token'], 'newer channel', 'true')

    with pytest.raises(Exception):
        #invalid u_id/ user does not exist
        assert invite_user(a['token'], 0, 10)

    with pytest.raises(Exception):
        #invalid channel_id/ channel does not exist
        assert invite_user(a['token'], 2, b['u_id'])


    with pytest.raises(Exception):
        #when authorized user tries to invite a user to channel they are not apart of
        assert invite_user(c['token'], 1, a['u_id'])

def test_channel_leave_valid():
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")

    create_channel(a['token'], 'new channel', 'true')
    invite_user(a['token'], 0, b['u_id'])

    assert leave_channel(b['token'], 0) == {}
    assert leave_channel(a['token'], 0) == {}



def test_channel_leave_exceptions():
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")
    c = register("matt@mail.com", "password", "matt", "juan")

    create_channel(a['token'], 'new channel', 'true')
    invite_user(a['token'], 0, b['u_id'])
    #when channel_id refers to an invalid channel
    with pytest.raises(Exception):
        assert leave_channel(b['token'], 1)

    with pytest.raises(Exception):
        assert leave_channel(c['token'], 0)


def test_channel_addowner():
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")

    create_channel(a['token'], 'new channel', 'true')
    invite_user(a['token'], 0, b['u_id'])    

    assert addowner_channel(a['token'], 0, b['u_id']) == {}


def test_channel_addowner_exceptions():
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")
    c = register("matt@mail.com", "password", "matt", "juan")

    create_channel(a['token'], 'new channel', 'true')
    invite_user(a['token'], 0, b['u_id'])   
    create_channel(a['token'], 'newer channel', 'true') 

    addowner_channel(a['token'], 0, b['u_id'])
    
    with pytest.raises(Exception):
        # when channel_id refers to an invalid channel
        assert addowner_channel(a['token'], 2, b['u_id'])

    with pytest.raises(Exception):
        # when user with user id is already an owner
        assert addowner_channel(a['token'], 0, b['u_id'])

    with pytest.raises(Exception):
        # when the user is not an owner of slackr or an owner of this channel
        assert addowner_channel(b['token'], 1, c['u_id'])
    
def test_channel_removeowner():
    #Testing possibilities for 'Owner removed'
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")

    create_channel(a['token'], 'new channel', 'true')
    invite_user(a['token'], 0, b['u_id'])   
    create_channel(a['token'], 'newer channel', 'true') 

    addowner_channel(a['token'], 0, b['u_id'])

    assert removeowner_channel(a['token'], 0, b['u_id']) == {}



def test_channel_removeowner_exceptions():
    #Testing possibilities for 'Owner removed'
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")
    c = register("matt@mail.com", "password", "matt", "juan")

    create_channel(a['token'], 'channel1', 'true')  
    create_channel(b['token'], 'channel2', 'true') 

    addowner_channel(a['token'], 0, b['u_id'])

    join_channel(c['token'], 0)


    with pytest.raises(Exception):
        # when channel_id refers to an invalid channel
        assert removeowner_channel(a['token'], 10, b['u_id'])

    with pytest.raises(Exception):
        # when user with user id is not an owner of channel
        assert removeowner_channel(b['token'], 1, c['u_id'])

    with pytest.raises(Exception):
        # when the user is not an owner of slackr or an owner of this channel
        assert removeowner_channel(c['token'], 1, b['u_id'])


def test_channel_listall(): # Testing works for each user
    clear_data()
    a = register("cheajeremy@gmail.com", "password", "jeremy", "chea")
    b = register("lyric.poo@gmail.com", "password", "lyric", "wang")
    c = create_channel(a['token'], 'channel1', 'true')    
    d = create_channel(b['token'], 'channel2', 'true')    

    assert list_all_user_channels(a['token']) == {'channels': [{'channel_id':c['channel_id'], 'name': 'channel1'},
                                                               {'channel_id':d['channel_id'], 'name': 'channel2'}]
                                                }


ch = 'a'
name_19 = ch * 19
invalidname_21 = ch * 21


def test_channels_create_valid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    assert(create_channel(a['token'],"matt", 'true')) == {'channel_id': 0}
    assert(create_channel(a['token'],"jeremy", 'true')) == {'channel_id': 1}
    assert(create_channel(a['token'],name_19, 'true')) == {'channel_id': 2}

def test_channels_create_invalid():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")
    with pytest.raises(Exception):
    #channel name too long
        assert(create_channel(a['token'],invalidname_21, 'true'))


def test_channel_join(): #Testing all possible channel join cases for known users

    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")

    b = register("l56.juan@unsw.edu.au", "123456", "l", "wang")

    create_channel(a['token'], 'public channel', 'true')

    assert join_channel(b['token'], 0) == {}


def test_join_exceptions():
    clear_data()
    a = register("m56.juan@unsw.edu.au", "123456", "m", "juan")

    b = register("l56.juan@unsw.edu.au", "123456", "l", "wang")
    create_channel(a['token'], 'private channel', False)

    c = register("j56.juan@unsw.edu.au", "123456", "j", "chea")

    with pytest.raises(Exception):
        # When users are not authorised to join (AccessError)
        assert join_channel(c['token'],0)

    with pytest.raises(Exception):
        # When channel doesn't exist (ValueError)
        assert join_channel(a['token'],1)



def test_channel_details_valid():
    clear_data()

    a = register("lyric@unsw.edu.au", "123456", "l", "wang")
    create_channel(a['token'], 'public channel', 'true')

    b = register("matthew@unsw.edu.au", "123456", "m", "juan")
    create_channel(b['token'], 'single channel', 'true')

    c = register("jeremy@unsw.edu.au", "123456", "j", "chea")

    d = register("adam@unsw.edu.au", "123456", "a", "ma")

    join_channel(b['token'], 0)
    join_channel(c['token'], 0)
    join_channel(d['token'], 0)
    #print(details_channel(a['token'],0))
    assert details_channel(a['token'],0) == {  'name': "public channel",
                                                    'owner_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''}],
                                                    'all_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''},
                                                                    {'u_id': b['u_id'],'name_first': "m", 'name_last': "juan", 'profile_img_url': ''},
                                                                    {'u_id': c['u_id'],'name_first': "j", 'name_last': "chea", 'profile_img_url': ''},
                                                                    {'u_id': d['u_id'],'name_first': "a", 'name_last': "ma", 'profile_img_url': ''}]
                                            }
    assert(details_channel(b['token'],0)) == {  'name': "public channel",
                                                    'owner_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''}],
                                                    'all_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''},
                                                                    {'u_id': b['u_id'],'name_first': "m", 'name_last': "juan", 'profile_img_url': ''},
                                                                    {'u_id': c['u_id'],'name_first': "j", 'name_last': "chea", 'profile_img_url': ''},
                                                                    {'u_id': d['u_id'],'name_first': "a", 'name_last': "ma", 'profile_img_url': ''}]
                                            }
                                                                
    assert(details_channel(c['token'],0)) == {  'name': "public channel",
                                                    'owner_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''}],
                                                    'all_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''},
                                                                    {'u_id': b['u_id'],'name_first': "m", 'name_last': "juan", 'profile_img_url': ''},
                                                                    {'u_id': c['u_id'],'name_first': "j", 'name_last': "chea", 'profile_img_url': ''},
                                                                    {'u_id': d['u_id'],'name_first': "a", 'name_last': "ma", 'profile_img_url': ''}]
                                            }
    assert(details_channel(d['token'],0)) == {  'name': "public channel",
                                                    'owner_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''}],
                                                    'all_members': [{'u_id': a['u_id'],'name_first': "l", 'name_last': "wang", 'profile_img_url': ''},
                                                                    {'u_id': b['u_id'],'name_first': "m", 'name_last': "juan", 'profile_img_url': ''},
                                                                    {'u_id': c['u_id'],'name_first': "j", 'name_last': "chea", 'profile_img_url': ''},
                                                                    {'u_id': d['u_id'],'name_first': "a", 'name_last': "ma", 'profile_img_url': ''}]
                                            }
                                                                                
def test_channel_details_invalid():
    clear_data()

    a = register("lyric@unsw.edu.au", "123456", "l", "wang")
    create_channel(a['token'], 'public channel', 'true')

    b = register("matthew@unsw.edu.au", "123456", "m", "juan")
    create_channel(b['token'], 'single channel', 'true')
    
    with pytest.raises(Exception):
         # When channel does not exist (ValueError)
        assert(details_channel(a['token'],2)) 
        assert(details_channel(b['token'],2)) 
    with pytest.raises(Exception):   
         # When user is not a member of a channel
        assert(details_channel(a['token'],1))
        assert(details_channel(c['token'],1))
 

def test_channels_list_valid():
    clear_data()

    a = register("lyric@unsw.edu.au", "123456", "l", "wang")
    create_channel(a['token'], 'public channel', 'true')

    c = register("jeremy@unsw.edu.au", "123456", "j", "chea")

    assert list_user_channels(a['token']) == { 'channels' :[{
                                                'channel_id' : 0,
                                                'name' : 'public channel'
                                            }]}


    assert list_user_channels(c['token']) == {'channels' :[]}
        
    join_channel(c['token'], 0)

    assert list_user_channels(c['token']) == { 'channels' :[{
                                                'channel_id' : 0,
                                                'name' : 'public channel'
                                            }]}


def test_get_messages_invalid():
    clear_data()
    a = register("lyric@unsw.edu.au", "123456", "l", "wang")
    b = register("lyric2@unsw.edu.au", "123456", "l2", "wang2")
    create_channel(a['token'], 'public channel', 'true')
    send_message(a['token'], 0, 'hello1')
    send_message(a['token'], 0, 'hello2')
    send_message(a['token'], 0, 'hello3')
    send_message(a['token'], 0, 'hello4')
    
    with pytest.raises(Exception):
        # invalid channel
        assert get_messages(a['token'], 8, 0)

    with pytest.raises(Exception):
        # start is too large
        assert get_messages(a['token'], 0, 5)

    with pytest.raises(Exception):
        # user not in channel
        assert get_messages(b['token'], 0, 0)

