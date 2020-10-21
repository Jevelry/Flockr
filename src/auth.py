"""
re(regex module): Gives access to regex for valid_email
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
haslip (hash module): Gives access to sha256 hashing (for password)
jwt (Pyjwt module): Gives access to jwts (for storing tokens)
"""

import data
import validation
from error import InputError
import hashlib
import jwt


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
    if data.get_user_with({ 'handle_str' : handle}) is not None:
        length = str(data.get_num_users())
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
        
    # Check if supplied password matches the email
    validation.check_correct_password(new_email, password)
        

    # Everything is valid.
    # User has definitely registered. Password is correct.
    # There is at least one user in data.data['users']
    user = data.get_user_with({ 'email' : email })
    if user is None:
        raise InputError(description="User does not exist")

    # Update global state.
    # Adds user to data['logged_in'].
    data.login_user(user['u_id'])
    
    return {
        'u_id' : user['u_id'],
        'token' : jwt.encode({'u_id': user['u_id']}, data.jwt_secret, algorithm='HS256')
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
    # Check if token is valid.
    u_id = validation.check_valid_token(token)

    # Check if user is active (logged in).
    if data.check_logged_in(u_id):
        data.logout_user(u_id)
        return {'is_success' : True}
    # Either not logged in or registered
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
    
    # Check whether email is already being used
    validation.check_existing_email(new_email)

    # Check whether first and last name are valid
    validation.check_valid_name(name_first, name_last)

    # Check whether password is long enough
    validation.check_valid_password(password)


    # Update global state.
    # Adds a new user to data['users'].
    new = {}
    new['channel_list'] = []
    new['first'] = name_first
    new['last'] = name_last
    new['u_id'] = data.get_num_users() + 1
    new['password'] = hashlib.sha256(password.encode()).hexdigest()
    new['email'] = new_email
    new['handle'] = generate_handle(name_first, name_last)
    if new['u_id'] == 1:
        new['permission_id'] = 1
    else:
        new['permission_id'] = 2
    data.register_user(new)

    # Log user in.
    data.login_user(new['u_id'])

    return {
        'u_id' : new['u_id'],
        'token': jwt.encode({'u_id': new['u_id']}, data.data['jwt_secret'], algorithm='HS256')
    }
