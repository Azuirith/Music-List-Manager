from random import randint
from time import sleep
from selenium import webdriver
from requests import post

def generate_authorization_state(length):
    state = ""
    for _ in range(length): state += str(randint(0, 9))
    return state

def prompt_authorization_window(url):
    browser = webdriver.Chrome()
    browser.get(url)

    # Waits until authorization request goes through
    while not "code=" in browser.current_url: sleep(0.1)
    authorized_url = browser.current_url
    browser.close()

    return authorized_url

def get_query_parameter(url, parameter):
    if not parameter in url: return None

    # + 1 makes it start at the equal sign that precedes the parameter value
    start_index = url.index(parameter) + len(parameter) + 1
    parsed_parameter = url[start_index:]

    end_index = None
    if "&" in parsed_parameter: end_index = parsed_parameter.index("&")
    else: end_index = len(parsed_parameter)
    parsed_parameter = parsed_parameter[:end_index]

    return parsed_parameter

def request_token(client_id, client_secret, redirect_uri): 
    # Done for security check later on
    state = generate_authorization_state(length=16) 

    url = "https://accounts.spotify.com/authorize?"
    url += f"client_id={client_id}&"
    url += "response_type=code&"
    url += f"redirect_uri={redirect_uri}&"
    url += f"state={state}&"
    url += "scope=playlist-modify-public"
    
    authorized_url = prompt_authorization_window(url)
    returned_state = get_query_parameter(authorized_url, "state")
    if (returned_state != state):
        raise Exception("Error: Client state and server state do not match.")

    authorization_code = get_query_parameter(authorized_url, "code")
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {"grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret}

    response = post(url, data=body, headers=headers)
    STATUS_CODE_OK = 200
    if response.status_code != STATUS_CODE_OK:
        raise Exception("Error: Failed to grab authorization token.")
    
    return response.json()["access_token"]