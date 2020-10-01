import data
from error import AccessError
from error import InputError
import auth
import channels

# Used in channel_invite
# Check if token is valid and if user is authorised user
def valid_token(token, channel_id):
    u_id = None
    # Check valid token, take u_id
    for user in data.data["logged_in"]:
        if user["token"] == token:
            u_id = user["u_id"]
    if u_id = None:
        return False
    # Check if user is existing member of channel
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            for channel in user["channel_list"]:
                if channel["channel_id"] == channel_id
                return True
            return False
            

# Used in channel_invite
# Check if valid channel id
def valid_channel_id(channel_id):
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id
            return True
    return False



# Used in channel_invite
# Check if valid u_id of invitee
def valid_u_id(u_id):
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            return True
        return False
                
def is_existing_channel_member(u_id, channel_id):
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            for channel in user["channel_list"]:
                if channel == channel_id:
                    return True
    return False


def channel_invite(token, channel_id, u_id):
    # Check if given valid channel_id
    if not valid_channel_id(token, channel_id):
        raise InputError
    # Check if token is valid and user is authorised(member of channel)    
    if not valid_token(token, channel_id):
        raise AccessError
    # Check if given valid u_id    
    if not valid_u_id(u_id):
        raise InputError
    # Check if invitee is already part of channel    
    if is_existing_channel_member(u_id, channel_id)
        return{
        }
    
    # Everything valid, Proceed with adding to channel
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["members"].append(u_id)
            
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            user["channel_list"].append(channel_id

    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    """
    Given a Channel with ID channel_id that the authorised user is part of, 
    return up to 50 messages between index "start" and "start + 50". Message 
    with index 0 is the most recent message in the channel. This function 
    returns a new index "end" which is the value of "start + 50", or, if this 
    function has returned the least recent messages in the channel, returns -1 
    in "end" to indicate there are no more messages to load after this return. 
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel
        start(int): index of starting message
        
    Returns:
        (dict): {messages, start, end}
    """
    #Check if given valid channel_id
    if not valid_channel_id(channel_id):
        raise InputError
        
    # Check if token is valid and user is authorised(member of channel)    
    if not valid_token(token, channel_id):
        raise AccessError
        
    # Proceed to getting messages
    channel_messages = {
        "messages" : [],
        "start" : start,
        "end": ""
    }    
    
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
			if len(channel["messages"] < start):
				raise InputError
            for message_id in channel["messages"][start:start + 50]:
                message = {}
                message["message_id"] = start
                message["u_id"] = message_id["u_id"]
                message["message"] = message_id["message"]
                message["time_created"] = message_id["date"]
                channel_messages["messages"].append(message)
			if len(channel["messages"]) < start + 50:
				channel_messages["end"] = -1
    return channel_messages
    
		"""
  
    {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }
"""

def channel_leave(token, channel_id):
    # Check if given valid channel_id
    if not valid_channel_id(channel_id):
        raise InputError
    # Check if token is valid and user is authorised(member of channel)        
    if not valid_token(token, channel_id):
        raise AccessError
    # Everything valid, Proceed with leaving channel
    # Find user and take u_id
    for user in data.data["logged_in"]:
        if user["token"] == token:
            u_id = user["u_id"]
            
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["owners"].remove(u_id)
            channel["members"].remove(u_id)
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            user["channel_list"].remove(channel_id)
                   
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }
