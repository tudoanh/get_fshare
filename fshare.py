#!/usr/bin/env python
import requests
from lxml import html


# Get file id from link
def get_id(link):
    return link.split("/")[-1]


# Get data for requests
def get_data(file_id):
    url = "https://www.fshare.vn/file/{0}".format(file_id)
    r = s.get(url)
    tree = html.fromstring(r.content)
    file_name = "".join(tree.xpath('//*[@class="margin-bottom-15"]/text()')).strip()
    cookie_id = r.cookies.values()[0]
    token = tree.xpath('//*[@name="fs_csrf"]')[0].value
    cookie = {"session_id" : cookie_id}
    data = {"LoginForm[email]" : "Your Email", "LoginForm[password]" : "Your password", "fs_csrf" : token}
    download = {'fs_csrf':token, "DownloadForm[pwd]":"", "DownloadForm[linkcode]":file_id, "ajax":"download-form", "undefined":"undefined"}
    headers = {"x-requested-with" : "XMLHttpRequest", 'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36", "content-type" : "application/x-www-form-urlencoded; charset=UTF-8", "referer":url}
    return {"url":url, "file_name":file_name, "cookie":cookie, "data":data, "download":download, "headers":headers}


def get_link(k):
    s.post("https://www.fshare.vn/login", cookies=k["cookie"], data=k["data"])
    return s.post("https://www.fshare.vn/download/get", data=k["download"], headers=k["headers"]).json()


if __name__ == "__main__":
    # Open file contain Fshare link, one line each link.
    with open('link.txt', 'r') as f:
        links = f.readlines()

    for link in links:
        s = requests.Session()
        file_id = get_id(link.strip())
        k = get_data(file_id)
        if get_link(k).has_key('url'):
            print getlink(k)['url']
        else:
            print "Failed"

