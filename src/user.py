"""
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
auth(auth.py): Gives access to check valid names and emails
channel(channel.py): Gives access to valid_u_id function
re(regex): Gives access to regex for valid_email
"""
import data
import validation

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
    validation.check_valid_token(token)
           
    #Check for valid u_id
    validation.check_valid_u_id(u_id) 
        
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
    validation.check_valid_token(token)
        
    #Check for valid name
    validation.check_valid_name(name_first, name_last)
           
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
    validation.check_valid_token(token)
        
    #Check for valid email
    validation.check_valid_email(email)
        
        
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
    validation.check_valid_token(token)
        
    #Check for valid handle    
    validation.check_valid_handle(handle_str)
           
    
    #Check for existing handle 
    validation.check_existing_handle(handle_str)
        
    #Everything valid, proceed with changing handle

    for users in data.data["users"]:
        if users["u_id"] == u_id: 
            users["handle"] = handle_str
       

