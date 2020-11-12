"""
The name is a combination of scribbl.io and kahoot. The
function works that when a moderator types /KAHIO/ Question / Answer / length(optional)
only the question will be printed and every person who types in chat
if what they type is a normalised version of the answer (removes spaces
capitalisation). Then the time since the question was asked and user is
stored, the function then posts from the moderator who started the game's
account that the user just answered. If a user guess the answer wrong it is
posted in chat. The game is over when the given (if no length of time the
game runs for 15 seconds) length of time has finished, the function will give
period updates every 5 seconds until the final 5 seconds when it is every
second. Then a list of users times who got the question right and there places
is posted by moderator who started the game.

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

def breakdown_message(message):
    """
    Will break the message it its components and return it as a dictionary
    """
    question = ""
    answer = ""
    given_time = ""
    message_stage = 0
    for i in message[6:]:
        if i == "/":
            message_stage += 1
            validation.check_kahio_message_stage(message_stage)
        elif message_stage == 1:
            question += i
        elif message_stage == 2:
            answer += i
        elif message_stage == 3:
            given_time += i
    if given_time == "":
        given_time = 15
    else:
        given_time = validation.check_kahio_time(given_time)
    validation.check_kahio_question(question)
    answer = validation.check_kahio_answer(answer)
    return {
        "question" : question,
        "answer" : answer,
        "time" : given_time
    }

def start_kahio(u_id, channel_id, message):
    """
    Will start a kahio game on the channel and return the new start message
    """
    validation.check_is_channel_owner(u_id, channel_id)

    validation.check_kahio_not_running(channel_id)

    message_sections = breakdown_message(message)
    time_start = datetime.datetime.now().replace().timestamp()
    data.create_kahio(channel_id, u_id, time_start, message_sections["answer"])
    timer_class = threading.Timer(0.1, kahio_timer, [u_id, channel_id, message_sections["time"]])
    timer_class.start()
    data.kahio_update_timer_class(channel_id, timer_class)
    return message_sections["question"]

def kahio_timer(*args):
    """
    Sends the standup message from the given u_id

    Parameters:
        args[0] (u_id(int)) : The u_id that standup will be sent from
        args[1] (channel_id(int)) : The channel that the message will be sent to
        args[2] (time_remaining) : The time that kahio has remaining
    """
    new_message_id = data.make_message_id()
    new_message = {}
    new_message["message"] = "The kahoi game has " + str(args[2]) + " seconds remaining"
    new_message["u_id"] = args[0]
    new_message["time_created"] = datetime.datetime.now().replace().timestamp()
    new_message["message_id"] = new_message_id
    new_message["reacts"] = [
        {
            "react_id": 1,
            "u_ids": []
        }
    ]

    if args[2] <= 0:
        #If the timer has finished it will print the end message
        data.end_kahio_game(args[1])
        send_kahio_score(args[1], new_message)
        return

    data.add_message(new_message, args[1])
    time_remaing = args[2]
    time_interval = 0
    if time_remaing <= 5:
        time_interval = 1
    elif time_remaing % 5 == 0:
        time_interval = 5
    else:
        time_interval = time_remaing % 5
    time_remaing -= time_interval
    timer_class = threading.Timer(time_interval, kahio_timer, [args[0], args[1], time_remaing])
    timer_class.start()
    data.kahio_update_timer_class(args[1], timer_class)

def send_kahio_score(channel_id, new_message):
    """
    Sends the standup message from the given u_id

    Parameters:
        args[0] (u_id(int)) : The u_id that standup will be sent from
        args[1] (channel_id(int)) : The channel that the message will be sent to
        args[2] (time_remaining(int)) : The time remaining until the results are printed
                                        and the kahio game is over
    """
    answer = data.return_kahio_answer(channel_id)
    new_message["message"] = "Kahio game has ended.\nThe correct answer was " + answer +"\n"
    num_correct_answers = data.return_kahio_num_correct_answers(channel_id)
    if num_correct_answers == 0:
        #If no message was added to the kahio it will not print kahio
        new_message["message"] += "No correct answers"
    else:
        new_message["message"] += str(num_correct_answers) + " correct answers"

    new_message["message"] += data.return_kahio_score(channel_id)

    data.add_message(new_message, channel_id)

def kahio_guess(u_id, channel_id, new_message):
    """
    Will check if the message is the correct answer or not
    """
    check_message = validation.check_kahio_answer(new_message["message"])
    answer = data.return_kahio_answer(channel_id)
    if check_message == answer:
        return kahio_correct_guess(u_id, channel_id, new_message)

    data.add_message(new_message, channel_id)

    return {
        "message_id": new_message["message_id"],
    }

def kahio_correct_guess(u_id, channel_id, new_message):
    """
    If the correct message was guessed the user will be appended to the list
    an error will be raised if the user should already have the answer
    """
    validation.check_kahio_user_has_answer(channel_id, u_id)

    new_message["message"] = data.correct_kahio_guess(u_id, channel_id, new_message["time_created"])
    new_message["u_id"] = data.return_kahio_starter(channel_id)

    data.add_message(new_message, channel_id)

    return {
        "message_id": new_message["message_id"],
    }

def kahio_end(u_id, channel_id):
    """
    Will end the kahio game running on the channel and end the timer
    """
    validation.check_is_channel_owner(u_id, channel_id)
    validation.check_kahio_running(channel_id)
    data.end_kahio_game(channel_id)
    timer_class = data.get_kahio_timer_class(channel_id)
    timer_class.cancel()
