import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
      client_id=#, 
      client_secret=#
    )  
)
tracks = {}
while len(tracks) < 200:
    results = sp.search(
        q=random.choice('abcdefghijklmnopqrstuvwxyz'),
        type='track',
        limit=50,
        offset=random.randint(0, 950)
    )    
    for track in results['tracks']['items']:
        if track['id'] not in tracks:
            artist_id = track['artists'][0]['id']
            artist = sp.artist(artist_id)

            tracks[track['id']] = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'artist_followers': artist['followers']['total'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'explicit': track['explicit'],
                'album_type': track['album']['album_type'],
                'release_date': track['album']['release_date']
            }

    print("collected:", len(tracks))

df = pd.DataFrame.from_dict(tracks, orient='index')
df.to_csv('tracks.csv', index=False)
