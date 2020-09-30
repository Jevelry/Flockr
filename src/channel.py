import data
from error import AccessError
from error import InputError
import auth
import channels


# Check if token is valid and if the user is authorised
def valid_token(token, channel_id):
    u_id = None
    # Check if valid token, take u_id
    for user in data.data["logged_in"]:
        if user["token"] == token:
            u_id = user["u_id"]
    if u_id == None:
        return False
    # Check if user is existing member of channel
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            for channel in user["channel_list"]:
                if channel == channel_id:
                    return True
    return False
            
# Check if valid channel id given
def valid_channel_id(channel_id):
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            return True
    return False

# Check if u_id of invitee is valid
def valid_u_id(u_id):
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            return True
    return False

# Check if invitee is already part of channel                 
def is_existing_channel_member(u_id, channel_id):
    # Find user
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            # Check user's channel list for channel_id
            for channel in user["channel_list"]:
                if channel == channel_id:
                    return True
    return False

def channel_invite(token, channel_id, u_id):
    """
    Invites a user (with user id u_id) to join a channel with ID channel_id. 
    Once invited the user is added to the  channel immediately
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel
        u_id(int): Identifier for user
    
    Returns:
        Nothing
    """
    # Check if given valid channel_id
    if not valid_channel_id(channel_id):
        raise InputError
    # Check if token is valid and user is authorised(member of channel)    
    if not valid_token(token, channel_id):
        raise AccessError
    # Check if given valid u_id    
    if not valid_u_id(u_id):
        raise InputError
    # Check if invitee is already part of channel. If so, do nothing    
    if is_existing_channel_member(u_id, channel_id):
        return {
        }    
    # Everything valid, Proceed with adding to channel
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["members"].append(u_id)
            
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            user["channel_list"].append(channel_id)
    return {
    }
            
def channel_details(token, channel_id):  
    """
    Given a Channel with ID channel_id that the authorised user is part of, 
    provide basic details about the channel
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel        
    
    Returns:
        (dict): { name, owner_members, all_members }
    """  
    # Check if given valid channel_id
    if not valid_channel_id(channel_id):
        raise InputError
    # Check if token is valid and user is authorised(member of channel)        
    if not valid_token(token, channel_id):
        raise AccessError
    # Everything valid, Proceed with getting details
    channel_details = {
        "name" : "",
        "owner_members" : [],
        "all_members" : []
    }

    # Find channel and copy infomation into channel_details    
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            channel_details["name"] = channel["name"]
            for u_id in channel["owners"]:  
                for user in data.data["users"]:
                    owner = {}
                    if user["u_id"] == u_id:
                        owner["u_id"] = u_id
                        owner["name_first"] = user["first"]
                        owner["name_last"] = user["last"]
                        channel_details["owner_members"].append(owner)
                        
            for u_id in channel["members"]:  
                for user in data.data["users"]:
                    member = {}
                    if user["u_id"] == u_id:
                        member["u_id"] = u_id
                        member["name_first"] = user["first"]
                        member["name_last"] = user["last"]
                        channel_details["all_members"].append(member)                               
    
    return channel_details

def channel_messages(token, channel_id, start):
    """
    Given a Channel with ID channel_id that the authorised user is part of, 
    return up to 50 messages between index "start" and "start + 50". Message 
    with index 0 is the most recent message in the channel. This function 
    returns a new index "end" which is the value of "start + 50", or, if 
    this function has returned the least recent messages in the channel, 
    returns -1 in "end" to indicate there are no more messages to load after 
    this return.
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel        
        start(int): index of starting message
        
    Returns:
        (dict): { messages, start, end }
    """ 
    return {
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

def channel_leave(token, channel_id):
    """
    Given a channel ID, the user removed as a member of this channel
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel        
    
    Returns:
        Nothing
    """  
                   
    return {
    }

def channel_join(token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join, 
    adds them to that channel
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel        
    
    Returns:
        Nothing
    """  
    return {
    }

def channel_addowner(token, channel_id, u_id):
    """
    Make user with user id u_id an owner of this channel
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel        
        u_id(int): Identifier for user
        
    Returns:
        Nothing
    """  
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    """
    Remove user with user id u_id an owner of this channel
    
    Parameters:
        token(string): an authorisation hash
        channel_id(int): identifier for channel        
        u_id(int): Identifier for user
        
    Returns:
        Nothing
    """  
    return {
    }
