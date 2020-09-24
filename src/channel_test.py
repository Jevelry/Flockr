import channel
import pytest
from error import InputError
from error import AccessError

def test_channel_invite_valid_token():
    user1 = auth_register("best_group123@gmail.com", "awesome", "best", "group")
    user2 = auth_register("bestest_group123@gmail.com", "awesome", "best", "group")
    channel_id = channels_create(user1["token"], "temp_channel", False) 
    channel_invite(user1["token"], channel_id, user2["u_id"])
    
    check_members = channel_details(user1["token"], channel_id)l
    
    mem = None
    for member in check_members.all_members:
        if member["u_id"] == user2["u_id"]:
            mem = member            
    assert(mem is not None)
    

def test_channel_invite_invalid_token():



def test_channel_invite_valid_channel_id():




def test_channel_invite_invalid_channel_id():



def test_channel_invite_valid_u_id():



def test_channel_invite_invalid_u_id():



    
    
    
    
   """
   1 valid token
   2 invalid token
   3 valid channel id
   4 invalid channel id
   5 valid u_id
   6 invalid u_id
   
    

    
   """
