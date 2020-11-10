"""
Contains common "user story" tests
Will test error conditions that a user can reasonably do as in a user cannot pass in
an incorrect token

re(regex): Gives access to regex for valid_email
pytest(pytest module): Gives access to pytest command
"""
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest
import datetime


# Fixture which gets the URL of the server and starts it
@pytest.fixture
def url():
    """
    Allows pytest to create a new server.
    Returns url for new server.
    """
    url_re = re.compile(r" \* Running on ([^ ]*)")
    server = Popen(["python3", "src/server.py"], stderr = PIPE, stdout = PIPE)
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
    """
    Takes 2 user dictionaries and asserts they are
    2 different people with unique attributes
    """
    assert user1 != user2
    assert user1["u_id"] != user2["u_id"]
    assert user1["token"] != user2["token"]
    assert user1["token"] is not None
    assert user2["token"] is not None
    assert user1["u_id"] is not None
    assert user2["u_id"] is not None
    assert len(user1) == 2
    assert len(user2) == 2

def time_from_now(seconds):
    """
    returns a unix timestamp for x seconds in the future
    """
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=seconds)
    return future.timestamp()

def register_user(name_first, name_second, email, password, url):
    """
    Takes information about a user and registers them
    """
    user_reg = {
        "name_first" : name_first,
        "name_last" : name_second,
        "email" : email,
        "password" : password
        }
    resp = requests.post(url + "/auth/register", json = user_reg)
    return resp.json()

def logout_user(token, url):
    """
    Takes information about a user and logs them out
    """
    logout_info = {
        "token" : token
    }
    resp = requests.post(url + "/auth/logout", json = logout_info)
    return resp.json()

def login_user(email, password, url):
    """
    Takes information about a user and logs them in
    """
    login_info = {
        "email" : email,
        "password" : password
    }
    resp = requests.post(url + "/auth/login", json = login_info)
    return resp.json()

def create_channel(token, name, is_public, url):
    """
    Takes information about a channel and creates it
    """
    channel_info = {
        "token" : token,
        "name" : name,
        "is_public" : is_public
    }
    resp = requests.post(url + "/channels/create", json = channel_info)
    chan_dict = resp.json()
    return chan_dict['channel_id']

def channel_list(token, url):
    list_info = {
        'token' : token
    }
    resp = requests.get(url + "/channels/list", params = list_info)
    list_dict = resp.json()
    return list_dict['channels']

def channel_listall(token, url):
    list_info = {
        'token' : token
    }
    resp = requests.get(url + "/channels/listall", params = list_info)
    listall_dict = resp.json()
    return listall_dict['channels']

def join_channel(token, channel_id, url):
    """
    Takes information about user and channel and adds them
    """
    join_info = {
        "token" : token,
        "channel_id" : channel_id,
    }
    resp = requests.post(url + "/channel/join", json = join_info)
    return resp.json()

def invite_channel(token, channel_id, u_id, url):
    invite_info = {
        "token" : token,
        "channel_id" : channel_id,
        "u_id" : u_id
    }
    resp = requests.post(url + "/channel/invite", json = invite_info)
    return resp.json()

def leave_channel(token, channel_id, url):
    leave_info = {
        'token' : token,
        'channel_id' : channel_id
    }
    resp = requests.post(url + "/channel/leave", json = leave_info)
    return resp.json()

def check_messages(token, channel_id, start, url):
    """
    Takes information about channel and returns a list of messages
    """
    chan_info = {
        "token" : token,
        "channel_id" : channel_id,
        "start" : start
    }
    resp = requests.get(url + "/channel/messages", params = chan_info)
    return resp.json()

def channel_info(token, channel_id, url):
    chan_info = {
        "token" : token,
        "channel_id" : channel_id
    }
    resp = requests.get(url + "/channel/details", params = chan_info)
    return resp.json()

def add_owner(token, channel_id, u_id, url):
    add_info = {
        "token" : token,
        "channel_id" : channel_id,
        "u_id" : u_id
    }
    resp = requests.post(url + "/channel/addowner", json = add_info)
    return resp.json()

def remove_owner(token, channel_id, u_id, url):
    remove_info = {
        "token" : token,
        "channel_id" : channel_id,
        "u_id" : u_id
    }
    resp = requests.post(url + "/channel/removeowner", json = remove_info)
    return resp.json()

