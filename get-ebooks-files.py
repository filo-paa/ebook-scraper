import requests
from bs4 import BeautifulSoup
import re
import os.path
import time

## Script Number 3
# finally the actual download.
# this is slightly more complicated, but this is what it does:
# goes into each author folder, read ebook list one by one
# if url is in another list (downloaded list) then skip it,
# otherwise do download it and save it, then add it to downloaded list.
# this is very useful so to fast skip books that have already been downloaded.
# (skipping is much faster this way than to check if title of ebook matches, i don't have to fetch the filename from web to skip!)

#additional notes:
#change line 60 for file extension, now set to dowload only "MOBI" files.

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

folder_list = os.listdir("authors/");

skip = 1;

start_from = "agatha-christie"; #choose author to start from.

for name in folder_list:

    if name == start_from:
        skip = 0; #if finally you got to wanted author, set tag to zero
    if skip: #if tag set to zero this wont skip the line anymore
        continue;
    
    path =  "authors/" + name + "/";
    elist = open(path + "ebook-list.txt","r"); #check the immutable 2-be-downloaded list
    if not os.path.isfile(path + "ebook-list-downloaded.txt"): #and open the already downloaded list if exist otherwise make it empty
            downloaded = open(path + "ebook-list-downloaded.txt","w");
            downloaded.write("");
            downloaded.close();

    for url in elist:

        downloaded = open(path + "ebook-list-downloaded.txt","r");

        skip_url = 0;

        original_url = url;

        for line in downloaded:
            if line == url: #if url is in already downloaded file, skip it
                skip_url = 1;
                break;
                
        if skip_url: #if skip was set to one, skip this url (continue)
            print("fast skip of: " + url.strip());
            continue;

        downloaded.close(); #now that we have checked if url was already downlaoded
        #we can move one to old usual code.
        
        #get te ebook extenstion from url
        ext = url.split("-")[-1].strip();
        if (ext != "mobi/"):
            continue; #skip it if it's not mobi (change line if interested in EPUB or PDF!)
        url = url.strip() + '2/'; #get page 2 where actual donwload link is present
        
        try:
            response = requests.get(url, headers=headers)
        except:
            print("error, could not retrive, continue.");
            continue;
        html = response.content;
        soup = BeautifulSoup(html, 'html.parser'); #parse with bs4
        try:
            #get url of ebook from h2 element in ebook page
            download = soup.find_all("h2")[1]("a")[0].get("href").split("url=")[-1];
        except:
            print("error: exeption: " + url);
            continue;
        response = requests.get(download, headers=headers);
        
        fname = path + download.split("/")[-1]; #get filename
        title = fname.replace("-20"," "); #some kind of encoding -20 is space
        title = title.replace("-2C",","); # and -2C is comma
        
        print(name + " - " + title.split("/")[-1] + ": ",end="");

        #just in case file exists, skip
        if os.path.isfile(title):
            print("file already exists, continue.");
            continue
        
        #open file with write bytes
        
        file = open(title,"wb")
        file.write(response.content); #write content
        file.close(); # and close
        #now append downlaoded ebook url to downloaded list
        downloaded = open(path + "ebook-list-downloaded.txt","a");
        downloaded.write(original_url);
        downloaded.close();
        print("new! saved");
        time.sleep(0.1);
    elist.close();
    time.sleep(0.1);
