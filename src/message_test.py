"""
    pytest: Gives access to pytest command (for testing)
    message(message.py): Gives access to message_send, message_remove, message_edit
    channel(channel.py): Gives access to channel functions
    auth(auth.py): Gives access to register, login and logout functions
    channels(channels.py): Gives access to channel_create
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
"""
import pytest
import message
import channel
import auth
import channels
import other
from error import InputError, AccessError

#Successful
def test_send_valid():
    """
    Testing if a single message can be sent and be stored
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                      message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                    test_channel_id["channel_id"], 0)
    assert message_exp == message_from_channel["messages"][0]["message"]
    assert test_user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_send_valid_multiple():
    """
    Testing if multiple messages can be sent and stored in correct order
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_user2 = auth.auth_register("thebumble@hotmail.com", "password", "Bumble", "Bee")
    test_user3 = auth.auth_register("cliffbooth@hotmail.com", "password", "Cliff", "Jumper")

    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    channel.channel_join(test_user2["token"], test_channel_id["channel_id"])
    channel.channel_join(test_user3["token"], test_channel_id["channel_id"])
    message_exp1 = "Test 1 bleep blop bloop"
    message_exp2 = "Test 2 1 0 1 1"
    message_exp3 = "Test 3 FLip Flop Slop"
    message_exp4 = "Test 4 Gling glong glip"
    message_id1 = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                       message_exp1)
    message_id2 = message.message_send(test_user2["token"], test_channel_id["channel_id"],
                                       message_exp2)
    message_id3 = message.message_send(test_user3["token"], test_channel_id["channel_id"],
                                       message_exp3)
    message_id4 = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                       message_exp4)
    message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                    test_channel_id["channel_id"], 0)

    assert message_exp1 == message_from_channel["messages"][3]["message"]
    assert test_user1["u_id"] == message_from_channel["messages"][3]["u_id"]
    assert message_id1["message_id"] == message_from_channel["messages"][3]["message_id"]

    assert message_exp2 == message_from_channel["messages"][2]["message"]
    assert test_user2["u_id"] == message_from_channel["messages"][2]["u_id"]
    assert message_id2["message_id"] == message_from_channel["messages"][2]["message_id"]

    assert message_exp3 == message_from_channel["messages"][1]["message"]
    assert test_user3["u_id"] == message_from_channel["messages"][1]["u_id"]
    assert message_id3["message_id"] == message_from_channel["messages"][1]["message_id"]

    assert message_exp4 == message_from_channel["messages"][0]["message"]
    assert test_user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id4["message_id"] == message_from_channel["messages"][0]["message_id"]

    other.clear()

def test_send_valid_long_message():
    """
    Testing if a 1000 character length message can be sent and be stored
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    #1000 character length string
    message_exp = (
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula "
        "eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient "
        "montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, "
        "pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, "
        "aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis "
        "vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras "
        "dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo "
        "ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus "
        "in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. "
        "Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper "
        "ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum "
        "rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum..."
    )
    message_id1 = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                       message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                    test_channel_id["channel_id"], 0)

    assert message_exp == message_from_channel["messages"][0]["message"]
    assert test_user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id1["message_id"] == message_from_channel["messages"][0]["message_id"]

    other.clear()


def test_send_invalid_long_message():

    """
    Testing if a message over 1000 characters long can be sent and be stored, and if raise Input Error
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    #1005 character length string
    message_exp = (
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula "
        "eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient "
        "montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, "
        "pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, "
        "aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis "
        "vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras "
        "dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo "
        "ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus "
        "in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. "
        "Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper "
        "ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum "
        "rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum... Long"
    )
    with pytest.raises(InputError):
        assert message.message_send(test_user1["token"], test_channel_id["channel_id"], message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                    test_channel_id["channel_id"], 0)
    assert message_exp != message_from_channel["messages"]

    other.clear()

