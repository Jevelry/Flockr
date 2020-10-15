"""
Really don't understand these yet
but we need a docstring
"""
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest
#import server



# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    """
    Does stuff. Returns server url
    """
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def register_2_users_and_assert_different(url, info1, info2):
    """
    Uses http to register 2 users and then
    uses asserts to prove u_id and tokens are unique (different)
    and that both users have been successfully registered.
    """
    resp1 = requests.post(url + '/auth/register', data=info1)
    resp2 = requests.post(url + '/auth/register', data=info2)
    user1 = json.loads(resp1.text)
    user2 = json.loads(resp2.text)

    assert user1['u_id'] != user2['u_id']
    assert user1['token'] != user2['token']

def test_auth_register_http_successful(url):
    """
    Testing successful uses of auth_register via http
    """
    test_info1 = {
        'name_first' : 'Fred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : 'fredsmith'
    }
    test_info2 = {
        'name_first' : 'Gilbert',
        'name_last' : 'Gilligan',
        'email' : 'gillo@gmail.com',
        'password' : 'gilliweed'
    }
    register_2_users_and_assert_different(url, test_info1, test_info2)

def test_same_names_auth_register_http_successful(url):
    test_info1 = {
        'name_first' : 'George',
        'name_last' : 'Snurl',
        'email' : 'george@gmail.com',
        'password' : 'password123'
    }
    test_info2 = {
        'name_first' : 'George',
        'name_last' : 'Snurl',
        'email' : 'snurl@gmail.com',
        'password' : '123456789'
    }
    register_2_users_and_assert_different(url, test_info1, test_info2)

def test_same_passwords_auth_register(url):
    """
    Tests successful uses of auth_register
    when using the same password
    """
    test_info1 = {
        'name_first' : 'Albert',
        'name_last' : 'Einsteib',
        'email' : 'emc3@gmail.com',
        'password' : 'password'
    }
    test_info2 = {
        'name_first' : 'Lays',
        'name_last' : 'Crusps',
        'email' : 'sourcream@gmail.com',
        'password' : 'password'
    }
    register_2_users_and_assert_different(url, test_info1, test_info2)

def test_invalid_email_auth_register_http(url):
    """
    Tests unsuccessful uses of auth_register
    when using an invalid email
    """
    test_info1 = {
        'name_first' : 'Guston',
        'name_last' : 'Marks',
        'email' : 'email',
        'password' : 'deguzman'
    }
    test_info2 = {
        'name_first' : 'Sprinkle',
        'name_last' : 'City',
        'email' : 'sprinkle@gmail',
        'password' : 'sparkly!'
    }
    test_info3 = {
        'name_first' : 'Freen',
        'name_last' : 'Sofa',
        'email' : '@gmail.com',
        'password' : 'yellow'
    }
    test_info4 = {
        'name_first' : 'Thisdesk',
        'name_last' : 'isbookable',
        'email' : 'dk@qrcode.',
        'password' : 'codeis4068'
    }
    test_info5 = {
        'name_first' : 'Donald',
        'name_last' : 'dlanoD',
        'email' : 'thedonATgmail.com',
        'password' : 'donalduck'
    }
    test_info6 = {
        'name_first' : 'Double',
        'name_last' : 'At',
        'email' : 'Double@gmail@bigpond.com',
        'password' : 'password'
    }
    resp1 = requests.post(url + '/auth/register', data=test_info1)
    assert json.loads(resp1.text) == "Email is invalid"

    resp2 = requests.post(url + '/auth/register', data=test_info2)
    assert json.loads(resp2.text) == "Email is invalid"

    resp3 = requests.post(url + '/auth/register', data=test_info3)
    assert json.loads(resp3.text) == "Email is invalid"

    resp4 = requests.post(url + '/auth/register', data=test_info4)
    assert json.loads(resp4.text) == "Email is invalid"

    resp5 = requests.post(url + '/auth/register', data=test_info5)
    assert json.loads(resp5.text) == "Email is invalid"

    resp6 = requests.post(url + '/auth/register', data=test_info6)
    assert json.loads(resp6.text) == "Email is invalid"

def test_existing_email_auth_register_http(url):
    """
    Tests successful uses of auth_register
    when using an existing email
    """
    test_info1 = {
        'name_first' : 'Frodo',
        'name_last' : 'ExceptModern',
        'email' : 'fred@gmail.com',
        'password' : 'Fredbaggins'
    }
    test_info2 = {
        'name_first' : 'French',
        'name_last' : 'Punishment',
        'email' : 'gillo@gmail.com',
        'password' : 'Guillotine'
    }
    resp1 = requests.post(url + '/auth/register', data=test_info1)
    assert json.loads(resp1.text) == "Email is already used"

    resp2 = requests.post(url + '/auth/register', data=test_info2)
    assert json.loads(resp2.text) == "Email is already used"

def test_invalid_password_auth_register_http(url):
    """
    Tests successful uses of auth_register
    when using an invalid password
    """
    test_info1 = {
        'name_first' : 'Arjun',
        'name_last' : 'Mukherjee',
        'email' : 'nottheking@gmail.com',
        'password' : ''
    }
    test_info2 = {
        'name_first' : 'Arjun',
        'name_last' : 'Toor',
        'email' : 'quiet@gmail.com',
        'password' : 'Arjun'
    }
    resp1 = requests.post(url + '/auth/register', data=test_info1)
    assert json.loads(resp1.text) == "Password is invalid"

    resp2 = requests.post(url + '/auth/register', data=test_info2)
    assert json.loads(resp2.text) == "Password is invalid"

def test_invalid_first_name_auth_register_http(url):
    """
    Tests successful uses of auth_register
    when using an invalid first name
    """
    test_info1 = {
        'name_first' : 'Wowthisreallyisabigfirstnameimaginethispersonsbirthcertificate',
        'name_last' : 'TheII',
        'email' : 'long@name.com',
        'password' : 'ThisIsShort'
    }
    test_info2 = {
        'name_first' : '',
        'name_last' : 'Thehonourable',
        'email' : 'hoolahoop@gmail.com',
        'password' : 'Bingbangbong'
    }
    resp1 = requests.post(url + '/auth/register', data=test_info1)
    assert json.loads(resp1.text) == "First name is invalid"

    resp2 = requests.post(url + '/auth/register', data=test_info2)
    assert json.loads(resp2.text) == "First name is invalid"

def test_invalid_last_name_auth_register():
    """
    Tests successful uses of auth_register
    when using an invalid last name
    """
    test_info1 = {
        'name_first' : 'Mark',
        'name_last' : 'WowIthoughtmylastnamewaslongbutitsjustpeanutscomparedtomarks',
        'email' : 'long@name.com',
        'password' : 'ShortPassword'
    }
    test_info2 = {
        'name_first' : 'Fruit',
        'name_last' : '',
        'email' : 'salad@gmail.com',
        'password' : 'YummyYummy'
    }
    resp1 = requests.post(url + '/auth/register', data=test_info1)
    assert json.loads(resp1.text) == "Last name is invalid"

    resp2 = requests.post(url + '/auth/register', data=test_info2)
    assert json.loads(resp2.text) == "Last name is invalid"
