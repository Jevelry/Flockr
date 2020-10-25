"""
auth(auth.py): Gives access to auth functions (Register, logout, login)
channel(channel.py): Gives access to channel functinos
channels(channels.py): Gives access to channels functions
message(message.py): Gives access to message functions (send, edit, remove)
pytest(pytest module): Gives access to pytest command
other(other.py): Gives access to other functions (clear)
user(user.py): Gives access to user functions (change profile)
error(error.py): Gives access to error classes
"""
import auth
import channel
import channels
import message
import pytest
import other
import user
from error import InputError, AccessError

@pytest.fixture
def user():
    """
    Pytest fixture that automatically registers a user and returns their info
    """
    user = auth.auth_register('testmail@gmail.com', 'password', 'first_name', 'last_name')
    auth.auth_register('another_test@hotmail.com', 'password123', 'first_name', 'last_name')
    return user

# Tests for users_all
# Sucessful
def test_users_all_sucess(user):
    """
    Tests successful uses of users_all
    """

    user_result = other.users_all(user['token'])
    assert user_result['users'][0]['u_id'] == 1
    assert user_result['users'][0]['email'] == 'testmail@gmail.com'
    assert user_result['users'][0]['name_first'] == 'first_name'
    assert user_result['users'][0]['name_last'] == 'last_name'

    assert user_result['users'][1]['u_id'] == 2
    assert user_result['users'][1]['email'] == 'another_test@hotmail.com'
    assert user_result['users'][1]['name_first'] == 'first_name'
    assert user_result['users'][1]['name_last'] == 'last_name'

    other.clear()

# Unsucessful
def test_users_all_invalid_token(user):
    """
    Tests unsuccessful uses of users_all,
    focusing on invalid tokens
    """
    with pytest.raises(AccessError):
        assert other.users_all('invalid_token')

    other.clear()


# Tests for admin_userpermission_change
# Sucessful
def test_admin_userpermission_change_success(user):
    """
    Tests successful uses of admin_userpermission_change
    """
    user2 = auth.auth_register('closet@yahoo.com.au', 'closetset12', 'first_name', 'last_name')
    assert other.admin_userpermission_change(user['token'], user2['u_id'], 1) == {}

    other.clear()

def test_admin_userpermission_change_revert_success(user):
    """
    Tests successful uses of admin_userpermission_change,
    focusing on reverting changes
    """
    user2 = auth.auth_register('pancake@yahoo.com.au', 'honeysyrup2', 'first_name', 'last_name')
    assert other.admin_userpermission_change(user['token'], user2['u_id'], 1) == {}
    assert other.admin_userpermission_change(user['token'], user2['u_id'], 2) == {}

    other.clear()

# Unsucessful
def test_admin_userpermission_change_invalid_token(user):
    """
    Tests unsuccessful uses of admin_userpermission_change,
    focusing on invalid tokens
    """

    with pytest.raises(AccessError):
        assert other.admin_userpermission_change('invalid_token', user['u_id'], 1)

    other.clear()

def test_admin_userpermission_change_not_owner(user):
    """
    Tests unsuccessful uses of admin_userpermission_change,
    focusing on the 'admin' not having owner privileges
    """
    user2 = auth.auth_register('chair@gmail.com', 'chair202', 'first_name', 'last_name')
    with pytest.raises(AccessError):
        assert other.admin_userpermission_change(user2['token'], user['u_id'], 2)

    other.clear()

def test_admin_userpermission_change_invalid_uid(user):
    """
    Testing unsuccessful uses of admin_userpermission_change,
    focusing on invalid user ids
    """
    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user['token'], 'invalid_uid', 1)

    other.clear()

def test_admin_userpermission_change_invalid_permission(user):
    """
    Testing unsuccessful uses of admin_userpermission_change,
    focusing on invalid permission id
    """

    user2 = auth.auth_register('chair@gmail.com', 'chair202', 'first_name', 'last_name')

    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user['token'], user2['u_id'], 3)

    other.clear()


# Tests for search
# Sucessful
def test_search_results_single(user):
    """
    Tests successful uses of search,
    focusing on single message results
    """

    test_channel = channels.channels_create(user['token'], 'test_name', True)
    test_message = 'This is a test message.'
    message.message_send(user['token'], test_channel['channel_id'], test_message)
    find_message = other.search(user['token'], 'is a test')

    assert find_message['messages'][0]['message_id'] == 1
    assert find_message['messages'][0]['u_id'] == 1
    assert find_message['messages'][0]['message'] == 'This is a test message.'

    other.clear()

def test_search_results_multiple(user):
    """
    Tests successful uses of search,
    focusing on queries that return multiple messages
    """

    user2 = auth.auth_register('rockyroad@hotmail.com', 'chocfudge222', 'first_name', 'last_name')
    test_channel = channels.channels_create(user['token'], 'test_name', True)
    channel.channel_join(user2['token'], test_channel['channel_id'])

    test_message = 'This is a test message.'
    test_message2 = 'This message is a test right?'
    test_message3 = 'Yes it is a test.'
    message.message_send(user['token'], test_channel['channel_id'], test_message)
    message.message_send(user2['token'], test_channel['channel_id'], test_message2)
    message.message_send(user['token'], test_channel['channel_id'], test_message3)
    find_message = other.search(user['token'], 'is a test')

    assert find_message['messages'][0]['message_id'] == 1
    assert find_message['messages'][0]['u_id'] == 1
    assert find_message['messages'][0]['message'] == 'This is a test message.'

    assert find_message['messages'][1]['message_id'] == 3
    assert find_message['messages'][1]['u_id'] == 1
    assert find_message['messages'][1]['message'] == 'Yes it is a test.'

    other.clear()

def test_search_no_results(user):
    """
    Tests on successful uses of search,
    focusing on querise that don't return any strings
    """
    channels.channels_create(user['token'], 'test_name', True)

    find_message = other.search(user['token'], 'is a test')
    assert find_message['messages'] == []

    other.clear()

# Unsucessful
def test_search_invalid_token(user):
    """
    Tests unsuccessful uses of search,
    focusing on invalid tokens
    """

    test_channel = channels.channels_create(user['token'], 'test_name', True)
    test_message = 'We love cats and dogs'
    message.message_send(user['token'], test_channel['channel_id'], test_message)
    
    with pytest.raises(AccessError):
        assert other.search('invalid_token', 'is a test')
    
    other.clear()
