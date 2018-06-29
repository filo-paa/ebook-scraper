import requests
from bs4 import BeautifulSoup
import re
import os.path
import string

letters = list(['l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']);
fh = open("ebook-list.txt","a");

for letter in letters:

    pagenum = 1;
    N = 1;

    while(pagenum<=N):
        print("let: "+letter+", page n: " + str(pagenum) + " of " + str(N));
        pagestart = "https://libri.me/category/" + letter + "/page/" + str(pagenum) + "/";
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        try:
            response = requests.get(pagestart, headers=headers)
        except:
            pagenum = pagenum + 1;
            continue;
        
        html = response.content;
        soup = BeautifulSoup(html, 'html.parser');
        if (pagenum == 1):
            try:
                N = int(soup.findAll("span", {"class": "pages"})[0].text.split("di")[1]);
            except:
                pass;
        for link in soup.find_all("a"):
                    href = link.get("href");
                    last4 = href[-5:-1];
                    if ((last4 != "-pdf") & (last4 != "epub") & (last4 != "mobi")):
                            continue;
                    fh.write(href + "\n");
        pagenum = pagenum + 1;
    
fh.close();
