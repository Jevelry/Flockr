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
    assert user1['token'] is not None
    assert user2['token'] is not None
    assert user1['u_id'] is not None
    assert user2['u_id'] is not None
    assert len(user1) == 2
    assert len(user2) == 2

def test_edit_profile_and_messages(url):
    """
    Tests lots of functions
    * auth_register
    * channels_create
    * message_send
    * channel_join
    * message_remove
    * user_setname (successful and unsuccessful)
    * user_sethandle
    * message_edit
    * channel_messages
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


def test_registering_and_channel(url):
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
    
def hostile_takeover(url):
    """
    Tests a hostile takeover of a channel including:
    * auth_register
    * channels_create (private)
    * channel_invite
    * message_send
    * channel_removeowner
    * channel_addowner
    * channel_leave
    * auth_logout
    * user_profile_setname
    * user_profile_sethandle
    * user_profile_setemail
    * user_profile_sethandle
    * auth_login (successful and unsuccessful)
    * user_profile
    """
    # Joe and Henry register accounts
    user1_info = {
        'name_first' : 'Joe',
        'name_last' : 'Gostt',
        'email' : 'ttsogoej@liamg.moc',
        'password' : 'sdrawkcab'
    }
    user2_info = {
        'name_first' : 'Henry',
        'name_last' : 'Prill',
        'email' : 'henry@gmail.com',
        'password' : 'word pass'
    }
    resp1 = requests.post(url + '/auth/register', json=user1_info)
    Joe = resp1.json()
    
    resp2 = requests.post(url + '/auth/register', json=user2_info)
    Henry = resp2.json()

    assert_different_people(Joe, Henry)

    # Henry makes a new channel (General)
    chan1_info = {
        'token' : Henry['token'],
        'name' : 'General',
        'is_public' : False
    }

    resp3 = requests.post(url + '/channels/create', json=chan1_info)
    chan1 = resp3.json()
    assert len(chan1) == 1
    assert chan1['channel_id'] is not None

    # Henry invites Joe
    chan_invite = {
        'token' : Henry['token'],
        'channel_id' : chan1['channel_id'],
        'u_id' : Joe['u_id']
    }

    resp4 = requests.post(url + '/channel/invite', json=chan_invite)
    assert resp4.json() == {}

    # Joe says 'goodbye'
    message1 = {
        'token' : Joe['token'],
        'channel_id' : chan1['channel_id'],
        'message' : 'Goodbye :)'
    }
    
    resp5 = requests.post(url + '/message/send', json = message1)
    mess1 = resp5.json()
    assert len(mess1) == 1
    assert mess1['message_id'] is not None

    # Joe (owner of Flockr) removes Henry's owner privileges
    remove_owner_info = {
        'token' : Joe['token'],
        'channel_id' : chan1['channel_id'],
        'u_id' : Henry['u_id']
    }

    resp6 = requests.post(url + '/channnel/removeowner', json=remove_owner_info)
    assert resp6.json() == {}

    # Henry tries to get owner privileges back
    add_owner_info = {
        'token' : Henry['token'],
        'channel_id' : chan1['channel_id'],
        'u_id' : Henry['u_id']
    }
    
    resp7 = requests.post(url + '/channel/addowner', json=add_owner_info)
    resp7_payload = resp7.json()
    assert resp7_payload['message'] == '<p>User is not owner of channel<p>'
    assert resp7_payload['code'] == 400

    # Henry leaves channel
    leave_channel1 = {
        'token' : Henry['token'],
        'channel_id' : chan1['channel_id']
    }

    resp8 = requests.post(url + '/channel/leave', json=leave_channel1)
    assert resp8.json() == {}

    # Henry logs out
    logout1 = {
        'token' : Henry['token']
    }

    resp9 = requests.post(url + '/auth/logout', json=logout1)
    assert resp9.json() == { 'is_success' : True }

    # Joe edits message
    message_edit = {
        'token' : Joe['token'],
        'message_id' : mess1['message_id'],
        'message' : 'I win'
    }

    resp10 = requests.put(url + '/message/edit', json=message_edit)
    assert resp10.json() == {}

    # Joe leaves channel
    leave_channel2 = {
        'token' : Joe['token'],
        'channel_id' : chan1['channel_id']
    }

    resp11= requests.post(url + '/channel/leave', json=leave_channel2)
    assert resp11.json() == {}

    # Joe creates new channel (General)
    chan2_info = {
        'token' : Joe['token'],
        'name' : 'General',
        'is_public' : False
    }

    resp12 = requests.post(url + '/channels/create', json=chan2_info)
    chan2 = resp12.json()
    assert len(chan1) == 2
    assert chan2['channel_id'] is not None
    assert chan2['channel_id'] != chan1['channel_id']

    # Joe changes his name
    change_name1 = {
        'token' : Joe['token'],
        'name_first' : 'The',
        'name_last' : 'KING'
    }

    resp13 = requests.put(url + '/user/profile/setname', json=change_name1)
    assert resp13.json() == {}

    # Joe changes his email
    change_email = {
        'token' : Joe['token'],
        'email' : 'theKING@gmail.com'
    }
    resp14 = requests.put(url + '/user/profile/setemail', json = change_email)
    assert resp14.json() == {}

    # Joe changes his handle
    change_handle = {
        'token' : Joe['token'],
        'handle_str' : 'WeAreNumberOne'
    }
    resp15 = requests.put(url + '/user/profile/sethandle', json = change_handle_
    assert resp15.json() == {}

    # Joe changes his password
    change_password = {
        'token' : Joe['token'],
        'password' : 'The Winner Takes It All'
    }

    resp16 = requests.put(url + '/user/profile/changepassword', data=change_password)
    assert resp16.json() == {}

    # Joe logs off
    logout2 = {
        'token' : Joe['token']
    }
    resp17 = requests.post(url + '/auth/logout', json = logout2)
    assert resp17 == { 'is_success' : True }

    # Joe logs in unsuccessfully (Forgot about password change)
    login1 = {
        'email' : 'theKING@gmail.com'
        'password' : 'sdrawkcab'
    }

    resp18 = requests.post(url + '/auth/login', json = login1)
    resp18_payload = resp18.json()
    assert resp18_payload['message'] == '<p>Password is incorrect<p>'
    assert resp18_payload['code'] == 400

    # Joe logs in successfully
    login2 = {
        'email' : 'theKING@gmail.com'
        'password' : 'The Winner Takes It All'
    }

    resp19 = requests.post(url + '/auth/login', json = login2)
    new_Joe = resp19.json()
    assert len(resp19_payload) == 2
    assert new_Joe['token'] is not None
    assert new_Joe['u_id'] is not None
    assert new_Joe['u_id'] == Joe['u_id']

    # Joe admired his new profile
    profile_check = {
        'token' : new_Joe['token']
        'u_id' : new_Joe['u_id']
    }

    resp20 = requests.get(url + '/user/profile', params=profile_check)
    expected_user = {
        'name_first' : 'The',
        'name_last' : 'KING',
        'u_id' : 1,
        'email' : 'theKING@gmail.com',
        'handle_str' : 'WeAreNumberOne'
    }
    expected_profile = { 'user' : expected_user }
    assert resp20.json() == expected_profile

    # Joe logs out
    logout3 = {
        'token' : new_Joe['token']
    }
    resp21 = requests.post(url + '/auth/logout', json = logout3)
    assert resp21 == { 'is_success' : True }