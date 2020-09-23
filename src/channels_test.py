import channels
import pytest
from error import InputError

def test_channels_list():
    assert channels.channels_list('token') == 'channels'

