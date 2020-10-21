"""
This is a file that checks everything 

"""
from error import InputError, AccessError
import data
import re
import hashlib
import jwt

def check_valid_token(token):
    """
    Determine whether supplied token is valid

    Parameters:
        token(string): An authorisation hash

    Returns:
        Raises an error if token is invalid
        Returns u_id if token is valid
    """
    try:
        payload = jwt.decode(token, data.jwt_secret, algorithms=['HS256'])
        correct_token = jwt.encode(payload, data.jwt_secret, algorithm='HS256')
        if (token == correct_token):
            return payload['u_id']
    except:
        raise AccessError(description="Token is invalid")
    raise AccessError(description="Token is invalid")



def check_valid_handle(handle_str):
    """
    Determine whether supplied handle is valid

    Parameters:
        handle_str(string): New handle

    Returns:
        Raises an error if handle is invalid
        Returns nothing if valid handle
    """
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description="Handle is invalid")
    return



def check_valid_email(email):
    """
    Determine whether email is valid.

    Parameters:
        email(string): Email in question

    Returns:
        Raises an error if email is invalid (Doesn't match regex or already in use)
        Returns nothing is valid email
    """
    # If email already taken.
    # for user in data.data['users']:
    #     if user['email'] == email:
    #         raise InputError(description="Email already in use")
    if data.get_user_with({ 'email' : email }) is not None:
        raise InputError(description="Email already in use")
    # Must be standard email (may change to custom later).
    # Regex mostly taken from geeksforgeeks site (linked in spec (6.2)).
    regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}(\.\w{2})?$'
    # If email doesn't match regex, it's not valid.
    if not re.search(regex, email):
        raise InputError(description="Email is invalid")
    return

def check_existing_email(email):
    """
    Determine whether email is used with an account.

    Parameters:
        email(string): Email in question

    Returns:
        Raises an error if email already exists
        Returns nothing if email doesn't exist
    """
    if data.get_user_with({ 'email' : email }) is not None:
        raise InputError('Email already in use')
    return

def check_existing_handle(handle_str):
    """
    Determine whether supplied handle already exists

    Parameters:
        handle_str(string): New handle

    Returns:
        Raises an error if handle already exists
        Returns nothing if handle doesn't exist
    """
    # for users in data.data["users"]:
    #     if users["handle"] == handle_str:
    #         raise InputError(description="Handle already in use")
    # return
    if data.get_user_with({ 'handle_str' : handle_str }) is not None:
        raise InputError(description="Handle already in use")
    return

def check_correct_password(email, password):
    """
    Determines whether password matches account
    created with given email

    Parameters:
        email(string): Email used for account being logged into
        password(string): Password given

    Returns:
        Raises an error if password doesn't match email
        Returns nothing if password and email match
    """
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    # for user in data.data['users']:
    #     if user['email'] == email and user['password'] == password_hash:
    #         return
    if data.get_user_with({ 'email' : email })['password'] == password_hash:
        return
    else:
        raise InputError(description="Password is incorrect")

def check_correct_email(email):
    """
    Determine whether email exists when loging in

    Parameters:
        email(string): Email in question

    Returns:
        Raises an error if email doesn't exist
        Returns nothing if email exists
    """
    if data.get_user_with({ 'email' : email }) is not None:
        return
    raise InputError(description="Email has not been registered")

def check_valid_name(first, last):
    """
    Determines whether first and last name are allowed.

    Parameters:
        first(string): User's given first name
        last(string): User's given last name

    Returns:
        Raises an error if invalid first name
        Returns nothing if valid first name
    """
    # If first name is invalid.
    if len(first) < 1 or len(first) > 50:
        raise InputError("First name is not valid")
    # If last name is invalid.
    if len(last) < 1 or len(last) > 50:
        raise InputError("Last name is not valid")
    return

def check_valid_password(password):
    """
    Determines whether password is allowed.

    Parameters:
        password(string): Password given by user

    Returns:
        Raises an error if invalid password
        Returns nothing if valid password
    """
    if len(password) < 6:
        raise InputError(description="Password is not valid")
    return

