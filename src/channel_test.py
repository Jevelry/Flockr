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
    for member in channel_details["all_members"]:
        if member["u_id"] == user["u_id"]:
            mem = member            
    assert(mem is not None)
    

#Channel_invite tests
#Successful
def test_channel_invite_valid_token():
    data.clear_data()      
    VALID_token = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    VALID_token = auth.auth_login("best_group123@gmail.com", "awesome")
    user2 = auth.auth_register("bestest_group123@gmail.com", "awesome", "best", "group")
    new_channel = channels.channels_create(VALID_token["token"], "temp_channel", False) 
    channel.channel_invite(VALID_token["token"], new_channel['channel_id'], user2["u_id"])    
    channel_details = channel.channel_details(VALID_token["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, user2)

def test_channel_invite_valid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("polarbae23@gmail.com", "grrr123", "polar", "bae")
    user1 = auth.auth_login("polarbae23@gmail.com", "grrr123")
    user2 = auth.auth_register("wsadwert@yahoo.com", "egegeg", "wsad", "wert")
    VALID_channel_id = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], VALID_channel_id['channel_id'], user2["u_id"])
    channel_details = channel.channel_details(user1["token"], VALID_channel_id['channel_id'])
    check_if_member_exists(channel_details, user2)

def test_channel_invite_valid_u_id():
    data.clear_data()
    user1 = auth.auth_register("iheartunsw@unsw.edu.au", "unsw123", "love", "UNSW")
    user1 = auth.auth_login("iheartunsw@unsw.edu.au", "unsw123")
    VALID_u_id = auth.auth_register("iheartusyd@usyd.edu.au", "sydney", "love", "usyd")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], new_channel['channel_id'], VALID_u_id["u_id"])
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, VALID_u_id)    
    
def test_private_channel_invite():   
    data.clear_data()
    user1 = auth.auth_register("dog@gmail.com", "awesome", "dog", "puppy")
    user1 = auth.auth_login("dog@gmail.com", "awesome")
    user2 = auth.auth_register("cat@gmail.com", "awesome", "cat", "kitty")
    user3 = auth.auth_register("eddyisgay@gmail.com","eddygay","eddy","gay")
    new_private_channel = channels.channels_create(user1["token"], "cool_kids_only", True) 
    channel.channel_invite(user1["token"], new_private_channel['channel_id'], user2["u_id"])   
    channel.channel_invite(user1["token"], new_private_channel['channel_id'], user3["u_id"])    
    channel_details = channel.channel_details(user1["token"], new_private_channel['channel_id'])    
    check_if_member_exists(channel_details, user2)
    check_if_member_exists(channel_details, user3)

def test_channel_invite_many_members():
    data.clear_data()
    user1 = auth.auth_register("simonpepe@gmail.com", "1234567", "simon", "pepe")
    user1 = auth.auth_login("simonpepe@gmail.com", "1234567")
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
    
def test_different_authorised_users_inviting():  
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice123", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user5 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    user1 = auth.auth_login("kevin.huang@gmail.com", "nice123")
    user2 = auth.auth_login("lucyjang@gmail.com", "lj1234")
    user3 = auth.auth_login("rickymai@gmail.com", "rm1234")
    user4 = auth.auth_login("elliotrotenstein@gmail.com", "er1234")
        
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
    
def test_channel_invite_self_invite():
    data.clear_data()
    user1 = auth.auth_register("ezmoney@gmail.com", "1234567", "ez", "money")
    user1 = auth.auth_login("ezmoney@gmail.com", "1234567")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    #expected to do nothing
    channel.channel_invite(user1["token"], new_channel['channel_id'], user1["u_id"]) 
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, user1)  
    
def test_channel_invite_existing_member():
    data.clear_data()
    user1 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user1 = auth.auth_login("rickymai@gmail.com", "rm1234")
    user2 = auth.auth_login("lucyjang@gmail.com", "lj1234")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    channel.channel_invite(user1["token"], new_channel['channel_id'], user2["u_id"]) 
    #expected to do nothing
    channel.channel_invite(user2["token"], new_channel['channel_id'], user1["u_id"]) 
    channel_details = channel.channel_details(user1["token"], new_channel['channel_id'])
    check_if_member_exists(channel_details, user1)  
    check_if_member_exists(channel_details, user2) 
    
#UNSUCCESSFUL    
def test_channel_invite_invalid_token():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user1 = auth.auth_login("kevin.huang@gmail.com", "nice1234")
    user2 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_public_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite("invalid_token", new_public_channel['channel_id'], user2["u_id"])
        
    user3 = auth.auth_register("eddyisgay@gmail.com", "eddygay", "eddy", "gay")
    user3 = auth.auth_login("eddyisgay@gmail.com", "eddygay")
    user4 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    new_private_channel = channels.channels_create(user3["token"], "temp_channel", True) 
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite("another_invalid_token", new_private_channel['channel_id'], user4["u_id"])

def test_channel_invite_invalid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user1 = auth.auth_login("best_group123@gmail.com", "awesome")
    user2 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False) 
    invalid_channel_id = 123456789 
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(user1["token"], invalid_channel_id, user2["u_id"])
    
def test_channel_invite_invalid_u_id():
    data.clear_data()
    user1 = auth.auth_register("elliotrotenstein@gmail.com", "er1234", "Elliot", "Rotenstein")
    user1 = auth.auth_login("elliotrotenstein@gmail.com", "er1234")
    user2 = auth.auth_register("hugosullivan@gmail.com", "hs1234", "Hugo", "Sullivan")
    invalid_u_id = -123456789
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(user1["token"], new_channel['channel_id'], invalid_u_id)

def test_channel_invite_unauthorised_user():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user3 = auth.auth_register("rickymai@gmail.com", "rm1234", "Ricky", "Mai")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite(user2["token"], new_channel['channel_id'], user3["u_id"])
        
#*******************************************************************************    
# Channel_details_tests
# Successful
def test_channel_details_valid_token():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin", "Huang")
    user1 = auth.auth_login("kevin.huang@gmail.com", "nice1234")
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

def test_channel_details_valid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "nice1234", "Kevin","Huang")
    user1 = auth.auth_login("kevin.huang@gmail.com", "nice1234")
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

def test_channel_details_multiple_members():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user1 = auth.auth_login("kevin.huang@gmail.com", "kh1234")
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
    
def test_channel_details_multiple_owners_and_members():
    pass
# Unsuccessful
def test_channel_details_invalid_token():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    user1 = auth.auth_login("kevin.huang@gmail.com", "kh1234")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
	    assert channel_details == channel.channel_details("Invalid Token", new_channel['channel_id'])

def test_channel_details_invalid_channel_id():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")    
    user1 = auth.auth_login("kevin.huang@gmail.com", "kh1234")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    invalid_channel_id = 123456789
    with pytest.raises(InputError) as e:
        assert channel_details == channel.channel_details(user1["token"], invalid_channel_id)
    
def test_channel_details_unauthorised_user():
    data.clear_data()
    user1 = auth.auth_register("kevin.huang@gmail.com", "kh1234", "Kevin", "Huang")    
    user2 = auth.auth_register("lucyjang@gmail.com", "lj1234", "Lucy", "Jang")
    new_channel = channels.channels_create(user1["token"], "temp_channel", False)
    with pytest.raises(AccessError) as e:
	    assert channel_details == channel.channel_details(user2["token"], new_channel['channel_id'])