def test_send_not_in_channel():
    """
    Testing if a single message can be sent by someone not in the channel
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    #The user has not joined the channel
    message_exp = "I'm not in the channel sad boi "
    with pytest.raises(AccessError):
        assert message.message_send(test_user1["token"], test_channel_id["channel_id"], message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                    test_channel_id["channel_id"], 0)
    assert message_exp != message_from_channel["messages"]

    other.clear()

def test_remove_valid_sender():
    """
    Testing if a single message can be sent, be stored and removed by sender
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_exp2 = "This is to stop there being no message in the channel"
    message_id = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                      message_exp)
    message.message_send(user_channel_creater["token"], test_channel_id["channel_id"],
                         message_exp2)
    message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                    test_channel_id["channel_id"], 0)
    #Checks that the message was added
    assert message_exp == message_from_channel["messages"][1]["message"]
    assert test_user1["u_id"] == message_from_channel["messages"][1]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][1]["message_id"]
    message.message_remove(test_user1["token"], message_id["message_id"])
    new_message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                        test_channel_id["channel_id"], 0)
    #Checks that the message was removed
    assert message_exp != new_message_from_channel["messages"][0]["message"]
    assert test_user1["u_id"] != new_message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] != new_message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_remove_valid_owner():

    """
    Testing if a single message can be sent, be stored and removed by owner
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    
    message_exp2 = "Test this is different from message_exp"
    message.message_send(user_channel_creater["token"], test_channel_id["channel_id"],
                         message_exp2)
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                      message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                    test_channel_id["channel_id"], 0)
    #Checks that the message was added
    assert message_exp == message_from_channel["messages"][0]["message"]
    assert test_user1["u_id"] == message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] == message_from_channel["messages"][0]["message_id"]
    message.message_remove(user_channel_creater["token"], message_id["message_id"])
    new_message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                        test_channel_id["channel_id"], 0)
    #Checks that the message was removed
    assert message_exp != new_message_from_channel["messages"][0]["message"]
    assert test_user1["u_id"] != new_message_from_channel["messages"][0]["u_id"]
    assert message_id["message_id"] != new_message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_remove_already_removed_message():
    """
    Testing if a message that has already been removed is removed again an input error appears
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                      message_exp)
    #Pre-removes the messages
    message.message_remove(user_channel_creater["token"], message_id["message_id"])
    with pytest.raises(InputError):
        message.message_remove(test_user1["token"], message_id["message_id"])
    other.clear()

def test_remove_multiple_messages_valid():
    """
    Testing if a message can be removed then a new message added then the new message removed
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id1 = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                       message_exp)
    #Pre-removes the message
    message.message_remove(user_channel_creater["token"], message_id1["message_id"])
    message_exp10 = "Spagetti and memeballs"
    message_id2 = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                       message_exp10)
    message_exp2 = "Test this is different from message_exp"
    message.message_send(user_channel_creater["token"], test_channel_id["channel_id"],
                         message_exp2)
    message.message_remove(test_user1["token"], message_id2["message_id"])
    new_message_from_channel = channel.channel_messages(user_channel_creater["token"],
                                                        test_channel_id["channel_id"], 0)
    assert message_exp != new_message_from_channel["messages"][0]["message"]
    assert test_user1["u_id"] != new_message_from_channel["messages"][0]["u_id"]
    assert message_id2["message_id"] != new_message_from_channel["messages"][0]["message_id"]
    other.clear()

def test_remove_same_message_multiple_message():
    """
    Testing is a message can be removed then a new messaged is added and try remove
    the old message again, this tests if the new id is not the same as the old id
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id1 = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                       message_exp)
    #Pre-removes the message
    message.message_remove(user_channel_creater["token"], message_id1["message_id"])
    message.message_send(test_user1["token"], test_channel_id["channel_id"],
                         message_exp)
    with pytest.raises(InputError):
        message.message_remove(test_user1["token"], message_id1["message_id"])
    other.clear()

def test_remove_not_owner_not_sender():
    """
    Tests that an error is raised when a person who is not the sender or owner is tries to
    remove a message
    """
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_user2 = auth.auth_register("thebumble@hotmail.com", "password", "Bumble", "Bee")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    channel.channel_join(test_user2["token"], test_channel_id["channel_id"])
    message_exp = "Test 1 test 2 swiggity Swagg"
    message_id1 = message.message_send(test_user1["token"], test_channel_id["channel_id"],
                                       message_exp)
    with pytest.raises(AccessError):
        message.message_remove(test_user2["token"], message_id1["message_id"])
    other.clear()

