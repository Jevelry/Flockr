"""
    pytest: Gives access to pytest command (for testing)
    auth(auth.py): Gives access to auth functions
    channel(channel.py): Gives access to channel functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
    user(user.py): Gives access to user functions
"""
import pytest
import auth
import channel
import channels
import user
import other
from error import InputError, AccessError

#USER_PROFILE TESTS
#SUCCESSFUL

def test_user_profile_request_self():
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user1_profile = {
            'u_id': 1,
            'email': 'kevin.huang@gmail.com',
            'name_first': 'Kevin',
            'name_last': 'Huang',
            'handle_str': 'kevinhuang',  
        }
    assert user.user_profile(user1["token"], user1["u_id"]) == user1_profile



def test_user_profile_request_others():
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user1_profile = {
            'u_id': 1,
            'email': 'kevin.huang@gmail.com',
            'name_first': 'Kevin',
            'name_last': 'Huang',
            'handle_str': 'kevinhuang',  
        }
    assert user.user_profile(user2["token"], user1["u_id"]) == user1_profile

#Unsuccessful
def test_user_profile_invalid_token():
    






def test_user_profile_invalid_uid():

#USER_PROFILE_SETNAME TESTS
#SUCCESSFUL

def test_user_setname_valid_name():



def test_user_setname_twice():



#Unsuccessful
def test_user_setname_invalid_token():




def test_user_setname_invalid_firstname():

"""
do over 50 characters and 0 characters
"""


def test_user_setname_invalid_lastname():



#USER_PROFILE_SETEMAIL TESTS
#SUCCESSFUL
def test_user_setemail_valid_email():



#Unsuccessful
def test_user_setemail_invalid_token():





def test_user_setemail_invalid_email():



def test_user_setemail_email_taken():




#USER_PROFILE_SETHANDLE TESTS
#SUCCESSFUL
def test_user_sethandle_valid_handle():



#Unsuccessful
def test_user_sethandle_invalid_token():




def test_user_sethandle_invalid_handle():



def test_user_sethandle_handle_taken(): 




