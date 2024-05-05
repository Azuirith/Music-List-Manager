# TODO: Make it so that you can back out of commands
from dotenv import load_dotenv
from os import environ

import authorization
import playlist_controls

load_dotenv()
CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]
REDIRECT_URI = environ["REDIRECT_URI"]

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
            playlist_controls.add_artist(token, name)
        case 2:
            name = input("Enter artist name: ")
            playlist_controls.remove_artist(token, name)
        case 3:
            title = input("Enter album title: ")
            playlist_controls.add_album(token, title)
        case 4:
            title = input("Enter album title: ")
            playlist_controls.remove_album(token, title)
        case 5:
            title = input("Enter song title: ")
            playlist_controls.add_song(token, title)
        case 6:
            title = input("Enter song title: ")
            playlist_controls.remove_song(token, title)
        case 7:
            program_running = False
            break
        case _: 
            print("Invalid input.\n")