import requests
from bs4 import BeautifulSoup
import re
import os.path
import time


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

folder_list = os.listdir("authors/");

skip = 1;

start_from = "agatha-christie";

for name in folder_list:

    if name == start_from:
        skip = 0;
    if skip:
        continue;
    
    path =  "authors/" + name + "/";
    elist = open(path + "ebook-list.txt","r");
    if not os.path.isfile(path + "ebook-list-downloaded.txt"):
            downloaded = open(path + "ebook-list-downloaded.txt","w");
            downloaded.write("");
            downloaded.close();

    
    
    for url in elist:

        downloaded = open(path + "ebook-list-downloaded.txt","r");

        skip_url = 0;

        original_url = url;

        for line in downloaded:
            if line == url:
                skip_url = 1;
                
        if skip_url:
            print("fast skip of: " + url.strip());
            continue;

        downloaded.close();
        
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
        except:
            print("error: exeption: " + url);
            continue;

        response = requests.get(download, headers=headers);
        fname = path + download.split("/")[-1];
        title = fname.replace("-20"," ");
        title = title.replace("-20"," ");
        print(name + " - " + title.split("/")[-1] + ": ",end="");

        if os.path.isfile(title):
            print("file already exists, continue.");
            continue

        file = open(title,"wb")
        file.write(response.content);
        file.close();
        downloaded = open(path + "ebook-list-downloaded.txt","a");
        downloaded.write(original_url);
        downloaded.close();
        print("new! saved");
        time.sleep(0.1);
    
    time.sleep(0.1);
