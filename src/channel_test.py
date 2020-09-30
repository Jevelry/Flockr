import channel
import pytest
import auth
import channels
import data
from error import InputError
from error import AccessError

#Check if invited member is in through channel details
def check_if_member_exists(channel_details, user):
    mem = None
    for member in channel_details.all_members:
        if member["u_id"] == user["u_id"]:
            mem = member            
    assert(mem is not None)
    

#Channel_invite tests
#Successful
def test_channel_invite_valid_token():
    data.clear_data()
    VALID_token = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("bestest_group123@gmail.com", "awesome", "best", "group")
    new_channel = channels.channels_create(VALID_token["token"], "temp_channel", False) 
    channel.channel_invite(VALID_token["token"], new_channel, user2["u_id"])    
    channel_details = channel.channel_details(VALID_token["token"], new_channel)
    check_if_member_exists(channel_details, user2)
        
    
def test_channel_invite_valid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("polarbae23@gmail.com", "grrr123", "polar", "bae")
    user2 = auth.auth_register("wsadwert@yahoo.com", "egegeg", "wsad", "wert")
    VALID_channel_id = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], VALID_channel_id, user2["u_id"])
    channel_details = channel.channel_details(user1["token"], VALID_channel_id)
    check_if_member_exists(channel_details, user2)

    
    
def test_channel_invite_valid_u_id():
    data.clear_data()
    user1 = auth.auth_register("iheartunsw@unsw.edu.au", "unsw123", "love", "UNSW")
    valid_u_id = auth.auth_register("iheartusyd@usyd.edu.au", "sydney", "love", "usyd")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], new_channel, valid_u_id["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel)
    check_if_member_exists(channel_details, valid_u_id)    
    
    data.clear_data()
"""    
above three tests are almost identical... is this ok?    
"""    
    
    
def test_private_channel_invite():   
    data.clear_data()
    user1 = auth.auth_register("dog@gmail.com", "awesome", "dog", "puppy")
    user2 = auth.auth_register("cat@gmail.com", "awesome", "cat", "kitty")
    user3 = auth.auth_register("eddyisgay@gmail.com","eddygay","eddy","gay")
    new_private_channel = channels.channels_create(user1["token"], "cool_kids_only", True) 
    channel.channel_invite(user1["token"], new_private_channel, user2["u_id"])   
    channel.channel_invite(user1["token"], new_private_channel, user3["u_id"])    
    channel_details = channel.channel_details(user1["token"], new_private_channel)    
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)
    
    data.clear_data()

def test_channel_invite_many_members():
    data.clear_data()
    user1 = auth.auth_register("simonpepe@gmail.com", "1234567", "simon", "pepe")
    user2 = auth.auth_register("ezmoney@gmail.com", "1234567", "ez", "money")
    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy","gay")
    user4 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin","Huang")
    user5 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user6 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user7 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot","Rotenstein")
    user8 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
        
    new_channel = channels.channels_create(user1["token"], "rave_club", False) 
    channel.channel_invite(user1["token"], new_channel, user2["u_id"])
    channel.channel_invite(user1["token"], new_channel, user3["u_id"])
    channel.channel_invite(user1["token"], new_channel, user4["u_id"])
    channel.channel_invite(user1["token"], new_channel, user5["u_id"])
    channel.channel_invite(user1["token"], new_channel, user6["u_id"])
    channel.channel_invite(user1["token"], new_channel, user7["u_id"])
    channel.channel_invite(user1["token"], new_channel, user8["u_id"])
    channel.channel_invite(user1["token"], new_channel, user9["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel)
    
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)
    check_if_member_exists(channel_details, user4)
    check_if_member_exists(channel_details, user5)
    check_if_member_exists(channel_details, user6)
    check_if_member_exists(channel_details, user7)
    check_if_member_exists(channel_details, user8)
    
    data.clear_data()
    
def test_different_authorised_users_inviting():  
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user5 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "comp1531", False) 
    channel.channel_invite(user1["token"], new_channel, user2["u_id"])
    channel.channel_invite(user2["token"], new_channel, user3["u_id"])
    channel.channel_invite(user3["token"], new_channel, user4["u_id"])
    channel.channel_invite(user4["token"], new_channel, user5["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel)
    check_if_member_exists(channel_details, user1)
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)
    check_if_member_exists(channel_details, user4)
    check_if_member_exists(channel_details, user5)

    data.clear_data()
    
def test_channel_invite_self_invite():
    data.clear_data()
    user1 = auth.auth_register("ezmoney@gmail.com", "1234567", "ez", "money")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    #expected to do nothing
    channel.channel_invite(user1["token"], new_channel, user1["u_id"]) 
    channel_details = channel.channel_details(user1["token"], new_channel)
    check_if_member_exists(channel_details, user1)  
    
    data.clear_data()
    
def test_channel_invite_existing_member():
    data.clear_data()
    user1 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], new_channel, user2["u_id"]) 
    #expected to do nothing
    channel.channel_invite(user2["token"], new_channel, user1["u_id"]) 
    channel_details = channel.channel_details(user1["token"], new_channel)
    check_if_member_exists(channel_details, user1)  
    check_if_member_exists(channel_details, user2) 
    
    data.clear_data()
    
