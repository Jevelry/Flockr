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
        
    
    
