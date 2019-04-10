import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def search_song(base_url, headers, search_term):

	search_result_list = []

	for page in range(1, 6):
		search_url = base_url + "/search"
		params = {'q': search_term, 'page': str(page)}

		response = requests.get(search_url, params=params, headers=headers)

		body = json.loads(response.text)

		for i in body['response']['hits']:

			artist = i['result']['primary_artist']['name']
			song = i['result']['title']
			song_api_path = i['result']['api_path']

			# print("\n {} :: {} :: {}".format(artist, song, song_api_path))
			search_result_list.append([artist, song, song_api_path])

	return search_result_list


def song_comparison(artist_list, search_list):

	all_artists = []
	for lst in artist_list:
		all_artists += lst
	all_artists_sanitized = [next(iter(artist.values())).lower() for artist in all_artists]

	song_pick = []
	for song_info in search_list:
		if song_info[0].lower() in all_artists_sanitized:
			song_pick.append(song_info)

	return song_pick


# code borrowed from https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
def find_lyrics(base_url, headers, song_api_path):

	search_url = base_url + song_api_path
	response = requests.get(search_url, headers=headers)
	body = json.loads(response.text)

	lyrics_path = body['response']['song']['path']

	search_url = "http://genius.com" + lyrics_path
	print(search_url)

	response = requests.get(search_url, headers=headers)

	html = BeautifulSoup(response.text, "html.parser")
	[h.extract() for h in html('script')]
	dirty_lyrics = html.find('div', class_ ='lyrics').get_text()  # updated css where the lyrics are based in HTML

	lyric_list = dirty_lyrics.split("\n")
	return lyric_list

def terminal_input():
	print("\n * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ *")
	search_term = input("Enter song: ")
	print("* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ * \n")

	return search_term


def genius_api_auth():

	CLIENT_ACCESS_TOKEN = os.getenv('GENIUS_CLIENT_ACCESS_TOKEN')
	base_url = "http://api.genius.com"
	headers = {'Authorization': 'Bearer {}'.format(CLIENT_ACCESS_TOKEN)}

	return {'base_url': base_url, 'headers': headers}


def get_lyrics(search_term):
	genius_auth = genius_api_auth()

	song_results = search_song(genius_auth['base_url'], genius_auth['headers'], search_term)

	song_api_path = song_results[0]

	sanitized_lyrics = find_lyrics(genius_auth['base_url'], genius_auth['headers'], song_api_path[2])

	return sanitized_lyrics


if __name__ == '__main__':
	search_term = terminal_input()
	lyrics = get_lyrics(search_term)

	[print(lyric) for lyric in lyrics]

