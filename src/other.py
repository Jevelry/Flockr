"""
data(data.py): Gives access to global variable
"""
import data
import validation
from error import InputError, AccessError

def clear():
    """
    Clears global data variable
    """

    # Keeping everything related to the
    # global variable in the same file.
    data.clear_data()

def users_all(token):
    """
    Returns a dictionary containing a list of all users in Flockr

    Parameters:
        token(string): A user authorisation hash

    Returns:
        users: A dictionary containing a list of all users in Flockr with their user details
    """
    # Check that token is valid
    validation.check_valid_token(token)

    # Initialise list of users to return to user
    users = {
        'users' : []
    }


    # Accesses data.py and appends user info of each user to users
    for user in data.data['users']:
        user_info = {
            'u_id' : user['u_id'],
            'email' : user['email'],
            'name_first' : user['first'],
            'name_last' : user['last'],
            'handle_str' : user['handle'],
            'permission_id' : user['permission_id'],
        }
        users['users'].append(user_info)

    return users


def admin_userpermission_change(token, u_id, permission_id):
    """
    Sets a user's permissions described by permission_id

    Parameters:
        token(string): A user authorisation hash
        u_id(int): Indentifier for User
        permission_id(int): A value describing a user's permissions
                            - permission_id for owners: 1
                            - permission_id for members: 2

    Returns:
        None
    """
    # Check that token is valid
    auth_u_id = validation.check_valid_token(token)

    # Dictionary of all valid permission values:
    valid_permission_id = {1, 2}

    # Checks if authorised user is an owner of Flockr
    # Returns AccessError if not an owner of Flockr
    for auth_user in data.data['users']:
        if auth_u_id == auth_user['u_id']:
            if auth_user['permission_id'] == 1:
                pass
            else:
                raise AccessError(description="User is not an owner")
    
    # Finds target user and sets 'permission_id' value to permission_id
    for user in data.data['users']:
        if user['u_id'] == u_id and permission_id in valid_permission_id:
            user['permission_id'] = permission_id
            return {}
    
    raise InputError(description="Permission id is not a valid value")




def search(token, query_str):
    """
    Returns a dictionary containing a list of all users in Flockr

    Parameters:
        token(string): A user authorisation hash

    Returns:
        messages: A dictionary containing a list of all messages that the user has sent 
                  with the corresponding query string
    """
    # Chec kthat token is valid
    u_id = validation.check_valid_token(token)

    # Initialises messages to return to user
    messages = {
        'messages': [],
    }

    # Finds all messages that the user has sent containing the query string
    for channel in data.data['channels']:
        if u_id in channel['members']:
            for message in channel['messages']:
                if query_str in message['message'] and message['u_id'] == u_id:
                    message_result = {
                        'message_id': message['message_id'],
                        'u_id': message['u_id'],
                        'message': message['message'],
                        'time_created': message['date'],
                        'token': token,
                        'query_str': query_str,
                    }
                    messages['messages'].append(message_result)
                        
    return messages