# Successful
def test_edit_valid_sender():
    """
    Testing if a single message can be sent, be stored and editted by sender
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    message.message_send(user_channel_creater['token'], test_channel_id['channel_id'],
                         message_exp2)
    message_id = message.message_send(test_user1['token'], test_channel_id['channel_id'],
                                      message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                    test_channel_id['channel_id'], 0)
    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    new_message = "This is the new message"
    message.message_edit(test_user1['token'], message_id['message_id'], new_message)
    new_message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                        test_channel_id['channel_id'], 0)
    #Checks that the message was changed
    assert new_message == new_message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == new_message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == new_message_from_channel['messages'][0]['message_id']
    other.clear()

def test_edit_valid_owner():
    """
    Testing if a single message can be sent, be stored and editted by owner
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    message.message_send(user_channel_creater['token'], test_channel_id['channel_id'],
                         message_exp2)
    message_id = message.message_send(test_user1['token'], test_channel_id['channel_id'],
                                      message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                    test_channel_id['channel_id'], 0)
    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    new_message = "This is the new message"
    message.message_edit(user_channel_creater['token'], message_id['message_id'], new_message)
    new_message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                        test_channel_id['channel_id'], 0)
    #Checks that the message was changed
    assert new_message == new_message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == new_message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == new_message_from_channel['messages'][0]['message_id']
    other.clear()

def test_edit_long_message_valid():
    """
    Testing if a 1000 character length message can be sent as an edit and be stored
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    #1000 character length string
    message_exp = ("This is the original message and will be changed")
    new_message = (
        'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula '
        'eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient '
        'montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, '
        'pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, '
        'aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis '
        'vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras '
        'dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo '
        'ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus '
        'in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. '
        'Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper '
        'ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum '
        'rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum...'
    )
    message_id1 = message.message_send(test_user1['token'], test_channel_id['channel_id'],
                                       message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                    test_channel_id['channel_id'], 0)

    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == message_from_channel['messages'][0]['message_id']

    message.message_edit(user_channel_creater['token'], message_id1['message_id'], new_message)
    new_message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                        test_channel_id['channel_id'], 0)

    assert new_message == new_message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == new_message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == new_message_from_channel['messages'][0]['message_id']

    other.clear()

# Unsuccessful
def test_edit_long_message_invalid():
    """
    Testing if a message over 1000 characters cannot be sent used to edit
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    # greater then 1000 character length string
    message_exp = ("This is the original message and will be changed")
    new_message = (
        'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula '
        'eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient '
        'montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, '
        'pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, '
        'aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis '
        'vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras '
        'dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo '
        'ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus '
        'in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. '
        'Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper '
        'ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum '
        'rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum...too long'
    )
    message_id1 = message.message_send(test_user1['token'], test_channel_id['channel_id'],
                                       message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                    test_channel_id['channel_id'], 0)

    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == message_from_channel['messages'][0]['message_id']

    with pytest.raises(InputError):
        message.message_edit(user_channel_creater['token'], message_id1['message_id'], new_message)

    other.clear()

def test_edit_no_message():
    """
    Tests that a message edit with no message acts as a delete
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    message.message_send(user_channel_creater['token'], test_channel_id['channel_id'],
                         message_exp2)
    message_id = message.message_send(test_user1['token'], test_channel_id['channel_id'],
                                      message_exp)
 
    message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                    test_channel_id['channel_id'], 0)
    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    #Uses the function message edit but has the message editted to an empty string
    message.message_edit(test_user1['token'], message_id['message_id'], '')
    new_message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                        test_channel_id['channel_id'], 0)
    #Checks that the message was removed
    assert message_exp != new_message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] != new_message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] != new_message_from_channel['messages'][0]['message_id']
    other.clear()

def test_edit_not_owner_or_creator():
    """
    Testing if an access error is raised if a user without authority tries to edit a message
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_user2 = auth.auth_register('anothertransformer@hotmail.com', 'password', 'New', 'Guy')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_exp2 = 'This is to stop there being no message in the channel'
    new_message = 'This is the edit message and changes'
    message.message_send(user_channel_creater['token'], test_channel_id['channel_id'],
                         message_exp2)
    message_id = message.message_send(test_user1['token'], test_channel_id['channel_id'],
                                      message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],
                                                    test_channel_id['channel_id'], 0)
    #Checks that the message was added
    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    new_message = "This is the new message"
    with pytest.raises(AccessError):
        message.message_edit(test_user2['token'], message_id['message_id'], new_message)
    other.clear()


