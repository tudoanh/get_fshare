import unittest
from get_fshare import FSAPI


class FshareAPITest(unittest.TestCase):
    def setUp(self):
        self.bot = FSAPI('utvyoxrk@emlpro.com', 'ahihihi')
        self.file_url = 'https://www.fshare.vn/file/TJ1WSZWAKT'
        self.folder_url = 'https://www.fshare.vn/folder/THFVWDY4YT'
        self.dead_url = 'https://www.fshare.vn/file/775S9PFR9RRB'
        self.media_id = 'TJ1WSZWAKT'
        self.invalid_url = 'https://google.com.vn/'

    def test_login(self):
        data = self.bot.login()
        self.assertIn('token', data)
        self.assertIn('session_id', data)

    def test_check_valid(self):
        with self.assertRaises(Exception) as context:
            self.bot.check_valid(self.invalid_url)

        self.assertTrue("Must be Fshare url" in str(context.exception))

        self.assertEqual(self.bot.check_valid(self.file_url), self.file_url)
