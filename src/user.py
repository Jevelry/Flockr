"""
Replace this with your own docstring.
I just want to pass pylint
"""
def user_profile(token, u_id):
    """
    Replace this with your own docstring.
    I just want to pass pylint
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

def user_profile_setname(token, name_first, name_last):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return (token, name_first, name_last) # Delete this line
    # return {
    # }

def user_profile_setemail(token, email):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return (token, email) # Delete this line
    # return {
    # }

def user_profile_sethandle(token, handle_str):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return (token, handle_str) # Delete this line
    # return {
    # }
