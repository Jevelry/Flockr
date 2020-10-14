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

def check_email_change(u_id, new_email):
    """
    Checks if set_email has successfully changed email

    Parameters:
        user(int): u_id (Identifier for user)
        new_email: new email

    Returns:
        Nothing
    """
    for user in data.data['users']:
        if user['u_id'] == u_id:
            assert user["email"] == new_email
            break
            
def check_handle_changed(u_id, new_handle):
    """
    Checks if set_handle has successfully changed handle

    Parameters:
        user(int): u_id (Identifier for user)
        new_handle: new handle

    Returns:
        Nothing
    """
    for user in data.data['users']:
        if user['u_id'] == u_id:
            assert user["handle"] == new_handle
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
    auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
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

    
#USER_PROFILE_SETEMAIL TESTS
#SUCCESSFUL
def test_user_setemail_valid_email():
    """
    Testing successful uses of user_profile_setemail
    focusing on valid emails
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_setemail(user1["token"], "newemail@unsw.edu.au")
    check_email_change(user1["u_id"], "newemail@unsw.edu.au")
    other.clear()
    
def test_user_setemail_sameemail():
    """
    Testing successful uses of user_profile_setemail
    focusing on using same existing email
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_setemail(user1["token"], "kevin.huang@gmail.com")
    #Should do nothing
    check_email_change(user1["u_id"], "kevin.huang@gmail.com")
    other.clear()
    
#Unsuccessful
def test_user_setemail_invalid_token():
    """
    Testing unsuccessful uses of user_profile_setemail
    focusing on invalid tokens
    """
    auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(AccessError):
        assert user.user_profile_setemail("invalid_token", "newemail@unsw.edu.au")
    other.clear()



def test_user_setemail_invalid_email():
    """
    Testing unsuccessful uses of user_profile_setemail
    focusing on invalid emails
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(InputError):
        assert user.user_profile_setemail(user1["token"], "thisisaninvalidemail.com")
        assert user.user_profile_setemail(user1["token"], "invalidemail")
    other.clear()


def test_user_setemail_email_taken():
    """
    Testing unsuccessful uses of user_profile_setemail
    focusing on email already in use
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    auth.auth_register("1531grouptask@hotmail.com","amazingstuff", "onefive", "threeone")
    with pytest.raises(InputError):
        assert user.user_profile_setemail(user1["token"], "1531grouptask@hotmail.com")
    other.clear()


#USER_PROFILE_SETHANDLE TESTS
#SUCCESSFUL
def test_user_sethandle_valid_handle():
    """
    Testing successful uses of user_profile_sethandle
    focusing on valid handles
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_sethandle(user1["token"], "newhandle")
    check_handle_changed(user1["u_id"], "newhandle")
    other.clear()

def test_user_sethandle_samehandle():
    """
    Testing successful uses of user_profile_sethandle
    focusing on changing to same existing handle
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user.user_profile_sethandle(user1["token"], "KevinHuang")
    #Should do nothing
    check_handle_changed(user1["u_id"], "KevinHuang")
    other.clear()

#Unsuccessful
def test_user_sethandle_invalid_token():
    """
    Testing unsuccessful uses of user_profile_sethandle
    focusing on invalid tokens
    """
    auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(AccessError):
        assert user.user_profile_sethandle("invalid_token", "newhandle")
    other.clear()

def test_user_sethandle_invalid_handle():
    """
    Testing unsuccessful uses of user_profile_sethandle
    focusing on invalid handles
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(user1["token"], "abcdefghijklmnopqrstuvwxyz")
        assert user.user_profile_sethandle(user1["token"], "me")    
    other.clear()

def test_user_sethandle_handle_taken(): 
    """
    Testing unsuccessful uses of user_profile_sethandle
    focusing on using existing handle
    """
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    auth.auth_register("1531grouptask@hotmail.com","amazingstuff", "onefive", "threeone")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(user1["token"], "onefivethreeone")
    other.clear()

