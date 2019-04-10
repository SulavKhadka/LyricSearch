
import spotipy
import user_auth_module as user_auth


def get_top_artists(spotify, token, username):
	if token:
		ranges = ['short_term', 'medium_term', 'long_term']
		artists = []
		for range in ranges:
			results = spotify.current_user_top_artists(time_range=range, limit=50)
			temp_list = []
			for i, item in enumerate(results['items']):
				temp_list.append({i: item['name']})
			artists.append(temp_list)

		return artists

	else:
		error = "Token Error"
		print("Can't get token for {}".format(username))
		return error


def print_top_artists(ranges):
	for range in ranges:
		print("range:", range)
		results = spotify.current_user_top_artists(time_range=range, limit=50)
		for i, item in enumerate(results['items']):
			print(i, item['name'])
		print()
		input("hi")


def search_track(spotify):
	print("\n * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ *")
	query = input("Enter song: ")
	print("* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ * \n")

	results = spotify.search(q=query, type='track')

	for i in results['tracks']['items']:
		#print(i['external_urls'])
		song = i['name']
		artist = i['artists'][0]['name']
		album_art = i['album']['images']
		song_link = i['external_urls']

		print(song.upper(), "::", artist.upper())
		print(song_link)


def current_song(spotify, token, username):

	song = spotify.currently_playing()
	print(song)


def get_auth(username, scope):
	token = user_auth.auth(scope, username)
	spotify = spotipy.Spotify(auth=token)
	spotify.trace = False

	return {'spotify': spotify, 'token': token}



def main():

	username = 'sulavkhadka'
	spotify_auth = get_auth(username, 'user-top-read')

	artist_list = get_top_artists(spotify_auth['spotify'], spotify_auth['token'], username)


	# token = user_auth.auth('user-read-currently-playing', username)
	# spotify = spotipy.Spotify(auth=token)
	# spotify.trace = False
	#
	# current_song(spotify, token, username)

main()