"""
    pytest: Gives access to pytest command (for testing)
    auth(auth.py): Gives access to auth functions
    channel(channel.py): Gives access to channel functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
    user(user.py): Gives access to user functions
    data(data.py): Gives access to global data variable
"""
import pytest
import auth
import channel
import channels
import user
import other
from error import InputError, AccessError
import data

def check_name_change(u_id, first, last):
    """
    Checks if set_name has successfully changed name

    Parameters:
        user(int): u_id (Identifier for user)
        first: new first name
        last: new last name

    Returns:
        Nothing
    """
    for user in data.data['users']:
        if user['u_id'] == u_id:
            assert user["first"] == first
            assert user["last"] == last
            break
            
            
#USER_PROFILE TESTS
#SUCCESSFUL
def test_user_profile_request_self():
    """
    Testing successful uses of user_profile
    focusing on request oneselves profile
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user1_profile = {
            'u_id': 1,
            'email': 'kevin.huang@gmail.com',
            'name_first': 'Kevin',
            'name_last': 'Huang',
            'handle_str': 'KevinHuang',  
        }
    assert user.user_profile(user1["token"], user1["u_id"]) == user1_profile
    other.clear()
def test_user_profile_request_others():
    """
    Testing Successful uses of user_profile 
    focusing on requesting other users profiles
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user1_profile = {
            'u_id': 1,
            'email': 'kevin.huang@gmail.com',
            'name_first': 'Kevin',
            'name_last': 'Huang',
            'handle_str': 'KevinHuang',  
        }
    assert user.user_profile(user2["token"], user1["u_id"]) == user1_profile
    other.clear()
#Unsuccessful
def test_user_profile_invalid_token():
    """
    Testing unsuccessful uses of user_profile 
    focusing on invalid tokens
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(AccessError):
        assert user.user_profile("invalid_token", user1["u_id"])
    other.clear()

def test_user_profile_invalid_uid():
    """
    Testing unsuccessful uses of user_profile     
    focusing on invalid u_id
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    invalid_uid = 9
    with pytest.raises(InputError):
        assert user.user_profile(user1["token"], invalid_uid)
    other.clear()
    
#USER_PROFILE_SETNAME TESTS
#SUCCESSFUL

def test_user_setname_valid_name():
    """
    Testing successful uses of user_profile_setname
    focusing on valid names
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_setname(user1["token"], "Awesome", "Joey")
    check_name_change(user1["u_id"], "Awesome", "Joey")
    other.clear()
    
def test_user_setname_lastname_only():
    """
    Testing successful uses of user_profile_setname
    focusing on changing lastname only
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_setname(user1["token"], "Kevin", "Awesome")
    check_name_change(user1["u_id"], "Kevin", "Awesome")
    other.clear()

def test_user_setname_firstname_only():
    """
    Testing successful uses of user_profile_setname
    focusing on changing firstname only
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_setname(user1["token"], "Awesome", "Huang")
    check_name_change(user1["u_id"], "Awesome", "Huang")
    other.clear()

def test_user_setname_samename():
    """
    Testing successful uses of user_profile_setname
    focusing on changing to same existing name
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_setname(user1["token"], "Kevin", "Huang")
    check_name_change(user1["u_id"], "Kevin", "Huang")
    other.clear()
    
#Unsuccessful
def test_user_setname_invalid_token():
    """
    Testing unsuccessful uses of user_profile_setname
    focusing on invalid tokens
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(AccessError):
        assert user.user_profile_setname("invalid_token", "new", "name")
    other.clear()

def test_user_setname_invalid_firstname():
    """
    Testing unsuccessful uses of user_profile_setname
    focusing on invalid firstnames
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(InputError):
        assert user.user_profile_setname(user1["token"], "iwbliueblaiublvuaeblriualerugbeiurbgliuebrgiubguiea", "name")
        
        assert user.user_profile_setname(user1["token"], "", "name")
    other.clear()
    
def test_user_setname_invalid_lastname():
    """
    Testing unsuccessful uses of user_profile_setname
    focusing on invalid lastnames
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(InputError):
        assert user.user_profile_setname(user1["token"], "new", "niwbliueblaiublvuaeblriualerugbeiurbgliuebrgiubguiea")

        assert user.user_profile_setname(user1["token"], "new", "")
    other.clear()

    
