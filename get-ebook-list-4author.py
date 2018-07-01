import requests
from bs4 import BeautifulSoup
import re
import os.path
import string

## Script Number 2
# script takes in author list and create subfolders for each author
# with a single file inside with all ebook links for that author

main_filename = "ebook-list-authors.txt";

fh_in = open(main_filename,"r");
old_elem = "hello";
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

num_lines = sum(1 for line in open(main_filename));
x = 0;

for line in fh_in:
    pagenum = 1; #pagenum starts with 1 and is incremented if a span with "Pagina 1 di 12" is found and assigned 12, see line 54
    x = x + 1; # x is the line number (to track number of authors out of the total ones scraped)
    N = 1;
    name = line.split("tag")[1].strip("/").strip(); #author's name from url
    author_path = "authors/"+name;
    print("\n >> m of N: " + str(x) + " of "+ str(num_lines) + ", AUTHOR: " + name ,end=" ");
    if not (os.path.isdir(author_path)):
        os.mkdir(author_path); #make dir if not existing
    else: continue; #if exist skip
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
                    if (((last4 != "-pdf") & (last4 != "epub") & (last4 != "mobi")) | (href == old_elem)):
                            continue;
                    fh_out.write(href + "\n");
                    old_elem = href;
                    c = c + 1;
        if (pagenum == 1):
            try:
                #i cant know prior to this line if the document has this span or not
                #so try to get it, if it's there overwrite N with max number of pages
                N = int(soup.findAll("span", {"class": "pages"})[0].text.split("di")[1]);
            except:
                print("[!] cannot find more than 1 page. break.")
                break; #otherwise it means it's only one page, so break.
        pagenum = pagenum + 1;
    print("added " + str(c) + " books to author");
    fh_out.close();
fh_in.close();
