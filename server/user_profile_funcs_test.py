import pytest
from server.user_profile_funcs import *
from server.auth_funcs import *
from server.data_funcs import *

def test_get_user_profile_valid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    token = user_1['token']
    u_id = user_1['u_id']
    assert(get_user_profile(token, u_id) == {'email' : "adam@gmail.com",
                                            'name_first' : "adam",
                                            'name_last' : "ma",
                                            'handle_str' : "adamma",
                                            'profile_img_url': '',
                                            'u_id': 0
                                        })
def test_get_user_profile_invalid():
    clear_data()
    with pytest.raises(Exception):
        get_user_profile("asdc", 3215)

def test_set_user_name_valid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    token = user_1['token']
    assert(set_user_name(token, "lyric", "wang") == {})

def test_set_user_name_invalid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    token = user_1['token']
    # When the first name is too long
    with pytest.raises(Exception):
        set_user_name(token, "lyric"*50, "wang")
    # When the last name is too long
    with pytest.raises(Exception):
        set_user_name(token, "lyric", "wang"*100)

def test_set_user_email_valid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    token = user_1['token']
    assert(set_user_email(token, "matt@cr.com") == {})
def test_set_user_email_invalid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    user_2 = register("lyric@gmail.com", "123456", "lyric", "wang")
    token = user_1['token']
    # When the email 
    # When email is invalid
    with pytest.raises(Exception):
        set_user_email(token, "mattc")
    # When email has been registered
    with pytest.raises(Exception):
        set_user_email(token, "lyric@gmail.com")

def test_set_user_handle_valid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    token = user_1['token']
    assert(set_user_handle(token, "caonimabi") == {})
def test_set_user_handle_invalid():

    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    user_2 = register("ada@gmail.com", "123456", "lyric", "wang")
    token = user_1['token']

    # When the length of the new handle is shorter than 3 characters
    with pytest.raises(Exception):
        set_user_handle(token, "sd")
    # When the length of the new handle is longer than 20 characters
    with pytest.raises(Exception):
        set_user_handle(token, "asdcasdcasdcasdcasdcasdcasdc")
    # When the handle has already been registered
    with pytest.raises(Exception):
        set_user_handle(token, "lyricwang")
    
def test_get_all_users_valid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    user_2 = register("lyric@gmail.com", "123456", "lyric", "wang")
    token = user_1['token']
    assert(get_all_users(token) == {'users': [{'email': 'adam@gmail.com', 'handle_str': 'adamma', 'name_first': 'adam', 'name_last': 'ma', 'profile_img_url':'','u_id':0}, {'email': 'lyric@gmail.com', 'handle_str': 'lyricwang', 'name_first': 'lyric', 'name_last': 'wang', 'profile_img_url':'','u_id':1}]})

def test_upload_photos_valid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    token = user_1['token']
    assert(upload_photo(token, "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg", 0, 0, 400, 400) == {})

def test_upload_photos_invalid():
    clear_data()
    user_1 = register("adam@gmail.com", "123456", "adam", "ma")
    token = user_1['token']
    #when the url is invalid
    with pytest.raises(Exception):
        upload_photo(token, "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower", 0, 0, 400, 400)
    #when cropping values are invalid:
    with pytest.raises(Exception):
        upload_photo(token, "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg", -1, 0, 400, 400)
    #when file is not a jpg:
    with pytest.raises(Exception):
        upload_photo(token, "https://png.pngtree.com/element_our/sm/20180327/sm_5aba147bcacf2.png", 0, 0, 400, 400)
       