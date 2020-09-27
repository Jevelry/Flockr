import channel
import pytest
import auth
import channels
from error import InputError
from error import AccessError

def test_channel_invite_valid_token():
    user1 = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("bestest_group123@gmail.com", "awesome", "best", "group")
    channel_id = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], channel_id, user2["u_id"])
    
    check_members = channel.channel_details(user1["token"], channel_id)l
    
    mem = None
    for member in check_members.all_members:
        if member["u_id"] == user2["u_id"]:
            mem = member            
    assert(mem is not None)
    
    #clear
    
    
def test_channel_invite_invalid_token():
    user1 = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("bestest_group123@gmail.com", "awesome", "best", "group")
    channel_id = channels.channels_create(user1["token"], "temp_channel", False) 
    with pytest.raises(AccessError) as e:
        channel.channel_invite("invalid_token", channel_id, user2["u_id"])
        
    #clear
def test_channel_invite_valid_channel_id():




def test_channel_invite_invalid_channel_id():



def test_channel_invite_valid_u_id():



def test_channel_invite_invalid_u_id():



def test_channel_invite_self_invite():


def test_channel_invite_member_already_added():




   """
   1 valid token
   2 invalid token
   3 valid channel id
   4 invalid channel id
   5 valid u_id
   6 invalid u_id
   invite person whos already in channel  #invalid
   invites yourself #invalid
    

    
   """

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
#assumes that the token is from an actual player 
def test_channel_join_invalid_token():
    test_user1 = auth.auth_register('Breeeak@hotmail.com', 'password', 'Trail','Breaker')
    user_channel_creater = auth.auth_register('createrprivate@bigpond.com', 'password', 'Ultra', 'Magnus')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id1', False)
    with pytest.raises(AccessError) as e:
        channel.channel_join(test_user1['token'],test_channel_private)

#tests that an error will appear if the user is already in the channel
def test_channel_join_invalid_user():
    test_user1 = auth.auth_register('firefly@hotmail.com', 'password', 'Fire','Flight')
    user_channel_creater = auth.auth_register('streetsmart@bigpond.com', 'password', 'Street', 'Wise')
    test_channel_id = channels.channels_create(user_channel_creater["token"] ,'test_channel_id1', True)
    channel.channel_join(test_user1['token'],test_channel_id)
    with pytest.raises(InputError) as e:
        channel.channel_join(test_user1['token'],test_channel_id)

#tests the function works when the conditions are valid
def test_channel_addowner_valid():
    user_channel_creater = auth.auth_register('bechcomber@bigpond.com', 'password', 'Beach', 'Comber')
    test_user1 = auth.auth_register('streaksahead@hotmail.com', 'password', 'Blue','Streak')
    test_user2 = auth.auth_register('alert@hotmail.com', 'password', 'Red','Alert')
    test_user3 = auth.auth_register('screener@hotmail.com', 'password', 'Smoke','Screen')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id1', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user1['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user2['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user3['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user1['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user2['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user3['u_id'])
    member1 = None
    for member in check_members.owner_members:
        if member["u_id"] == test_user1["u_id"]:
            member1 = member            
    assert(member1 is not None)
    member2 = None
    for member in check_members.owner_members:
        if member["u_id"] == test_user2["u_id"]:
            member2 = member            
    assert(member2 is not None)
    member3 = None
    for member in check_members.owner_members:
        if member["u_id"] == test_user3["u_id"]:
            member3 = member            
    assert(member3 is not None)

#Tests that an input error occurs when the member is already an owner
def channel_addowner_invalid_owner():
    user_channel_creater = auth.auth_register('backout@bigpond.com', 'password', 'Out', 'Back')
    test_user = auth.auth_register('poweerglider87@hotmail.com', 'password', 'Power','Glide')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(InputError) as e:
        channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])

