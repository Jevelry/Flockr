"""
Contains all the 'user story' tests
"""
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest
#import server



# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    """
    Allows pytest to create a new server.
    Returns url for new server.
    """
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_edit_profile():
    register_info = {
        'name_first' : 'Fred',
        'name_last' : 'Smith',
        'email' : 'fred@gmail.com',
        'password' : 'fredsmith'
    }
    resp1