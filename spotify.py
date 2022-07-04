import base64
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv() 

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
BASE64_ENCODED_HEADER_STRING = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "ISO-8859-1")).decode("ascii")

SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'


def get_auth_token() -> str:
    """ Obtain an auth token for server to server usage, i.e. no user auth """

    headers = {
        'Authorization': f"Basic {BASE64_ENCODED_HEADER_STRING}"
    }

    data = {
        'grant_type': 'client_credentials',
        'json': True
    }

    token_response = requests.post(
        'https://accounts.spotify.com/api/token', 
        headers=headers, 
        data=data
    )

    token_data = token_response.json()

    return token_data.get('access_token')

def search(name: str):
    """ Search for an artist by name, limiting to 1 for exact match """

    search_response = requests.get(
        f"{SPOTIFY_BASE_URL}/search", 
        headers={
            'Authorization': f'Bearer {get_auth_token()}',
        },
        params={
            'type': 'artist',
            'limit': 1,
            'q': name
        },
    )

    return search_response.json()

def top_tracks(id: str):
    """ Get an artist's top tracks to revise """

    top_tracks_response = requests.get(
    f"{SPOTIFY_BASE_URL}/artists/{id}/top-tracks", 
        headers={
            'Authorization': f'Bearer {get_auth_token()}',
        },
        params={'market': 'GB'}
    )

    top_tracks_data = top_tracks_response.json()
    return top_tracks_data.get('tracks', [])

def find_artist(name: str):
    """ Helper function to find an artist using search and returning the item """

    search_results = search(name)
    items = search_results.get('artists').get('items')

    return items[0] if len(items) > 0 else {}

def main():
    """ Takes BOA data and decorates with Spotify genres and top tracks """

    artists_in = json.load(open('bands.json', 'r'))
    artists_out = []

    for artist in artists_in:
        name = artist['name']
        print(name)

        detail = find_artist(name)
        artist.update({'genres': detail.get('genres', []), 'top_tracks': []})
        
        tracks = top_tracks(detail.get('id'))
        for track in tracks:
            artist['top_tracks'].append({
                'name': track['name'], 
                'preview_url': track['preview_url']
            })
        
        artists_out.append(artist)
        
    with open('bands_final.json', 'w') as out_file:
        out_file.write(json.dumps(artists_out))


if __name__ == '__main__':
    main()