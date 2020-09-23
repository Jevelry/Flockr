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
def test_channel_join():
    test_user1 = auth.auth_register('test1@hotmail.com', 'password', 'Optimus', 'Prime')
    test_user2 = auth.auth_register('test2@hotmail.com', 'password', 'Bumble', 'Bee')
    test_user3 = auth.auth_register('test3@hotmail.com', 'password', 'Cliff', 'Jumper')
    test_channel_id1 = channels.channels_create(test_user1["token"] ,'Test Channel Public', 1)
    
    #Checks a user can join a public channel
    channel.channel_join(test_user1["u_id"],test_channel_id1)
    channel.channel_join(test_user2["u_id"],test_channel_id1)
    channel.channel_join(test_user3["u_id"],test_channel_id1)
    list_result1 = channels.channels_list('test1@hotmail.com')
    list_result2 = channels.channels_list('test2@hotmail.com')
    list_result3 = channels.channels_list('test3@hotmail.com')
    assert list_result1[0]['name'] == 'Test Channel Public'
    assert list_result2[0]['name'] == 'Test Channel Public'
    assert list_result3[0]['name'] == 'Test Channel Public'

    test_channel_id2 = channels.channels_create(test_user2["token"] ,'Test Channel Private', 0)
    channel.channel_addowner(test_user2["token"],test_channel_id2,test_user2["u_id"])
    channel.channel_addowner(test_user3["token"],test_channel_id2,test_user3["u_id"])
    #test_user1 should raise an error since they don't have the authority AccessError
    channel.channel_join(test_user1["u_id"],test_channel_id1)
    channel.channel_join(test_user2["u_id"],test_channel_id1)
    channel.channel_join(test_user3["u_id"],test_channel_id1)
    #test_user1 should not have the test channel as a channel 
    assert list_result1[1]['name'] != 'Test Channel Private'
    assert list_result2[1]['name'] == 'Test Channel Private'
    assert list_result3[1]['name'] == 'Test Channel Private'
    #the Input Error should be raised by the users trying to join a channel not created
    channel.channel_join(test_user1["u_id"],test_channel_invalid)
    channel.channel_join(test_user2["u_id"],test_channel_invalid)








    
