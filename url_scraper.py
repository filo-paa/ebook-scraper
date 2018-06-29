import requests
from bs4 import BeautifulSoup
import re
import os.path

pagestart = "https://libri.me/category/a/page/2/";
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(pagestart, headers=headers)
html = response.content;
soup = BeautifulSoup(html, 'html.parser');

for link in soup.find_all("a"):
	print(link.get("href"));
	
