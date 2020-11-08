"""
Tests for validation module
auth(auth.py): Gives access to auth functions (Register, logout, login)
channel(channel.py): Gives access to channel functinos
channels(channels.py): Gives access to channels functions
message(message.py): Gives access to message functions (send, edit, remove)
pytest(pytest module): Gives access to pytest command
other(other.py): Gives access to other functions (clear)
user(user.py): Gives access to user functions
error(error.py): Gives access to error classes
standup(standup.py): Gives access to the standup
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
import standup

@pytest.fixture
def user1():
    """
    Registers and returns a user dictionary
    which contains all the information about the user
    (name, last name, email, handle, etc)
    """
    user = auth.auth_register("Test@subject.com", "Testing123", "Hello", "There")
    return data.get_user_info(user["u_id"])

def test_check_valid_handle(user1):
    """
    Valid_handle doesn't return anything when handle is valid,
    so "None" means it passed successfully
    """
    # Would raise an input error if handle wasn't valid
    assert validation.check_valid_handle(user1["handle_str"]) == None
    with pytest.raises(InputError):
        assert validation.check_valid_handle("ab")
        assert validation.check_valid_handle("abcdefghijklmnopqrstuvwxyz")

def test_check_valid_token():
    """
    Returns relevant u_id when token is valid
    raises AccessError when token is invalid
    """
    user = auth.auth_register("runner@gmail.com", "english", "dan", "theman")
    assert validation.check_valid_token(user["token"]) == user["u_id"]
    with pytest.raises(AccessError):
        assert validation.check_valid_token(user["token"])
        assert validation.check_valid_token("bacon")
    other.clear()
    

def test_check_valid_email():
    """
    check_valid_email returns None if email is valid.
    check_valid_email reutrns InputError if email is not valid.
    """
    
    assert validation.check_valid_email("elliot@gmail.com") == None
    auth.auth_register("elliot@gmail.com", "shhhhhh", "Elliot", "Gmail")
    with pytest.raises(InputError):
        assert validation.check_valid_email("elliot@gmail.com")
    with pytest.raises(InputError):
        assert validation.check_valid_email("kevin.com")
        assert validation.check_valid_email("kevin@gmail.com")
        assert validation.check_valid_email("kevin@@gmail.com")
    other.clear()

def test_check_existing_email():
    """
    check_existing_email returns None if email doesn't exist
    check_existing_email raises an InputError if email does exist
    """
    assert validation.check_existing_email("jake@gmail.com") == None
    assert validation.check_existing_email("steve@gmail.com") == None
    auth.auth_register("jake@gmail.com", "jacobhow", "jake", "jake")
    auth.auth_register("steve@gmail.com", "malone", "epic", "times")
    with pytest.raises(InputError):
        assert validation.check_existing_email("jake@gmail.com")
        assert validation.check_existing_email("steve@gmail.com")
    other.clear()

def test_check_existing_handle():
    """
    check_existing_handle returns None if the handle doesn't exist
    check_existing_handle raises an InputError if the handle does exist already
    """
    assert validation.check_existing_handle("jakejake") == None
    assert validation.check_existing_handle("jakejak1") == None
    auth.auth_register("jake@gmail.com", "jacobhow", "jake", "jake")
    auth.auth_register("ekaj@gmail.com", "jacobhow", "jake", "jake")
    with pytest.raises(InputError):
        assert validation.check_existing_handle("jakejake")
        assert validation.check_existing_handle("jakejak1")
    other.clear()

def test_check_correct_password():
    """
    check_correct_password returns None if the password and email match
    check_correct_password raises an InputError if the password is incorrect
    """
    with pytest.raises(InputError):
        assert validation.check_correct_password("ant@gmail.com", "ANTANT")
    auth.auth_register("ant@gmail.com", "ANTANT", "ant", "ant")
    assert validation.check_correct_password("ant@gmail.com", "ANTANT") == None
    other.clear()
    
def test_check_correct_email():
    """
    check_correct_email returns None if the email exists
    check_correct_email raises an InputError if the email doesn't exist
    """
    with pytest.raises(InputError):
        assert validation.check_correct_email("this@isannoying.com")
        assert validation.check_correct_email("im@getting.com")
    auth.auth_register("this@isannoying.com", "<--NotTrue", "Bathilda", "Bagshot")
    auth.auth_register("im@getting.com", "Hoopdiedoo", "Hilda", "Harrper")
    assert validation.check_correct_email("this@isannoying.com") == None
    assert validation.check_correct_email("im@getting.com") == None
    other.clear()

def test_check_valid_name():
    """
    check_valid_name returns None if name is valid (allowed)
    check_valid_name raises an InputError if name is invalid
    """
    assert validation.check_valid_name("Bob", "Appleby") == None
    assert validation.check_valid_name("Howdo", "Youdo") == None
    assert validation.check_valid_name("BloodOnThe", "Clocktower") == None
    with pytest.raises(InputError):
        assert validation.check_valid_name("","")
        assert validation.check_valid_name("","apple")
        assert validation.check_valid_name("apple","")
        assert validation.check_valid_name("apple",
            "whyarethesefunctionsnecessaryitsobviousthattheyworkbecauseeveryotherpytestispassing"
        )
    other.clear()

def test_check_valid_password():
    """
    check_valid_password returns None if name is password is valid
    check_valid_password raises an InputError if password is invalid
    """
    assert validation.check_valid_password("password") == None
    assert validation.check_valid_password("iloveyou") == None
    assert validation.check_valid_password("123456") == None
    with pytest.raises(InputError):
        assert validation.check_valid_password("")
        assert validation.check_valid_password("1")
        assert validation.check_valid_password("12")
        assert validation.check_valid_password("123")
        assert validation.check_valid_password("1245")
        assert validation.check_valid_password("12456")

def test_check_user_in_channel():
    """
    check_user_in_channel returns None if user is in channel
    check_user_in_channel raises an AccessError if user is not in channe;
    """
    user1 = auth.auth_register("this@is.so", "annoying", "thesefunc","tionswork")
    user2 = auth.auth_register("this@has.alr", "eadybeen", "tested","elsewhere")
    channel1 = channels.channels_create(user1["token"], "pleaseendsoon", True)
    channel2 = channels.channels_create(user2["token"], "noosdneesaelp", False)
    assert validation.check_user_in_channel(user1["u_id"], channel1["channel_id"]) == None
    assert validation.check_user_in_channel(user2["u_id"], channel2["channel_id"]) == None
    with pytest.raises(AccessError):
        assert validation.check_user_in_channel(user2["u_id"], channel1["channel_id"])
        assert validation.check_user_in_channel(user2["u_id"], channel2["channel_id"])
    other.clear()

def test_check_valid_channel_id():
    """
    check_valid_channel_id returns None if channel exists
    check_valid_channel_id raises an InputError if channel doesn't exist
    """
    with pytest.raises(InputError):
        assert validation.check_valid_channel_id(1)
        assert validation.check_valid_channel_id(2)
        assert validation.check_valid_channel_id("three")
    user = auth.auth_register("line174@validation.py", "Imeanttest","thisfile", "righthere")
    _chan1 = channels.channels_create(user["token"], "ONE", True)
    _chan2 = channels.channels_create(user["token"], "TWO", True)
    assert validation.check_valid_channel_id(1) == None
    assert validation.check_valid_channel_id(2) == None
    other.clear()
    

def test_check_valid_u_id():
    """
    check_valid_u_id returns None if user exists
    check_valid_u_id raises an InputError if user doesn't exist
    """
    with pytest.raises(InputError):
        assert validation.check_valid_u_id(1)
        assert validation.check_valid_u_id(2)
        assert validation.check_valid_u_id("three")
    auth.auth_register("bobby@gmail.com", "Plays Piano", "Sure", "Thing")
    auth.auth_register("falling@down.the", "stairs", "asdf", "movie")
    assert validation.check_valid_u_id(1) == None
    assert validation.check_valid_u_id(2) == None
    other.clear()
    
def test_check_is_existing_channel_member():
    """
    Check if invitee is member of channel already
    raises Input error if found
    """
    user1 = auth.auth_register("it@is.qtr", "past12", "already","pleasestop")
    user2 = auth.auth_register("we@better.not", "havetodo", "thedata","functiontests")
    channel1 = channels.channels_create(user1["token"], "oriwillbemad", True)
    assert validation.check_is_existing_channel_member(user1["u_id"],channel1["channel_id"]) == None
    with pytest.raises(InputError):        
        assert validation.check_is_existing_channel_member(user2["u_id"],channel1["channel_id"])
    other.clear()
    
def test_check_is_channel_owner():
    """
    check_is_channel_owner returns None if user is a channel owner
    check_is_channel_owner raises an InputError if user is not a channel owner
    """
    user1 = auth.auth_register("it@is.qtr", "past12", "already","pleasestop")
    user2 = auth.auth_register("we@better.not", "havetodo", "thedata","functiontests")
    channel1 = channels.channels_create(user1["token"], "oriwillbemad", True)
    channel.channel_join(user2["token"], channel1["channel_id"])
    assert validation.check_is_channel_owner(user1["u_id"], channel1["channel_id"]) == None
    with pytest.raises(AccessError):
        assert validation.check_is_channel_owner(user2["u_id"], channel1["channel_id"])
    other.clear()

def test_check_isnot_channel_owner():
    """
    check_isnot_channel_owner returns None if user is not a channel owner
    check_isnot_channel_owner raises an InputError if useris a channel owner
    """
    user1 = auth.auth_register("gertrude@gmail.com", "past12", "hi","there")
    user2 = auth.auth_register("wedo@bigpond.not", "dapper", "metal","tuxedo")
    channel1 = channels.channels_create(user1["token"], "bellyflop", True)
    channel.channel_join(user2["token"], channel1["channel_id"])
    assert validation.check_isnot_channel_owner(user2["u_id"], channel1["channel_id"]) == None
    with pytest.raises(AccessError):
        assert validation.check_isnot_channel_owner(user1["u_id"], channel1["channel_id"])
    other.clear()

def test_valid_message():
    """
    valid_message returns None is message is valid
    valid_message raises an InputError if message is invalid
    """

    message = ""
    for _i in range(1000):
        message += "A"
    assert validation.valid_message(message) == None
    assert validation.valid_message("") == None
    message += "!"
    with pytest.raises(InputError):
        assert validation.valid_message(message)
    other.clear()

def test_valid_message_id():
    """
    valid_message_id returns None if message_id is valid
    valid_message_id raises an InputError if message_id is invalid
    """
    user1 = auth.auth_register("im@going.mad", "whatami", "doing","here")
    channel1 = channels.channels_create(user1["token"], "ineedsleepwtf", True)
    _message1 = message.message_send(user1["token"], channel1["channel_id"], "sleeppls")
    assert validation.valid_message_id(1) == None
    with pytest.raises(InputError):
        assert validation.valid_message_id(2)
    other.clear()

def test_check_channel_is_public():
    """
    check_channel_is_public returns nothing if the channel is public
    check_channel_is_public raises an AccessError if the channel is private
    """
    user1 = auth.auth_register("im@about.to", "gotosleep", "assoonasi", "finishthis")
    channel1 = channels.channels_create(user1["token"], "thisispublicwoo", True)
    channel2 = channels.channels_create(user1["token"], "someoneelsecandodata", False)
    assert validation.check_channel_is_public(channel1["channel_id"]) == None
    with pytest.raises(AccessError):
        assert validation.check_channel_is_public(channel2["channel_id"])
    other.clear()

def test_check_standup_running():
    """
    Checks tests check_standup_running and check_standup_not_running
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    # Tests check_standup_running raises an erro when no standup is running and
    # check_standup_not_running does not raise an error
    with pytest.raises(InputError):
        validation.check_standup_running(test_channel_id["channel_id"])
    validation.check_standup_not_running(test_channel_id["channel_id"])
    # Tests check_standup_not_running raises an error when a standup is running and
    # check_standup_running does not raise an error
    standup.standup_start(user_channel_creater["token"], test_channel_id["channel_id"], 1)
    with pytest.raises(InputError):
        validation.check_standup_not_running(test_channel_id["channel_id"])
    validation.check_standup_running(test_channel_id["channel_id"])

def test_check_length_valid():
    """
    Tests check_length_valid returns an error when the input is negative and doesn't when it is 
    positive
    """
    with pytest.raises(InputError):
        validation.check_length_valid(-1)
