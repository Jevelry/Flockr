"""
time: Gives access to function sleep
threading: Gives access to multi threading
datetime: Gives access to the datetime functions
error(error.py): Gives access to error classes
data(data.py): Gives access to global data variable
validation(validation.py): Gives access to the premade validations
"""
import time
import threading
import datetime
from error import AccessError, InputError
import data
import validation

def standup_start(token, channel_id, length):
    """
    Starts the standup for the given channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel the standup is being started for
        length(int): The delay before the standup should be posted

    Returns:
        time_finish(int(unix timestamp)): When the standup will be posted
    """
    return {
        "time_finish": 0
    }

def standup_active(token, channel_id):
    """
    Checks if there is a standup active on the channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel that the standup is being checked

    Returns:
        is_active(boolean): If there is a standup active on the given channel
        time_finish(int(unix timestamp)): When the standup will be posted
    """
    return {
        "is_active": False,
        "time_finish": 0
    }

def standup_send(token, channel_id, message):
    """
    Adds a new message to the standup in a channel

    Parameters:
        token(string): An authorisation hash
        channel_id(int): The channel_id of the channel standup the message is being added too
        message(string): The message of the message being added

    Returns:
        Nothing
    """
    return {
    }
