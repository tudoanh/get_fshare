#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import requests
from lxml import html


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
                           "Chrome/49.0.2623.108 Safari/537.36")

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

    def get_link(self, url):
        """
        Get Fshare download link from given url.
        """
        if self.is_exist(url):
            r = self.s.get(url)
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
        r = self.s.head(url)
        if r.status_code == 200:
            return True
        else:
            return False

    def is_exist(self, url):
        '''
        Check if file is exist or not.
        If exist, return True. Else, return False
        '''
        r = self.s.get(url)
        tree = html.fromstring(r.content)
        if tree.xpath('//*[@class="text-danger margin-bottom-15"]'):
            return False
        else:
            return True