#Tests the user becoming an owner must be in the channel
def channel_addowner_invalid_channel():
    user_channel_creater = auth.auth_register('omegasup@bigpond.com', 'password', 'Omega', 'Supreme')
    test_user = auth.auth_register('gater@hotmail.com', 'password', 'Tail','Gate')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    with pytest.raises(InputError) as e:
        channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])


#Tests the token adding the owner must be in the channel
def channel_addowner_invalid_owner_not_in_channel():
    user_channel_creater = auth.auth_register('starport@bigpond.com', 'password', 'Broad', 'Side')
    invalid_channel_creater = auth.auth_register('aircat@bigpond.com', 'password', 'Sky', 'Lynx')
    test_user = auth.auth_register('stormboy@hotmail.com', 'password', 'Sand','Storm')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])

#Tests the token adding the owner must be an owner
def channel_addowner_invalid_owner_not_owner():
    user_channel_creater = auth.auth_register('arraid@bigpond.com', 'password', 'Air', 'Raid')
    invalid_channel_creater = auth.auth_register('bart@bigpond.com', 'password', 'Slimg', 'Shot')
    test_user = auth.auth_register('airdiver@hotmail.com', 'password', 'Sky','Dive')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,invalid_channel_creater['u_id'])
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])

#Tests the function works when the conditions are valid
def test_channel_removeowner_valid():
    user_channel_creater = auth.auth_register('bechcomber@bigpond.com', 'password', 'Beach', 'Comber')
    test_user1 = auth.auth_register('streaksahead@hotmail.com', 'password', 'Blue','Streak')
    test_user2 = auth.auth_register('alert@hotmail.com', 'password', 'Red','Alert')
    test_user3 = auth.auth_register('screener@hotmail.com', 'password', 'Smoke','Screen')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id1', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user1['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user2['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user3['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user1['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user2['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user3['u_id'])
    channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user1['u_id'])
    channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user2['u_id'])
    channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user3['u_id'])
    member1 = None
    for member in check_members.owner_members:
        if member["u_id"] == test_user1["u_id"]:
            member1 = member            
    assert(member1 is None)
    member2 = None
    for member in check_members.owner_members:
        if member["u_id"] == test_user2["u_id"]:
            member2 = member            
    assert(member2 is None)
    member3 = None
    for member in check_members.owner_members:
        if member["u_id"] == test_user3["u_id"]:
            member3 = member            
    assert(member3 is None)

#Test removing an owner that is just a member
def channel_removeowner_invalid_owner():
    user_channel_creater = auth.auth_register('backout@bigpond.com', 'password', 'Out', 'Back')
    test_user = auth.auth_register('poweerglider87@hotmail.com', 'password', 'Power','Glide')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(InputError) as e:
        channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])

#Below this needs to be changed
#Tests the user being removed from the being an owner must be in the channel
def channel_removeowner_invalid_channel():
    user_channel_creater = auth.auth_register('omegasup@bigpond.com', 'password', 'Omega', 'Supreme')
    test_user = auth.auth_register('gater@hotmail.com', 'password', 'Tail','Gate')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    with pytest.raises(InputError) as e:
        channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])

#Tests that the token being used to remove member an owner is from someone in the channel
def channel_removeowner_invalid_owner_not_in_channel():
    user_channel_creater = auth.auth_register('starport@bigpond.com', 'password', 'Broad', 'Side')
    invalid_channel_creater = auth.auth_register('aircat@bigpond.com', 'password', 'Sky', 'Lynx')
    test_user = auth.auth_register('stormboy@hotmail.com', 'password', 'Sand','Storm')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])

#Tests that the token being used to remove the member an owner is from someone in the channel and is a owner
def channel_removeowner_invalid_owner_not_owner():
    user_channel_creater = auth.auth_register('arraid@bigpond.com', 'password', 'Air', 'Raid')
    invalid_channel_creater = auth.auth_register('bart@bigpond.com', 'password', 'Slimg', 'Shot')
    test_user = auth.auth_register('airdiver@hotmail.com', 'password', 'Sky','Dive')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,invalid_channel_creater['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])



