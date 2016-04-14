#!/usr/bin/env python
import argparse
import requests
import subprocess
from lxml import html


parser = argparse.ArgumentParser(help="Download Fshare with given Link and Premium Account. Author: Tu Do Anh")
parser.add_argument("link", help="Fshare link", type=str)
args = parser.parse_args()


# Premium Accout Info
email = "Your Email Here"
password = "Your Password Here"


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
    data = {"LoginForm[email]" : email, "LoginForm[password]" : password, "fs_csrf" : token}
    download = {'fs_csrf':token, "DownloadForm[pwd]":"", "DownloadForm[linkcode]":file_id, "ajax":"download-form", "undefined":"undefined"}
    headers = {"x-requested-with" : "XMLHttpRequest", 'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36", "content-type" : "application/x-www-form-urlencoded; charset=UTF-8", "referer":url}
    return {"token": token, "url":url, "file_name":file_name, "cookie":cookie, "data":data, "download":download, "headers":headers}


# Get download link
def get_link(k):
    s.post("https://www.fshare.vn/login", cookies=k["cookie"], data=k["data"])
    s.post("https://www.fshare.vn/download/ClearSession", headers=k['headers'], data={"fs_csrf": k['token']})
    s.get(k['url'])
    return s.post("https://www.fshare.vn/download/get", data=k["download"], headers=k["headers"]).json()


# Run the script
def main():
    file_id = get_id(args.link)
    k = get_data(file_id)
    l = get_link(k)
    if l.has_key('url'):
        return l['url']
    else:
        main()


if __name__ == "__main__":
    s = requests.Session()
    dl = main()
    print dl
    subprocess.call(["wget", dl])
