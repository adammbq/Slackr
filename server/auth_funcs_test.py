import pytest 
from server.auth_funcs import *
from server.data_funcs import *

def test_auth_login_valid():
    clear_data()
    register("m.juan@unsw.edu.au", "123456", "m", "juan")
    register("fluffy.kittens@gmail.com", "maboqian", "m", "bo")
    a = login("m.juan@unsw.edu.au", "123456")
    assert all(k in a for k in ['u_id', 'token']) 
    b = login("fluffy.kittens@gmail.com", "maboqian")
    assert all(k in b for k in ['u_id', 'token']) 

def test_login_invalid():
    with pytest.raises(Exception):
        # invalid email
        assert login("wrong.email@unsw.edu.au", "123456")
        assert login("hi there", "newpassword") 
        
    with pytest.raises(Exception):
        # invalid password and valid email
        assert login("m.juan.email@unsw.edu.au", "bad1") 
        assert login("server.server@yahoo.com", " ") 

    with pytest.raises(Exception):
        #invalid password and email
        assert login("a@n.k", "123") 
        assert login("hi@hi@gmail.com", "i") 



def test_logout():
    clear_data()
    a = register("m.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("fluffy.kittens@gmail.com", "maboqian", "m", "bo")
    a_token = a['token']
    b_token = b['token']
    # test valid logout
    assert logout(a_token) == { 'is_success': True }
    assert logout(b_token) == { 'is_success': True }

    # test invalid logout
    invalid = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImludmFsaWQiLCJ0aW1lc3RhbXAiOjE1NzIwNjQxOTguNDI0NDA0fQ.vJVwihgmQfEgDAZh5viJfiNBgVsOhwzmh2aJB54ep_0'
    assert logout(invalid) == { 'is_success': False }

def test_auth_register_valid():
    clear_data()
    a = register("yeet@unsw.edu.au", "123456", "Matt", "yeet")
    assert all(k in a for k in ['u_id', 'token'])    
    b = register("yought@gmail.com", "123abc", "jesus", "Kitten")
    assert all(k in b for k in ['u_id', 'token'])
    c = register("mail@gmail.com", "valid_password", "b" * 50, "last_name")
    assert all(k in c for k in ['u_id', 'token']) 
    d = register("another_mail@gmail.com", "valid_password", "nathan", "l" * 50)
    assert all(k in d for k in ['u_id', 'token']) 
    e = register("new_mail@gmail.com", "valid_password", "n" * 50, "l" * 50)
    assert all(k in e for k in ['u_id', 'token']) 


def test_auth_register_invalid():
    with pytest.raises(Exception):
        # When email is invalid
        assert register("email", "password", "name_first", "name_last") 
        assert register("email@.com", "password", "name_first", "name_last")

    with pytest.raises(Exception):
        # When first name is more than 50 characters
        assert register("email@jesus.com", "password", "asdjhcbjahsdbcashjkdbcialuebcjalsdbcuiaelbcjdslkchbluiebasjdbcaulisdbcdjaksbciuabcjksdlbclkuasbdc", "name_last") 
        assert register("mail@gmail.com", "valid_password", "b" * 51, "last_name")

    with pytest.raises(Exception):
        # When last name is more than 50 characters 
        assert register("email@mail.com", "123123123", "name_first", "sajhdcasbdcjhaksbdclasbdlkjcabsdjkcbakjlsdbcujkbsdakjlcbadscasdc") 
        assert register("mail@gmail.com", "valid_password", "nathan", "l" * 51)

    with pytest.raises(Exception):
        # When address has been used already
        assert register("m.juan@unsw.edu.au", "niceonedood", "name_first", "name_last") 
        assert register("m.juan@unsw.edu.au", "niceonedood", "name_first", "name_last") 

    with pytest.raises(Exception):
        # When password is invalid 
        assert register("email", "pass", "name_first", "name_last") 
        assert register("email", "123", "name_first", "name_last") 

def test_admin_userpermission_change_valid():
    clear_data()
    a = register("m.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("a.ma@gmail.com", "123456", "a", "ma")
    c = register("j.chea@gmail.com", "123456", "j", "chea")
    d = register("l.wang@gmail.com", "123456", "l", "wang")
    # change to admin
    assert permission_change(a['token'], 1, 2) == {}
    
    # change to owner
    assert permission_change(a['token'], 2, 1) == {}
    
    # change to member
    assert permission_change(a['token'], 1, 3) == {}

def test_admin_userpermission_change_invalid():
    clear_data()
    a = register("m2.juan@unsw.edu.au", "123456", "m", "juan")
    b = register("a2.ma@gmail.com", "123456", "a", "ma")
    c = register("j2.chea@gmail.com", "123456", "j", "chea")
    d = register("l2.wang@gmail.com", "123456", "l", "wang")
    with pytest.raises(Exception):
        #u_id is not valid
        assert permission_change(a['token'], 20, 2) 
        assert permission_change(a['token'], 35, 2) 
        
    with pytest.raises(Exception):
        #permission_id is not valid
        assert permission_change(a['token'], 1, 5) 
        assert permission_change(a['token'], 2, 4) 
        
    with pytest.raises(Exception):
        #user is not owner or admin
        assert permission_change(d['token'], 1, 3)