'''
###################################################################################################
# Tests for message_react
# Successful    
def test_message_react_valid():
    """
    Testing if multiple messages can be reacted
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "First Channel", True)
    channel.channel_join(user2["token"], new_channel["channel_id"])
    
    test_message1 = "Hello Luke!"
    test_message2 = "Hi John!"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    message_id2 = message.message_send(user2["token"], new_channel["channel_id"], test_message2)
    message.message_react(user1["token"], message_id1["message_id"], 1)   
    message.message_react(user2["token"], message_id2["message_id"], 1)   
    message_from_channel = channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
      
    assert message_from_channel["messages"][0]["message"] == test_message1
    assert message_from_channel['messages'][0]['u_id'] == user1['u_id']
    assert message_from_channel['messages'][0]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][0]["time_created"] == 1606963294
    assert message_from_channel["messages"][0]["is_pinned"] == False
    assert message_from_channel["messages"][0]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][0]["reacts"]["u_id"] == user1["u_id"]
    assert message_from_channel["messages"][0]["reacts"]["is_this_user_reacted"] == True
    
    assert message_from_channel["messages"][1]["message"] == test_message1
    assert message_from_channel['messages'][1]['u_id'] == user1['u_id']
    assert message_from_channel['messages'][1]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][1]["time_created"] == 1606963294
    assert message_from_channel["messages"][1]["is_pinned"] == False
    assert message_from_channel["messages"][1]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][1]["reacts"]["u_id"] == user2["u_id"]
    assert message_from_channel["messages"][1]["reacts"]["is_this_user_reacted"] == True
    
    other.clear()
    

def test_message_react_same_message():
    """
    Testing if same message can be reacted by different users
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "First Channel", True)
    channel.channel_join(user2["token"], new_channel["channel_id"])
    
    test_message1 = "Hello Luke!"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)   
    message.message_react(user2["token"], message_id1["message_id"], 1)   
    message_from_channel = channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
    
    assert message_from_channel["messages"][0]["message"] == test_message1
    assert message_from_channel['messages'][0]['u_id'] == user1['u_id']
    assert message_from_channel['messages'][0]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][0]["time_created"] == 1606963294
    assert message_from_channel["messages"][0]["is_pinned"] == False
    assert message_from_channel["messages"][0]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][0]["reacts"]["u_id"] == user1["u_id"]
    assert message_from_channel["messages"][0]["reacts"]["is_this_user_reacted"] == True
    
    assert message_from_channel["messages"][0]["message"] == test_message1
    assert message_from_channel['messages'][0]['u_id'] == user2['u_id']
    assert message_from_channel['messages'][0]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][0]["time_created"] == 1606963294
    assert message_from_channel["messages"][0]["is_pinned"] == False
    assert message_from_channel["messages"][0]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][0]["reacts"]["u_id"] == user2["u_id"]
    assert message_from_channel["messages"][0]["reacts"]["is_this_user_reacted"] == True
    
    other.clear()
    

# Unsuccessful    
def test_message_react_invalid_message_id():
    """
    Testing that Input Error is raised when the message_id is an invalid message 
    that authorised use is member of
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "Star Wars", True)

    with pytest.raises(InputError):
        assert message.message_react(user1["token"], 123415, 1)

    other.clear()
    
def test_message_react_invalid_react_id():
    """
    Testing that Input Error is raised when the react_id is an invalid React ID 
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "Star Wars", True)
    
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    
    with pytest.raises(InputError):
        assert message.message_react(user1["token"], message1_id["message_id"], 2)

    other.clear()
	
	
def test_message_react_already_reacted():
    """
    Testing that Input Error is raised when a user attempts to react same message twice
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "Star Wars", True)
    
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)  
    
    with pytest.raises(InputError):
        assert message.message_react(user1["token"], message1_id["message_id"], 1)
        
    other.clear()
    
    
###################################################################################################
# Tests for message_unreact 
# Successful

def test_message_unreact_valid():
    """
    Testing if multiple messages can be unreacted 
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "First Channel", True)
    channel.channel_join(user2["token"], new_channel["channel_id"])
    
    test_message1 = "Hello Luke!"
    test_message2 = "Hi John!"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    message_id2 = message.message_send(user2["token"], new_channel["channel_id"], test_message2)
    message.message_react(user1["token"], message_id1["message_id"], 1)   
    message.message_react(user2["token"], message_id2["message_id"], 1)   
    message_from_channel = channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
      
    assert message_from_channel["messages"][0]["message"] == test_message1
    assert message_from_channel['messages'][0]['u_id'] == user1['u_id']
    assert message_from_channel['messages'][0]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][0]["is_pinned"] == False
    assert message_from_channel["messages"][0]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][0]["reacts"]["u_id"] == user1["u_id"]
    assert message_from_channel["messages"][0]["reacts"]["is_this_user_reacted"] == True
    
    assert message_from_channel["messages"][1]["message"] == test_message1
    assert message_from_channel['messages'][1]['u_id'] == user1['u_id']
    assert message_from_channel['messages'][1]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][1]["is_pinned"] == False
    assert message_from_channel["messages"][1]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][1]["reacts"]["u_id"] == user2["u_id"]
    assert message_from_channel["messages"][1]["reacts"]["is_this_user_reacted"] == True
    
    message.message_unreact(user1["token"], message_id1["message_id"], 1) 
    message.message_unreact(user2["token"], message_id2["message_id"], 1)   
      
    assert message_from_channel["messages"][0]["message"] == test_message1
    assert message_from_channel['messages'][0]['u_id'] == user1['u_id']
    assert message_from_channel['messages'][0]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][0]["is_pinned"] == False
    assert message_from_channel["messages"][0]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][0]["reacts"]["u_id"] == user1["u_id"]
    assert message_from_channel["messages"][0]["reacts"]["is_this_user_reacted"] == False
    
    assert message_from_channel["messages"][1]["message"] == test_message1
    assert message_from_channel['messages'][1]['u_id'] == user1['u_id']
    assert message_from_channel['messages'][1]['message_id'] == message_id['message_id']
    assert message_from_channel["messages"][1]["is_pinned"] == False
    assert message_from_channel["messages"][1]["reacts"]["react_id"] == 1
    assert message_from_channel["messages"][1]["reacts"]["u_id"] == user2["u_id"]
    assert message_from_channel["messages"][1]["reacts"]["is_this_user_reacted"] == False
    
    other.clear()
    
    
def test_message_unreact_same_message():
    """
    Testing if same message can be reacted by different users
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "First Channel", True)
    channel.channel_join(user2["token"], new_channel["channel_id"])
    
    test_message1 = "Hello Luke!"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)   
    message.message_react(user2["token"], message_id1["message_id"], 1)   
    message_from_channel = channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
    

    other.clear()
    
    
def test_message_unreact_invalid_message_id():
    """
    Testing that Input Error is raised when the message_id is an invalid message 
    that authorised use is member of
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "Star Wars", True)
       
    with pytest.raises(InputError):
        assert message.message_unreact(user1["token"], 123415, 1)

    other.clear()    
	

def test_message_unreact_invalid_react_id():
    """
    Testing that Input Error is raised when the react_id is an invalid React ID 
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "Star Wars", True)
    
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    message.message_react(user1["token"], message_id1["message_id"], 1)
    
    with pytest.raises(InputError):
        assert message.message_react(user1["token"], message1_id["message_id"], 2)

    other.clear()
	
	
def test_message_unreact_already_reacted():
    """
    Testing that Input Error is raised when a user attempts to unreact same message twice
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "Star Wars", True)
    
    test_message1 = "Hello"
    message_id1 = message.message_send(user1["token"], new_channel["channel_id"], test_message1)
    
    with pytest.raises(InputError):
        assert message.message_unreact(user1["token"], message1_id["message_id"], 1)
        
    other.clear()
###################################################################################################   
# Tests for message_pin
# Successful
'''                                 
def test_message_pin_valid():
    """
    Testing if multiple messages can be successfully pinned 
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    chan = channels.channels_create(user1["token"], "First Channel", True)['channel_id']
    channel.channel_join(user2["token"], chan)

    m1 = "Hi Luke!"
    m2 = "Hello John! Nice to meet you!"
    m_id1 = message.message_send(user1["token"], chan, m1)['message_id']
    m_id2 = message.message_send(user2["token"], chan, m2)['message_id']
	
    assert message.message_pin(user1["token"], m_id1) == {}
    assert message.message_pin(user1["token"], m_id2) == {}
	
    test = channel.channel_messages(user1["token"], chan, 0)
    assert test["messages"][1]["is_pinned"] == True
    assert test["messages"][0]["is_pinned"] == True

    other.clear()
    

# Unsuccessful    
def test_message_pin_invalid_message_id():
    """
    Testing that Input Error is raised when the message_id is invalid
    """
    user1 = auth.auth_register("vader@gmail.com", "father", "Anakin", "Skywalker")
    channels.channels_create(user1["token"], "Star Wars", True)

    with pytest.raises(InputError):
        assert message.message_pin(user1["token"], 123415)

    other.clear()
	
	
def test_message_pin_already_pinned():
    """
    Testing that Input Error is raised when user is trying to pin a message
    which has already been pinned
    """
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "Star Wars", True)['channel_id']		

    test_message1 = "Very proud of my new channel!"
    m_id1 = message.message_send(user1["token"], new_channel, test_message1)['message_id']
    message.message_pin(user1["token"], m_id1)

    with pytest.raises(InputError):
        assert message.message_pin(user1["token"], m_id1)
        
    other.clear()

    
def test_message_pin_not_member():
    """
    Testing that Access Error is raised when user who is not member of the channel
    tries to pin a message
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    new_channel = channels.channels_create(user2["token"], "General", True)['channel_id']

    test_message1 = "Very proud of my new channel!" 
    mess1 = message.message_send(user2["token"], new_channel, test_message1)

    with pytest.raises(AccessError):
        assert message.message_pin(user1["token"], mess1['message_id'])

    other.clear()
		