def send_message(token, channel_id, message, url):
    """
    Takes information about a messag and sends it to the channel
    """
    mess_info = {
        "token" : token,
        "channel_id" : channel_id,
        "message" : message
    }
    resp = requests.post(url + "/message/send", json = mess_info)
    message_dict = resp.json()
    if len(message_dict) == 1:
        return message_dict['message_id']
    return message_dict

def remove_message(token, message_id, url):
    remove_info = {
        "token" : token,
        "message_id" : message_id
    }
    resp = requests.delete(url + "/message/remove", json = remove_info)
    return resp.json()

def edit_message(token, message_id, message, url):
    edit_info = {
        "token" : token,
        "message_id" : message_id,
        "message" : message
    }
    resp = requests.put(url + "/message/edit", json = edit_info)
    return resp.json()

def sendlater(token, channel_id, message, time, url):
    later_info = {
        "token" : token,
        "channel_id" : channel_id,
        "message" : message,
        "time" : time
    }
    resp = requests.post(url + "/message/sendlater", json = later_info)
    later_dict = resp.json()
    return later_dict['message_id']

def react_message(token, message_id, react_id, url):
    react_info = {
        "token" : token,
        "message_id" : message_id,
        "react_id" : react_id
    }
    resp = requests.post(url + '/message/react', json = react_info)
    return resp.json()

def unreact_message(token, message_id, react_id, url):
    unreact_info = {
        "token" : token,
        "message_id" : message_id,
        "react_id" : react_id
    }
    resp = requests.post(url + '/message/unreact', json = unreact_info)
    return resp.json()

def pin_message(token, message_id, url):
    pin_info = {
        "token" : token,
        "message_id" : message_id
    }
    resp = requests.post(url + "/message/pin", json = pin_info)
    return resp.json()

def unpin_message(token, message_id, url):
    unpin_info = {
        "token" : token,
        "message_id" : message_id
    }
    resp = requests.post(url + "/message/unpin", json = unpin_info)
    return resp.json()

def send_later(token, channel_id, message, time_sent, url):
    later_info = {
        "token" : token,
        "channel_id" : channel_id,
        "message" : message,
        "time_sent" : time_sent
    }
    resp = requests.post(url + "/message/sendlater", json = later_info)
    later_dict = resp.json()
    return later_dict['message_id']

def check_profile(token, u_id, url):
    profile_info = {
        "token" : token,
        "u_id" : u_id
    }
    resp = requests.get(url + "/user/profile", params = profile_info)
    profile_dict = resp.json()
    return profile_dict['user']

def change_name(token, first, last, url):
    name_info = {
        "token" : token,
        "name_first" : first,
        "name_last" : last
    }
    resp = requests.put(url + "/user/profile/setname", json = name_info)
    return resp.json()

def change_handle(token, handle, url):
    handle_info = {
        "token" : token,
        "handle_str" : handle
    }
    resp = requests.put(url + "/user/profile/sethandle", json = handle_info)
    return resp.json()

def change_email(token, email, url):
    email_info = {
        "token" : token, 
        "email" : email
    }
    resp = requests.put(url + "/user/profile/setemail", json = email_info)
    return resp.json()
def change_password(token, password, url):
    password_info = {
        "token" : token, 
        "password" : password
    }
    resp = requests.put(url + "/user/profile/setpassword", json = password_info)
    return resp.json()

def search_message(token, query, url):
    search_info = {
        "token" : token, 
        "query_str" : query
    }
    resp = requests.get(url + "/search", params = search_info)
    search_dict = resp.json()
    return search_dict['messages']

def change_permission(token, u_id, perm_id, url):
    perm_info = {
        "token" : token,
        "u_id" : u_id,
        "permission_id" : perm_id
    }
    resp = requests.post(url + "/admin/userpermission/change", json = perm_info)
    return resp.json()

def user_list(token, url):
    list_info = {
        "token" : token
    }
    resp = requests.get(url + "/users/all", params = list_info)
    user_dict = resp.json()
    return user_dict['users']

def start_standup(token, channel_id, length, url):
    start_info = {
        "token" : token,
        "channel_id" : channel_id,
        "length" : length
    }
    resp = requests.post(url + "/standup/start", json = start_info)
    stan_info = resp.json()
    return stan_info['time_finish']

