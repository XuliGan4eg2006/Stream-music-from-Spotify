import time
import typing
import spotipy
import config
from spotipy.oauth2 import SpotifyOAuth
from telethon.sync import TelegramClient
from telethon import functions, types

api_id = config.api_id
api_hash = config.api_hash

spotify = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		scope="user-read-currently-playing",
		client_id=config.client_id,
		client_secret=config.client_secret,
		redirect_uri=config.redirect_uri,
		username=config.spotiusername,
	)
)


current_playing = typing.List[typing.Union[str, str, str]]

def update_status(_current_playing):
	current = spotify.current_user_playing_track()
	if current:

		track = current["item"]["name"]
		album = current["item"]["album"]["name"]
		artist = current["item"]["artists"][0]["name"]

		if _current_playing != [track, album, artist]:
			muzon = "🎧 Spotify | " + artist + " - " + track
			
			with TelegramClient('anon', api_id, api_hash) as client:
				result = client(functions.account.UpdateProfileRequest(about=muzon))
			print(f"🎧 Spotify | {track} - {artist}")

	if not _current_playing is None:
		print("None is playing")
		
if __name__ == '__main__':
	try:
		while True:
			# print("Получаю обновления")
			current_playing = update_status(current_playing)
			time.sleep(8)

	except Exception as e:
		print(e)
