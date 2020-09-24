import auth
import channels 
import channel
import pytest
from error import InputError
from error import AccessError

def test_channel_invite():
    
    
    
       



def test_channel_invite_excpet():
    with pytest.raises(InputError) as e:
        




def test_channel_details():
    auth_register(best_group123@gmail.com, awesome, best, group)
    auth_register(bestest_group123@gmail.com, awesome, bestest, group)
    channel_id = channels_create(best_group123@gmail.com, temp_channel, 0) 
    channel_invite(best_group123@gmail.com, channel_id, 2)
    assert channel_details(bestest_group123@gmail.com, channel_id)

#Checks a token with authority can join a channel
def test_channel_join_valid():
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_user2 = auth.auth_register('thebumble@hotmail.com', 'password', 'Bumble', 'Bee')
    test_user3 = auth.auth_register('cliffbooth@hotmail.com', 'password', 'Cliff', 'Jumper')
    test_channel_id1 = channels.channels_create(user_channel_creater["token"] ,'test_channel_id1', True)
    
    #Checks a user can join a public channel Valid
    channel.channel_join(test_user1['token'],test_channel_id1)
    channel.channel_join(test_user2['token'],test_channel_id1)
    channel.channel_join(test_user3['token'],test_channel_id1)
    list_result1 = channels.channels_list(test_user1['token'])
    list_result2 = channels.channels_list(test_user2['token'])
    list_result3 = channels.channels_list(test_user3['token'])
    assert list_result1[0] == test_channel_id1
    assert list_result2[0] == test_channel_id1
    assert list_result3[0] == test_channel_id1
    test_public_channel_details = channel.channel_details(test_user1['token'],test_channel_id1)
    
    member1 = None
    for member in check_members.all_members:
        if member["u_id"] == test_user1["u_id"]:
            member1 = member            
    assert(member1 is not None)
    member2 = None
    for member in check_members.all_members:
        if member["u_id"] == test_user2["u_id"]:
            member2 = member            
    assert(member2 is not None)
    member3 = None
    for member in check_members.all_members:
        if member["u_id"] == test_user3["u_id"]:
            member1 = member            
    assert(member3 is not None)

#test for an invalid channel id
def test_channel_join_invalid_channel():
    test_user1 = auth.auth_register('testHotRod@hotmail.com', 'password', 'Hot','Rod')
    with pytest.raises(InputError) as e:
        channel.channel_join(test_user1["token"],invalid_channel_id)
    list_result1 = channels.channels_list(test_user1['token'])
    assert list_result1[0] != invalid_channel_id


#test for an invalid token
def test_channel_join_invalid_token():
    test_user1 = auth.auth_register('Breeeak@hotmail.com', 'password', 'Trail','Breaker')
    user_channel_creater = auth.auth_register('createrprivate@bigpond.com', 'password', 'Ultra', 'Magnus')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id1', False)
    with pytest.raises(AccessError) as e:
        channel.channel_join(test_user1['token'],test_channel_private)
    pass





