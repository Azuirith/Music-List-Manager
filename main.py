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

def search_for_item(token, name, item_type):
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}

    url = "https://api.spotify.com/v1/search?"
    url += f"q={item_type}:{name}&"
    url += f"type={item_type}"
    response = get(url, headers=headers)

    returned_items = response.json()[item_type + "s"]
    first_item = returned_items["items"][0]
    return first_item

def add_artist(token, name):
    pass

def remove_artist(token, name):
    pass

def add_album(token, title):
    album_item = search_for_item(token=token, name=title, item_type="album")
    album_id = album_item["id"]

    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"

    response = get(url, headers=headers)
    returned_items = response.json()["items"]

    track_uris = []
    for item in returned_items:
        track_uris.append(item["uri"])

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += "uris="
    for uri in track_uris: url += uri + ","
     
    response = post(url, headers=headers)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to add requested album to playlist.\n")
        print(response.status_code)
    else:
        print("Album added successfully.\n")

def remove_album(token, title):
    album_item = search_for_item(token=token, name=title, item_type="album")
    album_id = album_item["id"]

    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"

    response = get(url, headers=headers)
    returned_items = response.json()["items"]

    track_uris = []
    for item in returned_items:
        track_uris.append(item["uri"])

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
    
    track_items = []
    for uri in track_uris:
        track_items.append({"uri": uri})

    body = {"tracks": track_items}
    body = dumps(body)

    response = delete(url, data=body, headers=headers)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to remove album.\n")
        print(response.status_code)
    else:
        print("Album removed successfully.\n")

def add_song(token, title):
    song_item = search_for_item(token=token, name=title, item_type="track")
    song_uri = song_item["uri"]

    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += f"uris={song_uri}"
    
    response = post(url, headers=headers)

    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to add requested song to playlist.\n")
    else:
        print("Song added successfully.\n")

# TODO: Fix error when song is not found in playlist
def remove_song(token, title):
    song_item = search_for_item(token=token, name=title, item_type="track")
    song_uri = song_item["uri"]

    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
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