"""
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
auth(auth.py): Gives access to check valid names and emails
channel(channel.py): Gives access to valid_u_id function
re(regex): Gives access to regex for valid_email
"""
from auth import existing_email, valid_name
import data
from error import InputError, AccessError
from channel import valid_u_id
import re

def valid_token(token):
    """
    Determine whether supplied token is valid

    Parameters:
        token(string): An authorisation hash

    Returns:
        Boolean based on whether token is valid
    """
    for user in data.data["logged_in"]:
        if user["token"] == token:
            return True  
    return False  


def get_uid(token):
    """
    Get users u_id from token
    
    Parameters:
        token(string): An authorisation hash

    Returns:
        u_id(int) 
    """
    for user in data.data["logged_in"]:
        if user["token"] == token:
            return user["u_id"]

def valid_handle(handle_str):
    """
    Determine whether supplied handle is valid
    
    Parameters:
        handle_str(string): New handle

    Returns:
        Boolean based on whether handle is valid  
    """    
    if len(handle_str) < 3 or len(handle_str) > 20:
        return False
    return True
    
def valid_email(email):
    """
    Determine whether email is valid.

    Parameters:
        email(string): Email in question

    Returns:
        Boolean depending on validity of email
    NOTE: Very similar to valid_email in auth but does not check for existing email
    """
    # Must be standard email (may change to custom later).
    # Regex mostly taken from geeksforgeeks site (linked in spec (6.2)).
    regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}(\.\w{2})?$'
    # If email doesn't match regex, it's not valid.
    if not re.search(regex, email):
        return False
    return True
    
def existing_handle(handle_str):
    """
    Determine whether supplied handle already exists
    
    Parameters:
        handle_str(string): New handle

    Returns:
        Boolean based on whether handle already exists 
    """
    for users in data.data["users"]:
        if users["handle"] == handle_str:
            return True
    return False


def user_profile(token, u_id):
    """
    For a valid user, returns information about their user_id, 
    email, first name, last name, and handle
    
    Parameters:
        token(string): An authorisation hash
        u_id(int): Identifier for user
        
    Returns:
        Dictionary with information about user
    """
    #Check for valid token
    if valid_token(token) == False:
        raise AccessError
    #Check for valid u_id
    if valid_u_id(u_id) == False:
        raise InputError
    #Everything valid, proceed with getting profile details
    user = {}
    for users in data.data["users"]:
        if users["u_id"] == u_id:
            user["u_id"] = users["u_id"]
            user["email"] = users["email"]
            user["name_first"] = users["first"]
            user["name_last"] = users["last"]
            user["handle_str"] = users["handle"]
        return user      

    """
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'hjacobs',
            'token' : token, # Delete this line. Pylint is complaining about unused variables.
            'id' : u_id + 1 # Delete this line
        },
    }
    """
    
    
    
    
    
def user_profile_setname(token, name_first, name_last):
    """
    For a valid user, update their name
    
    Parameters:
        token(string): An authorisation hash
        name_first(string): new first name
        name_last(stirng): new last name
        
    Returns:
        Nothing
    """
    #Check for valid token
    if not valid_token(token):
        raise AccessError
    #Check for valid name
    if not valid_name(name_first, name_last):
        raise InputError    
    #Everything valid, proceed with changing name
    u_id = get_uid(token)
    for users in data.data["users"]:
        if users["u_id"] == u_id: 
            users["first"] = name_first
            users["last"] = name_last  
        


def user_profile_setemail(token, email):
    """
    For a valid user, update their handle
    
    Parameters:
        token(string): An authorisation hash
        email(string): New email
        
    Returns:
        Nothing
    """
    u_id = get_uid(token)
    #Check for valid token
    if not valid_token(token):
        raise AccessError
    #Check for valid email
    if not valid_email(email):
        raise InputError
    #Check if changing to same emails
    for users in data.data["users"]:
        if users["u_id"] == u_id: 
            if users["email"] == email:
                return
    #Check for existing email
    if existing_email(email):
        raise InputError
    #Everything valid, proceed with changing email
    for users in data.data["users"]:
        if users["u_id"] == u_id: 
            users["email"] = email

  
def user_profile_sethandle(token, handle_str):
    """
    For a valid user, update their handle
    
    Parameters:
        token(string): An authorisation hash
        handle_str(string): New Handle
        
    Returns:
        Nothing
    """
    u_id = get_uid(token)
    #Check for valid token
    if not valid_token(token):
        raise AccessError
    #Check for valid handle    
    if not valid_handle(handle_str):
        raise InputError   
    #Check if new handle same as old
    for users in data.data["users"]:
        if users["u_id"] == u_id: 
            if users["handle"] == handle_str:
                return
    #Check for existing handle 
    if existing_handle(handle_str):
        raise InputError
    #Everything valid, proceed with changing handle

    for users in data.data["users"]:
        if users["u_id"] == u_id: 
            users["handle"] = handle_str
       

