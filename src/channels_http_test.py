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

def test_http_channels_list_single_user(url):
    test_channels_list_result = [
        {
        'channel_id' : 1,
        'name' : 'test channel',
        }
    ]

    user_reg = {
        'name_first' : 'Jack',
        'name_last' : 'Smith',
        'email' : 'jsmith123@gmail.com',
        'password' : 'password123'
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)
    user_jack = resp1.json()

    test_channel_info = {
        'token' : user_jack['token'],
        'name' : 'test channel',
        'is_public' : True,
    }

    requests.post(url + '/channels/create', json=test_channel_info)

    resp2 = requests.get(url + '/channels/list', params={'token' : user_jack['token']})
    assert json.loads(resp2.text) == test_channels_list_result

def test_http_channels_list_multiple_users(url):
    test_channels_list_result1 = [
        {
            'channel_id' : 1,
            'name' : "Jack's channel",
        }
    ]

    test_channels_list_result2 = [
        {
            'channel_id' : 2,
            'name' : "Jess' channel",
        }
    ]    

    user_reg1 = {
        'name_first' : 'Jack',
        'name_last' : 'Smith',
        'email' : 'jsmith123@gmail.com',
        'password' : 'password123',
    }

    user_reg2 = {
        'name_first' : 'Jess',
        'name_last' : 'Smith',
        'email' : 'jsmith321@gmail.com',
        'password' : 'password12321',
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg1)
    resp2 = requests.post(url + '/auth/register', json=user_reg2)
    user_jack = resp1.json()
    user_jess = resp2.json()
    
    test_channel_info1 = {
        'token' : user_jack['token'],
        'name' : "Jack's Channel"
        'is_public' : True,
    }

    test_channel_info2 = {
        'token' : user_jess['token'],
        'name' : "Jess' Channel",
        'is_public' : True,
    }

    requests.post(url + '/channels/create', json=test_channel_info1)
    requests.post(url + '/channels/create', json=test_channel_info2)

    resp3 = requests.get(url + '/channels/list', params={'token' : user_jack['token']})
    assert json.loads(resp3.text) == test_channels_list_result1

    resp4 = requests.get(url + '/channels/list', params={'token' : user_jess['token']})
    assert json.loads(resp4.text) == test_channels_list_result2

def test_http_channels_list_multiple_channels(url):
    test_channels_list_result = [
        {
            'channel_id' : 1,
            'name' : "Jack's channel",
        },
        {
            'channel_id' : 2,
            'name' : "Jack's channel too",
        },
        {
            'channel_id' : 3,
            'name' : "Jack's channel 3",
        }
    ]

    user_reg = {
        'name_first' : 'Jack',
        'name_last' : 'Donalds',
        'email' : 'jd123@gmail.com',
        'password' : 'password123',
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)    
    user_jack = resp1.json()

    test_channel_info1 = {
        'token' : user_jack['token'],
        'name' : "Jack's Channel"
        'is_public' : True,
    }

    test_channel_info2 = {
        'token' : user_jack['token'],
        'name' : "Jack's Channel too",
        'is_public' : True,
    }

    test_channel_info3 = {
        'token' : user_jack['token'],
        'name' : "Jack's Channel 3",
        'is_public' : True,
    }

    requests.post(url + '/channels/create', json=test_channel_info1)
    requests.post(url + '/channels/create', json=test_channel_info2)
    requests.post(url + '/channels/create', json=test_channel_info3)

    resp2 = requests.get(url + '/channels/list', params={'token' : user_jack['token']})
    assert json.loads(resp2.text) == test_channels_list_result

def test_http_channels_list_none(url):
    test_channels_list_result = []

    user_reg = {
        'name_first' : 'Ryan',
        'name_last' : 'Prince',
        'email' : 'rprince@gmail.com',
        'password' : 'password12321'
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)
    user_ryan = resp1.json()

    resp2 = requests.get(url + '/channels/list', params={'token' : user_ryan['token']})
    assert json.loads(resp2.text) == test_channels_list_result

