#album cover = colors
#popularity = brightness
#album type = # of layers (single - 1, album - 3)
#duration = # of shapes
#explicit = circle (false) vs square (true)
#years since released = # of lines (>20 is black, <20 is white)
#artist followers = stroke thickness

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from sklearn.cluster import KMeans
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
      client_id=#,
      client_secret=#
    )
)
#get album colors
def colors(album_url):
    response = requests.get(album_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_ / 255.0
    return colors.tolist()

#get track info
def trackinfo(url):
    track = sp.track(url)
    artist = sp.artist(track["artists"][0]["id"])
    album_url = track["album"]["images"][0]["url"]
    album_colors = colors(album_url)
    release_date = pd.to_datetime(track["album"]["release_date"], errors="coerce")
    years_since = (pd.Timestamp.today() - release_date).days / 365.25
    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "popularity": track["popularity"],
        "duration": track["duration_ms"]/1000,
        "explicit": track["explicit"],
        "artist_followers": artist["followers"]["total"],
        "album_type": track["album"]["album_type"],
        "album_colors": album_colors,
        "years_since": years_since,
    }

#generate art
def art(song):
    #set features
    np.random.seed(len(song["name"]))
    num_shapes = int(song["duration"]) 
    num_layers = 1 if song["album_type"] == "single" else 3
    num_lines = int(song["years_since"])
    stroke = max(1, int(song["artist_followers"]/5000000)) #stroke is at least 1

    #set up canvas
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    #layers
    for layer in range(num_layers):
        #shape based on explicit, album colors, and popularity
        for shape in range(int(num_shapes/num_layers)):
            x = np.random.rand()*10
            y = np.random.rand()*10
            s = np.random.rand()
            color = np.array(song["album_colors"][np.random.randint(len(song["album_colors"]))])
            color = color * song["popularity"]/100
            if song["explicit"]:
                ax.add_patch(plt.Rectangle((x, y), s*2, s*2, color = color, alpha = 0.5))
            else: 
                ax.add_patch(plt.Circle((x, y), s, color = color, alpha = 0.5))
        
    #lines based on artist followers and years since
    for line in range(num_lines):
        x0 = np.random.rand() * 10
        x1 = np.random.rand() * 10
        y0 = np.random.rand() * 10
        y1 = np.random.rand() * 10
        color = (0, 0, 0) if song["years_since"]>20 else (1, 1, 1) 
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=stroke, alpha=0.5)

    plt.show()

#display
url = input("Enter spotify track URL: ")
art(trackinfo(url))




