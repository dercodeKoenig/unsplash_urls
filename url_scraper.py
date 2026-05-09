#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from curl_cffi import requests
import random
import time
import os


def get_urls(query, pages):
    # Realistic headers (copy from a real browser as closely as possible)
    headers = {
        ":authority": "unsplash.com",
        "accept": "application/json, text/plain, */*",       
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en,de;q=0.9,de-DE;q=0.8",
        "cache-control": "max-age=0",
        "dnt": "1",
        "priority": "u=0, i",
        "sec-ch-ua": '"Microsoft Edge";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",           
        "sec-fetch-mode": "cors",            
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0",
        "Referer": "https://unsplash.com/s/photos/wallpaper",
    }

    urls = set()

    query = query.replace("-", "+")
    for page in range(1, 1+pages):
        url = "https://unsplash.com/napi/search/photos?page="+str(page)+"&per_page=20&query="+query
        #print(url)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for entry in data["results"]:
                urls.add(entry["urls"]["raw"].split("?")[0])
        else:
            print("ERROR:", url, response.text)
            return None

    return urls


# In[ ]:


with open("unspl_links.txt", "r") as f:
    lines = f.read().split("\n")
print(len(lines))

dirname = "unsplash_urls"

os.makedirs(dirname, exist_ok=True)


for i in lines:
    topic = i.split("/")[-1]
    target_path = os.path.join(dirname, topic)

    if os.path.exists(target_path):
        print("skip", topic)
        continue

    print("working", topic)
    urls = get_urls(topic, 20)
    if urls is None:
        print("ERROR, urls is None")
        continue

    print("urls:", len(urls))
    with open(target_path, "w") as f:
        for url in urls:
            f.write(url+"\n")
    print("ok")
    print("")
    time.sleep(5)


# In[ ]:




