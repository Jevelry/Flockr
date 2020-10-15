"""
re(regex): Gives access to regex for valid_email
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
"""

import data
import validation


# Used in auth_register.
# Generates a unique handle (username) for each user.
def generate_handle(first, last):
    """
    Generates a unique handle based on first and last name

    Parameters:
        first(string): User's given girst name
        last(string): User's given last name

    Returns:
        handle(string) concatenated from first and last line
    """
    names = first + last
    # Handle is 20 letters max.
    handle = names[:20]
    for user in data.data['users']:
        # If handle is taken, add numbers on the end.
        if user['handle'] == handle:
            length = str(len(data.data['users']))
            handle = handle[:len(length) * -1] + length
    return handle

# Logs user in (must be an existing account).
def auth_login(email, password):
    """
    Attempts to log user in by checking whether
    eamil and password match

    Parameters:
        email(string): Email given by user
        password(string): Password given by user

    Returns:
        Dictionary with user's token and u_id (if successful)
    """
    # Convert email to lowercase.
    new_email = email.lower()

    # Checks to determine whether email and password are correct.
    validation.check_correct_email(new_email)
        
    validation.check_correct_password(new_email, password)
        

    # Everything is valid.
    # User has definitely registered. Password is correct.
    # There is at least one user in data.data['users']
    user = None
    for user in data.data['users']:
        if user['email'] == email:
            break
    if user is None:
        raise InputError
    # Update global state.
    # Adds user to data['logged_in'].
    data.data['logged_in'].append({
        'token' : new_email,
        'u_id' : user['u_id']
    })
    return {
        'u_id' : user['u_id'],
        'token' : new_email
    }


# Logs an active user out.
def auth_logout(token):
    """
    Logs the user out after checking
    that they are originally logged in

    Parameters:
        token(string): An authorisation hash

    Returns:
        Dictionary with a boolean that depends
        on whether user can be successfully logged out
    """
    # Check if user is active (logged in).
    for user in data.data['logged_in']:
        if user['token'] == token:
            # Remove user from data['logged_in'].
            data.data['logged_in'].remove(user)
            return {'is_success' : True}

    # Either user is not registered or user is not logged in.
    return {'is_success' : False}


# Create an account for a new user.
def auth_register(email, password, name_first, name_last):
    """
    Registers the user after checking to make sure
    all information given is valid

    Parameters:
        email(string): Email given by user
        password(string): Password given by user
        name_first(string): First name given by user
        name_last(string): Last name given by user

    Returns:
        Dictionary with user's u_id and token
    """
    # Convert email to lowercase.
    new_email = email.lower()

    # Checks to determine whether names, password and email are valid.
    validation.check_valid_email(new_email)
        
    validation.check_existing_email(new_email)

    validation.check_valid_name(name_first, name_last)

    validation.check_valid_password(password)


    # Update global state.
    # Adds a new user to data['users'].
    new = {}
    new['channel_list'] = []
    new['first'] = name_first
    new['last'] = name_last
    new['u_id'] = len(data.data['users']) + 1
    new['password'] = password
    new['email'] = new_email
    new['handle'] = generate_handle(name_first, name_last)
    if new['u_id'] == 1:
        new['owner'] = True
    else:
        new['owner'] = False
    data.data['users'].append(new)

    # Log user in.
    data.data['logged_in'].append({
        'token' : new_email,
        'u_id' : new['u_id']
    })

    return {
        'u_id' : new['u_id'],
        'token': new_email
    }
