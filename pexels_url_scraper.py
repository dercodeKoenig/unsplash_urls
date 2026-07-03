#!/usr/bin/env python
# coding: utf-8

# In[1]:


from curl_cffi import requests
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor

def get_urls(query, pages):

    headers = {
        "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr"
    }

    urls = set()
    query = query.replace("-", "+")
    for page in range(1, 1+pages):
        url = "https://www.pexels.com/en-us/api/v3/search/photos?query="+query+"&page="+str(page)+"&per_page=20"
        #print(url)
        response = requests.get(url, impersonate="chrome", headers=headers)

        if response.status_code == 200:
            data = response.json()
            for entry in data["data"]:
                urls.add(entry["attributes"]["image"]["download_link"].split("?")[0])
        else:
            print("ERROR:", url, response.text)
            return None

    return urls


# In[ ]:


with open("pexels_links.txt", "r") as f:
    lines = f.read().split("\n")
print(len(lines))

dirname = "pexels_urls"

os.makedirs(dirname, exist_ok=True)

def work(topic, target_path):
    print("working", topic, target_path)
    try:
        urls = get_urls(topic, 20)
    except Exception as e:
        print("ERROR:", e)
        return

    if urls is None:
        print("ERROR, urls is None")
        return

    print("urls:", len(urls))
    try:
        with open(target_path, "w") as f:
            for url in urls:
                f.write(url+"\n")
    except Exception as e:
        print("ERROR:", e)
        try:
            os.remove(target_path)
        except Exception as e:
            print(e)

    print("ok")
    print("")

working_topics = set()
with ThreadPoolExecutor(max_workers=10) as executor:
    for link in lines:
        topic = link.split("/")[-1]
        target_path = os.path.join(dirname, topic)
        if topic in working_topics:
            continue
        if os.path.exists(target_path):
            print("skip", topic)
            continue
        working_topics.add(topic)
        executor.submit(work, topic, target_path)
        time.sleep(5)




# In[ ]:





# In[ ]:




