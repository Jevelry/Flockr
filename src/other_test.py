import auth
import channel
import channels
import message
import pytest
import other
import user
from error import InputError
from error import AccessError

# Tests for users_all
# Sucessful
def test_users_all_sucess():
    other.clear()

    user = auth.auth_register('testmail@gmail.com', 'password', 'first_name', 'last_name')
    user2 = auth.auth_register('another_test@hotmail.com', 'password123', 'first_name', 'last_name')

    user_result = other.users_all(user['token'])
    assert user_result['users'][0]['u_id'] == 1
    assert user_result['users'][0]['email'] == 'testmail@gmail.com'
    assert user_result['users'][0]['name_first'] == 'first_name'
    assert user_result['users'][0]['name_last'] == 'last_name'
    assert user_result['users'][0]['permission_id'] == 1

    assert user_result['users'][1]['u_id'] == 2
    assert user_result['users'][1]['email'] == 'another_test@hotmail.com'
    assert user_result['users'][1]['name_first'] == 'first_name'
    assert user_result['users'][1]['name_last'] == 'last_name'
    assert user_result['users'][1]['permission_id'] == 2

    other.clear()

# Unsucessful
def test_users_all_invalid_token():
    other.clear()

    user = auth.auth_register('testmailtest@gmail.com', 'password121', 'first_name', 'last_name')
    user2 = auth.auth_register('another_testtwo@hotmail.com', 'password12321', 'first_name', 'last_name')
    with pytest.raises(AccessError):
        assert other.users_all('invalid_token')

    other.clear()


# Tests for admin_userpermission_change
# Sucessful
def test_admin_userpermission_change_success():
    other.clear()

    user = auth.auth_register('cupboard@hotmail.com', 'cupcupboard', 'first_name', 'last_name')
    user2 = auth.auth_register('closet@yahoo.com.au', 'closetset12', 'first_name', 'last_name')
    other.admin_userpermission_change(user['token'], user2['u_id'], 1)
    user_result = other.users_all(user['token'])
    assert user_result['users'][1]['permission_id'] == 1

    other.clear()

def test_admin_userpermission_change_revert_success():
    other.clear()

    user = auth.auth_register('cupcake@hotmail.com', 'strawberry1', 'first_name', 'last_name')
    user2 = auth.auth_register('pancake@yahoo.com.au', 'honeysyrup2', 'first_name', 'last_name')
    other.admin_userpermission_change(user['token'], user2['u_id'], 1)
    user_result = other.users_all(user['token'])
    assert user_result['users'][1]['permission_id'] == 1

    other.admin_userpermission_change(user['token'], user2['u_id'], 2)
    user_result2 = other.users_all(user['token'])

    assert user_result2['users'][1]['permission_id'] == 2

    other.clear()

# Unsucessful
def test_admin_userpermission_change_invalid_token():
    other.clear()

    user = auth.auth_register('abc123abc@gmail.com', 'passwordabc1', 'first_name', 'last_name')
    user2 = auth.auth_register('xyz456xyz@gmail.com', 'passwordxyz1', 'first_name', 'last_name')

    with pytest.raises(AccessError):
        assert other.admin_userpermission_change('invalid_token', user2['u_id'], 1)

    other.clear()

def test_admin_userpermission_change_not_owner():
    other.clear()

    user = auth.auth_register('lamp@gmail.com', 'lamp101', 'first_name', 'last_name')
    user2 = auth.auth_register('chair@gmail.com', 'chair202', 'first_name', 'last_name')

    with pytest.raises(AccessError):
        assert other.admin_userpermission_change(user2['token'], user['u_id'], 2)

    other.clear()

def test_admin_userpermission_change_invalid_uid():
    other.clear()

    user = auth.auth_register('apple@gmail.com', 'apple123', 'first_name', 'last_name')
    user2 = auth.auth_register('banana@gmail.com', 'banana321', 'first_name', 'last_name')

    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user['token'], 'invalid_uid', 1)

    other.clear()

def test_admin_userpermission_change_invalid_permission():
    other.clear()

    user = auth.auth_register('lamp@gmail.com', 'lamp101', 'first_name', 'last_name')
    user2 = auth.auth_register('chair@gmail.com', 'chair202', 'first_name', 'last_name')

    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user['token'], user2['u_id'], 3)

    other.clear()


# Tests for search
# Sucessful
def test_search_results_single():
    other.clear()

    user = auth.auth_register('cookies@gmail.com', 'chocchip123', 'first_name', 'last_name')
    test_channel = channels.channels_create(user['token'], 'test_name', True)

    test_message = 'This is a test message.'
    sent_message = message.message_send(user['token'], test_channel['channel_id'], test_message)
    find_message = other.search(user['token'], 'is a test')

    assert find_message['messages'][0]['message_id'] == '1'
    assert find_message['messages'][0]['u_id'] == 1
    assert find_message['messages'][0]['message'] == 'This is a test message.'
    assert find_message['messages'][0]['token'] == user['token']
    assert find_message['messages'][0]['query_str'] == 'is a test'

    other.clear()

def test_search_results_multiple():
    other.clear()

    user = auth.auth_register('icecream@gmail.com', 'mintchip123', 'first_name', 'last_name')
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

    assert find_message['messages'][0]['message_id'] == '1'
    assert find_message['messages'][0]['u_id'] == 1
    assert find_message['messages'][0]['message'] == 'This is a test message.'
    assert find_message['messages'][0]['token'] == user['token']
    assert find_message['messages'][0]['query_str'] == 'is a test'

    assert find_message['messages'][1]['message_id'] == '3'
    assert find_message['messages'][1]['u_id'] == 1
    assert find_message['messages'][1]['message'] == 'Yes it is a test.'
    assert find_message['messages'][1]['token'] == user['token']
    assert find_message['messages'][1]['query_str'] == 'is a test'

    other.clear()

def test_search_no_results():
    other.clear()

    user = auth.auth_register('lollipop@gmail.com', 'sweetysweet', 'first_name', 'last_name')
    test_channel = channels.channels_create(user['token'], 'test_name', True)

    find_message = other.search(user['token'], 'is a test')
    assert find_message['messages'] == []

    other.clear()

# Unsucessful
def test_search_invalid_token():
    other.clear()
    user = auth.auth_register('mango@gmail.com', 'mangogo', 'first_name', 'last_name')
    test_channel = channels.channels_create(user['token'], 'test_name', True)
    test_message = 'We love cats and dogs'
    message.message_send(user['token'], test_channel['channel_id'], test_message)
    
    with pytest.raises(AccessError):
        assert other.search('invalid_token', 'is a test')
    
    other.clear()
