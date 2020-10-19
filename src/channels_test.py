import auth
import channel
import channels
import pytest
import other
from error import InputError
from error import AccessError

# Tests for channels_list:
# Successful
def test_channels_list_valid_token():
    other.clear()

    user = auth.auth_register('testmail@gmail.com', 'password', 'first_name', 'last_name')
    channels.channels_create(user['token'], 'test_channel', True)
    list_result = channels.channels_list(user['token'])
    assert list_result[0]['channel_id'] == 1
    assert list_result[0]['name'] == 'test_channel'

    user2 = auth.auth_register('another_test@hotmail.com', 'password123', 'first_name', 'last_name')
    channels.channels_create(user2['token'], 'test_channel_two', True)
    channels.channels_create(user2['token'], 'test_channel_three', True)
    list_result2 = channels.channels_list(user2['token'])
    assert list_result2[0]['channel_id'] == 2
    assert list_result2[0]['name'] == 'test_channel_two'
    assert list_result2[1]['channel_id'] == 3
    assert list_result2[1]['name'] == 'test_channel_three'

    other.clear()

# Unsuccessful
def test_channels_list_invalid_token():
    other.clear()

    user = auth.auth_register('testmailtest@gmail.com', 'password121', 'first_name', 'last_name')
    channels.channels_create(user['token'], 'test_channel', True)
    with pytest.raises(AccessError) as e:
        assert channels.channels_list('invalid_token')

    user2 = auth.auth_register('another_testtwo@hotmail.com', 'password12321', 'first_name', 'last_name')
    channels.channels_create(user2['token'], 'test_channel_two', True)
    channels.channels_create(user2['token'], 'test_channel_three', True)
    with pytest.raises(AccessError) as e:
        assert channels.channels_list('another_invalid_token')

    other.clear()

# Tests for channels_listall:
# Successful
def test_channels_listall_valid_token():
    other.clear()

    user = auth.auth_register('abc123@gmail.com', 'passwordabc', 'first_name', 'last_name')
    test_channel = channels.channels_create(user['token'], 'my_channel', True)
    list_result = channels.channels_listall(user['token'])
    assert list_result[0]['channel_id'] == 1
    assert list_result[0]['name'] == 'my_channel'
    
    user2 = auth.auth_register('xyz456@gmail.com', 'passwordxyz', 'first_name', 'last_name')
    channel.channel_join(user2['token'], test_channel['channel_id'])
    channels.channels_create(user2['token'], 'our_channel', True)
    list_result2 = channels.channels_listall(user2['token'])
    assert list_result2[0]['channel_id'] == 1
    assert list_result2[0]['name'] == 'my_channel'
    assert list_result2[1]['channel_id'] == 2
    assert list_result2[1]['name'] == 'our_channel'
    
    other.clear()

# Unsuccessful
def test_channels_listall_invalid_token():
    other.clear()

    user = auth.auth_register('abc123abc@gmail.com', 'passwordabc1', 'first_name', 'last_name')
    test_channel = channels.channels_create(user['token'], 'my_channel', True)
    with pytest.raises(AccessError) as e:
        assert channels.channels_listall('invalid_token')
    
    user2 = auth.auth_register('xyz456xyz@gmail.com', 'passwordxyz1', 'first_name', 'last_name')
    channel.channel_join(user2['token'], test_channel['channel_id'])
    channels.channels_create(user2['token'], 'our_channel', True)
    with pytest.raises(AccessError) as e:
        assert channels.channels_listall('another_invalid_token')

    other.clear()
    
# Tests for channels_create:
# Successful
def test_channels_create_name_valid():
    other.clear()

    user = auth.auth_register('testmail@gmail.com', 'passwordpassword', 'first_name', 'last_name')
    channels.channels_create(user['token'], 'test_name', True)
    list_result = channels.channels_list(user['token'])
    assert list_result[0]['channel_id'] == 1
    assert len(list_result[0]['name']) < 20

    user2 = auth.auth_register('mailtest@gmail.com', 'passwordword', 'first_name', 'last_name')
    channels.channels_create(user2['token'], 'test_name_two', False)
    list_result2 = channels.channels_list(user2['token'])
    assert list_result2[0]['channel_id'] == 2
    assert len(list_result2[0]['name']) < 20

    other.clear()

# Unsuccessful
def test_channels_create_invalid_token():
    other.clear()

    user = auth.auth_register('testmail12321@gmail.com', 'passwordpass1', 'first_name', 'last_name')
    with pytest.raises(AccessError) as e:
        assert channels.channels_create('invalid_token', 'test_name1', True)

    user2 = auth.auth_register('mailtest12321@gmail.com', 'passwpassword1', 'first_name', 'last_name')
    with pytest.raises(AccessError) as e:
        assert channels.channels_create('another_invalid_token', 'test_name1', False)

    other.clear()

def test_channels_create_name_error():
    other.clear()

    user = auth.auth_register('testmail123@gmail.com', 'passwordpass', 'first_name', 'last_name')
    with pytest.raises(InputError) as e:
        assert channels.channels_create(user['token'], 'test_name_12345678910x', True)

    user2 = auth.auth_register('mailtest123@gmail.com', 'passwpassword', 'first_name', 'last_name')
    with pytest.raises(InputError) as e:
        assert channels.channels_create(user2['token'], 'test_name_0987654321x', False)

    other.clear()

