"""
Tests for validation module

"""
from error import InputError, AccessError
import data
import re
import hashlib
import jwt
import validation
import pytest
import auth
import channels
import channel
import message
import other

def test_check_valid_handle():
    """
    Valid_handle doesn't return anything when handle is valid,
    so we can't test it directly
    """
    with pytest.raises(InputError):
        assert validation.check_valid_handle("ab")
        assert validation.check_valid_handle('abcdefghijklmnopqrstuvwxyz')

def test_check_valid_token():
    """
    Returns relevant u_id when token is valid
    raises AccessError when token is invalid
    """
    user = auth.auth_register('runner@gmail.com', 'english', 'dan', 'theman')
    assert validation.check_valid_token(user['token']) == user['u_id']
    with pytest.raises(AccessError):
        assert validation.check_valid_token('user["token"]')
        assert validation.check_valid_token('bacon')
    other.clear()
    

def test_check_valid_email():
    """
    Returns nothing if valid email
    Returns InputError if email is not valid
    """
    auth.auth_register('kevin@gmail.com', 'password', 'firstname', 'lastname')
    with pytest.raises(InputError):
        assert validation.check_valid_email('kevin.com')
        assert validation.check_valid_email('kevin@gmail.com')
        assert validation.check_valid_email('kevin@@gmail.com')
    other.clear()

def test_check_existing_email():
    """
    Tests uses of check_existing_email.
    Returns nothing if email doesn't exist so can't test that
    """
    auth.auth_register('jake@gmail.com', 'jacobhow', 'jake', 'jake')
    auth.auth_register('steve@gmail.com', 'malone', 'epic', 'times')
    with pytest.raises(InputError):
        assert validation.check_existing_email('jake@gmail.com')
        assert validation.check_existing_email('steve@gmail.com')
    other.clear()

def test_check_existing_handle():
    """
    Returns nothing if handle doesn't exist so can't assert that
    """
    auth.auth_register('jake@gmail.com', 'jacobhow', 'jake', 'jake')
    auth.auth_register('ekaj@gmail.com', 'jacobhow', 'jake', 'jake')
    with pytest.raises(InputError):
        assert validation.check_existing_handle('jakejake')
        assert validation.check_existing_handle('jakejak1')
    other.clear()

def test_check_correct_password():
    """
    Returns nothing if password is correct so can't test that
    """
    auth.auth_register('ant@gmail.com', 'ANNNTNTTNNTNTNT', 'ant', 'ant')
    with pytest.raises(InputError):
        assert validation.check_correct_password('ANANNANNT','ant@gmail.com')
    other.clear()
    
def test_check_correct_email():
    """
    Returns nothing if email exists so can't test that
    """
    with pytest.raises(InputError):
        assert validation.check_correct_email('this@isannoying.com')
        assert validation.check_correct_email('im@getting.com')
    other.clear()

def test_check_valid_name():
    """
    Returns nothing if name is valid so can't test that
    """
    with pytest.raises(InputError):
        assert validation.check_valid_name('','')
        assert validation.check_valid_name('','apple')
        assert validation.check_valid_name('apple','')
        assert validation.check_valid_name('apple',
            'whyarethesefunctionsnecessaryitsobviousthattheyworkbecauseeveryotherpytestispassing'
        )
    other.clear()

def test_check_valid_password():
    """
    Returns nothing if password is valid so can't test that
    """
    with pytest.raises(InputError):
        assert validation.check_valid_password('')
        assert validation.check_valid_password('1')
        assert validation.check_valid_password('12')
        assert validation.check_valid_password('123')
        assert validation.check_valid_password('1245')
        assert validation.check_valid_password('12456')

def test_check_user_in_channel():
    """
    Returns nothing if user is in channel so can't test that
    """
    user1 = auth.auth_register('this@is.so', 'annoying', 'thesefunc','tionswork')
    user2 = auth.auth_register('this@has.alr', 'eadybeen', 'tested','elsewhere')
    channel1 = channels.channels_create(user1['token'], 'pleaseendsoon', True)
    channel2 = channels.channels_create(user2['token'], 'noosdneesaelp', False)
    with pytest.raises(AccessError):
        assert validation.check_user_in_channel(user2['u_id'], channel1['channel_id'])
        assert validation.check_user_in_channel(user2['u_id'], channel2['channel_id'])
    other.clear()

def test_check_valid_channel_id():
    """
    Returns nothing if channel already exists so can't test that
    """
    with pytest.raises(InputError):
        assert validation.check_valid_channel_id(1)
        assert validation.check_valid_channel_id(2)
        assert validation.check_valid_channel_id('three')

def test_check_valid_u_id():
    """
    Returns nothing if channel already exists so can't test that
    """
    with pytest.raises(InputError):
        assert validation.check_valid_u_id(1)
        assert validation.check_valid_u_id(2)
        assert validation.check_valid_u_id('three')

# Same as check_user_in_chjannel
# def test_check_is_existing_channel_member():
#     """
#     Returns nothing if user is in the channel so can't test that
#     """

def test_check_is_channel_owner():
    """
    Returns nothing if user is an owner so can't test that
    """
    user1 = auth.auth_register('it@is.qtr', 'past12', 'already','pleasestop')
    user2 = auth.auth_register('we@better.not', 'havetodo', 'thedata','functiontests')
    channel1 = channels.channels_create(user1['token'], 'oriwillbemad', True)
    channel.channel_join(user2['token'], channel1['channel_id'])
    with pytest.raises(InputError):
        assert validation.check_is_channel_owner(user2['u_id'], channel1['channel_id'])
    other.clear()

def test_check_isnot_channel_owner():
    """
    Returns nothing if user is not an owner os can't test that
    """
    user1 = auth.auth_register('imat@mywits.end', 'withthis', 'thing','already')
    channel1 = channels.channels_create(user1['token'], 'oriwillbemad', True)
    with pytest.raises(InputError):
        assert validation.check_isnot_channel_owner(user1['u_id'], channel1['channel_id'])
    other.clear()

def test_valid_message():
    """
    Returns nothing if message is valid so can't test that
    """
    message = ''
    for _i in range(1001):
        message += 'A'
    with pytest.raises(InputError):
        assert validation.valid_message(message)

def test_valid_message_id():
    """
    Returns nothing if message id is valid so can't test that
    """
    user1 = auth.auth_register('im@going.mad', 'whatami', 'doing','here')
    channel1 = channels.channels_create(user1['token'], 'ineedsleepwtf', True)
    _message1 = message.message_send(user1['token'], channel1['channel_id'], 'sleeppls')
    with pytest.raises(InputError):
        assert validation.valid_message_id(2)
    other.clear()

def test_check_channel_is_public():
    """
    Returns nothing if channel is public so can't test that
    """
    user1 = auth.auth_register('im@about.to', 'gotosleep', 'assoonasi','finishthis')
    channel1 = channels.channels_create(user1['token'], 'someoneelsecandodata', False)
    with pytest.raises(AccessError):
        assert validation.check_channel_is_public(channel1['channel_id'])
    other.clear()