def get_standup(token, channel_id, url):
    get_info = {
        "token" : token, 
        "channel_id" : channel_id
    }
    resp = requests.get(url + "/standup/active", params = get_info)
    return resp.json()

def send_standup(token, channel_id, message, url):
    send_info = {
        "token" : token,
        "channel_id" : channel_id,
        "message" : message
    }
    resp = requests.post(url + "/standup/send", json = send_info)
    return resp.json()
# ========================================

def test_edit_profile_and_messages(url):
    """
    Tests editing everything that can be edited
    """

    # Fred and Alan register
    Fred = register_user("Fred","Smith", "fred@gmail.com", "Freddo", url)
    Alan = register_user("Alan","Borm", "alan@yahoo.com", "Boromir", url)

    assert_different_people(Fred, Alan)

    # Fred creates channel 'welcome'
    chan1 = create_channel(Fred['token'], "Welcome", True, url)
    assert chan1 == 1

    # Fred sends message to empty channel
    mess1 = send_message(Fred["token"], chan1, "Hello nobody :(", url)
    assert mess1 == 1

    # Alan join channel
    join1 = join_channel(Alan['token'], chan1, url)
    assert join1 == {}

    # Fred deletes message
    rem1 = remove_message(Fred['token'], mess1, url)
    assert rem1 == {}

    # Alan sends a message
    mess2 = send_message(Alan['token'], chan1, "Good morning Fred!", url)
    assert mess2 == 2

    # Fred changes his name unsuccessfully
    name_change1 = change_name(Fred['token'], 
        "I wonder how long my name should be. Is there a limit or nah",
        "Wazco", url)
    assert name_change1['message'] == "<p>First name is invalid</p>"
    assert name_change1['code'] == 400

    # Fred changes his last name successfully
    name_change2 = change_name(Fred['token'], "Howard", "Wazco", url)
    assert name_change2 == {}

    # Fred changes his handle unsuccessfully
    handle_change1 = change_handle(Fred['token'], "AlanBorm", url)
    assert handle_change1['message'] == "<p>Handle already in use</p>"
    assert handle_change1['code'] == 400 

    # Fred tries again
    handle_change2 = change_handle(Fred['token'], "HW", url)
    assert handle_change2['message'] == "<p>Handle is invalid</p>"
    assert handle_change2['code'] == 400 

    # Fred successfully changes his handle
    handle_change3 = change_handle(Fred['token'], "WazcoWizard", url)
    assert handle_change3 == {}

    # Alan edits his original message
    edit1 = edit_message(Alan['token'], mess2, "Good morning Howard!", url)
    assert edit1 == {}

    # Ex-Fred (now Howard) gets annoyed (sends attempted message)
    msg = "A" * 1001
    mess3 = send_message(Fred['token'], chan1, msg, url)
    assert mess3["message"] ==  "<p>Invalid message</p>"
    assert mess3['code'] == 400

    # Howard is now angry (sends messages)
    msg2 = ">:( " * 200
    mess4 = send_message(Fred['token'], chan1, msg2, url)
    assert mess4 == 3

    # Alan checks the message history using channel_messages
    history1 = check_messages(Alan['token'], chan1, 0, url)
    assert history1["messages"][0]["message"] == ">:( " * 200
    assert history1["messages"][1]["message"] == "Good morning Howard!"
    assert history1["start"] == 0
    assert history1["end"] == -1

