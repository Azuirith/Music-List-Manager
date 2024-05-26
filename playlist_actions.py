from enum import Enum

class Action(Enum):
    ADD_ARTIST = 1
    REMOVE_ARTIST = 2
    ADD_ALBUM = 3
    REMOVE_ALBUM = 4
    ADD_SONG = 5
    REMOVE_SONG = 6
    QUIT = 7

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