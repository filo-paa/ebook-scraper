import requests
from bs4 import BeautifulSoup
import re
import os.path
import string

#script takes in author list and create subfolder for each actor with each a single file with ebook list of link
fh_in = open("ebook-list-authors.txt","r");

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

for line in fh_in:
    pagenum = 1;
    N = 1;
    name = line.split("tag")[1].strip("/").strip();
    author_path = "authors/"+name;
    print("\n >> AUTHOR: " + name ,end=" ");
    if not (os.path.isdir(author_path)):
        os.mkdir(author_path);
    else: continue;
    fh_out = open(author_path + "/ebook-list.txt","w");
    c = 0;
    while(pagenum<=N):
        name = line.split("tag")[1];
        url = line.strip() + "page/" + str(pagenum);
        try:
            response = requests.get(url, headers=headers)
        except:
            print("could not retrive, break");
            break;
        html = response.content;
        soup = BeautifulSoup(html,'html5lib');
        #restrict research here / parse actor page better
        mydiv = soup.find_all("div",{"class":["td-pb-span8","td-main-content"]})[0];
        for link in mydiv.find_all("a"):
                    href = link.get("href");
                    last4 = href[-5:-1];
                    if ((last4 != "-pdf") & (last4 != "epub") & (last4 != "mobi")):
                            continue;
                    print("adding " + href);
                    fh_out.write(href + "\n");
                    c = c + 1;
        if (pagenum == 1):
            try:
                N = int(soup.findAll("span", {"class": "pages"})[0].text.split("di")[1]);
            except:
                print("[!] cannot find more than 1 page. break.")
                break;
        pagenum = pagenum + 1;
    print("added " + str(c) + " books to author");
    fh_out.close();
fh_in.close();
