import sys
import spotipy.util as util


def auth(scope, username):
	import os
	from json.decoder import JSONDecodeError

	try:
		token = util.prompt_for_user_token(username, scope, client_id='befc8027f374443e96b445ce281dc09a',
		                                   client_secret='a42fadde26f144a5af8fd0c40ec05bd0',
		                                   redirect_uri='http://localhost/')

	except (AttributeError, JSONDecodeError):
		os.remove(f".cache-{username}")
		token = util.prompt_for_user_token(username, scope, client_id='befc8027f374443e96b445ce281dc09a',
		                                   client_secret='a42fadde26f144a5af8fd0c40ec05bd0',
		                                   redirect_uri='http://localhost/')

	return token


if __name__ == "__main__":
	if len(sys.argv) > 2:
		scope = sys.argv[1]
		username = sys.argv[2]
	else:
		print("Usage: %s scope username" % (sys.argv[0],))
		sys.exit()

	auth(scope, username)