def test_registering_login_and_logout(url):
    """
    Tests an attempt to register with invalid details (password, email, first name, last name) including:
    * auth_register
    * auth_logout
    * channel_create
    
    """
    #Yanik trying to register with password that is too short
    reg1 = register_user("Yanik", "Gulm", "bbq@gmail.com", "123", url)
    assert reg1["message"] == "<p>Password is invalid</p>"
    assert reg1["code"] == 400
    
    
    #Yanik trying to register with invalid email
    reg2 = register_user("Yanik", "Gulm", "yanik1@gmailcom", "123Ters", url)
    assert reg2["message"] == "<p>Email is invalid</p>"
    assert reg2["code"] == 400
    
    #Yanik tries to register with invalid first name
    name1 = "Yanik" * 20
    reg3 = register_user(name1, "Gulm", "bbq@gmail.com", "123Ters", url)
    assert reg3["message"] == "<p>First name is invalid</p>"
    assert reg3["code"] == 400
    
    #Yanik tries to register with invalid last name 
    name2 = "Gulm" * 20
    reg4 = register_user("Yanik", name2, "bbq@gmail.com", "123Ters", url)
    assert reg4["message"] == "<p>Last name is invalid</p>"
    assert reg4["code"] == 400
    
    #Yanik successfully registers
    Yanik = register_user("Yanik", "Gulm", "bbq@gmail.com", "123Ters", url)

    #Arthur trying to register with Yanik's email
    reg5 = register_user("Arthur", "Holmes", "bbq@gmail.com", "HMMMMM", url)
    assert reg5["message"] == "<p>Email already in use</p>"
    assert reg5["code"] == 400

    #Yanik creates a new channel called "My First Channel" and joins
    chan1 = create_channel(Yanik['token'], "My First Channel", True, url)
    assert chan1 == 1
    
    #Yanik successfully logs out
    logout1 = logout_user(Yanik['token'], url)
    assert logout1['is_success'] == True

    
def hostile_takeover(url):
    """
    Tests using commands with different channel permissions
    and changing profile attributes
    """
    # Joe and Henry register accounts
    Joe = register_user("Joe", "Gostt", "ttsogoej@liamg.moc", "sdrawkcab", url)
    Henry = register_user("Henry", "Prill", "henry@gmail.com", "word pass", url)

    assert_different_people(Joe, Henry)

    # Henry makes a new channel (General)
    chan1 = create_channel(Henry['token'], "General", False, url)
    assert chan1 == 1

    # Henry invites Joe
    invite1 = invite_channel(Henry['token'], chan1, Joe['u_id'], url)
    assert invite1 == {}

    # Joe says "goodbye"
    mess1 = send_message(Joe['token'], chan1, "Goodbye >:)", url)
    assert mess1 == 1

    # Joe (owner of Flockr) removes Henry's owner privileges
    remowner1 = remove_owner(Joe['token'], chan1, Henry['u_id'], url)
    assert remowner1 == {}

    # Henry tries to get owner privileges back
    addowner1 = add_owner(Henry['token'], chan1, Henry['u_id'], url)
    assert addowner1['message'] == "<p>User is not owner of channel</p>"
    assert addowner1['code'] == 400

    # Henry leaves channel
    leave1 = leave_channel(Henry['token'], chan1, url)
    assert leave1.json() == {}

    # Henry logs out
    logout1 = logout_user(Henry['token'], url)
    assert logout1 == { "is_success" : True }

    # Joe edits message
    edit1 = edit_message(Joe['token'], mess1, "I win.", url)
    assert edit1 == {}

    # Joe leaves channel
    leave2 = leave_channel(Joe['token'], chan1, url)
    assert leave2 == {}

    # Joe creates new channel (General)
    chan2 = create_channel(Joe['token'], "General", False, url)
    assert chan2 == 2

    # Joe changes his name
    name1 = change_name(Joe['token'], "The", "KING", url)
    assert name1 == {}

    # Joe changes his email
    email1 = change_email(Joe['token'], 'theKING@gmail.com', url)
    assert email1 == {}

    # Joe changes his handle
    handle1 = change_handle(Joe['token'], "WeAreNumberOne", url)
    assert handle1 == {}

    # Joe changes his password
    password1 = change_password(Joe['token'], 'The Winner Takes It All', url)
    assert password1 == {}

    # Joe logs off
    logout2 = logout_user(Joe['token'], url)
    assert logout2 == { "is_success" : True }

    # Joe logs in unsuccessfully (Forgot about password change)
    login1 = login_user("theKING@gmail.com", "sdrawkcab", url)
    assert login1["message"] == "<p>Password is incorrect<p>"
    assert login1["code"] == 400

    # Joe logs in successfully
    new_Joe = login_user("theKING@gmail.com", "The Winner Takes It All", url)
    assert len(new_Joe) == 2
    assert new_Joe["token"] is not None
    assert new_Joe["token"] != Joe["token"] # Could potentially fail 1 in 100,000 times
    assert new_Joe["u_id"] == Joe["u_id"]

    # Joe admired his new profile
    profile1 = check_profile(new_Joe['token'], new_Joe['u_id'], url)
    expected_user = {
        "name_first" : "The",
        "name_last" : "KING",
        "u_id" : 1,
        "email" : "theKING@gmail.com",
        "handle_str" : "WeAreNumberOne"
    }
    
    expected_profile = { "user" : expected_user }
    assert profile1 == expected_profile

    # Joe logs out
    logout3 = logout_user(new_Joe['token'], url)
    assert logout3 == { "is_success" : True }

