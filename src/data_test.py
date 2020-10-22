"""
Tests for data.py functions
"""
from error import AccessError, InputError
import data
import auth
import channels
import other
import channel
import pytest 

@pytest.fixture
def user():
    user = auth.auth_register("kevin@gmail.com", "kh12345", "Kevin", "Huang")
    user1 = data.get_user_info(user["u_id"])
    return user1
@pytest.fixture
def channel():
    user = auth.auth_register("kevin@gmail.com", 'kh12345', 'Kevin', 'Huang')
    channel = channels.channels_create(user["token"], "test_channel", True)
    return channel


def test_get_user_with(user):
    """
    Returns user when given correct attribute, otherwise returns none
    """    
    assert data.get_user_with({"email":'kevin@gmail.com'})
    assert data.get_user_with({"email":'doesntexist@gmail.com'}) == None
    other.clear()

def test_get_user_info(user):
    """
    Returns user when given correct u_id, otherwise returns none
    """ 
    assert data.get_user_info(1) 
    assert data.get_user_info(2) == None
    other.clear()

def test_update_user(user):
    """
    Updates attribute of user. Returns nothing
    """
    data.update_user(user,{"name_last":"Hang"})
    assert data.get_user_with({"name_last": "Hang"}) == data.users[1]
    other.clear()

def test_update_user_channel_list(user):
    """
    Adds channel id to user's channel list. Returns nothing
    """
    data.update_user_channel_list(user, 52)
    assert data.users[1]["channel_list"] == {52}
    other.clear()

def test_register_user(user):
    """
    Checks if user has been adding to existing list of users
    """
    assert data.users[1] == user
    other.clear()

def test_login_user(user):
    """
    Check if user has been logged in
    """
    data.logout_user(user["u_id"])
    data.login_user(user["u_id"])
    assert data.check_logged_in(user["u_id"]) is True
    other.clear()

def test_check_logged_in(user):
    """
    Check if checking user is logged in works???
    """
    assert data.check_logged_in(user["u_id"]) is True
    other.clear()

def test_logout_user(user):
    """
    Check if user has been logged out
    """
    data.logout_user(user["u_id"])
    assert data.check_logged_in(user["u_id"]) is False
    other.clear()

def test_get_channel_info(channel):
    """
    Returns channel when given corresponding channel_id
    """
    assert data.get_channel_info(channel["channel_id"]) == data.channels[channel["channel_id"]]
    assert data.get_channel_info(561) == None
    other.clear()

def test_channel_add_member(channel):
    user2 = auth.auth_register('Elliot@hotmail.com', 'password123', 'Elliot', 'Rottenstein')
    data.channel_add_member(channel["channel_id"], user2["u_id"])
    assert data.check_user_in_channel(channel["channel_id"], user2["u_id"]) == True
    other.clear()

def test_check_user_in_channel(channel):
    """
    Returns True if user is member of channel
    """
    assert data.check_user_in_channel(channel["channel_id"], 1) == True
    assert data.check_user_in_channel(channel["channel_id"], 643) == False
    other.clear()
    
def test_check_channel_owner(channel):
    """
    Returns True if user is owner of channel
    """
    assert data.check_channel_owner(channel["channel_id"], 1) == True
    assert data.check_channel_owner(channel["channel_id"], 643) == False
    other.clear()

def test_channel_add_owner(channel):
    """
    Adds user to list of owners in channel, returns nothing
    """
    user2 = auth.auth_register('Elliot@hotmail.com', 'password123', 'Elliot', 'Rottenstein')
    data.channel_add_owner(channel["channel_id"],user2["u_id"])
    assert data.check_channel_owner(channel["channel_id"], user2["u_id"]) == True
    other.clear()

def test_channel_remove_member(channel):
    """
    Removes member from channel, returns nothing
    """
    user = data.get_user_info(1)
    data.channel_remove_member(channel["channel_id"], user["u_id"])
    assert data.check_user_in_channel(channel["channel_id"], user["u_id"]) == False
    other.clear()

def test_channel_remove_owner(channel):
    """
    Removes member as an owner, returns nothing
    """
    user = data.get_user_info(1)
    data.channel_remove_owner(channel["channel_id"], user["u_id"])
    assert data.check_channel_owner(channel["channel_id"], user["u_id"]) == False
    other.clear()

def test_get_message_num():
    """
    Return the value of message_num
    """
    assert data.get_message_num() == 0
    other.clear()

def test_get_num_users(user):
    """
    Return the number of total users
    """
    num = data.get_num_users()
    assert num == 1
    other.clear()

def test_make_message_id():
    """
    Returns a unique message_id for a new message
    """
    assert data.make_message_id() == 1
    assert data.make_message_id() == 2
    assert data.make_message_id() == 3
    other.clear()

def test_get_num_channels(channel):  
    """
    Returns the total number of channels
    """
    user2 = auth.auth_register('Elliot@hotmail.com', 'password123', 'Elliot', 'Rottenstein')
    num1 = data.get_num_channels()
    assert num1 == 1
    channels.channels_create(user2["token"],"nicecenew",True)
    num2 = data.get_num_channels()
    assert num2 == 2
    other.clear()


def test_find_channel():
    pass

def test_get_message():
    pass

def test_add_message():
    pass

def test_remove_message():
    pass

def test_edit_message():
    pass

def test_user_list():
    pass

def test_change_permission():
    pass