#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import io
from lxml import html
import math
import ntpath
import os
import string
import requests


class FS:
    """
    Get link Fshare with your account. If you have VIP, you will get
    premium download link.
    """
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.s = requests.Session()
        self.login_url = "https://www.fshare.vn/site/login"
        self.user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/59.0.3071.115 Safari/537.36"
        )
        self.folder_api = (
            'https://www.fshare.vn/api/v3/files/'
            'folder?linkcode={}&sort=type,name'
        )
        self.file_url = 'https://www.fshare.vn/file/{}'
        self.media_api = (
            'https://www.fshare.vn/api/v3/files/'
            'download?dl_type=media&linkcode={}'
        )

    def get_token(self, response):
        """
        Get csrf token for POST requests.
        """
        tree = html.fromstring(response.content)
        try:
            token = tree.xpath('//*[@name="csrf-token"]')[0].get('content')
            return token
        except IndexError:
            raise Exception('No token for url {}'.format(response.url))
            pass

    def login(self):
        """
        Login to Fshare with given account info.
        """
        self.s.headers.update({'User-Agent': self.user_agent})
        r = self.s.get(self.login_url)
        token = self.get_token(r)
        cookies = r.cookies
        data = {
            '_csrf-app': token,
            'LoginForm[email]': self.email,
            'LoginForm[password]': self.password,
            'LoginForm[rememberMe]': 1,
        }
        self.s.post(self.login_url, cookies=cookies, data=data)
        r = self.s.get('https://www.fshare.vn/')

        tree = html.fromstring(r.content)
        if tree.xpath('//*[@href="/signup"]'):
            raise Exception('Login failed. Please check your email & password')
        else:
            pass

    def get_media_link(self, media_id):
        """
        Get direct link for video file from your storage account.
        """
        url = self.media_api.format(media_id)

        authorization_code = self.s.cookies.get_dict()['fshare-app']
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.8,vi;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.fshare.vn/file/manager',
            'Connection': 'keep-alive',
            'Host': 'www.fshare.vn',
            'Authorization': 'Bearer {}'.format(authorization_code)
        }

        r = self.s.get(url, headers=headers)

        try:
            link = r.json()
            return link
        except json.decoder.JSONDecodeError:
            print(r.status_code, r.text, self.movie_token, data)
            raise Exception('Get media link failed.')

    def get_link(self, url):
        """
        Get Fshare download link from given url.
        """
        if self.is_exist(url):
            r = self.s.get(url, allow_redirects=False)
            if r.status_code == 200:
                token = self.get_token(r)
                file_id = url.split("/")[-1]
                dl_data = {
                    '_csrf-app': token,
                    "fcode5": "",
                    "linkcode": file_id,
                    "withFcode5": 0,
                }
                r = self.s.post("https://www.fshare.vn/download/get",
                                data=dl_data)
                try:
                    link = r.json()
                    return link.get('url')
                except json.decoder.JSONDecodeError:
                    raise Exception('Get link failed.')
            else:  # In case auto download is enable in account setting
                return r.headers['Location']
        else:
            return ''

    def extract_links(self, folder_url):
        """
        Get all links in Fshare folder.
        Return list of all item with info of each.
        """
        folder_id = folder_url.split('/')[-1]
        data = self.s.get(self.folder_api.format(folder_id)).json()

        folder_data = [
            {
                'file_name': d['name'],
                'file_url': self.file_url.format(d['linkcode']),
                'file_size': d['size']
            }
            for d in data['items']
        ]
        return folder_data

    def get_file_name(self, url):
        """
        Strip extra space out of file's name
        """
        r = requests.get(url)
        tree = html.fromstring(r.content)
        file_name = tree.xpath(
            '//*[@property="og:title"]'
        )[0].get('content').split(' - Fshare')[0]
        return file_name

    def get_file_size(self, url):
        """
        Get file size. If not have, return Unknow
        """
        r = requests.get(url)
        tree = html.fromstring(r.content)
        file_size = tree.xpath('//*[@class="size"]/text()')
        if file_size:
            return file_size[1].strip()
        else:
            return 'Unknown'

    def get_folder_name(self, folder_url):
        """
        Get folder name (title)
        """
        r = self.s.get(folder_url)
        tree = html.fromstring(r.content)
        title = tree.xpath('//title/text()')
        if title:
            return title[0].strip('Fshare - ')
        else:
            return r.url

    def is_alive(self, url):
        """
        Check if link is alive.
        """
        r = self.s.head(url, allow_redirects=True)
        if r.status_code == 200:
            return True
        else:
            return False

    def is_exist(self, url):
        '''
        Check if file is exist or not.
        If exist, return True. Else, return False
        '''
        r = self.s.get(url, allow_redirects=False)
        if r.status_code == 200:
            tree = html.fromstring(r.content)
            title = tree.xpath('//title/text()')[0]
            if title == 'Not Found - Fshare':
                return False
            else:
                return True
        else:  # In case auto download is enable in account setting
            return True

    def log_out(self):
        self.s.get('https://www.fshare.vn/site/logout')

    def upload_file(self, file_path, secured=0):
        """
        Upload file to Fshare
        """
        UPLOAD_URL = 'https://www.fshare.vn/api/session/upload'
        file_name = ntpath.basename(file_path)
        file_size = str(os.path.getsize(file_path))
        try:
            data = io.open(file_path, 'rb', buffering=25000000)
        except FileNotFoundError:
            raise Exception('File does not exist!')

        r1 = self.s.get('https://www.fshare.vn/home?upload=1')
        tree = html.fromstring(r1.content)
        token_data = tree.xpath('//*[@class="pull-left breadscum"]')
        if token_data:
            token = token_data[0].get('data-token')
        else:
            raise Exception('Can not get token')

        payload = {'SESSID': dict(self.s.cookies).get('session_id'),
                   'name': file_name,
                   'path': '/',
                   'secured': secured,
                   'size': file_size,
                   'token': token}

        res = self.s.post(UPLOAD_URL, data=json.dumps(payload))
        body = res.json()

        if body.get('code') != 200:
            raise Exception('Initial handshake errors %r', body)

        location = body['location']

        # OPTIONS for chunk upload configuration
        max_chunk_size = 25000000
        chunk_total = math.ceil(int(file_size)/max_chunk_size)

        for i in range(chunk_total):
            chunk_number = i + 1
            sent = last_index = i * max_chunk_size
            remaining = int(file_size) - sent
            if remaining < max_chunk_size:
                current_chunk = remaining
            else:
                current_chunk = max_chunk_size

            next_index = last_index + current_chunk

            chunk_params = {
                'flowChunkNumber': chunk_number,
                'flowChunkSize': max_chunk_size,
                'flowCurrentChunkSize': current_chunk,
                'flowTotalSize': file_size,
                'flowIdentifier': '{0}-{1}'.format(current_chunk, file_name),
                'flowFilename': file_name,
                'flowRelativePath': file_name,
                'flowTotalChunks': chunk_total
            }

            res = self.s.options(location, params=chunk_params)

            # POST upload data
            headers = {
                'Host': 'up.fshare.vn',
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.fshare.vn/transfer',
                'Content-Range': 'bytes {0}-{1}/{2}'.format(
                    last_index,
                    next_index - 1,
                    file_size),
                'Content-Length': str(current_chunk),
                'Origin': 'https://www.fshare.vn',
                'DNT': '1',
                'Connection': 'keep-alive'
            }
            res = self.s.post(location,
                              params=chunk_params,
                              headers=headers,
                              data=data.read(max_chunk_size))
            try:
                if res.json():
                    return res.json()
                pass
            except Exception:
                pass
        data.close()


