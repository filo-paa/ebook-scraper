import requests
from bs4 import BeautifulSoup
import re
import os.path


elist = open("ebook_list.txt","r");

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

for url in elist:
    
    url = url.strip() + '2/';
    
    response = requests.get(url, headers=headers)
    
    html = response.content;
    
    soup = BeautifulSoup(html, 'html.parser');

    try:
        download = soup.find_all("h2")[1]("a")[0].get("href").split("url=")[1];
        print("found dwnlg for url: " + url);
    except:
        print("error: exeption: " + url);
        continue;
    
    response = requests.get(download, headers=headers);

    fname = "dwnlg/"+download.split("/")[-1];
    
            
    print("saving " + fname + "...",end="");

    if os.path.isfile(fname):
        print("exists");
        continue
    
    file = open(fname,"wb")

    file.write(response.content);

    file.close();

    print("new! saved");
    
