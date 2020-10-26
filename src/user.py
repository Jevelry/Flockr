"""
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
auth(auth.py): Gives access to check valid names and emails
channel(channel.py): Gives access to valid_u_id function
re(regex): Gives access to regex for valid_email
"""
import data
import validation


def user_profile(token, u_id):
    """
    Check whether user is valid and for a valid user, returns information 
    about their user_id, email, first name, last name, and handle
    
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

    user = data.get_user_info(u_id)
    profile = {
        "u_id" : user["u_id"],
        "email" : user["email"],
        "name_first" : user["name_first"],
        "name_last" : user["name_last"],
        "handle_str" : user["handle_str"],
    }
    return {"user" : profile}
 

    
def user_profile_setname(token, name_first, name_last):
    """
    Check whether use is valid and for a valid user, update their name
    
    Parameters:
        token(string): An authorisation hash
        name_first(string): new first name
        name_last(stirng): new last name
        
    Returns:
        Nothing
    """
    #Check for valid token
    u_id = validation.check_valid_token(token)
        
    #Check for valid name
    validation.check_valid_name(name_first, name_last)
           
    #Everything valid, proceed with changing name
    user = data.get_user_info(u_id)
    data.update_user(user, {"name_first": name_first,"name_last":name_last})  
    return {}
        
def user_profile_setemail(token, email):
    """
    Check whether use is valid and for a valid user, update their handle
    
    Parameters:
        token(string): An authorisation hash
        email(string): New email
        
    Returns:
        Nothing
    """
    #Check for valid token
    u_id = validation.check_valid_token(token)
        
    #Check for valid email
    validation.check_valid_email(email)
        
        
    #Everything valid, proceed with changing email
        
    user = data.get_user_info(u_id) 
    data.update_user(user, {"email": email})
    return {}
  
def user_profile_sethandle(token, handle_str):
    """
    Check whether use is valid and for a valid user, update their handle
    
    Parameters:
        token(string): An authorisation hash
        handle_str(string): New Handle
        
    Returns:
        Nothing
    """
    #Check for valid token
    u_id = validation.check_valid_token(token)
        
    #Check for valid handle    
    validation.check_valid_handle(handle_str)
           
    
    #Check for existing handle 
    validation.check_existing_handle(handle_str)
        
    #Everything valid, proceed with changing handle

    user = data.get_user_info(u_id) 
    data.update_user(user, {"handle_str": handle_str})
    return {}