def test_editing_removing_messages(url):
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

    # Paul and Seal register
    Paul = register_user("Paul", "Schlamp", "rs@bigpond.com", "m23rdewf2DE", url)
    Seal = register_user("Seal", "Sire", "FireSire@hotmail.com", "phlem$#PHLEM", url)

    assert_different_people(Paul, Seal)
    
    # Paul creates a channel "General"
    chan1 = create_channel(Paul['token'], "Misc", True, url)
    assert chan1 == 1
    
    # Seal joins the channel "Misc"
    join1 = join_channel(Seal['token'], chan1, url)
    assert join1 == {}

    # Paul and Seal send messages to each other in "Misc"
    msg1 = "First rule in general channel do not talkaboutgeneralchannel"
    mess1 = send_message(Seal['token'], chan1, msg1, url)
    assert mess1 == 1
    
    msg2 = "Second Rule ... First rule again"
    mess2 = send_message(Paul['token'], chan1, msg2, url)
    assert mess2 == 2
    
    msg3 = "You seem bad at this"
    mess3 = send_message(Seal['token'], chan1, msg3, url)
    assert mess3 == 3

    # Paul addes Seal as an owner of "Misc"
    addowner1 = add_owner(Paul['token'], chan1, Seal['u_id'], url)
    assert addowner1 == {}

    # Seal calls for a list of all messages in "Misc"
    messages1 = check_messages(Seal['token'], chan1, 0, url)
    assert len(messages1['messages']) == 3
    assert messages1["end"] == -1 

    # Seal edits a message
    msg4 = "New message YaYaYaYa" 
    for sent_message in messages1['messages']:
        edit = edit_message(Seal['token'], sent_message['message_id'], msg4, url)
        assert edit == {}

    messages2 = check_messages(Seal['token'], chan1, 0, url)
    assert len(messages2['messages']) == 3
    assert messages2["end"] == -1

    # Check message_edit worked
    for sent_message in messages2["messages"]:
        assert sent_message["message"] == msg4

    # Slam registers and joins the channel "Misc"
    Slam = register_user("Slam","Bam","nam@bigpond.net", "rightEOUS!ath", url)

    join2 = join_channel(Slam['token'], chan1, url)
    assert join2 == {}

    # Slam sends a message to "Misc"
    msg5 = "I love your channel"
    mess4 = send_message(Slam['token'], chan1, msg5, url)
    assert mess4 == 4

    # Slam deletes their message

    """Mimics how a person would find and delete a message"""
    search1 = search_message(Slam['token'], "love", url)
    assert len(search1) == 1

    for message in search1:
        found_message = message['message_id']
    rem1 = remove_message(Slam['token'], found_message, url)
    assert rem1 == {}

    # Slam sends a new message to "Misc"
    msg6 = "I REALLY love your channel"
    mess5 = send_message(Slam['token'], chan1, msg6, url)
    assert mess5 == 5

    # Seal removes the message
    rem2 = remove_message(Seal['token'], mess5, url)
    assert rem2 == {}

    messages3 = check_messages(Seal['token'], chan1, 0, url)
    assert len(messages3['messages']) == 3

def test_admin_permission_change(url):
    """
    Tests whether an owner of Flockr is an owner of all channels they've joined
    """

    # Jack and Jill register
    Jack = register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)
    Jill = register_user("Jill", "Smith", "jillsmith12@gmail.com", "jilljill123", url)

    assert_different_people(Jack, Jill)

    # Jack makes Jill an owner/admin of Flockr
    change_perm1 = change_permission(Jack['token'], Jill['u_id'], 1, url)
    assert change_perm1 == {}

    # Jack creates and joins a channel "Jack"s channel"
    chan1 = create_channel(Jack['token'], "Jack's Channel", True, url)
    assert chan1 == 1

    # Jill joins the channel
    join1 = join_channel(Jill['token'], chan1, url)
    assert join1 == {}

    # Jack checks for the owners of "Jack's Channel"
    channel_details = channel_info(Jack['token'], chan1, url)

    assert channel_details["name"] == "Jack's Channel"
    assert channel_details["owner_members"][0]["u_id"] == Jack["u_id"]
    assert channel_details["all_members"][0]["u_id"] == Jack["u_id"] 
    assert channel_details["all_members"][1]["u_id"] == Jill["u_id"]

