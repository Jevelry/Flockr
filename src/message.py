"""
Replace this with your own docstring.
I just want to pass pylint
"""
def message_send(token, channel_id, message):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return {
        'token' : token, # Delete this line. Pylint is complaining about unused variables.
        'channel_id' : channel_id, #Delete this line.
        'message' : message, # Delete this line
        'message_id': 1,
    }

def message_remove(token, message_id):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return {
        'token' : token, # Delete this line.
        'message_id' : message_id # Delete this line
    }

def message_edit(token, message_id, message):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return {
        'token' : token, # Delete this line
        'message_id' : message_id, # Delete this line
        'message' : message # Delete this line
    }
