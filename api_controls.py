from requests import get, post, delete
from json import dumps

from dotenv import load_dotenv
from os import environ

STATUS_CODE_OK = 200

load_dotenv()
PLAYLIST_ID = environ["PLAYLIST_ID"]

request_headers = {} # This technically is sorta a constant 
                     # but it does get changed once at the start of the program

def create_request_headers(token):
    global request_headers
    request_headers = {"Authorization": "Bearer " + token,
                      "Content-Type": "application/x-www-form-urlencoded"}

# TODO: Maybe add some error protection if the item is not found in the search
def search_for_item(name, item_type):
    url = "https://api.spotify.com/v1/search?"
    url += f"q={item_type}:{name}&"
    url += f"type={item_type}"
    response = get(url, headers=request_headers)

    returned_items = response.json()[item_type + "s"]
    return returned_items["items"][0]

def add_artist(name):
    artist_item = search_for_item(name=name, item_type="artist")
    artist_id = artist_item["id"]
    
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?"
    url += "include_groups=album"

    response = get(url, headers=request_headers)
    returned_albums = response.json()["items"] 

    album_ids = []
    for album in returned_albums: album_ids.append(album["id"])

    albums = []
    for album_id in album_ids:
        url = f"https://api.spotify.com/v1/albums/{album_id}"

        response = get(url, headers=request_headers)
        album_item = response.json()

        album_name = album_item["name"]
        album_popularity = album_item["popularity"]
        albums.append((album_name, album_id, album_popularity))

    albums = sorted(albums, key=lambda album: album[2], reverse=True) # TODO: write own sorting algorithm for funsies
    top_albums = albums[:3]

    track_uris = []
    for album in top_albums:
        url = f"https://api.spotify.com/v1/albums/{album[1]}/tracks"

        response = get(url, headers=request_headers)
        returned_tracks = response.json()["items"]

        for track in returned_tracks: track_uris.append(track["uri"])

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += "uris="
    for uri in track_uris: url += uri + ","

    response = post(url, headers=request_headers)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to add requested artist to playlist\n")
    else:
        print("Artist added successfully\n")    

def remove_artist(token, name):
    pass

def add_album(name):
    album_item = search_for_item(name=name, item_type="album")
    album_id = album_item["id"]
    
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"

    response = get(url, headers=request_headers)
    returned_items = response.json()["items"]

    track_uris = []
    for item in returned_items:
        track_uris.append(item["uri"])

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += "uris="
    for uri in track_uris: url += uri + ","
     
    response = post(url, headers=request_headers)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to add requested album to playlist.\n")
        print(response.status_code)
    else:
        print("Album added successfully.\n")

def remove_album(name):
    album_item = search_for_item(name=name, item_type="album")
    album_id = album_item["id"]
    
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"

    response = get(url, headers=request_headers)
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

    response = delete(url, data=body, headers=request_headers)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to remove album.\n")
        print(response.status_code)
    else:
        print("Album removed successfully.\n")

def add_song(name):
    song_item = search_for_item(name=name, item_type="track")
    song_uri = song_item["uri"]

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += f"uris={song_uri}"
    
    response = post(url, headers=request_headers)

    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to add requested song to playlist.\n")
    else:
        print("Song added successfully.\n")

# TODO: Fix error when song is not found in playlist
# TODO: Find a way to search for items quickly in a playlist
def remove_song(name):  
    song_item = search_for_item(name=name, item_type="track")
    song_uri = song_item["uri"]

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
    body = {"tracks": [{"uri": song_uri}]}
    body = dumps(body) # Program seems to think the formatting is wrong without this

    response = delete(url, headers=request_headers, data=body)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to delete requested song from playlist.\n")
        print(response.json()["error"]["message"])
    else:
        print("Song deleted succesfully.\n")