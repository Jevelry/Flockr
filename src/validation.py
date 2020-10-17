"""
This is a file that checks everything 
"""
from error import InputError, AccessError
import data
import re

def check_valid_token(token):
    """
    Determine whether supplied token is valid

    Parameters:
        token(string): An authorisation hash

    Returns:
        Boolean based on whether token is valid
    """
    for user in data.data["logged_in"]:
        if user["token"] == token:
            return  
    raise AccessError
      
def check_valid_handle(handle_str):
    """
    Determine whether supplied handle is valid
    
    Parameters:
        handle_str(string): New handle

    Returns:
        Boolean based on whether handle is valid  
    """    
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError
    return 

def check_valid_email(email):
    """
    Determine whether email is valid.

    Parameters:
        email(string): Email in question

    Returns:
        Boolean depending on validity of email
    """
    # If email already taken.
    for user in data.data['users']:
        if user['email'] == email:
            raise InputError
    # Must be standard email (may change to custom later).
    # Regex mostly taken from geeksforgeeks site (linked in spec (6.2)).
    regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}(\.\w{2})?$'
    # If email doesn't match regex, it's not valid.
    if not re.search(regex, email):
        raise InputError
    return
    
def check_existing_email(email):
    """
    Determine whether email is used with an account.

    Parameters:
        email(string): Email in question

    Returns:
        Boolean depending on if email is in use already.
    """
    for user in data.data['users']:
        if user['email'] == email:
            raise InputError
    return
    
def check_existing_handle(handle_str):
    """
    Determine whether supplied handle already exists
    
    Parameters:
        handle_str(string): New handle

    Returns:
        Boolean based on whether handle already exists 
    """
    for users in data.data["users"]:
        if users["handle"] == handle_str:
            raise InputError
    return
    
def check_correct_password(email, password):
    """
    Determines whether password matches account
    created with given email

    Parameters:
        email(string): Email used for account being logged into
        password(string): Password given

    Returns:
        Boolean depending on whether email and password match
    """
    for user in data.data['users']:
        if user['email'] == email and user['password'] == password:
            return
    raise InputError
def check_correct_email(email):
    """
    Determine whether email exists when logining in

    Parameters:
        email(string): Email in question

    Returns:
        Boolean depending on if email is in use already.
    """
    for user in data.data['users']:
        if user['email'] == email:
            return
    raise InputError

def check_valid_name(first, last):
    """
    Determines whether first and last name are allowed.

    Parameters:
        first(string): User's given first name
        last(string): User's given last name

    Returns:
        Boolean depending on whether names are allowed
    """
    # If first name is invalid.
    if len(first) < 1 or len(first) > 50:
        raise InputError
    # If last name is invalid.
    if len(last) < 1 or len(last) > 50:
        raise InputError
    return 
    
def check_valid_password(password):
    """
    Determines whether password is allowed.

    Parameters:
        password(string): Password given by user

    Returns:
        Boolean depending on whether password is allowed.
    """
    if len(password) < 6:
        raise InputError
    return
    
def check_valid_token_inchannel(token, channel_id):
    """
    Determine whether supplied token is valid

    Parameters:
        token(string): An authorisation hash
        channel_id(int): Identifier for channel

    Returns:
        Boolean based on whether token is valid
    """
    u_id = None
    # Check if valid token, take u_id
    for user in data.data["logged_in"]:
        if user["token"] == token:
            u_id = user["u_id"]
    if u_id is None:
        raise AccessError
    # Check if user is existing member of channel
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            for channel in user["channel_list"]:
                if channel == channel_id:
                    return 
    raise AccessError
    
def check_valid_channel_id(channel_id):
    """
    Determines whether given channel_id matches an existing channel

    Parameters:
        channel_id(int): Identifier for a channel

    Returns:
        Boolean depending on whether the supplied channel exists
    """
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            return
    raise InputError
    
def check_valid_u_id(u_id):
    """
    Check if u_id of invitee is valid

    Parameters:
        u_id(int): Identifier for user

    Returns:
        Boolean depending on whether u_id is valid
    """
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            return
    raise InputError
    
def check_is_existing_channel_member(u_id, channel_id):
    """
    Check if inviteee is already part of channel

    Parameters:
        u_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Boolean depending on whether u_id is valid
    """
    # Find user
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            # Check user's channel list for channel_id
            for channel in user["channel_list"]:
                if channel == channel_id:
                    raise InputError
    return
    
def check_is_channel_owner(user_id, channel_id):
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
                    return
    raise AccessError

def check_isnot_channel_owner(user_id, channel_id):
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            for owner in channel["owners"]:
                if owner == user_id:
                    raise InputError
    