#UNSUCCESSFUL    
def test_channel_invite_invalid_token():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user2 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_public_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite("invalid_token", new_public_channel, user2["u_id"])
        
    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy", "gay")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    new_private_channel = channels.channels_create(user3["token"], "temp_channel", True) 
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite("another_invalid_token", new_private_channel, user4["u_id"])
    
    data.clear_data()

def test_channel_invite_invalid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    invalid_channel_id = 123456789 
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(user1["token"], invalid_channel_id, user2["u_id"])

    data.clear_data()
    
def test_channel_invite_invalid_u_id():
    data.clear_data()
    user1 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user2 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    invalid_u_id = -123456789
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(user1["token"], new_channel, invalid_u_id)
    
    data.clear_data()

def test_channel_invite_unauthorised_user():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite(user2["token"], new_channel, user3)

    data.clear_data()
#*******************************************************************************    
# Channel_details_tests
# Successful
def test_channel_details_valid_token():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel_details = channel.channel_details(user1["token"], new_channel)
    member = {
        'u_id': 1,
        'name_first': 'Kevin',
        'name_last': 'Huang',
    }
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == member
    assert channel_details["all_members"] == member
    
    data.clear_data()

def test_channel_details_valid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin","Huang")
    VALID_channel_id = channels.channels_create(user1["token"], "temp_channel", False)
    channel_details = channel.channel_details(user1["token"], VALID_channel_id)
    member = [
        {
            'u_id': 1,
            'name_first': 'Kevin',
            'name_last': 'Huang',
        }
    ]        
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == member
    assert channel_details["all_members"] == member
    
    data.clear_data()

def test_channel_details_multiple_members():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user5 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel.channel_invite(user1["token"], new_channel, user2)
    channel.channel_invite(user1["token"], new_channel, user3)
    channel.channel_invite(user1["token"], new_channel, user4)
    channel.channel_invite(user1["token"], new_channel, user5)
               
    channel_details = channel.channel_details(user1["token"], new_channel)
    owner_members = [
        {
            'u_id': 1,
            'name_first': 'Kevin',
            'name_last': 'Huang',
        }
    ] 
    all_members = [
        {
            'u_id': 2,
            'name_first': 'Lucy',
            'name_last': 'Jang',
		},
		{
            'u_id': 3,
            'name_first': 'Ricky',
            'name_last': 'Mai',
		},
        {
            'u_id': 4,
            'name_first': 'Elliot',
            'name_last': 'Rotenstein',
        },
        {
            'u_id': 5,
            'name_first': 'Hugo',
            'name_last': 'Sullivan',
        }        
    ] 
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == owner_members
    assert channel_details["all_members"] == all_members
    
    channel_details_2 = channel.channel_details(user2["token"], new_channel)
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == owner_members
    assert channel_details["all_members"] == all_members
    
    data.clear_data()

# Unsuccessful
def test_channel_details_invalid_token():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
	    assert channel_details == channel.channel_details("Invalid Token", new_channel)
	    
    data.clear_data()

def test_channel_details_invalid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")    
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    invalid_channel_id = 123456789
    with pytest.raises(InputError) as e:
        assert channel_details == channel.channel_details(user1["token"], invalid_channel_id)

    data.clear_data()
    
def test_channel_details_unauthorised_user():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")    
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
	    assert channel_details == channel.channel_details(user2["token"], new_channel)
    
    data.clear_data()
    

"""
   
    mem = None
    for member in check_members.all_members:
        if member["u_id"] == user2["u_id"]:
            mem = member            
    assert(mem is not None)

"""

#**************************************************************************************
#Checks a token with authority can join a channel
def test_channel_join_valid():
    data.clear_data()
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
    data.clear_data()