def test_admin_permission_change_invalid(url):
    """
    Tests invalid inputs of changing owner/admin permissions
    """

    # Jack and Jill register
    Jack = register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)
    Jill = register_user("Jill", "Smith", "jillsmith12@gmail.com", "jilljill123", url)
    assert_different_people(Jack, Jill)

    # Jack attempts change Jill's permissions with nvalid permission_id value
    change_perm1 = change_permission(Jack['token'], Jill['u_id'], 3, url)
    assert change_perm1["message"] == "<p>Permission id is not a valid value</p>"
    assert change_perm1["code"] == 400

    # Jack attempts to make a non-existent member an owner/admin
    change_perm2 = change_permission(Jack['token'], "invalid_uid", 1, url)
    assert change_perm2["message"] == "<p>Target user does not exist</p>"
    assert change_perm2["code"] == 400

    # Jill attempts to change Jack"s permissions
    change_perm3 = change_permission(Jill['token'], Jack['u_id'], 2, url)
    assert change_perm3["message"] == "<p>User is not owner of Flockr</p>"
    assert change_perm3["code"] == 400


def test_invalid_user_inputs(url):
    """
    Tests realistic invalid inputs from a user.
    e.g Entering an incorrect password is realistic
    but passing an incorrect token is not very realistic
    because the user has little control over that
    """
    # Jack registers
    Jack = register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)

    # Jack attempts to change his first name to a short name
    name1 = change_name(Jack['token'], '', 'Smith', url)
    assert name1["message"] == "<p>First name is invalid</p>"
    assert name1["code"] == 400

    # Jack attempts to change his first name to a longer name
    msg1 = "JacksJacksJacksJacksJacksJacksJacksJacksJacksJacksJacks"
    name2 = change_name(Jack['token'], msg1, "Smith", url)
    assert name2["message"] == "<p>First name is invalid</p>"
    assert name2["code"] == 400

    # Jack attempts to change his last name to a shorter name
    name3 = change_name(Jack['token'], 'Jack', '', url)
    assert name3["message"] == "<p>Last name is invalid</p>"
    assert name3["code"] == 400

    # Jack attempts to change his last name to a longer name
    msg2 = "SmithSmithSmithSmithSmithSmithSmithSmithSmithSmithSmithSmith"
    name4 = change_name(Jack['token'], 'Jack', msg2, url)
    assert name4["message"] == "<p>Last name is invalid</p>"
    assert name4["code"] == 400

    # Jack attempts to change his email
    email1 = change_email(Jack['token'], 'jsmithgmail.com', url)
    assert email1["message"] == "<p>Email is invalid</p>"
    assert email1["code"] == 400

    # Jim registers
    Jim = register_user("Jim","Smath", "js@gmail.com", "pasffef2U", url)

    # Jack attempts to change his email to Jim's
    email2 = change_email(Jack['token'], 'js@gmail.com', url)
    assert email2["message"] == "<p>Email already in use</p>"
    assert email2["code"] == 400

    # Jack attempts to change his handle shorter
    handle1 = change_handle(Jack['token'], 'si', url)
    assert handle1["message"] == "<p>Handle is invalid</p>"
    assert handle1["code"] == 400

    # Jack attempts to make his handle longer
    msg3 = 'SisinSisinSisinSisinSisin'
    handle2 = change_handle(Jack['token'], msg3, url)
    assert handle2["message"] == "<p>Handle is invalid</p>"
    assert handle2["code"] == 400

    # Jim and Jack change their handles to be the same
    msg4 = "jsjsjsjs"
    handle3 = change_handle(Jack['token'], msg4, url)
    assert handle3 == {}

    handle4 = change_handle(Jim['token'], msg4, url)
    assert handle4["message"] == "<p>Handle already in use</p>"
    assert handle4["code"] == 400

    # Jack creates a channel "jackattacka"
    chan1 = create_channel(Jack['token'], "jackattacka", True, url)
    assert chan1 == 1

    # Jack sends some messages to "jackattacka"
    long_string = "602" * 1000
    mess1 = send_message(Jack['token'], chan1, long_string, url)
    assert mess1["message"] == "<p>Invalid message</p>" 
    assert mess1["code"] == 400

    msg5 = "fefebfoebfnijfcnshoffjZDfnJH"
    mess2 = send_message(Jack['token'], chan1, msg5, url)
    assert mess2 == 1

    # Jim joins "jackattacka"
    join1 = join_channel(Jim['token'], chan1, url)
    assert join1 == {}

    # Jim attempts to remove a message
    rem1 = remove_message(Jim['token'], mess2, url)
    assert rem1["message"] == "<p>User is not creator or owner</p>"
    assert rem1["code"] == 400

    # Jim attempts to edit a message
    edit1 = edit_message(Jim['token'], mess2, "We win these", url)
    assert edit1["message"] == "<p>User is not creator or owner</p>"
    assert edit1["code"] == 400

    # Jack attempts to edit a message
    edit2 = edit_message(Jack['token'], mess2, long_string, url)
    assert edit2["message"] == "<p>Invalid message</p>"
    assert edit2["code"] == 400

