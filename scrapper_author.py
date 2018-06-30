import requests
from bs4 import BeautifulSoup
import re
import os.path
import time


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

name = input("Enter author name: ");

path = "authors/" + name + "/";

elist = open(path + "ebook-list-2.txt","r");

for url in elist:
    ext = url.split("-")[-1].strip();
    if (ext != "mobi/"):
        continue;
    url = url.strip() + '2/';
    try:
        response = requests.get(url, headers=headers)
    except:
        print("error, could not retrive, continue.");
        continue;
    html = response.content;
    soup = BeautifulSoup(html, 'html.parser');

    try:
        download = soup.find_all("h2")[1]("a")[0].get("href").split("url=")[-1];
        print("found dwnlg for url: " + url);
    except:
        print("error: exeption: " + url);
        continue;

    response = requests.get(download, headers=headers);
    fname = path + download.split("/")[-1];
    print("saving " + fname + "...",end="");

    if os.path.isfile(fname):
        print("file already exists, continue.");
        continue

    file = open(fname.replace("-20", " "),"wb")
    file.write(response.content);
    file.close();
    print("new! saved");
    time.sleep(1);
