import requests
from bs4 import BeautifulSoup
import re
import os.path
import string

## Script number 1
# This one will create a file "ebook-list-authors" scraping the site libri.me
# to collect all authors urls from page A to page B (every page has around 100 authors)

fh = open("ebook-list-authors.txt","a");
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
A = 1; #page start
B = 10; #page end
old_elem = "hello";

# scrap all pages from A to B

for n in range(A,B+1):
    print("fetching page " + str(n),end=" ");
    main = "https://libri.me/lista-tutti-gli-autori-numero-ebook/?page29534=" + str(n);
    try:
        response = requests.get(main, headers=headers)
    except:
        #if not found, skip
        print("error, could not retrive");
        continue;
    html = response.content;
    soup = BeautifulSoup(html,"html5lib"); #use sb4 to parse the html
    #IMPORTANT: find this particular div and whitin that get all the anchor tags
    authors = soup.find_all("div",{"id":"w4pl-inner-29534"})[0].find_all("a");
    c = 0;
    for link in authors:
        href = link.get("href");
        #this following if statement avoid inserting other than authors urls
        if ("tag" not in href): #must contain .../tag/...
            continue;
        fh.write(href + "\n");
        c = c + 1;
    print("retrived " + str(c) + " authors for this page.");
fh.close();
