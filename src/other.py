"""
data(data.py): Gives access to global variable
"""
import data

def clear():
    """
    Clears global data variable
    """
    # Keeping everything related to the
    # global variable in the same file.
    data.clear_data()

def users_all(token):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
                'coin' : token # Delete this line. Pylint is complaining about unused variables.
            },
        ],
    }

def admin_userpermission_change(token, u_id, permission_id):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return (token, u_id, permission_id) # Delete this line

def search(token, query_str):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
                'token' : token,
                'query_str' : query_str
            }
        ],
    }
