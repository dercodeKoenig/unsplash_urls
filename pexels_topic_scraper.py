#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
from curl_cffi import requests
import urllib

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        links.append(a['href'])
    return links

links = []
try:
    with open("pexels_links.txt", "r") as f:
        links = f.read().split("\n")
except:pass
print("existing lines:", len(links))
links = set(links)
print("existing unique links:", len(links))

toscan = []

def add_link(link):
    if link not in links:
        print("adding", link)
        toscan.append(link)
        links.add(link)
        with open("pexels_links.txt", "a") as f:
            f.write(link+"\n")

# seed / add to scan
add_link("/search/wallpaper")
for i in links:
    toscan.append(i)

while len(toscan) > 0:
    c = toscan.pop()
    print("working", c)
    url = urllib.parse.urljoin("https://pexels.com", c)
    html= requests.get(url, impersonate="chrome").text
    links_on_page = extract_links(html)
    for i in links_on_page:
        if i.startswith("/search/"):
            i = i.split("?")[0]
            if i.endswith("/"):
                i = i[0:-1]
            add_link(i)


# In[ ]:





# In[ ]:




