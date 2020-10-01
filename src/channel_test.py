import channel
import pytest
import auth
import channels
import other
from error import InputError
from error import AccessError

#Check if invited member is in through channel details
def check_if_member_exists(channel_details, user):
    mem = None
    for member in channel_details["all_members"]:
        if member["u_id"] == user["u_id"]:
            mem = member            
    assert(mem is not None)
    

#Channel_invite tests
#Successful
def test_channel_invite_valid_token():   
    VALID_token = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("bestest_group123@gmail.com", "awesome", "best", "group")
    new_channel = channels.channels_create(VALID_token["token"], "temp_channel", False) 
    channel.channel_invite(VALID_token["token"], new_channel['channel_id'], user2["u_id"])    
    channel_details = channel.channel_details(VALID_token["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, user2)

    other.clear()

def test_channel_invite_valid_channel_id():
    user1 = auth.auth_register("polarbae23@gmail.com", "grrr123", "polar", "bae")
    user2 = auth.auth_register("wsadwert@yahoo.com", "egegeg", "wsad", "wert")
    VALID_channel_id = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], VALID_channel_id['channel_id'], user2["u_id"])
    channel_details = channel.channel_details(user1["token"], VALID_channel_id['channel_id'])
    check_if_member_exists(channel_details, user2)

    other.clear()

def test_channel_invite_valid_u_id():
    user1 = auth.auth_register("iheartunsw@unsw.edu.au", "unsw123", "love", "UNSW")
    VALID_u_id = auth.auth_register("iheartusyd@usyd.edu.au", "sydney", "love", "usyd")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], new_channel['channel_id'], VALID_u_id["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, VALID_u_id)  

    other.clear()  
    
def test_private_channel_invite():   
    user1 = auth.auth_register("dog@gmail.com", "awesome", "dog", "puppy")
    user2 = auth.auth_register("cat@gmail.com", "awesome", "cat", "kitty")
    user3 = auth.auth_register("eddyisgay@gmail.com","eddygay","eddy","gay")
    new_private_channel = channels.channels_create(user1["token"], "cool_kids_only", True) 
    channel.channel_invite(user1["token"], new_private_channel['channel_id'], user2["u_id"])   
    channel.channel_invite(user1["token"], new_private_channel['channel_id'], user3["u_id"])    
    channel_details = channel.channel_details(user1["token"], new_private_channel['channel_id'])    
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)

    other.clear()

def test_channel_invite_many_members():
    user1 = auth.auth_register("simonpepe@gmail.com", "1234567", "simon", "pepe")
    user2 = auth.auth_register("ezmoney@gmail.com", "1234567", "ez", "money")
    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy","gay")
    user4 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin","Huang")
    user5 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user6 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user7 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot","Rotenstein")
    user8 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
        
    new_channel = channels.channels_create(user1["token"], "rave_club", False) 
    channel.channel_invite(user1["token"], new_channel['channel_id'], user2["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user3["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user4["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user5["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user6["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user7["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user8["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)
    check_if_member_exists(channel_details, user4)
    check_if_member_exists(channel_details, user5)
    check_if_member_exists(channel_details, user6)
    check_if_member_exists(channel_details, user7)
    check_if_member_exists(channel_details, user8)

    other.clear()
    
def test_different_authorised_users_inviting():  
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user5 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
        
    new_channel = channels.channels_create(user1["token"], "comp1531", False) 
    channel.channel_invite(user1["token"], new_channel['channel_id'], user2["u_id"])
    channel.channel_invite(user2["token"], new_channel['channel_id'], user3["u_id"])
    channel.channel_invite(user3["token"], new_channel['channel_id'], user4["u_id"])
    channel.channel_invite(user4["token"], new_channel['channel_id'], user5["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, user1)
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)
    check_if_member_exists(channel_details, user4)
    check_if_member_exists(channel_details, user5)

    other.clear()
    
def test_channel_invite_self_invite():
    user1 = auth.auth_register("ezmoney@gmail.com", "1234567", "ez", "money")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    #expected to do nothing
    channel.channel_invite(user1["token"], new_channel['channel_id'], user1["u_id"]) 
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, user1)  

    other.clear()
    
def test_channel_invite_existing_member():
    user1 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], new_channel['channel_id'], user2["u_id"]) 
    #expected to do nothing
    channel.channel_invite(user2["token"], new_channel['channel_id'], user1["u_id"]) 
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, user1)  
    check_if_member_exists(channel_details, user2) 

    other.clear()
    
#UNSUCCESSFUL    
def test_channel_invite_invalid_token():
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user2 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_public_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite("invalid_token", new_public_channel['channel_id'], user2["u_id"])
        
    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy", "gay")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    new_private_channel = channels.channels_create(user3["token"], "temp_channel", True) 
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite("another_invalid_token", new_private_channel['channel_id'], user4["u_id"])

    other.clear()

def test_channel_invite_invalid_channel_id():
    user1 = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    invalid_channel_id = 123456789 
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(user1["token"], invalid_channel_id, user2["u_id"])
    
    other.clear()
    
def test_channel_invite_invalid_u_id():
    user1 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user2 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    invalid_u_id = -123456789
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(user1["token"], new_channel['channel_id'], invalid_u_id)

    other.clear()

def test_channel_invite_unauthorised_user():
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite(user2["token"], new_channel['channel_id'], user3["u_id"])
    
    other.clear()
        
#*******************************************************************************    
# Channel_details_tests
# Successful
def test_channel_details_valid_token():
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    member = [{
        'u_id': 1,
        'name_first': 'Kevin',
        'name_last': 'Huang',
    }]
    assert channel_details["name"] == "temp_channel"
    assert channel_details["owner_members"] == member
    assert channel_details["all_members"] == member

    other.clear()

def test_channel_details_valid_channel_id():
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin","Huang")
    VALID_channel_id = channels.channels_create(user1["token"], "temp_channel", False)
    channel_details = channel.channel_details(user1["token"], VALID_channel_id['channel_id'])
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

    other.clear()

def test_channel_details_multiple_members():
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user5 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    channel.channel_invite(user1["token"], new_channel['channel_id'], user2["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user3["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user4["u_id"])
    channel.channel_invite(user1["token"], new_channel['channel_id'], user5["u_id"])
               
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    owner_members = [
        {
            'u_id': 1,
            'name_first': 'Kevin',
            'name_last': 'Huang',
        }
    ] 
    all_members = [
        {
            'u_id': 1,
            'name_first': 'Kevin',
            'name_last': 'Huang',
        },
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

    other.clear()
    
# Unsuccessful
def test_channel_details_invalid_token():
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
	    assert channel.channel_details("Invalid Token", new_channel['channel_id'])
    
    other.clear()

def test_channel_details_invalid_channel_id():
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")    
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    invalid_channel_id = 123456789
    with pytest.raises(InputError) as e:
        assert channel.channel_details(user1["token"], invalid_channel_id)
    
    other.clear()
    
def test_channel_details_unauthorised_user():
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")    
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
	    assert channel.channel_details(user2["token"], new_channel['channel_id'])
    other.clear()

#**************************************************************************************
#Checks a token with authority can join a channel
def test_channel_join_valid():
    user_channel_creater = auth.auth_register('creator@bigpond.com', 'password', 'Quick', 'Shadow')
    test_user1 = auth.auth_register('optumis4ime@hotmail.com', 'password', 'Optimus', 'Prime')
    test_user2 = auth.auth_register('thebumble@hotmail.com', 'password', 'Bumble', 'Bee')
    test_user3 = auth.auth_register('cliffbooth@hotmail.com', 'password', 'Cliff', 'Jumper')
    test_channel_id1 = channels.channels_create(user_channel_creater["token"] ,'test_channel_id1', True)
    
    #Checks a user can join a public channel Valid
    channel.channel_join(test_user1['token'],test_channel_id1['channel_id'])
    channel.channel_join(test_user2['token'],test_channel_id1['channel_id'])
    channel.channel_join(test_user3['token'],test_channel_id1['channel_id'])
    list_result1 = channels.channels_list(test_user1['token'])
    list_result2 = channels.channels_list(test_user2['token'])
    list_result3 = channels.channels_list(test_user3['token'])
    assert list_result1[0]['channel_id'] == test_channel_id1['channel_id']
    assert list_result2[0]['channel_id'] == test_channel_id1['channel_id']
    assert list_result3[0]['channel_id'] == test_channel_id1['channel_id']
    test_public_channel_details = channel.channel_details(test_user1['token'],test_channel_id1['channel_id'])
    
    member1 = None
    for member in test_public_channel_details['all_members']:
        if member["u_id"] == test_user1["u_id"]:
            member1 = member            
    assert(member1 is not None)
    member2 = None
    for member in test_public_channel_details['all_members']:
        if member["u_id"] == test_user2["u_id"]:
            member2 = member            
    assert(member2 is not None)
    member3 = None
    for member in test_public_channel_details['all_members']:
        if member["u_id"] == test_user3["u_id"]:
            member3 = member            
    assert(member3 is not None)

    other.clear()

#test for an invalid channel id
def test_channel_join_invalid_channel():
    invalid_channel_id = 'invalid_id'
    test_user1 = auth.auth_register('testHotRod@hotmail.com', 'password', 'Hot','Rod')
    with pytest.raises(AccessError) as e:
        assert channel.channel_join(test_user1["token"],invalid_channel_id)
    list_result1 = channels.channels_list(test_user1['token'])
    assert len(list_result1) == 0

    other.clear()


#test for an invalid token
#assumes that the token is from an actual player 
def test_channel_join_invalid_token():
    test_user1 = auth.auth_register('Breeeak@hotmail.com', 'password', 'Trail','Breaker')
    user_channel_creater = auth.auth_register('createrprivate@bigpond.com', 'password', 'Ultra', 'Magnus')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id1', False)
    with pytest.raises(AccessError) as e:
        assert channel.channel_join(test_user1['token'],test_channel_private)

    other.clear()

#tests that an error will appear if the user is already in the channel
def test_channel_join_invalid_user():
    test_user1 = auth.auth_register('firefly@hotmail.com', 'password', 'Fire','Flight')
    user_channel_creater = auth.auth_register('streetsmart@bigpond.com', 'password', 'Street', 'Wise')
    test_channel_id = channels.channels_create(user_channel_creater["token"] ,'test_channel_id1', True)
    channel.channel_join(test_user1['token'],test_channel_id['channel_id'])
    with pytest.raises(InputError) as e:
        assert channel.channel_join(test_user1['token'],test_channel_id["channel_id"])

    other.clear()
#******************************************************************************* 

#Channel_messages tests
#Test for valid channel_id
def test_channel_messages_valid_channel():
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    user2 = auth.auth_register("monstersinc@gmail.com", "boo123", "James", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "test channel", True)
    messages = channel.channel_messages(user1["token"], new_channel["channel_id"], 0)
    assert len(messages["messages"]) == 0

    other.clear()
 
#Test for invalid channel_id 
def test_channel_messages_invalid_channel():
    user1 = auth.auth_register("monstersinc@gmail.com", "boo123", "Mike", "Wazowski")
    new_channel = channels.channels_create(user1["token"], "test channel", True)

    invalid_channel_id = 1234
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(user1["token"], invalid_channel_id, 0)

    other.clear()
        
#Test for invalid start parameter (i.e. start > total number of messages in the channel)    
def test_channel_messages_invalid_start():
    user1 = auth.auth_register("monstersinc@gmail.com", "boo123", "James", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "test channel", True)

    with pytest.raises(InputError) as e:
        assert channel.channel_messages(user1["token"], new_channel["channel_id"], 50)
        assert channel.channel_messages(user1["token"], new_channel["channel_id"], -1)

    other.clear()

#Test for when user is not a member of the channel        
def test_channel_messages_not_member():
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    user2 = auth.auth_register("monstersinc@gmail.com", "boo123", "James", "Sullivan")
    new_channel = channels.channels_create(user1["token"], "test channel", False)

    channel.channel_messages(user1["token"], new_channel["channel_id"], 0) 
    with pytest.raises(AccessError) as e:
        assert channel.channel_messages(user2["token"], new_channel["channel_id"], 0)
    
    other.clear()

#Test for invalid token
def test_channel_messages_invalid_token():
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj12", "Lucy", "Jang")
    user2 = auth.auth_register("validuser@gmail.com", "volcano123", "Mike", "Wazowski")
    new_channel = channels.channels_create(user1["token"], "test channel", False)

    with pytest.raises(AccessError) as e:
        channel.channel_messages(user2["token"], new_channel["channel_id"], 0)
    
    other.clear()
    
#Channel_leave tests
#Test for valid channel id
def test_channel_leave_valid():
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    user2 = auth.auth_register("validuser@gmail.com", "volcanologist23", "Kevin", "Huang")
    new_channel = channels.channels_create(user1["token"], "test channel", True)

    assert channel.channel_leave(user1["token"], new_channel['channel_id']) == {}
    
    other.clear()
	
	
#Test for invalid channel id	
def test_channel_leave_invalid():
    invalid_channel_id = ''
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj123", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "test channel", True)
    with pytest.raises(InputError) as e:
        channel.channel_leave(user1["token"],invalid_channel_id)
        list_result = channels.channels_list(user1["token"]) 
        assert len(list_result) != invalid_channel_id

    other.clear() 
        
#Test for when trying to leave non existing channel   
def test_channel_leave_not_existing():
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj12", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "test channel", True)
    channel.channel_leave(user1["token"], new_channel['channel_id'])
    with pytest.raises(AccessError):
        channel.channel_leave(user1["token"], new_channel['channel_id'])

    other.clear()
    
#Test for invalid token    
def test_channel_leave_invalid_token():
    user1 = auth.auth_register("lucyjang@gmail.com", "lucyj12", "Lucy", "Jang")
    user2 = auth.auth_register("validuser@gmail.com", "vulture123", "Mike", "Wazowski")
    new_channel = channels.channels_create(user1["token"], "test channel", True)

    with pytest.raises(AccessError) as e:
        channel.channel_leave(user2["token"], new_channel['channel_id'])

    other.clear()

#******************************************************************************* 
#tests the function works when the conditions are valid
def test_channel_addowner_valid():
    creator = auth.auth_register('bechcomber@bigpond.com', 'password', 'Beach', 'Comber')
    test_user1 = auth.auth_register('streaksahead@hotmail.com', 'password', 'Blue','Streak')
    test_user2 = auth.auth_register('alert@hotmail.com', 'password', 'Red','Alert')
    test_user3 = auth.auth_register('screener@hotmail.com', 'password', 'Smoke','Screen')
    priv_channel = channels.channels_create(creator['token'] ,'test_channel_id1', False)
    channel_id = priv_channel['channel_id']
    channel.channel_invite(creator['token'],channel_id,test_user1['u_id'])
    channel.channel_invite(creator['token'],channel_id,test_user2['u_id'])
    channel.channel_invite(creator['token'],channel_id,test_user3['u_id'])
    channel.channel_addowner(creator['token'],channel_id,test_user1['u_id'])
    channel.channel_addowner(creator['token'],channel_id,test_user2['u_id'])
    channel.channel_addowner(creator['token'],channel_id,test_user3['u_id'])
    # Asserts would fail if channel_addowner didn't work
    assert channel.channel_removeowner(creator['token'], channel_id, test_user1['u_id']) == {}
    assert channel.channel_removeowner(creator['token'], channel_id, test_user2['u_id']) == {}
    assert channel.channel_removeowner(creator['token'], channel_id, test_user3['u_id']) == {}
    other.clear()
    

#Tests that an input error occurs when the member is already an owner
def channel_addowner_invalid_owner():
    user_channel_creater = auth.auth_register('backout@bigpond.com', 'password', 'Out', 'Back')
    test_user = auth.auth_register('poweerglider87@hotmail.com', 'password', 'Power','Glide')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    other.clear()

#Tests the user becoming an owner must be in the channel
def channel_addowner_invalid_channel():
    user_channel_creater = auth.auth_register('omegasup@bigpond.com', 'password', 'Omega', 'Supreme')
    test_user = auth.auth_register('gater@hotmail.com', 'password', 'Tail','Gate')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    other.clear()


#Tests the token adding the owner must be in the channel
def channel_addowner_invalid_owner_not_in_channel():
    user_channel_creater = auth.auth_register('starport@bigpond.com', 'password', 'Broad', 'Side')
    invalid_channel_creater = auth.auth_register('aircat@bigpond.com', 'password', 'Sky', 'Lynx')
    test_user = auth.auth_register('stormboy@hotmail.com', 'password', 'Sand','Storm')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])
    other.clear()

#Tests the token adding the owner must be an owner
def channel_addowner_invalid_owner_not_owner():
    user_channel_creater = auth.auth_register('arraid@bigpond.com', 'password', 'Air', 'Raid')
    invalid_channel_creater = auth.auth_register('bart@bigpond.com', 'password', 'Slimg', 'Shot')
    test_user = auth.auth_register('airdiver@hotmail.com', 'password', 'Sky','Dive')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    channel.channel_invite(user_channel_creater['token'],test_channel_private,invalid_channel_creater['u_id'])
    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(invalid_channel_creater['token'],test_channel_private,test_user['u_id'])
    other.clear()
    
#******************************************************************************* 
#Tests the function works when the conditions are valid
def test_channel_removeowner_valid():
    # same as test_channel_addowner_valid because they're testing different functions
    creator = auth.auth_register('bechcomber@bigpond.com', 'password', 'Beach', 'Comber')
    test_user1 = auth.auth_register('streaksahead@hotmail.com', 'password', 'Blue','Streak')
    test_user2 = auth.auth_register('alert@hotmail.com', 'password', 'Red','Alert')
    test_user3 = auth.auth_register('screener@hotmail.com', 'password', 'Smoke','Screen')
    priv_channel = channels.channels_create(creator['token'] ,'test_channel_id1', False)
    channel_id = priv_channel['channel_id']
    channel.channel_invite(creator['token'],channel_id,test_user1['u_id'])
    channel.channel_invite(creator['token'],channel_id,test_user2['u_id'])
    channel.channel_invite(creator['token'],channel_id,test_user3['u_id'])
    channel.channel_addowner(creator['token'],channel_id,test_user1['u_id'])
    channel.channel_addowner(creator['token'],channel_id,test_user2['u_id'])
    channel.channel_addowner(creator['token'],channel_id,test_user3['u_id'])
    assert channel.channel_removeowner(creator['token'], channel_id, test_user1['u_id']) == {}
    assert channel.channel_removeowner(creator['token'], channel_id, test_user2['u_id']) == {}
    assert channel.channel_removeowner(creator['token'], channel_id, test_user3['u_id']) == {}
    other.clear()
#Test removing an owner that is just a member
def channel_removeowner_invalid_owner():
    user_channel_creater = auth.auth_register('backout@bigpond.com', 'password', 'Out', 'Back')
    test_user = auth.auth_register('poweerglider87@hotmail.com', 'password', 'Power','Glide')
    test_channel_private = channels.channels_create(user_channel_creater['token'] , 'test_channel_id', False)
    channel.channel_invite(user_channel_creater['token'], test_channel_private, test_user['u_id'])
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    other.clear()

#Below this needs to be changed
#Tests the user being removed from the being an owner must be in the channel
def channel_removeowner_invalid_channel():
    user_channel_creater = auth.auth_register('omegasup@bigpond.com', 'password', 'Omega', 'Supreme')
    test_user = auth.auth_register('gater@hotmail.com', 'password', 'Tail','Gate')
    test_channel_private = channels.channels_create(user_channel_creater['token'] ,'test_channel_id', False)
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(user_channel_creater['token'],test_channel_private,test_user['u_id'])
    other.clear()

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
    other.clear()

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
    other.clear()


