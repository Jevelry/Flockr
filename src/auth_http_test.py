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

def register_2_users_and_assert_different(url, info1, info2) {
    resp1 = requests.post(url + '/auth/register', json=info1)
    resp1 = requests.post(url + '/auth/register', json=info2)
    payload1 = resp1.json()
    payload2 = resp1.json()
    assert user1['u_id'] != user2['u_id']
    assert user1['token'] != user2['token'] 
}

def test_successful_auth_register_http():
    """
    Testing successful uses of auth_register via http
    """
    info1 = {
        'name_first' : 'Fred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : 'fredsmith'
    }
    info2 = {
        'name_first' : 'Gilbert',
        'name_last' : 'Gilligan',
        'email' : 'gillo@gmail.com',
        'password' : 'gilliweed'
    }
    register_2_users_and_assert_different(info1, info2)

def test_same_names_auth_register_http_successful(url):
    """
    Testing successful uses of auth_register via http,
    focusing on same names
    """
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
    register_2_users_and_assert_different(url, info1, info2)

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
    register_2_users_and_assert_different(url, info1, info2)

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

def test_same_name_and_password_auth_register(url):
    """
    Tests successful uses of auth_register
    when using the same name and password
    """
    test_info1 = {
        'name_first' : 'Albert',
        'name_last' : 'Einsteib',
        'email' : 'emc3@gmail.com',
        'password' : 'password'
    }
    test_info2 = {
        'name_first' : 'Albert',
        'name_last' : 'Einsteib',
        'email' : 'sourcream@gmail.com',
        'password' : 'password'
    }
    register_2_users_and_assert_different(url, test_info1, test_info2)

def test_invalid_email_auth_register_http(url):
    """
    Tests unsuccessful uses of auth_register
    when using a variety of invalid emails
    """
    info1 = {
        'name_first' : 'Guston',
        'name_last' : 'Marks',
        'email' : 'email',
        'password' : 'deguzman'
    }
    info2 = {
        'name_first' : 'Sprinkle',
        'name_last' : 'City',
        'email' : 'sprinkle@gmail',
        'password' : 'sparkly!'
    }
    info3 = {
        'name_first' : 'Freen',
        'name_last' : 'Sofa',
        'email' : '@gmail.com',
        'password' : 'yellow'
    }
    info4 = {
        'name_first' : 'Thisdesk',
        'name_last' : 'isbookable',
        'email' : 'dk@qrcode.',
        'password' : 'codeis4068'
    }
    info5 = {
        'name_first' : 'Donald',
        'name_last' : 'dlanoD',
        'email' : 'thedonATgmail.com',
        'password' : 'donalduck'
    }
    info6 = {
        'name_first' : 'Double',
        'name_last' : 'At',
        'email' : 'Double@gmail@bigpond.com',
        'password' : 'password'
    }
    resp1 = requests.post(url + '/auth/register', json=info1)
    assert resp1.json() == "Email is invalid"

    resp2 = requests.post(url + '/auth/register', json=info2)
    assert resp2.json() == "Email is invalid"

    resp3 = requests.post(url + '/auth/register', json=info3)
    assert resp3.json() == "Email is invalid"

    resp4 = requests.post(url + '/auth/register', json=info4)
    assert resp4.json() == "Email is invalid"

    resp5 = requests.post(url + '/auth/register', json=info5)
    assert resp5.json() == "Email is invalid"

    resp6 = requests.post(url + '/auth/register', json=info6)
    assert resp6.json() == "Email is invalid"

def test_existing_email_auth_register_http(url):
    """
    Tests successful uses of auth_register
    when using an existing email
    """
    info1 = {
        'name_first' : 'Frodo',
        'name_last' : 'ExceptModern',
        'email' : 'fred@gmail.com',
        'password' : 'Fredbaggins'
    }
    info2 = {
        'name_first' : 'French',
        'name_last' : 'Punishment',
        'email' : 'fred@gmail.com',
        'password' : 'Guillotine'
    }
    resp1 = requests.post(url + '/auth/register', json=info1)
    assert resp1.json() == {}

    resp2 = requests.post(url + '/auth/register', json=info2)
    assert resp2.json() == "Email is already used"

def test_invalid_password_auth_register_http(url):
    """
    Tests successful uses of auth_register
    when using an invalid password
    """
    info1 = {
        'name_first' : 'Arjun',
        'name_last' : 'Mukherjee',
        'email' : 'nottheking@gmail.com',
        'password' : ''
    }
    info2 = {
        'name_first' : 'Arjun',
        'name_last' : 'Toor',
        'email' : 'quiet@gmail.com',
        'password' : 'Arjun'
    }
    resp1 = requests.post(url + '/auth/register', json=info1)
    assert resp1.json() == "Password is invalid"

    resp2 = requests.post(url + '/auth/register', json=info2)
    assert resp2.json() == "Password is invalid"

def test_invalid_first_name_auth_register_http(url):
    """
    Tests successful uses of auth_register
    when using an invalid first name
    """
    info1 = {
        'name_first' : 'Wowthisreallyisabigfirstnameimaginethispersonsbirthcertificate',
        'name_last' : 'TheII',
        'email' : 'long@name.com',
        'password' : 'ThisIsShort'
    }
    info2 = {
        'name_first' : '',
        'name_last' : 'Thehonourable',
        'email' : 'hoolahoop@gmail.com',
        'password' : 'Bingbangbong'
    }
    resp1 = requests.post(url + '/auth/register', json=info1)
    assert resp1.json() == "First name is invalid"

    resp2 = requests.post(url + '/auth/register', json=info2)
    assert resp2.json() == "First name is invalid"

def test_invalid_last_name_auth_register():
    """
    Tests successful uses of auth_register
    when using an invalid last name
    """
    info1 = {
        'name_first' : 'Mark',
        'name_last' : 'WowIthoughtmylastnamewaslongbutitsjustpeanutscomparedtomarks',
        'email' : 'long@name.com',
        'password' : 'ShortPassword'
    }
    info2 = {
        'name_first' : 'Fruit',
        'name_last' : '',
        'email' : 'salad@gmail.com',
        'password' : 'YummyYummy'
    }
    resp1 = requests.post(url + '/auth/register', json=info1
    assert resp1.json() == "Last name is invalid"

    resp2 = requests.post(url + '/auth/register', json=info2)
    assert resp2.json() == "Last name is invalid"
