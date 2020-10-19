"""
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
"""
import data
import validation
from error import InputError, AccessError



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
    validation.check_valid_channel_id(channel_id)

    # Check if token is valid and user is authorised(member of channel)
    validation.check_valid_token_inchannel(token, channel_id)
        
    # Check if given valid u_id
    validation.check_valid_u_id(u_id)
    
    # Check if invitee is already part of channel. If so,raise input error
    validation.check_is_existing_channel_member(u_id, channel_id)
      
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
    validation.check_valid_channel_id(channel_id)
      
    # Check if token is valid and user is authorised(member of channel)
    validation.check_valid_token_inchannel(token, channel_id)

    # Everything valid, Proceed with getting details
    channel_info = {
        "name" : "",
        "owner_members" : [],
        "all_members" : []
    }
    # Find channel and copy infomation into channel_details
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            channel_info["name"] = channel["name"]
            for u_id in channel["owners"]:
                for user in data.data["users"]:
                    owner = {}
                    if user["u_id"] == u_id:
                        owner["u_id"] = u_id
                        owner["name_first"] = user["first"]
                        owner["name_last"] = user["last"]
                        channel_info["owner_members"].append(owner)

            for u_id in channel["members"]:
                for user in data.data["users"]:
                    member = {}
                    if user["u_id"] == u_id:
                        member["u_id"] = u_id
                        member["name_first"] = user["first"]
                        member["name_last"] = user["last"]
                        channel_info["all_members"].append(member)

    return channel_info

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
    validation.check_valid_channel_id(channel_id)

    # Check if token is valid and user is authorised(member of channel)
    validation.check_valid_token_inchannel(token, channel_id)

    # Proceed to getting messages
    messages = {
        "messages" : [],
        "start" : start,
        "end": start + 50
    }

    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            if len(channel["messages"]) < start:
                raise InputError
            for message_id in channel["messages"][start:start + 50]:
                messages['messages'].append(message_id)
            if len(channel["messages"]) < start + 50:
                messages["end"] = -1
    return messages

def channel_leave(token, channel_id):
    """
    Checks if user is in channel, then removes the user from the channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): Identifier for channels

    Returns:
        Empty dictionary
    """
    # Check if given valid channel_id
    validation.check_valid_channel_id(channel_id)

    # Check if token is valid and user is authorised(member of channel)
    validation.check_valid_token_inchannel(token, channel_id)

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

#Will take a token and return the id
def token_to_id(token):
    """
    Converts a valid token to its corresponding id

    Parameters:
        token(string): An authorisation hash

    Returns:
        u_id relating to the supplied token
    """
    for user in data.data["logged_in"]:
        if user["token"] == token:
            return user["u_id"]
    raise AccessError
'''
#Will determine if someone is a member of a given channel
def is_channel_owner(user_id, channel_id):
    """
    Determines whether user is an owner of a given channel

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        True if user is an owner of the channel
        False if user is not an owner of the channel
    """
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            for owner in channel["owners"]:
                if owner == user_id:
                    return True
    return False
'''    
'''
#Will determine if someone is a member of a given channel
def is_channel_member(user_id, channel_id):
    """
    Determines whether user is a member of a given channel

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        True if user is a member of the channel
        False if user is not a member of the channel
    """

    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            for member in channel["members"]:
                if member == user_id:
                    return True
    return False
'''

# Will make owner of Flockr owner of channel
def add_owner(u_id, channel_id):
    """
    Makes the owner of flockr an owner when they join

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Nothing
    """
    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel['owners'].append(u_id)

'''
# Will check if channel exists
def channel_exists(channel_id):
    """
    Determines whether channel exists

    Parameters:
        channel_id(int): Identifier for channels

    Returns:
        True if the channel exists
        False if the channel doesn't exist
    """
    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False
'''

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

    user_id = token_to_id(token)

    # Checks channel exists
    validation.check_valid_channel_id(channel_id)


    #Checks the person wasn't already in the channel
    validation.check_is_existing_channel_member(user_id, channel_id)
       

    #Checks the channel is public and adds the user to the members
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            if channel["state"] is True:
                channel["members"].append(user_id)
            else:
                raise AccessError

    #Puts the channel in the users channels
    for user in data.data["users"]:
        if user["u_id"] == user_id:
            user["channel_list"].append(channel_id)
            if user['permission_id'] :
                add_owner(user['u_id'], channel_id)


    return {}



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
    owner_id = token_to_id(token)

    #checks the owner is an owner of the channel
    validation.check_is_channel_owner(owner_id, channel_id)


    #checks the member is a member of the channel
    validation.check_valid_token_inchannel(token, channel_id)


    #checks the member is not an owner
    validation.check_isnot_channel_owner(u_id, channel_id)

    #Will change the u_id from member to owner
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["owners"].append(u_id)
    return {}


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
    owner_id = token_to_id(token)

    #checks the owner is an owner of the channel
    validation.check_is_channel_owner(owner_id, channel_id)


    #checks the u_id is a member of the channel
    validation.check_is_channel_owner(u_id, channel_id)

    #Will change the u_id from member to owner
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["owners"].remove(u_id)
    return {}
