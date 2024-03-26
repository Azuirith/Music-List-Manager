from dotenv import load_dotenv
from os import environ
from requests import post

import authorization

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
    song_uri = "spotify:track:4LB264fAdV4BPK99w4UMxl"

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += f"uris={song_uri}"
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    
    response = post(url, headers=headers)
    print(response.status_code)

def remove_song(token, title):
    pass

print("### Music List Manager ###")

print("Authorizing user...")
token = authorization.request_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
print("\nUser authorized.") # New line to space message from window library output

program_running = True
while (program_running):
    selected_action = prompt_action_select()
    try:
        selected_action = int(selected_action)
    except:
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