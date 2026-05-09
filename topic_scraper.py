#!/usr/bin/env python
# coding: utf-8

# In[12]:


# pip install playwright beautifulsoup4 tldextract

from bs4 import BeautifulSoup
import requests
import urllib

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        links.append(a['href'])
    return links

links = []
with open("unspl_links.txt", "r") as f:
    links = f.read().split("\n")
print("existing lines:", len(links))
links = set(links)
print("existing unique links:", len(links))

toscan = []

def add_link(link):
    if link not in links:
        print("adding", link)
        toscan.append(link)
        links.add(link)
        with open("unspl_links.txt", "a") as f:
            f.write(link+"\n")

# seed / add to scan
add_link("/s/photos/wallpaper")
for i in links:
    toscan.append(i)

while len(toscan) > 0:
    c = toscan.pop()
    url = urllib.parse.urljoin("https://unsplash.com", c)
    html= requests.get(url).text
    links_on_page = extract_links(html)
    for i in links_on_page:
        if i.startswith("/s/photos/"):
            add_link(i)



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




