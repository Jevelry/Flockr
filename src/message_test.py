import message
import pytest
import channel
import auth
import channels
import other
from error import InputError, AccessError

def test_message_send_valid():
    """
    Testing if a single message can be sent and be stored
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    message_exp = 'Test 1 test 2 swiggity Swagg'
    message_id = message.message_send(test_user1['token'], test_channel_id['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],test_channel_id['channel_id'],0)
    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id['message_id'] == message_from_channel['messages'][0]['message_id']
    other.clear()

def test_message_send_valid_multiple():
    """
    Testing if multiple messages can be sent and stored in correct order
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_user2 = auth.auth_register('thebumble@hotmail.com', 'password', 'Bumble', 'Bee')
    test_user3 = auth.auth_register('cliffbooth@hotmail.com', 'password', 'Cliff', 'Jumper')

    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    channel.channel_join(test_user2['token'], test_channel_id['channel_id'])
    channel.channel_join(test_user3['token'], test_channel_id['channel_id'])
    message_exp1 = 'Test 1 bleep blop bloop'
    message_exp2 = 'Test 2 1 0 1 1'
    message_exp3 = 'Test 3 FLip Flop Slop'
    message_exp4 = 'Test 4 Gling glong glip'
    message_id1 = message.message_send(test_user1['token'], test_channel_id['channel_id'], message_exp1)
    message_id2 = message.message_send(test_user2['token'], test_channel_id['channel_id'], message_exp2)
    message_id3 = message.message_send(test_user3['token'], test_channel_id['channel_id'], message_exp3)
    message_id4 = message.message_send(test_user1['token'], test_channel_id['channel_id'], message_exp4)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],test_channel_id['channel_id'],0)
    
    assert message_exp1 == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == message_from_channel['messages'][0]['message_id']
    
    assert message_exp2 == message_from_channel['messages'][1]['message']
    assert test_user2['u_id'] == message_from_channel['messages'][1]['u_id']
    assert message_id2['message_id'] == message_from_channel['messages'][1]['message_id']
    
    assert message_exp3 == message_from_channel['messages'][2]['message']
    assert test_user3['u_id'] == message_from_channel['messages'][2]['u_id']
    assert message_id3['message_id'] == message_from_channel['messages'][2]['message_id']
    
    assert message_exp4 == message_from_channel['messages'][3]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][3]['u_id']
    assert message_id4['message_id'] == message_from_channel['messages'][3]['message_id']
    
    other.clear()

def test_message_valid_long_message():
    """
    Testing if a 1000 character length message can be sent and be stored 
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    #1000 character length string
    message_exp = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum...'
    message_id1 = message.message_send(test_user1['token'], test_channel_id['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],test_channel_id['channel_id'],0)
    
    assert message_exp == message_from_channel['messages'][0]['message']
    assert test_user1['u_id'] == message_from_channel['messages'][0]['u_id']
    assert message_id1['message_id'] == message_from_channel['messages'][0]['message_id']
    

    other.clear()


def test_message_invalid_long_message():
    
    """
    Testing if a message over 1000 characters long can be sent and be stored 
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    channel.channel_join(test_user1['token'], test_channel_id['channel_id'])
    #1002 character length string
    message_exp = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum Long'
    with pytest.raises(InputError):
        assert message.message_send(test_user1['token'], test_channel_id['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],test_channel_id['channel_id'],0)
    assert message_exp != message_from_channel['messages']

    other.clear()

def test_message_not_in_channel():
    """
    Testing if a single message can be sent by someone not in the channel
    """
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_channel_id = channels.channels_create(user_channel_creater["token"], 'test', True)
    #The user has not joined the channel
    message_exp = "I'm not in the channel sad boi "
    with pytest.raises(AccessError):
        assert message.message_send(test_user1['token'], test_channel_id['channel_id'], message_exp)
    message_from_channel = channel.channel_messages(user_channel_creater['token'],test_channel_id['channel_id'],0)
    assert message_exp != message_from_channel['messages']

    other.clear()

