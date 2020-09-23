import channels
import pytest
from error import InputError

def test_channels_list():
    result = channels.channels_list('testemail@gmail.com')
    assert result[0]['channel_id'] == 1
    
def test_channels_listall():
    result = channels.channels_list('testemail@gmail.com')
    assert result[0]['channel_id'] == 1

def test_channels_create():
    result = channels.channels_create('testmail@gmail.com', 'test_name', 'is_public')
    assert result['channels_id'] == 1

def test_channels_create_except():
    result = channels.channels_create('testmail@gmail.com', 'test_name_12345678910', 'is_public')
    assert result['channels_id'] == 1

    with pytest.raises(InputError):
        assert len('test_name_12345678910') > 20