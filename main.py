from dotenv import load_dotenv
from os import environ
from random import randint
from selenium import webdriver
from time import sleep
from requests import get, post
from json import loads

load_dotenv()
CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]
REDIRECT_URI = environ["REDIRECT_URI"]

def generate_authorization_state(length):
    state = ""
    for _ in range(length): state += str(randint(0, 9))
    return state

def prompt_authorization_window(url):
    browser = webdriver.Chrome()
    browser.get(url)

    while not "code=" in browser.current_url: sleep(1)
    authorized_url = browser.current_url
    browser.close()

    return authorized_url

def get_url_header(url, header):
    if not header in url: return None

    # + 1 accounts for the equals sign that follows the header
    start_index = url.index(header) + len(header) + 1
    parsed_header = url[start_index:]

    end_index = None
    if ("&" in parsed_header): end_index = parsed_header.index("&")
    else: end_index = len(parsed_header)
    parsed_header = parsed_header[:end_index]

    return parsed_header

def request_authorization(): 
    # Done for security check
    state = generate_authorization_state(length=16) 

    # URL headers must be added manually because URL is opened directly rather than using
    # request library
    url = "https://accounts.spotify.com/authorize?"
    url += "client_id=" + CLIENT_ID + "&"
    url += "response_type=code&"
    url += "redirect_uri=" + REDIRECT_URI + "&"
    url += "state=" + state + "&"
    url += "scope=playlist-modify-public"
    
    authorized_url = prompt_authorization_window(url)
    returned_state = get_url_header(authorized_url, "state")
    if (returned_state != state):
        raise Exception("Error: Client state and server state do not match.")

    authorization_code = get_url_header(authorized_url, "code")

    # TODO: Research http request bodies vs headers
    url = "https://accounts.spotify.com/api/token"
    body = {"grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET}

    response = post(url, data=body)
    print(loads(response.content)["expires_in"])
    
request_authorization()