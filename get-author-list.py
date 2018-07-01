import requests
from bs4 import BeautifulSoup
import re
import os.path
import string

fh = open("ebook-list-authors.txt","a");
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
N = 10;
old_elem = "hello";

for n in range(1,N+1):
    print("fetching page " + str(n),end=" ");
    main = "https://libri.me/lista-tutti-gli-autori-numero-ebook/?page29534=" + str(n);
    try:
        response = requests.get(main, headers=headers)
    except:
        print("error, could not retrive");
        continue;
    html = response.content;
    soup = BeautifulSoup(html,"html5lib");
    authors = soup.find_all("div",{"id":"w4pl-inner-29534"})[0].find_all("a");
    c = 0;
    for link in authors:
        href = link.get("href");
        if ("tag" not in href):
            continue;
        fh.write(href + "\n");
        c = c + 1;
    print("retrived " + str(c) + " authors for this page.");
