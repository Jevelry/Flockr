import requests


def build_string(payload):
    """
    Returns a string for details of weather
    """
    return f"""
The weather in {payload['location']['name']} \
is {payload['current']['weather_descriptions'][0]} \
and {payload['current']['temperature']}ºC
    """

def get_weather(location):
    """
    Gets information about weather
    """
    web = "http://api.weatherstack.com/current"
    web += "?access_key=9d7c65e58b3420d4e4fff81bfbdca776"
    web += "&query=" + location
    resp = requests.get(web)
    payload = resp.json()
    return build_string(payload)
