from requests import get, post, delete
from json import dumps

from dotenv import load_dotenv
from os import environ

STATUS_CODE_OK = 200

load_dotenv()
PLAYLIST_ID = environ["PLAYLIST_ID"]

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
    artist_item = search_for_item(token=token, name=name, item_type="artist")
    artist_id = artist_item["id"]

    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/x-www-form-urlencoded"}
    
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?"
    url += "include_groups=album"

    response = get(url, headers=headers)
    returned_albums = response.json()["items"] 

    album_ids = []
    for album in returned_albums: album_ids.append(album["id"])

    albums = []
    for album_id in album_ids:
        url = f"https://api.spotify.com/v1/albums/{album_id}"

        response = get(url, headers=headers)
        album_item = response.json()

        album_name = album_item["name"]
        album_popularity = album_item["popularity"]
        albums.append((album_name, album_id, album_popularity))

    albums = sorted(albums, key=lambda album: album[2], reverse=True)
    top_albums = albums[:3]

    track_uris = []
    for album in top_albums:
        url = f"https://api.spotify.com/v1/albums/{album[1]}/tracks"

        response = get(url, headers=headers)
        returned_tracks = response.json()["items"]

        for track in returned_tracks: track_uris.append(track["uri"])

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += "uris="
    for uri in track_uris: url += uri + ","

    response = post(url, headers=headers)
    if response.status_code != STATUS_CODE_OK:
        print("Error: Failed to add requested artist to playlist\n")
    else:
        print("Artist added successfully\n")    

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