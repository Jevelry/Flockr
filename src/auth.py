import data
from error import InputError
import re

def invalid_email(email):
    for user in data.data['users']:
        if user['email'] == email:
            return True
    
    # Taken from geeksforgeeks site (linked in spec)
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}(\.\w{2})?$'
    if not re.search(regex,email):
        print ("bad email")
        return True
    return False

def existing_email(email):
    for user in data.data['users']:
        if user['email'] == email:
            return True
    return False


def incorrect_password(email, password):
    for user in data.data['users']:
        if user['email'] == email and user['password'] == password:
            return False
    return True

def auth_login(email, password):
    new_email = email.lower()
    if not existing_email(new_email):
        raise InputError
    elif incorrect_password(new_email, password):
        raise InputError
    # Valid log-in (user definitely exists)
    for user in data.data['users']:
        if user['email'] == email:
            break
    data.data['logged_in'].append({
        'token' : email,
        'u_id' : user['u_id']
    })
    return {
        'u_id' : user['u_id'],
        'token' : email
    }


def auth_logout(token):
    for user in data.data['logged_in']:
        if user['token'] == token:
            data.data['logged_in'].remove(user)
            return {'is_success' : True}
    return {'is_success' : False}



def invalid_name(first, last):
    if len(first) < 1 or len(first) > 50:
        return True
    if len(last) < 1 or len(last) > 50:
        return True
    return False

def invalid_password(password):
    if len(password) < 6:
        return True
    return False

def auth_register(email, password, name_first, name_last):
    #print(data['users'])
    new_email = email.lower()
    if invalid_email(new_email):
        raise InputError
    if existing_email(new_email):
        raise InputError
    elif invalid_name(name_first, name_last):
        raise InputError
    elif invalid_password(password):
        raise InputError
    new = {}
    new['channel_list'] = []
    new['first'] = name_first
    new['last'] = name_last
    new['u_id'] = len(data.data['users']) + 1
    new['password'] = password
    new['email'] = new_email
    data.data['users'].append(new)
    return {
        'u_id' : new['u_id'],
        'token': new['email']
    }
    '''
    return {
        'u_id': 1,
        'token': '12345',
    }
    '''

if __name__ == '__main__':
    user = auth_register('snow@white.com', 'dwarves', 'Snow', 'White')
    auth_logout(user['token'])
    user = auth_login('snow@white.com', 'dwarves')