def test_message_pin_after_leaving():
    """
    Testing that Access Error is raised when owner of channel leaves and tries to
    pin a message in that channel
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    # user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    chan = channels.channels_create(user1["token"], "General", True)['channel_id']

    test_message1 = "Welcome!" 
    mess1 = message.message_send(user1["token"], chan, test_message1)['message_id'] 
    channel.channel_leave(user1["token"], chan)

    with pytest.raises(AccessError):
        assert message.message_pin(user1["token"], mess1)
        
    other.clear()	


def test_message_pin_not_owner():
    """
    Testing that Access Error is raised when the authorised user is not an owner
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    new_channel = channels.channels_create(user1["token"], "General", True)['channel_id']
    channel.channel_join(user2["token"], new_channel)

    test_message1 = "New channel is created"
    mess1 = message.message_send(user2["token"], new_channel, test_message1)['message_id']

    with pytest.raises(AccessError):
        assert message.message_pin(user2["token"], mess1)

    other.clear()
    

###################################################################################################    
# Tests for message_unpin
# Successful

def test_message_unpin_valid():
    """
    Testing if multiple messages can be successfully unpinned 
    """    
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyjang", "Lucy", "Jang")
    user2 = auth.auth_register("kevinhuang@gmail.com", "kevinhuang", "Kevin", "Huang")
    chan = channels.channels_create(user1["token"], "Project Chat", True)['channel_id']
    channel.channel_join(user2["token"], chan)

    msg1 = "Hey how's it going?"
    msg2 = "I'm going well!"
    mess1 = message.message_send(user1["token"], chan, msg1)['message_id']
    mess2 = message.message_send(user2["token"], chan, msg2)['message_id']

    message.message_pin(user1["token"], mess1) == {}
    message.message_pin(user1["token"], mess2) == {}

    messages = channel.channel_messages(user1["token"], chan, 0)
    assert messages["messages"][0]["is_pinned"] == True
    assert messages["messages"][1]["is_pinned"] == True

    assert message.message_unpin(user1["token"], mess1) == {}
    assert message.message_unpin(user1["token"], mess2) == {}

    messages = channel.channel_messages(user1["token"], chan, 0)
    assert messages["messages"][0]["is_pinned"] == False
    assert messages["messages"][1]["is_pinned"] == False

    other.clear()


