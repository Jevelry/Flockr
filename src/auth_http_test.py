"""
re(regex module): Gives access to regex used in url fixture
subprocess(subprocess module): Gives access to opening other files(?)
signal(signal module): Gives access to signals
time(time module): Gives access to sleep (to start server)
json(json module): Gives access to data unpacking
requests(requests module): Gives access to automated server requests
pytest(pytest module): Gives access to pytest commands
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

# def register_2_users_and_assert_different(url, info1, info2) {
#     """
#     Registers 2 users and uses asserts to prove that they are different
#     """
#     resp1 = requests.post(url + '/auth/register', json=info1)
#     resp1 = requests.post(url + '/auth/register', json=info2)
#     payload1 = resp1.json()
#     payload2 = resp1.json()
#     assert user1['u_id'] != user2['u_id']
#     assert user1['token'] != user2['token']
# }

def test_successful_auth_register_http(url):
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
    resp1 = requests.post(url + '/auth/register', json=info1)
    resp2 = requests.post(url + '/auth/register', json=info2)
    user1 = resp1.json()
    user2 = resp2.json()
    assert user1['u_id'] != user2['u_id']
    assert user1['token'] != user2['token'] 

def test_same_names_auth_register_http_successful(url):
    """
    Testing successful uses of auth_register via http,
    focusing on same names
    """
    info1 = {
        'name_first' : 'George',
        'name_last' : 'Snurl',
        'email' : 'george@gmail.com',
        'password' : 'password123'
    }
    info2 = {
        'name_first' : 'George',
        'name_last' : 'Snurl',
        'email' : 'snurl@gmail.com',
        'password' : '123456789'
    }
    resp1 = requests.post(url + '/auth/register', json=info1)
    resp2 = requests.post(url + '/auth/register', json=info2)
    user1 = resp1.json()
    user2 = resp2.json()
    assert user1['u_id'] != user2['u_id']
    assert user1['token'] != user2['token'] 

def test_same_passwords_auth_register(url):
    """
    Tests successful uses of auth_register
    when using the same password
    """
    info1 = {
        'name_first' : 'Albert',
        'name_last' : 'Einsteib',
        'email' : 'emc3@gmail.com',
        'password' : 'password'
    }
    info2 = {
        'name_first' : 'Lays',
        'name_last' : 'Crusps',
        'email' : 'sourcream@gmail.com',
        'password' : 'password'
    }
    resp1 = requests.post(url + '/auth/register', json=info1)
    resp2 = requests.post(url + '/auth/register', json=info2)
    user1 = resp1.json()
    user2 = resp2.json()
    assert user1['u_id'] != user2['u_id']
    assert user1['token'] != user2['token'] 

# def test_same_names_auth_register_http_successful(url):
#     """
#     Testing successful uses of auth_reguster
#     when using the same name
#     """
#     test_info1 = {
#         'name_first' : 'George',
#         'name_last' : 'Snurl',
#         'email' : 'george@gmail.com',
#         'password' : 'password123'
#     }
#     test_info2 = {
#         'name_first' : 'George',
#         'name_last' : 'Snurl',
#         'email' : 'snurl@gmail.com',
#         'password' : '123456789'
#     }
#     resp1 = requests.post(url + '/auth/register', json=info1)
#     resp1 = requests.post(url + '/auth/register', json=info2)
#     payload1 = resp1.json()
#     payload2 = resp1.json()
#     assert user1['u_id'] != user2['u_id']
#     assert user1['token'] != user2['token'] 

def test_same_name_and_password_auth_register(url):
    """
    Tests successful uses of auth_register
    when using the same name and password
    """
    info1 = {
        'name_first' : 'Albert',
        'name_last' : 'Einsteib',
        'email' : 'emc3@gmail.com',
        'password' : 'password'
    }
    info2 = {
        'name_first' : 'Albert',
        'name_last' : 'Einsteib',
        'email' : 'sourcream@gmail.com',
        'password' : 'password'
    }
    resp1 = requests.post(url + '/auth/register', json=info1)
    resp2 = requests.post(url + '/auth/register', json=info2)
    user1 = resp1.json()
    user2 = resp2.json()
    assert user1['u_id'] != user2['u_id']
    assert user1['token'] != user2['token'] 

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
    payload1 = resp1.json()
    assert payload1['message'] == '<p>Email is invalid</p>'
    assert payload1['code'] == 400

    resp2 = requests.post(url + '/auth/register', json=info2)
    payload2 = resp2.json()
    assert payload2['message'] == '<p>Email is invalid</p>'
    assert payload2['code'] == 400

    resp3 = requests.post(url + '/auth/register', json=info3)
    payload3 = resp3.json()
    assert payload3['message'] == '<p>Email is invalid</p>'
    assert payload3['code'] == 400

    resp4 = requests.post(url + '/auth/register', json=info4)
    payload4 = resp4.json()
    assert payload4['message'] == '<p>Email is invalid</p>'
    assert payload4['code'] == 400

    resp5 = requests.post(url + '/auth/register', json=info5)
    payload5 = resp5.json()
    assert payload5['message'] == '<p>Email is invalid</p>'
    assert payload5['code'] == 400

    resp6 = requests.post(url + '/auth/register', json=info6)
    payload6 = resp6.json()
    assert payload6['message'] == '<p>Email is invalid</p>'
    assert payload6['code'] == 400

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
    requests.post(url + '/auth/register', json=info1)
    #resp1.json() == {}

    resp2 = requests.post(url + '/auth/register', json=info2)
    payload2 = resp2.json()
    assert payload2['message'] == '<p>Email already in use</p>'
    assert payload2['code'] == 400
    # assert resp2.json() == "Email is already used"

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
    payload1 = resp1.json()
    assert payload1['message'] == '<p>Password is not valid</p>'
    assert payload1['code'] == 400
    #assert resp1.json() == "Password is invalid"

    resp2 = requests.post(url + '/auth/register', json=info2)
    payload2 = resp2.json()
    assert payload2['message'] == '<p>Password is not valid</p>'
    assert payload2['code'] == 400
    #assert resp2.json() == "Password is invalid"

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
    payload1 = resp1.json()
    assert payload1['message'] == '<p>First name is not valid</p>'
    assert payload1['code'] == 400
    #assert resp1.json() == "First name is invalid"

    resp2 = requests.post(url + '/auth/register', json=info2)
    payload2 = resp2.json()
    assert payload2['message'] == '<p>First name is not valid</p>'
    assert payload2['code'] == 400
    #assert resp2.json() == "First name is invalid"

def test_invalid_last_name_auth_register(url):
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
    resp1 = requests.post(url + '/auth/register', json=info1)
    payload1 = resp1.json()
    assert payload1['message'] == '<p>Last name is not valid</p>'
    assert payload1['code'] == 400
    # payload = resp1.json()
    # assert payload.message == "Last name is invalid"
    #assert resp1.json() == "Last name is invalid"

    resp2 = requests.post(url + '/auth/register', json=info2)
    payload2 = resp2.json()
    assert payload2['message'] == '<p>Last name is not valid</p>'
    assert payload1['code'] == 400
    #assert resp2.json() == "Last name is invalid"
