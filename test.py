import unittest
from unittest.mock import patch
import musixmatch_module as mm

class TestLyrics(unittest.TestCase):

    def test_auth(self):

        expected_return = {'base_url': 'http://api.genius.com', 'headers': {'Authorization': 'Bearer yeehaw'}}

        with unittest.mock.patch.dict('os.environ', {'GENIUS_CLIENT_ACCESS_TOKEN':'yeehaw'}):
            genius_auth = mm.genius_api_auth()

        self.assertEqual(genius_auth, expected_return)


if __name__ == '__main__':
    unittest.main()