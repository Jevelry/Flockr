import auth
import channel
import channels
import pytest
from error import InputError

# Tests for channels_list:
def test_channels_list():
    user = auth.auth_register('testmail@gmail.com', 'password', 'first_name', 'last_name')
    channels.channels_create(user['token'], 'test_channel', True)
    list_result = channels.channels_list(user['token'])
    assert list_result['channels'][1]['channel_id'] == 1
    assert list_result['channels'][1]['name'] == 'test_channel'

    user2 = auth.auth_register('another_test@hotmail.com', 'password123', 'first_name', 'last_name')
    channels.channels_create(user2['token'], 'test_channel_two', True)
    channels.channels_create(user2['token'], 'test_channel_three', True)
    list_result2 = channels.channels_list(user2['token'])
    assert list_result2['channels'][2]['channel_id'] == 2
    assert list_result2['channels'][2]['name'] == 'test_channel_two'
    assert list_result2['channels'][3]['channel_id'] == 3
    assert list_result2['channels'][3]['name'] == 'test_channel_three'

# Tests for channels_listall:
def test_channels_listall():
    user = auth.auth_register('abc123@gmail.com', 'passwordabc', 'first_name', 'last_name')
    channels.channels_create(user['token'], 'my_channel', True)
    list_result = channels.channels_listall(user['token'])
    assert list_result['channels'][1]['channel_id'] == 1
    assert list_result['channels'][1]['name'] == 'my_channel'
    
    user2 = auth.auth_register('xyz456@gmail.com', 'passwordxyz', 'first_name', 'last_name')
    channel.channel_join(user2['token'], ' my_channel')
    channels.channels_create(user2['token'], 'our_channel', True)
    list_result2 = channels.channels_listall(user2['token'])
    assert list_result2['channels'][1]['channel_id'] == 1
    assert list_result2['channels'][1]['name'] == 'my_channel'
    assert list_result2['channels'][2]['channel_id'] == 2
    assert list_result2['channels'][2]['name'] == 'our_channel'
    
# Tests for channels_create:
# Successful
def test_channels_create_name_valid():
    user = auth.auth_register('testmail@gmail.com', 'passwordpassword', 'first_name', 'last_name')
    channels.channels_create(user['token'], 'test_name', True)
    list_result = channels.channels_list(user['token'])
    assert list_result['channels'][1]['channel_id'] == 1
    assert len(list_result['channels'][1]['name']) < 20

    user2 = auth.auth_register('mailtest@gmail.com', 'passwordword', 'first_name', 'last_name')
    channels.channels_create(user2['token'], 'test_name_two', False)
    list_result2 = channels.channels_list(user2['token'])
    assert list_result2['channels'][2]['channel_id'] == 2
    assert len(list_result2['channels'][2]['name']) < 20

# Unsuccessful
def test_channels_create_name_error():
    user = auth.auth_register('testmail123@gmail.com', 'passwordpass', 'first_name', 'last_name')
    channels.channels_create(user['token'], 'test_name_12345678910x', True)
    list_result = channels.channels_list(user['token'])
    assert list_result['channels'][1]['channel_id'] == 1

    with pytest.raises(InputError) as e:
        assert len(list_result['channels'][1]['name']) > 20

    user2 = auth.auth_register('mailtest123@gmail.com', 'passwpassword', 'first_name', 'last_name')
    channels.channels_create(user2['token'], 'test_name_0987654321x', False)
    list_result2 = channels.channels_list(user2['token'])
    assert list_result2['channels'][2]['channel_id'] == 2

    with pytest.raises(InputError) as e:
        assert len(list_result2['channels'][2]['name']) > 20
