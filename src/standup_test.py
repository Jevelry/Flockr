# Does standup post if there were no standup/send
# Does standup/start send it as one message if it is over 1000 characters (Any size restrictions)
# Does it post in the given format
# Can we have a standup period of zero
# how would we test the time is exactly the same

"""
    datetime: Gives access to datetime functions to compare with standup function returns
    pytest: Gives access to pytest command (for testing)
    channel(channel.py): Gives access to channel functions
    auth(auth.py): Gives access to register, login and logout functions
    channels(channels.py): Gives access to channel_create
    standup(standup.py): Gives access to standup_start, standup_active, standUp_send
    other(other.py): Gives access to other.clear command
    error(error.py): Gives access to error classes
"""
"""
import datetime
import pytest
import channel
import auth
import channels
import standup
import other
from error import InputError, AccessError

# Successful
def test_start_valid():

    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    currtime = datetime.datetime.now().replace().timestamp()
    standup_time = standup.standup_start(user_channel_creater["token"], test_channel_id["channel_id"], 1)
    # Asserts the time given is between 1 second ahead and less then 2 seconds ahead
    assert currtime + 1 <= standup_time["time_finish"]
    assert currtime + 2 > standup_time["time_finish"]
    other.clear()

# Tests two standups cannot be started at the same time in the same channel
def test_start_invalid_same_channel():
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id = channels.channels_create(user_channel_creater["token"], "test", True)
    channel.channel_join(test_user1["token"], test_channel_id["channel_id"])
    standup.standup_start(user_channel_creater["token"], test_channel_id["channel_id"], 1)
    with pytest.raises(InputError):
        standup.standup_start(test_user1["token"], test_channel_id["channel_id"], 1)
    other.clear()

# Tests an error is raised when an invalid channel is given
def test_start_invalid_no_channel():
    test_user1 = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    with pytest.raises(InputError):
        standup.standup_start(test_user1["token"], 4, 1)
    other.clear()

# Tests if two standups can be started in two different channels
def test_start_diff_channel():
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_channel_id1 = channels.channels_create(user_channel_creater["token"], "test1", True)
    test_channel_id2 = channels.channels_create(user_channel_creater["token"], "test2", True)
    standup.standup_start(user_channel_creater["token"], test_channel_id1["channel_id"], 1)
    standup.standup_start(user_channel_creater["token"], test_channel_id2["channel_id"], 1)
    other.clear()

# Tests a person not in the channel cannot start the standup
def test_start_not_in_channel():
    user_channel_creater = auth.auth_register("creator@bigpond.com", "password", "Quick", "Shadow")
    test_user1 = auth.auth_register("optumis4ime@hotmail.com", "password", "Optimus", "Prime")
    test_channel_id1 = channels.channels_create(user_channel_creater["token"], "test1", True)
    with pytest.raises(AccessError):
        standup.standup_start(test_user1["token"], test_channel_id1["channel_id"], 1)
    other.clear()
"""