"""
datetime: Gives access to the datetime functions
error(error.py): Gives access to error classes
data(data.py): Gives access to global data variable
validation(validation.py): Gives access to the premade validations
"""
import datetime
from error import AccessError, InputError
import data
import validation


# # When given the channel id it will create a unique string for the message_id
# def make_message_id():
#     """
#     Creates a unique string to be a message_id for a new message

#     Parameters:

#     Returns:
#         A String that is the number of strings that have been sent ever
#     """
#     if data.data['message_num'] == '':
#         data.data['message_num'] = 1
#     else:
#         data.data['message_num'] += 1

#     return str(data.data['message_num'])


def find_channel_with_message(message_id, u_id):
    """
    Will go through every channel and if message_in_channel returns a channel it
    will return it otherwise it raises an input error

    Parameters:
        message_id(string): The id of the message being searched for
        user_id(string): The id of the user searching for the message it will return
                         an access error if the user is not an owner of the channel
                         or creator of the message
    Returns:
        channel(channel dictionary): If the channel was found it will return the channel
                                     dictionary
    """
    # found_message = False
    # for channel in data.data['channels']:
    #     found_message = message_in_channel(message_id, user_id, channel)
    #     if found_message:
    #         return channel
    # raise InputError(description="Message not in any channel")
    # # Elliot's attempt
    # found_message = False
    channel_id = data.find_channel(message_id)
    message = data.get_message(channel_id, message_id)
    if message['u_id'] == u_id or data.check_channel_owner(channel_id, u_id):
        return channel_id
    raise AccessError(description="User is not creator or owner")
    # raise InputError(description="Message not in any channel")
    # For each channel check if message was posted there
    # check message (either u_id matches message_u_id or u_id is an owner of channel)
    # Return true if user has permission to edit, else false




# def message_in_channel(message_id, user_id, channel):
#     """
#     Will go through a given and if the message_id is in the channel it will return
#     true if the user is the creator of the message or an owner of the channel
#     otherwise an AccessError will be raised

#     Parameters:
#         message_id(string): The id of the message being searched for
#         user_id(string): The id of the user searching for the message it will return
#                          an access error if the user is not an owner of the channel
#                          or creator of the message
#         channel(channel dictionary): The channel that is being checked
#     Returns:
#         boolean: True If the message_id is found and the user has access
#                  False if the message_id is not found or user doesn't have access
#     """
#     for message in channel['messages']:
#         if message['message_id'] == message_id:
#             if message['u_id'] == user_id or user_id in channel['owners']:
#                 return True
#             else:
#                 raise AccessError(description="User is not creator or owner")
#     return False

def message_send(token, channel_id, message):
    """
    Adds a new message to the message to the messages in a channel

    Parameters:
        token(string): An authorisation hash
        channel_id(string): The channel_id of the channel the message is being added too
        message(string): The message of the message being added

    Returns:
        message_id(string): An identifier for the new message
    """
    # Check that the token is valid
    user_input_id = validation.check_valid_token(token)

    # Check that the message is valid.
    validation.valid_message(message)

    # Check that the channel_id is valid
    validation.check_valid_channel_id(channel_id)
    
    # Check that user is in channel
    validation.check_user_in_channel(user_input_id, channel_id)

    new_message_id = data.make_message_id()
    new_message = {}
    new_message['message'] = message
    new_message['u_id'] = user_input_id
    new_message['date'] = datetime.datetime.now()
    new_message['message_id'] = new_message_id

    # for channel in data.data['channels']:
    #     if channel['channel_id'] == channel_id:
    #         channel['messages'].append(new_message)
    data.add_message(new_message, channel_id)

    return {
        'message_id': new_message_id,
    }

def message_remove(token, message_id):
    """
    Removes an existing message from the channel it is in

    Parameters:
        token(string): An authorisation hash
        message_id(string): The id of the message being removed
        message(string): The message of the message being added

    Returns:
    """
    # Check valid token
    user_input_id = validation.check_valid_token(token)

    # Check valid message id
    validation.valid_message_id(message_id)
    

    channel_id = find_channel_with_message(message_id, user_input_id)
    data.remove_message(channel_id, message_id)

    return {}

def message_edit(token, message_id, message):
    """
    Removes an existing message from the channel it is in

    Parameters:
        token(string): An authorisation hash
        message_id(string): The id of the message being removed

    Returns:
        Nothing
    """
    # Check valid token
    user_input_id = validation.check_valid_token(token)

    # Check valid message
    validation.valid_message(message)
    
    # Check valid message id
    validation.valid_message_id(message_id)

    # Editing a message to an empty string will delete the message.
    if message == '':
        return message_remove(token, message_id)
        

    channel_id = find_channel_with_message(message_id, user_input_id)
    for cur_message in channel['messages']:
        if cur_message['message_id'] == message_id:
            cur_message['message'] = message
    data.edit_message(channel_id, message_id, message)
    return {}