def test_list_users_and_channels(url):
    """
    Tests listing of all channels, channels of the user and all users on Flockr
    """
    # Jack and Jill register
    Jack = register_user("Jack", "Smith", "jsmith@gmail.com", "jackjack123", url)
    Jill = register_user("Jill", "Smith", "jillsmith12@gmail.com", "jilljill123", url)
    assert_different_people(Jack, Jill)

    # Jack gets a list of all users
    users = user_list(Jack['token'], url)
    assert users[0]["u_id"] == Jack["u_id"]
    assert users[1]["u_id"] == Jill["u_id"]

    # Jack creates and joins the channels "First" and "Second"
    chan1 = create_channel(Jack['token'], "First", True, url)
    chan2 = create_channel(Jack['token'], "Second", True, url)
    assert chan1 == 1
    assert chan2 == 2

    # Jack calls for a list of all channels in Flockr
    listall1 = channel_listall(Jack['token'], url)
    channels_listall_result = [
        {
            "channel_id" : 1,
            "name" : "First",
        },
        {
            "channel_id": 2,
            "name" : "Second"
        }
    ]

    assert listall1 == channels_listall_result

    # Jill joins "Second Channel"
    join1 = join_channel(Jill['token'], chan2, url)
    assert join1 == {}

    # Jill calls for a list of all channels she has joined
    listin1 = channel_list(Jill['token'], url)
    channels_list_result = [
        {
            "channel_id": 2,
            "name" : "Second"
        }
    ]
    # assert listin1 == {"channels" : channels_list_result}
    assert listin1 == channels_list_result

def test_message_interactions(url):
    """
    Tests every different thing you can do to a message
    """
    # Testing with owner permissinos
    user1 = register_user("Jeffrey", "Hoits", "jeffsemail@gmail.com", "gambling", url)
    assert user1['u_id'] == 1

    chan1 = create_channel(user1['token'], "Testing testing 123", False, url)
    assert chan1 == 1

    mess1 = send_message(user1['token'], chan1, "RADIOACTIVE -- DO NOT TOUCh", url)
    assert mess1 == 1

    pin1 = pin_message(user1['token'], mess1, url)
    assert pin1 == {}

    react1 = react_message(user1['token'], mess1, 1, url)
    assert react1 == {}

    edit1 = edit_message(user1['token'], mess1, 'pls stay pinned', url)
    assert edit1 == {}

    messages = check_messages(user1['token'], chan1, 0, url)
    assert messages['messages'][0]['is_pinned']

    unpin1 = unpin_message(user1['token'], mess1, url)
    assert unpin1 == {}

    unreact1 = unreact_message(user1['token'], mess1, 1, url)
    assert unreact1 == {}

    # Testing with member permissions
    user2 = register_user("Member", "ofGroup", "member@liamg.com", "member", url)
    assert_different_people(user1, user2)

    pin2 = pin_message(user2['token'], mess1, url)
    assert pin2['message'] == "<p>User is not owner of channel</p>"
    assert pin2['code'] == 400

    react2 = react_message(user1['token'], mess1, 1, url)
    assert react2 == {}

    edit2 = edit_message(user1['token'], mess1, 'pls stay pinned', url)
    assert edit2 == {}

    messages = check_messages(user1['token'], chan1, 0, url)
    assert not messages['messages'][0]['is_pinned']

    unpin2 = unpin_message(user2['token'], mess1, url)
    assert unpin2['message'] == "<p>Message is not currently pinned</p>"
    assert unpin2['code'] == 400


    unreact1 = unreact_message(user1['token'], mess1, 1, url)
    assert unreact1 == {}

    rem1 = remove_message(user2['token'], mess1, url)
    assert rem1['message'] == "<p>User is not creator or owner</p>"
    assert rem1['code'] == 400

    rem2 = remove_message(user1['token'], mess1, url)
    assert rem2 == {}