class FSAPI:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = ''
        self.s = requests.Session()
        self.s.headers['User-Agent'] = 'okhttp/3.6.0'

    def login(self):
        r = self.s.post(
            'https://api.fshare.vn/api/user/login',
            json={
                'user_email': self.email,
                'password': self.password,
                'app_key': "L2S7R6ZMagggC5wWkQhX2+aDi467PPuftWUMRFSn"
            }
        )

        data = r.json()
        self.token = data['token']
        cookie = data['session_id']
        self.s.cookies.set('session_id', cookie)
        return data

    def check_valid(self, url):
        url = url.strip()
        if not url.startswith('https://www.fshare.vn/'):
            raise Exception("Must be Fshare url")
        return url

    def download(self, url):
        url = self.check_valid(url)
        r = self.s.post(
            'https://api.fshare.vn/api/session/download',
            json={
                'token': self.token,
                'url': url
            }
        )

        if r.status_code != 200:
            raise Exception("Link is dead")

        data = r.json()
        link = data['location']
        return link

    def get_folder_urls(self, url, page=0, limit=60):
        url = self.check_valid(url)
        r = self.s.post(
            'https://api.fshare.vn/api/fileops/getFolderList',
            json={
                'token': self.token,
                'url': url,
                'dirOnly': 0,
                'pageIndex': page,
                'limit': limit
            }
        )
        data = r.json()
        return data

    def get_home_folders(self):
        r = self.s.get('https://api.fshare.vn/api/fileops/list?pageIndex=0&dirOnly=0&limit=60')
        return r.json()

    def get_file_info(self, url):
        url = self.check_valid(url)
        r = self.s.post(
            'https://api.fshare.vn/api/fileops/get',
            json={
                'token': self.token,
                'url': url,
            }
        )
        return r.json()

    def upload(self, local_path, remote_path, secured=1):
        import os
        import io
        import ntpath
        import unidecode
        file_name = ntpath.basename(local_path)
        def format_filename(s):
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            filename = ''.join(c for c in s if c in valid_chars)
            return filename
        file_name = format_filename(unidecode.unidecode(file_name))
        file_size = str(os.path.getsize(local_path))
        try:
            data = io.open(local_path, 'rb', buffering=25000000)
        except FileNotFoundError:
            raise Exception('File does not exist!')

        r = self.s.post(
            'https://api.fshare.vn/api/session/upload',
            json={
                'token': self.token,
                'name': file_name,
                'path': remote_path,
                'secured': 1,
                'size': file_size
            }
        )
        print(self.token, local_path, remote_path)
        print(r.json())

        location = r.json()['location']

        # OPTIONS for chunk upload configuration
        max_chunk_size = 25000000
        chunk_total = math.ceil(int(file_size)/max_chunk_size)

        for i in range(chunk_total):
            chunk_number = i + 1
            sent = last_index = i * max_chunk_size
            remaining = int(file_size) - sent
            if remaining < max_chunk_size:
                current_chunk = remaining
            else:
                current_chunk = max_chunk_size

            next_index = last_index + current_chunk

            chunk_params = {
                'flowChunkNumber': chunk_number,
                'flowChunkSize': max_chunk_size,
                'flowCurrentChunkSize': current_chunk,
                'flowTotalSize': file_size,
                'flowIdentifier': '{0}-{1}'.format(current_chunk, file_name),
                'flowFilename': file_name,
                'flowRelativePath': file_name,
                'flowTotalChunks': chunk_total
            }

            res = self.s.options(location, params=chunk_params)
            # POST upload data
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Range': 'bytes {0}-{1}/{2}'.format(
                    last_index,
                    next_index - 1,
                    file_size),
                'DNT': '1',
                'Connection': 'keep-alive'
            }
            res = self.s.post(location,
                              params=chunk_params,
                              headers=headers,
                              data=data.read(max_chunk_size))
            try:
                if res.json():
                    return res.json()
                pass
            except Exception:
                pass
        data.close()

