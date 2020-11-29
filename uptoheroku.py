import time
import os
import typing
import spotipy
import telebot
from spotipy.oauth2 import SpotifyOAuth
from telethon.sync import TelegramClient
from telethon import functions, types

bot = telebot.TeleBot(os.environ["bot_token"])

admin_id = os.environ["telegram_id"]

api_id = os.environ["api_id"]
api_hash = os.environ["api_hash"]

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Send me file pls")

@bot.message_handler(content_types=['document'])
def dowfile(message):
	if message.chat.id == admin_id:
	    chat_id = message.chat.id
	    file_info = bot.get_file(message.document.file_id)
	    downloaded_file = bot.download_file(file_info.file_path)

	    download = download_dict[message.chat.id]
	    bot.send_message(message.chat.id, "Thx")

		spotify = spotipy.Spotify(
			auth_manager=SpotifyOAuth(
				scope="user-read-currently-playing",
				client_id=os.environ["client_id"],
				client_secret=os.environ["client_secret"],
				redirect_uri=os.environ["redirect_uri"],
				username=os.environ["spotiusername"],
			)
		)


		current_playing = typing.List[typing.Union[str, str, str]]

		def update_status(_current_playing):
			current = spotify.current_user_playing_track()
			if not current is None:

				track = current["item"]["name"]
				album = current["item"]["album"]["name"]
				artist = current["item"]["artists"][0]["name"]

				if _current_playing != [track, album, artist]:
					muzon = "🎧 Spotify | " + artist + " - " + track
					
					with TelegramClient('anon', api_id, api_hash) as client:
						result = client(functions.account.UpdateProfileRequest(about=muzon))
					print(f"🎧 Spotify | {track} - {artist}")

				return [track, album, artist]

			if not _current_playing is None:
				with TelegramClient('anon', api_id, api_hash) as client:
					result = client(functions.account.UpdateProfileRequest(about=os.environ["def_status"]))
			
			return
	else:
		bot.send_message(message.chat.id, "Error id!")
		
if __name__ == '__main__':
	try:
		while True:
			bot.polling(none_stop=True)
			# print("Получаю обновления")
			current_playing = update_status(current_playing)
			time.sleep(3)

	except Exception as e:
		print(e)