def test_interacting_with_standup_message(url):
    user = register_user("Standup", "Guy", "comedy@bigpond.com", "comedygold", url)
    assert user['u_id'] == 1

    chan1 = create_channel(user['token'], "LAUGH", False, url)
    assert chan1 == 1

    # Create a standup and send messages to it
    stan1 = start_standup(user['token'], chan1, 2, url)
    assert stan1 != {} and stan1 != None

    check1 = get_standup(user['token'], chan1, url)
    assert check1['is_active']
    assert check1['time_finish'] == stan1

    mess1 = send_standup(user['token'], chan1, "This is the end", url)
    assert mess1 == {}

    mess2 = send_standup(user['token'], chan1, "Message 2 :/", url)
    assert mess2 == {}

    check2 = get_standup(user['token'], chan1, url)
    assert check2 == check1

    # Sleep for more than standup to account for bad internet
    sleep(3)

    # Standup is finished
    check3 = get_standup(user['token'], chan1, url)
    assert check3 != check1
    assert not check3['is_active']

    # Find standup message (none of the functions return message_id)
    messages = check_messages(user['token'], chan1, 0, url)
    assert len(messages['messages']) == 1
    mess1 = messages['messages'][0]['message_id']
    assert mess1 == 1

    # Check if can interact with a standup message
    pin1 = pin_message(user['token'], mess1, url)
    assert pin1 == {}

    react1 = react_message(user['token'], mess1, 1, url)
    assert react1 == {}

    edit1 = edit_message(user['token'], mess1, 'STANDUP == BAD', url)
    assert edit1 == {}

    rem1 = remove_message(user['token'], mess1, url)
    assert rem1 == {}

    unpin1 = unpin_message(user['token'], mess1, url)
    assert unpin1['message'] == "<p>Message does not exist</p>"
    assert unpin1['code'] == 400

    unreact1 = unreact_message(user['token'], mess1, 1, url)
    assert unreact1['message'] == '<p>Message does not exist</p>'
    assert unreact1['code'] == 400

def test_interacting_with_sendlater_message(url):
    user = register_user("Sned", "Ltaer", "msg@gmail.com", "notnow", url)
    assert user['u_id'] == 1

    chan1 = create_channel(user['token'], "Cahnnel", True, url)
    assert chan1 == 1

    msg = "Hopefully this will arive soon"
    mess1 = send_later(user['token'], chan1, msg, time_from_now(2), url)
    assert mess1 == 1

    sleep(2)

    pin1 = pin_message(user['token'], mess1, url)
    assert pin1 == {}

    react1 = react_message(user['token'], mess1, 1, url)
    assert react1 == {}

    edit1 = edit_message(user['token'], mess1, 'SEDNLATRE != GOOD', url)
    assert edit1 == {}

    rem1 = remove_message(user['token'], mess1, url)
    assert rem1 == {}

    unpin1 = unpin_message(user['token'], mess1, url)
    assert unpin1['message'] == "<p>Message does not exist</p>"
    assert unpin1['code'] == 400

    unreact1 = unreact_message(user['token'], mess1, 1, url)
    assert unreact1['message'] == '<p>Message does not exist</p>'
    assert unreact1['code'] == 400

    