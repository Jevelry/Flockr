"""
Tests for validation module

"""
from error import InputError, AccessError
import data
import re
import hashlib
import jwt
import validation

def test_check_valid_handle():
    with pytest.raises(InputError):
        assert validation.check_valid_handle("ab")
        assert validation.check_valid_handle('abcdefghijklmnopqrstuvwxyz')

def test_check_valid_token():
    pass

def test_check_valid_email():

    with pytest.raises(InputError):
        assert validation.check_valid_email(kevin.com)
def test_check_existing_email():
    pass

def test_check_existing_handle():
    pass

def test_check_correct_password():
    pass
def test_check_correct_email():
    pass
def test_check_valid_name():
    pass
def test_check_valid_password():
    pass
def test_check_user_in_channel():
    pass
def test_check_valid_channel_id():
    pass
def test_check_valid_u_id():
    pass
def test_check_is_existing_channel_member():
    pass
def test_check_is_channel_owner():
    pass
def test_check_isnot_channel_owner():
    pass
def test_valid_message():
    pass
def test_valid_message_id():
    pass
def test_check_channel_is_public():
    pass
