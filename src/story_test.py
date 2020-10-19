"""
Contains all the 'user story' tests
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
    Allows pytest to create a new server.
    Returns url for new server.
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

def assert_different_people(user1, user2):
    assert user1 != user2
    assert user1['u_id'] != user2['u_id']
    assert user1['token'] != user2['token']

def test_edit_profile_and_messages():
    """
    Tests changing profile information and messages in groups
    """
    user1_reg = {
        'name_first' : 'Fred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : 'Freddo'
    }
    user2_reg = {
        'name_first' : 'Alan',
        'name_last' : 'Borm',
        'email' : 'alan@yahoo.com',
        'password' : 'Boromir'
    }
    # Fred and Alan register
    resp1 = requests.post(url + '/auth/register', json=user1_reg)
    resp2 = requests.post(url + '/auth/register', json=user2_reg)
    Fred = resp1.json()
    Alan = resp2.json()
    assert_different_people(Fred, Alan)

    chan1_info = {
        'token' : Fred['token'],
        'name' : 'Welcome',
        'is_public' : True
    }
    # Fred creates and joins channel 'Welcome'
    resp3 = requests.post(url + '/channels/create', json=chan1_info)
    chan1 = resp3.json()
    assert len(chan1) == 1
    assert chan1['channel_id'] is not None

    message1 = {
        'token' : Fred['token'],
        'channel_id' : chan1['channel_id'],
        'message' : "Hello nobody"
    }
    # Fred sends message to empty channel
    resp4 = requests.post(url + '/message/send', json=message1)
    mess1 = resp4.json()
    assert len(mess1) == 1
    assert mess1['message_id'] is not None

    chan_join_info = {
        'token' : Alan['token'],
        'channel_id' : chan1['channel_id']
    }
    # Alan joins channel
    resp5 = requests.post(url + '/channel/join', json=chan_join_info)
    assert resp5.json == {}

    message_remove1 = {
        'token' : Fred['token'],
        'message_id' : mess1['message_id']
    }
    # Fred deletes message
    resp6 = requests.delete(url+'/message/remove', json=message_remove1)
    assert resp6.json() == {}

    message2 = {
        'token' : Alan['token'],
        'channel_id' : chan1['channel_id'],
        'message' : "Good morning Fred!"
    }
    # Alan sends a message
    resp5 = requests.post(url + '/message/send', json=message2)
    mess2 = resp5.json()
    assert len(mess2) == 1
    assert mess2['message_id'] is not None
    assert mess1['message_id'] != mess2['message_id']

    change_name1 = {
        'token' : Fred['token'],
        'name_first' : "I wonder how long my name should be. Is there a limit or nah",
        'name_last' : "Wazco"
    }

    # Fred changes his name unsuccessfully
    resp6 = requests.put(url + '/user/profile/setname', json=change_name1)
    resp6_payload = resp6.json()
    assert resp6_payload['message'] == '<p>First name is not valid<p>'
    assert resp6_payload['code'] == 400

    change_name2 = {
        'token' : Fred['token'],
        'name_first' : 'George',
        'name_last' : 'Wazco'
    }
    # Fred changes his name successfully
    resp7 = requests.put(url + '/user/profile/setname', json=change_name2)
    assert resp7.json() == {}

    change_handle = {
        'token' : Fred['token'],
        'handle_str' : 'GeorgeTheWizard'
    }

    # Ex-Fred changes his handle
    resp8 = requests.put(url + '/user/profile/sethandle', json=change_handle)
    assert resp8.json() == {}

    message_edit1 = {
        'token' : Alan['token'],
        'message_id' : mess2['message_id'],
        'message' : 'Good morning George!'
    }
    # Alan edits his original message
    resp9 = requests.put(url + '/message/edit', json=message_edit1)
    assert resp9.json == {}

    chan1_messages = {
        'token' : Alan['token'],
        'channel_id' : chan1['channel_id'],
        'start' : 1
    }
    # Alan checks only his message using channel_messages
    resp10 = requests.get(url + '/channel/details', params=chan1_messages)
    payload10 = resp10.json()
    assert payload10['messages'] == [mess2['message_id']]
    assert payload10['start'] == 1
    assert payload10['end'] == -1


def test_registering_and_channel():
    reg_password_too_short = {
        'name_first' : 'Fred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : '123'
    }
    reg_email_invalid = {
        'name_first' : 'Fred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : '123'
    }
    reg_email_existing = {
        'name_first' : 'Fred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : '123'
    }
    reg_firstname_invalid = {
        'name_first' : 'FredFredFredFredFredFredFredFredFredFredFredFredFredFredFred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : '123'
    }
    reg_lastname_invalid = {
        'name_first' : 'Fred',
        'name_last' : 'SmithSmithSmithSmithSmithSmithSmithSmithSmithSmithSmith',
        'email' : 'fred@gmail.com',
        'password' : '123'
    }
        
    resp1 = requests.post(url + '/auth/register', json=reg_password_too_short)
    resp1_payload = resp1.json()
    assert resp1_payload['message'] == '<p>Password is not valid<p>'
    assert resp1_payload['code'] == 400
    
    resp2 = requests.post(url + '/auth/register', json=reg_email_invalid)
    resp2_payload = resp2.json()
    assert resp2_payload['message'] == '<p>Email is invalid<p>'
    assert resp2_payload['code'] == 400
    
    resp3 = requests.post(url + '/auth/register', json=reg_email_existing)
    resp3_payload = resp3.json()
    assert resp3_payload['message'] == '<p>Email already in use<p>'
    assert resp3_payload['code'] == 400
    
    resp4 = requests.post(url + '/auth/register', json=reg_firstname_invalid)
    resp4_payload = resp4.json()
    assert resp4_payload['message'] == '<p>First name is not valid<p>'
    assert resp4_payload['code'] == 400
    
    resp5 = requests.post(url + '/auth/register', json=reg_lastname_invalid)
    resp5_payload = resp5.json()
    assert resp5_payload['message'] == '<p>Last name is not valid<p>'
    assert resp5_payload['code'] == 400
    
