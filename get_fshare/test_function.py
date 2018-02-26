import unittest
from get_fshare import FS


class FshareTest(unittest.TestCase):
    def setUp(self):
        self.bot = FS('utvyoxrk@emlpro.com', 'Tu0703$$')
        self.bot.login()
        self.file_url = 'https://www.fshare.vn/file/TJ1WSZWAKT'
        self.folder_url = 'https://www.fshare.vn/folder/THFVWDY4YT'
        self.dead_url = 'https://www.fshare.vn/file/775S9PFR9RRB'
        self.media_id = 'TJ1WSZWAKT'

    def test_login(self):
        r = self.bot.s.get('https://www.fshare.vn/')
        assert r.text.find('Đăng nhập') == -1

    def test_get_file_name(self):
        name = self.bot.get_file_name(self.file_url)
        assert name == 'Silicon.Valley.S01.720p.HDTV.E001-PhimVIPvn.net.mp4'

    def test_get_file_size(self):
        size = self.bot.get_file_size(self.file_url)
        assert size == '251.5 MB'

    def test_get_folder_name(self):
        folder_name = self.bot.get_folder_name(self.folder_url)
        assert folder_name == "Silicon.Valley.S01.720p.HDTV"

    def test_is_exist(self):
        ok_status = self.bot.is_exist(self.file_url)
        dead_status = self.bot.is_exist(self.dead_url)
        self.assertTrue(ok_status)
        self.assertFalse(dead_status)

    def test_get_link(self):
        link = self.bot.get_link(self.file_url)
        assert link != ''

    def test_extract_links(self):
        links = self.bot.extract_links(self.folder_url)
        assert len(links) == 6

    def test_get_media_link(self):
        link = self.bot.get_media_link(self.media_id)
        assert isinstance(link, str) is True

    def tearDown(self):
        self.bot.log_out()
