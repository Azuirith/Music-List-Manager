from dotenv import load_dotenv
from os import environ

import authorization
import api_controls
from playlist_actions import Action, prompt_action_select

load_dotenv()
CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]
REDIRECT_URI = environ["REDIRECT_URI"]

print("### Music List Manager ###")

print("Authorizing user...")
token = authorization.request_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
api_controls.create_request_headers(token=token)
print("\nUser authorized.\n") # New line at start to space message from window library output

program_running = True
while (program_running):
    selected_action = prompt_action_select()
    try:
        selected_action = Action(int(selected_action))
    except ValueError:
        print("Invalid input.\n")
        continue

    if selected_action == Action.QUIT:
        program_running = False
        break

    name = input("Enter name (enter . to cancel): ")
    if name == ".":
        print() # New line
        continue

    match selected_action:
        case Action.ADD_ARTIST: api_controls.manage_artist(name, "add")
        case Action.REMOVE_ARTIST: api_controls.manage_artist(name, "remove")
        case Action.ADD_ALBUM: api_controls.manage_album(name, "add")
        case Action.REMOVE_ALBUM: api_controls.manage_album(name, "remove")
        case Action.ADD_SONG: api_controls.manage_song(name, "add")
        case Action.REMOVE_SONG: api_controls.manage_song(name, "remove")