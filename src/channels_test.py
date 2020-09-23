import channels
import pytest
from error import InputError

def test_channels_list():
    assert channels.channels_list('token') == 'channels'
    
def test_channels_listall():
    assert channels.channels_list('token') == 'channels'

def test_channels_create():
    result = channels.channels_create(token, name, is_public)

def test_channels_create_except():
    with pytest.raises(InputError) as e:
        assert len(name) > 20