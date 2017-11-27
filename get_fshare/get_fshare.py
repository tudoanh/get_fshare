#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import io
from lxml import html
import math
import ntpath
import os
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
        self.login_url = "https://www.fshare.vn/login"
        self.user_agent = ("Mozilla/5.0 (X11; Linux x86_64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/59.0.3071.115 Safari/537.36")

    def get_token(self, response):
        """
        Get csrf token for POST requests.
        """
        tree = html.fromstring(response.content)
        try:
            token = tree.xpath('//*[@name="fs_csrf"]')[0].value
            return token
        except IndexError:
            raise Exception('No token for url {}'.format(response.url))
            pass

    def get_movie_token(self):
        """
        Get data token of homepage.
        """
        response = self.s.get('https://www.fshare.vn/home')
        tree = html.fromstring(response.content)
        try:
            token = tree.xpath(
                '//*[@class="pull-left breadscum"]')[0].get('data-token')
            self.movie_token = token
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
        data = {'fs_csrf': token,
                'LoginForm[email]': self.email,
                'LoginForm[password]': self.password,
                'LoginForm[rememberMe]': 1,
                'LoginForm[checkloginpopup]': 0,
                'yt0': u'Đăng nhập'}
        self.s.post(self.login_url, cookies=cookies, data=data)
        r = self.s.get('https://www.fshare.vn/')

        tree = html.fromstring(r.content)
        if tree.xpath('//*[@href="/signup"]'):
            raise Exception('Login failed. Please check your email & password')
        else:
            pass

    def get_movie(self, movie_id):
        """
        Get direct link for video file from your storage account.
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8,vi;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.fshare.vn/home',
            'Content-Length': '81',
            'Origin': 'https://www.fshare.vn',
            'Connection': 'keep-alive',
            'Host': 'www.fshare.vn'
        }

        token = self.movie_token
        data = {'token': token, 'linkcode': movie_id}

        r = self.s.post('https://www.fshare.vn/api/fileops/watch',
                        json=data,
                        headers=headers)

        try:
            link = r.json()
            return link
        except json.decoder.JSONDecodeError:
            print(r.status_code, r.text, self.movie_token, data)
            raise Exception('Get link failed.')

    def get_link(self, url):
        """
        Get Fshare download link from given url.
        """
        if self.is_exist(url):
            r = self.s.get(url, allow_redirects=False)
            if r.status_code == 200:
                token = self.get_token(r)
                file_id = url.split("/")[-1]
                dl_data = {'fs_csrf': token,
                           "DownloadForm[pwd]": "",
                           "DownloadForm[linkcode]": file_id,
                           "ajax": "download-form",
                           "undefined": "undefined"}
                r = self.s.post("https://www.fshare.vn/download/get",
                                data=dl_data)
                try:
                    link = r.json()
                    return link.get('url')
                except json.decoder.JSONDecodeError:
                    raise Exception('Get link failed.')
            else: # Case auto download set True in Fshare account setting
                return r.headers['Location']
        else:
            return ''

    def extract_links(self, folder_url):
        """
        Get all links in Fshare folder.
        Return list of all item with info of each.
        """
        r = self.s.get(folder_url)
        tree = html.fromstring(r.content)
        links = tree.xpath('//*[@class="filename"]/@href')
        names = tree.xpath('//*[@class="filename"]/@title')
        sizes = tree.xpath(
            '//*[@class="pull-left file_size align-right"]/text()')

        data = list(zip(names, links, sizes))
        folder_data = [
            {
                'file_name': d[0],
                'file_url': d[1],
                'file_size': d[2]
            }
            for d in data
        ]
        return folder_data

    def get_file_name(self, url):
        """
        Strip extra space out of file's name
        """
        r = self.s.get(url)
        tree = html.fromstring(r.content)
        file_name = "".join(tree.xpath(
                            '//*[@class="margin-bottom-15"]/text()')).strip()
        return file_name

    def get_file_size(self, url):
        """
        Get file size. If not have, return Unknow
        """
        r = self.s.get(url)
        tree = html.fromstring(r.content)
        loader = tree.xpath(
            '//*[@class="fa fa-hdd-o"]/following-sibling::text()')
        if loader:
            return loader[0].strip()
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
            if tree.xpath('//*[@class="text-danger margin-bottom-15"]'):
                return False
            else:
                return True
        else: # Case auto download set True in Fshare account setting
            return True

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
