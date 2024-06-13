from requests import get, post, delete
from json import dumps

from dotenv import load_dotenv
from os import environ

STATUS_CODE_OK = 200

load_dotenv()
PLAYLIST_ID = environ["PLAYLIST_ID"]

request_headers = {} # This is technically a constant but it does get changed once 
                     # at the start of the program so it is not marked as one

def create_request_headers(token):
    global request_headers
    request_headers = {"Authorization": "Bearer " + token,
                      "Content-Type": "application/x-www-form-urlencoded"}

def search_for_item(name, item_type):
    url = "https://api.spotify.com/v1/search?"
    url += f"q={item_type}:{name}&"
    url += f"type={item_type}"

    response = get(url, headers=request_headers)
    returned_object = response.json()[item_type + "s"]
    return returned_object["items"][0]

def manage_artist(name, add_or_remove):
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

    albums = sorted(albums, key=lambda album: album[2], reverse=True)
    top_albums = albums[:3]

    track_uris = []
    for album in top_albums:
        url = f"https://api.spotify.com/v1/albums/{album[1]}/tracks"

        response = get(url, headers=request_headers)
        returned_tracks = response.json()["items"]

        for track in returned_tracks: track_uris.append(track["uri"])

    if (add_or_remove == "add"):
        response = add_songs_from_uris(track_uris)
        if response.status_code != STATUS_CODE_OK:
            print("Error: Failed to add requested artist to playlist.\n")
        else:
            print("Artist added successfully.\n")  
    else:
        response = remove_songs_from_uris(track_uris)
        if response.status_code != STATUS_CODE_OK:
            print("Error: Failed to remove artist.\n")
        else:
            print("Artist removed successfully.\n")  

def manage_album(name, add_or_remove):
    album_item = search_for_item(name=name, item_type="album")
    album_id = album_item["id"]
    
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"

    response = get(url, headers=request_headers)
    returned_items = response.json()["items"]

    track_uris = []
    for item in returned_items: 
        track_uris.append(item["uri"])

    if (add_or_remove == "add"):
        response = add_songs_from_uris(track_uris)
        if response.status_code != STATUS_CODE_OK:
            print("Error: Failed to add requested album to playlist.\n")
        else:
            print("Album added successfully.\n")
    else:
        response = remove_songs_from_uris(track_uris)
        if response.status_code != STATUS_CODE_OK:
            print("Error: Failed to remove album.\n")
        else:
            print("Album removed successfully.\n")

def manage_song(name, add_or_remove):
    track_item = search_for_item(name=name, item_type="track")
    track_uri = track_item["uri"]

    if (add_or_remove == "add"):
        response = add_songs_from_uris([track_uri]) 
        if response.status_code != STATUS_CODE_OK:
            print("Error: Failed to add requested song to playlist.\n")
        else:
            print("Song added successfully.\n")
    else:
        response = remove_songs_from_uris([track_uri])
        if response.status_code != STATUS_CODE_OK:
            print("Error: Failed to delete requested song from playlist.\n")
        else:
            print("Song deleted succesfully.\n")

def add_songs_from_uris(uris):
    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?"
    url += "uris="
    for uri in uris: url += uri + ","

    response = post(url, headers=request_headers)
    return response

def remove_songs_from_uris(uris):
    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"

    formatted_uris = []
    for uri in uris:
        formatted_uris.append({"uri": uri})

    body = {"tracks": formatted_uris}
    body = dumps(body)

    response = delete(url, headers=request_headers, data=body)
    return response