#test for an invalid channel id
def test_channel_join_invalid_channel():
    data.clear_data()
    test_user1 = auth.auth_register('testHotRod@hotmail.com', 'password', 'Hot','Rod')
    with pytest.raises(InputError) as e:
        channel.channel_join(test_user1["token"],invalid_channel_id)
    list_result1 = channels.channels_list(test_user1['token'])
    assert list_result1[0] != invalid_channel_id
    data.clear_data()


#test for an invalid token
#assumes that the token is from an actual player 
def test_channel_join_invalid_token():
    test_user1 = auth.auth_register('Breeeak@hotmail.com', 'password', 'Trail','Breaker')
    user_channel_creater = auth.auth_register('createrprivate@bigpond.com', 'password', 'Ultra', 'Magnus')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id1', False)
    with pytest.raises(AccessError) as e:
        assert channel.channel_join(test_user1['token'],test_channel_private)
    data.clear_data()

#tests that an error will appear if the user is already in the channel
def test_channel_join_invalid_user():
    data.clear_data()
    test_user1 = auth.auth_register('firefly@hotmail.com', 'password', 'Fire','Flight')
    user_channel_creater = auth.auth_register('streetsmart@bigpond.com', 'password', 'Street', 'Wise')
    test_channel_id = channels.channels_create(user_channel_creater["token"] ,'test_channel_id1', True)
    channel.channel_join(test_user1['token'],test_channel_id)
    with pytest.raises(InputError) as e:
        assert channel.channel_join(test_user1['token'],test_channel_id)
    data.clear_data()
    
#******************************************************************************* 
#tests the function works when the conditions are valid
def test_channel_addowner_valid():
    data.clear_data()
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
    data.clear_data()

#Tests that an input error occurs when the member is already an owner
def channel_addowner_invalid_owner():
    data.clear_data()
    user_channel_creater = auth.auth_register('backout@bigpond.com', 'password', 'Out', 'Back')
    test_user = auth.auth_register('poweerglider87@hotmail.com', 'password', 'Power','Glide')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()

#Tests the user becoming an owner must be in the channel
def channel_addowner_invalid_channel():
    data.clear_data()
    user_channel_creater = auth.auth_register('omegasup@bigpond.com', 'password', 'Omega', 'Supreme')
    test_user = auth.auth_register('gater@hotmail.com', 'password', 'Tail','Gate')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()


#Tests the token adding the owner must be in the channel
def channel_addowner_invalid_owner_not_in_channel():
    data.clear_data()
    user_channel_creater = auth.auth_register('starport@bigpond.com', 'password', 'Broad', 'Side')
    invalid_channel_creater = auth.auth_register('aircat@bigpond.com', 'password', 'Sky', 'Lynx')
    test_user = auth.auth_register('stormboy@hotmail.com', 'password', 'Sand','Storm')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()

#Tests the token adding the owner must be an owner
def channel_addowner_invalid_owner_not_owner():
    data.clear_data()
    user_channel_creater = auth.auth_register('arraid@bigpond.com', 'password', 'Air', 'Raid')
    invalid_channel_creater = auth.auth_register('bart@bigpond.com', 'password', 'Slimg', 'Shot')
    test_user = auth.auth_register('airdiver@hotmail.com', 'password', 'Sky','Dive')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,invalid_channel_creater['u_id'])
    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()
    
#******************************************************************************* 
#Tests the function works when the conditions are valid
def test_channel_removeowner_valid():
    data.clear_data()
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
    data.clear_data()

#Test removing an owner that is just a member
def channel_removeowner_invalid_owner():
    data.clear_data()
    user_channel_creater = auth.auth_register('backout@bigpond.com', 'password', 'Out', 'Back')
    test_user = auth.auth_register('poweerglider87@hotmail.com', 'password', 'Power','Glide')
    test_channel_private = channels.channels_create(user_channel_creater['token'] , 'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'], test_channel_private, test_user['u_id'])
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()

#Below this needs to be changed
#Tests the user being removed from the being an owner must be in the channel
def channel_removeowner_invalid_channel():
    user_channel_creater = auth.auth_register('omegasup@bigpond.com', 'password', 'Omega', 'Supreme')
    test_user = auth.auth_register('gater@hotmail.com', 'password', 'Tail','Gate')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()

#Tests that the token being used to remove member an owner is from someone in the channel
def channel_removeowner_invalid_owner_not_in_channel():
    user_channel_creater = auth.auth_register('starport@bigpond.com', 'password', 'Broad', 'Side')
    invalid_channel_creater = auth.auth_register('aircat@bigpond.com', 'password', 'Sky', 'Lynx')
    test_user = auth.auth_register('stormboy@hotmail.com', 'password', 'Sand','Storm')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()

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
        assert channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])
    data.clear_data()



