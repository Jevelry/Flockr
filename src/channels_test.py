import channels
import pytest
from error import InputError

def test_channels_list():
    assert channels.channels_list('token') == 'channels'
    
def test_hannels_listall():
    assert channels.channels_list('token') == 'channels'