# Unsuccessful
def test_message_unpin_invalid_message_id():
    """
    Testing that Input Error is raised when the message_id is invalid
    """
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyjang", "Lucy", "Jang")
    channels.channels_create(user1["token"], "Star Wars", True)

    with pytest.raises(InputError):
        assert message.message_unpin(user1["token"], 123415)

    other.clear()


def test_message_unpin_already_unpinned():
    """
	Testing that Input Error is raised when user attempts to unpin a message
	which is already unpinned
	"""	
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    chan = channels.channels_create(user1["token"], "General", True)['channel_id']    

    msg1 = "Hello"
    mess1 = message.message_send(user1["token"], chan, msg1)['message_id']
    message.message_pin(user1["token"], mess1)
    message.message_unpin(user1["token"], mess1)
    
    with pytest.raises(InputError):
        assert message.message_unpin(user1["token"], mess1)
        
    other.clear()
    
def test_message_unpin_never_pinned():
    """
    Testing that Input Error is raised when user attempts to unpin a message 
    which was never pinned
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    chan = channels.channels_create(user1["token"], "General", True)['channel_id']
    
    msg = "Hello"
    mess = message.message_send(user1["token"], chan, msg)['message_id']

    with pytest.raises(InputError):
        message.message_unpin(user1["token"], mess)
        
    other.clear()

    
def test_message_unpin_not_member():
    """
	Testing that Access Error is raised when user who is not member of the channel
	attempts to unpin a message
	"""
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    chan = channels.channels_create(user1["token"], "Star Wars", True)['channel_id']
    
    msg = "I am invincible"
    mess = message.message_send(user1["token"], chan, msg)['message_id']
    message.message_pin(user1["token"], mess)
    
    with pytest.raises(AccessError):
        assert message.message_unpin(user2["token"], mess)
        
    other.clear()
    

def test_message_unpin_after_leaving():
    """
    Testing that Access Error is raised when owner of channel leaves and attempts to
    unpin a message in that channel
    """
    user1 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    chan = channels.channels_create(user1["token"], "General", True)['channel_id']

    msg = "Welcome!" 
    mess = message.message_send(user1["token"], chan, msg)['message_id']  
    message.message_pin(user1["token"], mess)
    channel.channel_leave(user1["token"], chan)

    with pytest.raises(AccessError):
        assert message.message_unpin(user1["token"], mess)
        
    other.clear()	   
	

def test_message_unpin_not_owner():
    """
	Testing that Access Error is raised when the authorised user is not an owner
	"""   
    user1 = auth.auth_register("darthvader@gmail.com", "iamyourfather", "Anakin", "Skywalker")
    user2 = auth.auth_register("lukeskywalker@gmail.com", "starwars", "Luke", "Skywalker")
    chan = channels.channels_create(user1["token"], "Star Wars", True)['channel_id']
    channel.channel_join(user2["token"], chan)
    
    msg = "I am the owner of this channel"
    mess = message.message_send(user1["token"], chan, msg)['message_id']
    message.message_pin(user1["token"], mess)
    
    with pytest.raises(AccessError):
        message.message_unpin(user2["token"], mess)
        
    other.clear()
    

###################################################################################################     
# Tests for message_sendlater
# Sucessful
def test_message_sendlater_success():
    user = auth.auth_register('apple1@gmail.com', 'paswword' , 'first_name', 'last_name')
    chan = channels.channels_create(user['token'], 'test_channel', True)['channel_id']
    
    msg = 'Test message from the past!'
    mess = message.message_sendlater(user['token'], chan, msg, 1604707000)['message_id']

    message_list = channel.channel_messages(user['token'], chan, 0)
    assert message_list['messages'][0]['message'] == msg
    assert message_list['messages'][0]['message_id'] == mess
    assert message_list['messages'][0]['u_id'] == user['u_id']

    other.clear()

def test_message_sendlater_success_multiple():
    user1 = auth.auth_register('raspberry@gmail.com', 'paswword' , 'rasp', 'berry')
    user2 = auth.auth_register('blueberry@gmail.com', 'password', 'blue', 'berry')
    user3 = auth.auth_register('strawberry@gmail.com', 'password', 'straw', 'berry')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']
    channel.channel_join(user2['token'], chan)
    channel.channel_join(user3['token'], chan)

    msg1 = 'Test 1 bleep blop bloop'
    msg2 = 'Test 2 1 0 1 1'
    msg3 = 'Test 3 FLip Flop Slop'
    msg4 = 'Test 4 Gling glong glip'

    mess1 = message.message_sendlater(user1['token'], chan, msg1, 1604707000)['message_id']
    mess2 = message.message_sendlater(user2['token'], chan, msg2, 1604707001)['message_id']
    mess3 = message.message_sendlater(user3['token'], chan, msg3, 1604707002)['message_id']
    mess4 = message.message_sendlater(user1['token'], chan, msg4, 1604707003)['message_id']

    message_list = channel.channel_messages(user1['token'], chan,  0)
    assert message_list['messages'][0]['message'] == msg1
    assert message_list['messages'][0]['message_id'] == mess1
    assert message_list['messages'][0]['u_id'] == user1['u_id']

    assert message_list['messages'][1]['message'] == msg2
    assert message_list['messages'][1]['message_id'] == mess2
    assert message_list['messages'][1]['u_id'] == user2['u_id']

    assert message_list['messages'][2]['message'] == msg3
    assert message_list['messages'][2]['message_id'] == mess3
    assert message_list['messages'][2]['u_id'] == user3['u_id']

    assert message_list['messages'][3]['message'] == msg4
    assert message_list['messages'][3]['message_id'] == mess4
    assert message_list['messages'][3]['u_id'] == user1['u_id']

    other.clear()
    
# Unsucessful
def test_message_sendlater_invalid_channel():
    user1 = auth.auth_register('grape@gmail.com', 'paswword' , 'first_name', 'last_name')
    channels.channels_create(user1['token'], 'test_channel', True)
    
    msg = 'Test message from the past!'

    with pytest.raises(InputError):
        assert message.message_sendlater(user1['token'], 602, msg, 1606963294)
  
    other.clear()

def test_message_sendlater_invalid_message():
    user1 = auth.auth_register('mango@gmail.com', 'paswword' , 'first_name', 'last_name')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']


    msg = 'A' * 1001
    # test_message = (
    #     'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula '
    #     'eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient '
    #     'montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, '
    #     'pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, '
    #     'aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis '
    #     'vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras '
    #     'dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo '
    #     'ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus '
    #     'in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. '
    #     'Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper '
    #     'ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum '
    #     'rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum...too long'
    # )

    with pytest.raises(InputError):
        assert message.message_sendlater(user1['token'], chan, msg, 1606963294)

    other.clear()
    
def test_message_sendlater_invalid_time():
    user1 = auth.auth_register('melon@gmail.com', 'paswword' , 'first_name', 'last_name')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']
    
    msg = 'Test message from the future!'

    with pytest.raises(InputError):
        assert message.message_sendlater(user1['token'], chan, msg, 0)
  
    other.clear()

def test_message_sendlater_not_in_channel():
    user1 = auth.auth_register('melon@gmail.com', 'paswword' , 'first_name', 'last_name')
    user2 = auth.auth_register('blueberry@gmail.com', 'password', 'first_name', 'last_name')
    chan = channels.channels_create(user1['token'], 'test_channel', True)['channel_id']
    
    msg = 'Test message from the past!'

    with pytest.raises(AccessError):
        assert message.message_sendlater(user2['token'], chan, msg, 1606963294)
  
    other.clear()
