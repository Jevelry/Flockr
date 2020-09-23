import channel
import channels
import pytest
from error import InputError

#Tests for channels_list:
def test_channels_list():
    channels.channels_create('testmail@gmail.com', 'test_channel', 'is_public')
    channel.channel_join('testmail@gmail.com', 'test_channel')
    list_result = channels.channels_list('testemail@gmail.com')
    assert list_result[0]['channel_id'] == 1
    assert list_result[0]['name'] == 'test_channel'

    channels.channels_create('another_test@hotmail.com', 'test_channel_two', 'is_public')
    channels.channels_create('another_test@hotmail.com', 'test_channel_three', 'is_public')
    channel.channel_join('another_test@hotmail.com', 'test_channel_two')
    channel.channel_join('another_test@hotmail.com', 'test_channel_three')
    list_result = channels.channels_list('another_test@hotmail.com')
    assert list_result[0]['channel_id'] == 2
    assert list_result[0]['name'] == 'test_channel_two'
    assert list_result[1]['channel_id'] == 3
    assert list_result[1]['name'] == 'test_channel_three'

#Tests for channels_listall:
def test_channels_listall():
    channels.channels_create('abc123@gmail.com', 'my_channel', 'is_public')
    channels.channels_create('xyz456@gmail.com', 'our_channel', 'is_public')
    list_result = channels.channels_list('xyz456@gmail.com')
    assert list_result[0]['channel_id'] == 1
    assert list_result[0]['name'] == 'my_channel'
    assert list_result[1]['channel_id'] == 2
    assert list_result[1]['name'] == 'our_channel'

#Tests for channels_create:
def test_channels_create():
    result = channels.channels_create('testmail@gmail.com', 'test_name', 'is_public')
    assert result['channels_id'] == 1

def test_channels_create_except():
    result = channels.channels_create('testmail@gmail.com', 'test_name_12345678910', 'is_public')
    assert result['channels_id'] == 1

    with pytest.raises(InputError) as e:
        assert len('test_name_12345678910') > 20