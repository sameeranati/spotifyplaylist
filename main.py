from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


date=input("which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year=date.split('-')
yy=year[0]
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')

song_names_spans = soup.select('li ul li h3')
song_names = [song.getText().strip() for song in song_names_spans]
# print(song_names)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id="5c90e2c76c224e0f9befad16d677ceae",
        client_secret="6010d2d86b70408b84ba675d8f488818",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{yy}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
# print(song_uris)
playlist=sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)