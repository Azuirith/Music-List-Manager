from dotenv import load_dotenv
from os import environ
from requests import get, post, delete
from json import dumps

import authorization

STATUS_CODE_OK = 200

load_dotenv()
CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]
REDIRECT_URI = environ["REDIRECT_URI"]
PLAYLIST_ID = environ["PLAYLIST_ID"]

def prompt_action_select():
    print("Select action:")
    print("1: Add artist")
    print("2: Remove artist")
    print("3: Add album")
    print("4: Remove album")
    print("5: Add song")
    print("6: Remove song")
    print("7: Quit\n")
    return input()

def add_artist(token, title):
    pass

def remove_artist(token, title):
    pass

def add_album(token, title):
    pass

def remove_album(token, title):
    pass

def add_song(token, title):
    # Here because both requests use the same headers
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}

    SEARCH_RETURN_COUNT = 10
    url = "https://api.spotify.com/v1/search?"
    url += f"q=track:{title}&"
    url += "type=track&"
    url += f"limit={SEARCH_RETURN_COUNT}"

    response = get(url, headers=headers)
    returned_tracks = response.json()["tracks"]
    song_uri = returned_tracks["items"][0]["uri"]

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += f"uris={song_uri}"
    
    response = post(url, headers=headers)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to add requested song to playlist.\n")
    else:
        print("Song added successfully.\n")

def remove_song(token, title):
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    
    SEARCH_RETURN_COUNT = 10
    url = "https://api.spotify.com/v1/search?"
    url += f"q=track:{title}&"
    url += "type=track&"
    url += f"limit={SEARCH_RETURN_COUNT}"

    response = get(url, headers=headers)
    returned_tracks = response.json()["tracks"]
    song_uri = returned_tracks["items"][0]["uri"]

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
    body = {"tracks": [{"uri": song_uri}]}
    body = dumps(body) # Program seems to think the formatting is wrong without this

    response = delete(url, headers=headers, data=body)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to delete requested song from playlist.\n")
        print(response.json()["error"]["message"])
    else:
        print("Song deleted succesfully.\n")

print("### Music List Manager ###")

print("Authorizing user...")
token = authorization.request_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
print("\nUser authorized.\n") # New line at start to space message from window library output

program_running = True
while (program_running):
    selected_action = prompt_action_select()
    try:
        selected_action = int(selected_action)
    except ValueError:
        print("Invalid input.\n")
        continue

    match selected_action:
        case 1:
            name = input("Enter artist name: ")
            add_artist(token, name)
        case 2:
            name = input("Enter artist name: ")
            remove_artist(token, name)
        case 3:
            title = input("Enter album title: ")
            add_album(token, title)
        case 4:
            title = input("Enter album title: ")
            remove_album(token, title)
        case 5:
            title = input("Enter song title: ")
            add_song(token, title)
        case 6:
            title = input("Enter song title: ")
            remove_song(token, title)
        case 7:
            program_running = False
            break
        case _: 
            print("Invalid input.\n")