def test_http_channels_list_invalid_token(url):
    user_reg = {
        'name_first' : 'Brad',
        'name_last' : 'Andrews',
        'email' : 'bandr3ws@gmail.com',
        'password' : 'passwordpass'
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)
    user_brad = resp1.json()

    test_channel_info = {
        'token' : user_brad['token']
        'name' : 'test channel',
        'is_public' : True,
    }

    requests.post(url + '/channels/create', json=test_channel_info)

    resp2 = requests.get(url + '/channels/list', params={'token' : 'invalid_token'})
    payload = resp2.json()
    assert payload['message'] == '<p>Token is invalid</p>'
    assert payload['code'] == 400

def test_http_channels_listall_successful(url):
def test_http_channels_listall_add_new(url):
def test_http_channels_listall_none(url):
def test_http_channels_listall_invalid_token(url):
    
def test_http_channels_create_public_successful(url):
    user_reg = {
        'name_first' : 'John',
        'name_last' : 'Smith',
        'email' : 'jsmith@gmail.com',
        'password' : 'password123',
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)
    user_john = resp1.json()

    test_channel_info = {
        'token' : user_john['token'],
        'name' : 'My Channel',
        'is_public' : True,
    }

    resp2 = requests.post(url + '/channels/create', json=test_channel_info)
    test_channel = resp2.json()
    assert test_channel['channel_id'] is not None
    assert test_channel['name'] == 'My Channel'

def test_http_channels_create_private_successful(url):
    user_reg = {
        'name_first' : 'Sam',
        'name_last' : 'Citizen',
        'email' : 'scitizen1@gmail.com',
        'password' : 'passwordword12',
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)
    user_sam = resp1.json()

    test_channel_info = {
        'token' : user_sam['token'],
        'name' : 'My Channel',
        'is_public' : False,
    }

    resp2 = requests.post(url + '/channels/create', json=test_channel_info)
    test_channel = resp2.json()
    assert test_channel['channel_id'] is not None
    assert test_channel['name'] == 'My Channel'

def test_http_channels_create_same_name_successful(url):
    user_reg = {
        'name_first' : 'Tom',
        'name_last' : 'Celery',
        'email' : 'celeryt@gmail.com',
        'password' : 'celeryandcarrots1',
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)
    user_tom = resp1.json()

    test_channel_info1 = {
        'token' : user_tom['token'],
        'name' : 'My Channel',
        'is_public' : True,
    }

    test_channel_info2 = {
        'token' : user_tom['token'],
        'name' : 'Our Channel',
        'is_public' : True,
    }

    resp1 = requests.post(url + '/channels/create', json=test_channel_info1)
    resp2 = requests.post(url + '/channels/create', json=test_channel_info2)
    test_channel1 = resp1.json()
    test_channel2 = resp2.json()
    assert test_channel1['channel_id'] != test_channel2['channel_id']
    assert test_channel1['name'] == test_channel2['name']

def test_http_channels_create_invalid_token(url):
    user_reg = {
        'name_first' : 'Lee',
        'name_last' : 'Le',
        'email' : 'leeleelee@gmail.com',
        'password' : 'applebanana123',
    }

    requests.post(url + '/auth/register', json=user_reg)

    test_channel_info = {
        'token' : 'invalid_token',
        'name' : 'test channel',
        'is_public' : True,
    }

    resp = requests.post(url + '/channels/create', json=test_channel_info)
    payload = resp.json()
    assert payload['message'] == '<p>Token is invalid</p>'
    assert payload['code'] == 400

def test_http_channels_create_invalid_name(url):
    user_reg = {
        'name_first' : 'Audrey',
        'name_last' : 'Johnson',
        'email' : 'ajohnson@gmail.com',
        'password' : 'Cupcakes123',
    }

    resp1 = requests.post(url + '/auth/register', json=user_reg)
    user_audrey = resp1.json()

    test_channel_info1 = {
        'token' : user_audrey['token'],
        'name' : 'A really long channel name',
        'is_public' : True,
    }

    test_channel_info2 = {
        'token' : user_audrey['token'],
        'name' : 'This is also a really long channel name but it is what it is',
        'is_public' : False,
    }

    resp1 = requests.post(url + '/channels/create', json=test_channel_info1)
    payload1 = resp1.json()
    assert payload1['message'] == '<p>Channel name cannot be more than 20 characters long</p>'
    assert payload1['code'] == 400

    resp2 = requests.post(url + '/channels/create', json=test_channel_info2)
    payload2 = resp2.json()
    assert payload2['message'] == '<p>Channel name cannot be more than 20 characters long</p>'
    assert payload2['code'] == 400