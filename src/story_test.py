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

def register_user(name_first, name_second, email, password):
    user_reg = {
        'name_first' : name_first,
        'name_last' : name_second,
        'email' : email,
        'password' : password
        }
    resp = requests.post(url + '/auth/register', json=user_reg)
    return resp.json()


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

    # Fred and Alan register
    Fred = register_user('Fred','Smith','fred@gmail.com','Freddo')
    Alan = register_user('Alan','Borm','alan@yahoo.com','Boromir')

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

def test_registering_login_and_logout(url):
    """
    Tests an attempt to register with invalid details (password, email, first name, last name) including:
    * auth_register
    * auth_logout
    * channel_create
    
    """
    #Fred trying to register with password that is too short
    resp1_payload = register_user('Fred','Smith','fred@gmail.com','123')
    assert resp1_payload['message'] == '<p>Password is not valid<p>'
    assert resp1_payload['code'] == 400
    
    
    #Fred trying to register with invalid email
    resp2_payload = register_user('Fred','Smith','fred1@gmailcom','123Ters')
    assert resp2_payload['message'] == '<p>Email is invalid<p>'
    assert resp2_payload['code'] == 400
    
    #Fred trying to register with email which already exists
    resp3_payload = register_user('Fred','Smith','fred@gmail.com','123Ters')
    assert resp3_payload['message'] == '<p>Email already in use<p>'
    assert resp3_payload['code'] == 400
    
    #Trying to register with invalid first name
    resp4_payload = register_user('FredFredFredFredFredFredFredFredFredFredFredFredFredFredFred', 'Smith', 'fred2@gmail.com', '123Ters')
    assert resp4_payload['message'] == '<p>First name is not valid<p>'
    assert resp4_payload['code'] == 400
    
    #Trying to register with invalid last name 
    resp5_payload = register_user('Fred','SmithSmithSmithSmithSmithSmithSmithSmithSmithSmithSmith', 'fred3gmail.com', '123Ters')
    assert resp5_payload['message'] == '<p>Last name is not valid<p>'
    assert resp5_payload['code'] == 400
    
    #Fred successfully registers
    Fred = register_user('Fred', 'Silt', 'silt@gmail.com', '123Ters')
    #Fred creates a new channel called 'My First Channel' and joins
    chan1_info = {
        'token' : Fred['token'],
        'name' : "My First Channel",
        'is_public' : True
    }
    resp7 = requests.post(url + '/channels/create', json=chan1_info)
    chan1 = resp7.json()
    assert len(chan1) == 1
    assert chan1['channel_id'] is not None
    
    #Fred successfully logs out
    logout = {
        'token' : Fred['token']
    }
    resp8 = requests.post(url + '/auth/logout', json = logout)
    assert resp8 == { 'is_success' : True }

    
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
    Joe = register_user('Joe', 'Gostt', 'ttsogoej@liamg.moc', 'sdrawkcab')
    Henry = register_user('Henry', 'Prill', 'henry@gmail.com', 'word pass')

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
    resp15 = requests.put(url + '/user/profile/sethandle', json = change_handle)
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
        'email' : 'theKING@gmail.com',
        'password' : 'sdrawkcab'
    }

    resp18 = requests.post(url + '/auth/login', json = login1)
    resp18_payload = resp18.json()
    assert resp18_payload['message'] == '<p>Password is incorrect<p>'
    assert resp18_payload['code'] == 400

    # Joe logs in successfully
    login2 = {
        'email' : 'theKING@gmail.com',
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
        'token' : new_Joe['token'],
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

def editing_removing_messages(url):
    """
    Tests a user going on a message editing and removing spree:
    * auth_register
    * channels_create (public)
    * channel_join
    * channe_messages
    * message_send 
    * message_remove
    * message_edit
    * channel_addowner
    """
    # Joe and Henry register accounts
    Paul = register_user('Paul', 'Schlamp', 'rs@bigpond', 'm23rdewf2DE')
    Seal = register_user('Seal', 'Sire', 'FireSire@hotmail.com', 'phlem$#PHLEM')

    chan1_info = {
        'token' : Paul['token'],
        'name' : 'General',
        'is_public' : True,
    }

    resp3 = requests.post(url + '/channels/create', json=chan1_info)
    chan1 = resp3.json()
    
    chan1_join = {
        'token' : Seal['token'],
        'channel_id' : chan1['channel_id'],
    }

    resp4 = requests.post(url + '/channel/join', json=chan1_join)
    assert resp4.json() == {}

    message1_1_info = {
        'token' : Paul['token'],
        'channel_id': chan1['channel_id'],
        'message' : 'First rule in general channel do not talkaboutgeneralchannel'
    }
    requests.post(url + 'message/send', json=message1_1_info)

    message1_2_info = {
        'token' : Paul['token'],
        'channel_id' : chan1['channel_id'],
        'message' : 'Second Rule ... First rule again',
    }

    requests.post(url + 'message/send', json=message1_2_info)

    message1_3_info = {
        'token' : Seal['token'],
        'channel_id' : chan1['channel_id'],
        'message' : 'You seem bad at this'
    }

    requests.post(url + 'message/send', json=message1_3_info)


    addowner_info = {
        'token' : Paul['token'],
        'channel_id' : chan1['channel_id'],
        'u_id' : Seal['u_id'],
    }

    resp8 = requests.post(url + 'channel/addowner', json=addowner_info)
    assert resp8.json() == {}

    get_messages_info = {
        'token' : Seal['token'],
        'channel_id' : chan1['channel_id'],
        'start' : 0
    }
    resp9 = requests.post(url + 'channel/messages',json=get_messages_info)
    channel_message1 = resp9.json()
    assert channel_message1['end'] == -1 

    for sent_message in channel_message1['messages']:
        edit_message_info = {
            'token' : Seal['token'],
            'message_id' : sent_message['message_id'],
            'message' : 'New message YaYaYaYa' 
        }
        resp10 = requests.post(url + 'message/edit', json=edit_message_info)
        assert resp10.json() == {}

    resp11 = requests.post(url + 'channel/messages',json=get_messages_info)
    channel_message2 = resp11.json()
    assert channel_message2['end'] == -1

    for sent_message in channel_message2['messages']:
        assert sent_message['message'] == 'New message YaYaYaYa'
        assert sent_message['u_id'] == Seal['u_id']

    user3_info = {
        'name_first' : 'Slam',
        'name_last' : 'Bam',
        'email' : 'nam@bigpond.net',
        'password' : 'rightEOUS!ath'
    }

    resp12 = requests.post(url + '/auth/register', json=user3_info)
    Slam = resp12.json()

    chan1_join2 = {
        'token' : Slam['token'],
        'channel_id' : chan1['channel_id'],
    }

    resp13 = requests.post(url + 'channel/join', json=chan1_join2)
    assert resp13.json() == {}

    message1_4_info = {
        'token' : Slam['token'],
        'channel_id': chan1['channel_id'],
        'message' : 'I love your channel'
    }

    requests.post(url + 'message/send', json=message1_4_info)

    get_messages_info2 = {
        'token' : Slam['token'],
        'channel_id' : chan1['channel_id'],
        'start' : 0
    }

    resp15 = requests.post(url + 'channel/messages', json=get_messages_info2)
    channel_message3 = resp15.json()

    """Minics how a person would find and delete a message"""
    for message in channel_message3['messages']:
        if message['message'] == 'I love your channel':
            message_remove_info = {
                'token' : Slam['token'],
                'message_id' : message['message_id'],
            }
            resp16 = requests.post(url + 'message/remove', json=message_remove_info)
            assert resp16.json() == {}

    message1_5_info = {
        'token' : Slam['token'],
        'channel_id' : chan1['channel_id'],
        'message' : 'I REALLY love your channel',
    }

    resp17 = requests.post(url + 'message/send', json=message1_5_info)
    message1_5 = resp17.json()

    message_remove_info = {
        'token' : Seal['token'],
        'message_id' : message1_5['message_id'],
    }

    resp18 = requests.post(url + 'message/remove',json=message_remove_info)
    assert resp18.json() == {}

    resp19 = requests.post(url + 'channel/messages',json=get_messages_info2)
    channel_message4 = resp19.json()

    assert 'I REALLY love your channel' not in channel_message4['messages']['message']

def test_admin_permission_change(url):
    """
    Tests whether an owner of Flockr is an owner of all channels they've joined
    """
    # Jack and Jill register
    Jack = register_user('Jack', 'Smith', 'jsmith@gmail.com', 'jackjack123')
    Jill = register_user('Jill', 'Smith', 'jillsmith12@gmail.com', 'jilljill123')
    assert_different_people(Jack, Jill)

    # Jack makes Jill an owner/admin of Flockr
    admin_change_params =  {
        'token' : Jack['token'],
        'u_id' : Jill['u_id'],
        'permission_id' : 1,
    }

    resp1 = requests.post(url + '/admin/userpermssion/change',json=admin_change_params)
    assert resp1.json() == {}

    # Jack creates and joins a channel 'Jack's channel'
    channel_create_info = {
        'token' : Jack['token'],
        'name' : "Jack's Channel",
        'is_public' : True,
    }

    resp2 = requests.post(url + '/channels/create', json=channel_create_info)
    channel = resp2.json()

    # Jill joins the channel
    channel_join_info = {
        'token' : Jill['token'],
        'channel_id' : channel['channel_id'],
    }

    requests.post(url + '/channel/join',json=channel_join_info)

    # Jack checks for the owners of 'Jack's Channel'
    channel_detail_request = {
        'token' : Jack['token'],
        'channel_id' : channel['channel_id'],
    }

    resp3 = requests.get(url + '/channel/details',json=channel_detail_request)
    channel_details = resp3.json()
    assert channel_details['name'] == "Jack's Channel"
    assert channel_details['owner_members'] == [Jack['u_id'], Jill['u_id']]
    assert channel_details['all_members'] == [Jack['u_id'], Jill['u_id']]

def test_admin_permission_change_invalid(url):
    """
    Tests invalid inputs of changing owner/admin permissions
    """
    # Jack and Jill register
    Jack = register_user('Jack', 'Smith', 'jsmith@gmail.com', 'jackjack123')
    Jill = register_user('Jill', 'Smith', 'jillsmith12@gmail.com', 'jilljill123')
    assert_different_people(Jack, Jill)

    # Jack attempts change Jill's permissions with nvalid permission_id value
    admin_change_params1 =  {
        'token' : Jack['token'],
        'u_id' : Jill['u_id'],
        'permission_id' : 3,
    }

    resp1 = requests.post(url + '/admin/userpermssion/change',json=admin_change_params1)
    payload1 = resp1.json()
    assert payload1['message'] == '<p>Invalid permission_id value</p>'
    assert payload1['code'] == 400

    # Jack attempts to make a non-existent member an owner/admin
    admin_change_params2 =  {
        'token' : Jack['token'],
        'u_id' : 'invalid_uid',
        'permission_id' : 1,
    }

    resp2 = requests.post(url + '/admin/userpermssion/change',json=admin_change_params2)
    payload2 = resp2.json()
    assert payload2['message'] == '<p>Invalid u_id</p>'
    assert payload2['code'] == 400

    # Jill attempts to change Jack's permissions
    admin_change_params3 =  {
        'token' : Jill['token'],
        'u_id' : Jack['u_id'],
        'permission_id' : 2,
    }

    resp3 = requests.post(url + '/admin/userpermssion/change',json=admin_change_params3)
    payload3 = resp3.json()
    assert payload3['message'] == '<p>User is not an owner</p>'
    assert payload3['code'] == 400


    
