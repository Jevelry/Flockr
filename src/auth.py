import data
from error import InputError
import re


# Used in auth_register.
# Must register with a valid email.
def valid_email(email):
    # If email already taken.
    for user in data.data['users']:
        if user['email'] == email:
            return False
    
    # Must be standard email (may change to custom later).
    # Regex mostly taken from geeksforgeeks site (linked in spec (6.2)).
    regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}(\.\w{2})?$'
    # If email doesn't match regex, it's not valid.
    if not re.search(regex,email):
        return False
    return True


# Used in auth_login.
# Email must already exist.
def existing_email(email):
    for user in data.data['users']:
        if user['email'] == email:
            return True
    return False


# Used in auth_login.
# Must provide correct password.
def correct_password(email, password):
    for user in data.data['users']:
        if user['email'] == email and user['password'] == password:
            return True
    return False


# Used in auth_register.
# Can't register with an invalid first or last name.
def valid_name(first, last):
    # If first name is invalid.
    if len(first) < 1 or len(first) > 50:
        return False
    # If last name is invalid.
    if len(last) < 1 or len(last) > 50:
        return False
    return True


# Used in auth_register.
# Can't register with an invalid password.
def valid_password(password):
    if len(password) < 6:
        return False
    return True
    

# Used in auth_register.
# Generates a unique handle (username) for each user.
def generate_handle(first, last):
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
    # Convert email to lowercase.
    new_email = email.lower()

    # Checks to determine whether email and password are correct.
    if not existing_email(new_email):
        raise InputError
    elif not correct_password(new_email, password):
        raise InputError

    # Everything is valid.
    # User has definitely registered. Password is correct.
    for user in data.data['users']:
        if user['email'] == email:
            break
    
    # Update global state.
    # Adds user to data['logged_in'].
    data.data['logged_in'].append({
        'token' : email,
        'u_id' : user['u_id']
    })
    return {
        'u_id' : user['u_id'],
        'token' : email
    }


# Logs an active user out.
def auth_logout(token):
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
    # Convert email to lowercase.
    new_email = email.lower()

    # Checks to determine whether names, password and email are valid.
    if not valid_email(new_email):
        raise InputError
    if existing_email(new_email):
        raise InputError
    elif not valid_name(name_first, name_last):
        raise InputError
    elif not valid_password(password):
        raise InputError

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
    data.data['users'].append(new)

    # Log user in.
    data.data['logged_in'].append({
        'token' : email,
        'u_id' : new['u_id']
    })

    return {
        'u_id' : new['u_id'],
        'token': new['email']
    }


if __name__ == '__main__':
    user = auth_register('snow@white.com', 'dwarves', 'thisaisreallylongname', 'White')
    for person in data.data['users']:
        if user['u_id'] == person['u_id']:
            print(person['handle'])

    user = auth_register('snow1@white.com', 'dwarves', 'Snow', 'White')
    for person in data.data['users']:
        if user['u_id'] == person['u_id']:
            print(person['handle'])
    
    user = auth_register('snow45@white.com', 'dwarves', 'Snow', 'White')
    for person in data.data['users']:
        if user['u_id'] == person['u_id']:
            print(person['handle'])