def check_user_in_channel(u_id, channel_id):
    """
    Determine whether user is in a particular channel

    Parameters:
        u_id(int): Identifier for user
        channel_id(int): Identifier for channel

    Returns:
        Raises an error if user not in channel
        Returns nothing if user is in channel
    """
    if not data.check_logged_in(u_id):
        raise AccessError(description="User is not logged in")
    if not data.check_user_in_channel(channel_id, u_id):
        raise AccessError(description="User is not in channel")
    # logged_in = False
    # for user in data.data['logged_in']:
    #     if user == u_id:
    #         logged_in = True
    #         break
    # if not logged_in:
    #     raise AccessError(description="User is not logged in")
    # # Check if user is existing member of channel
    # for user in data.data["users"]:
    #     if user["u_id"] == u_id:
    #         for channel in user["channel_list"]:
    #             if channel == channel_id:
    #                 return
    # raise AccessError(description="User is not in channel")

def check_valid_channel_id(channel_id):
    """
    Determines whether given channel_id matches an existing channel

    Parameters:
        channel_id(int): Identifier for a channel

    Returns:
        Raises an error if channel doesn't exist
        Returns nothing if channel exists
    """
    if data.get_channel_info(channel_id) is None:
        raise InputError(description="Channel does not exist")

def check_valid_u_id(u_id):
    """
    Check if u_id of invitee is valid

    Parameters:
        u_id(int): Identifier for user

    Returns:
        Raises an error if user doesn't exist
        Returns nothing if user exists
    """
    if data.get_user_info(u_id) is None:
        raise InputError(description="User does not exist")

def check_is_existing_channel_member(u_id, channel_id):
    """
    Check if inviteee is already part of channel

    Parameters:
        u_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Raises an error if user is not part of channel
        Returns nothing if user is part of channel
    """
    if not data.check_user_in_channel(channel_id, u_id):
        raise InputError(description="User is not part of channel")
    # Find user
    # for user in data.data["users"]:
    #     if user["u_id"] == u_id:
    #         # Check user's channel list for channel_id
    #         for channel in user["channel_list"]:
    #             if channel == channel_id:
    #                 raise InputError(description="User is not part of channel")
    # return

def check_is_channel_owner(user_id, channel_id):
    """
    Determines whether user is an owner of a given channel

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Raises an error if user is not an owner of channel
        Returns nothing if user is an owner of channel
    """
    if not data.check_channel_owner(channel_id, user_id):
        raise AccessError(description="User is not owner of channel")
    # for channel in data.data["channels"]:
    #     if channel["channel_id"] == channel_id:
    #         for owner in channel["owners"]:
    #             if owner == user_id:
    #                 return
    

def check_isnot_channel_owner(user_id, channel_id):
    """
    Determines whether user is not an owner of a given channel

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        Raises an error if user is an owner of channel
        Returns nothign is user is not an owner of channel
    """
    if data.check_channel_owner(channel_id, user_id):
        raise InputError(description="User is owner of channel")
    # for channel in data.data["channels"]:
    #     if channel["channel_id"] == channel_id:
    #         for owner in channel["owners"]:
    #             if owner == user_id:
    #                 raise InputError(description="User is owner of channel")

def valid_message(message):
    """
    Will raise an input error if the message string is greater then 1000 characters long

    Parameters:
        message(string): The string of the message to be sent
    Returns:
    """
    if len(message) > 1000:
        raise InputError(description='Invalid message')

def valid_message_id(message_id):
    """
    Will check that message_id given has a message it refers to in the global variable will 
    raise an InputError

    Parameters:
        message_id(string): The message_id of the channel being checked
    Returns:
    """
    if message_id > data.get_message_num():
        raise InputError(description='Invalid message_id')
    # found_message = False
    # for channel in data.data['channels']:
    #     for message in channel['messages']:
    #         if message['message_id'] == message_id:
    #             found_message = True
    # if not found_message:
    #     raise InputError
 
def check_channel_is_public(channel_id):
    channel = data.get_channel_info(channel_id)
    if channel["is_public"]:
        return
    else:
        raise InputError(description="Cannot join private channel")
