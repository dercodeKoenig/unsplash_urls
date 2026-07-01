#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import os

dirname = "flickr_urls"

os.makedirs(dirname, exist_ok=True)

def search_flickr_images(query, images, page):
    # Official Flickr API endpoint
    url = "https://www.flickr.com/services/rest/"

    # Define the parameters for the API call
    params = {
        "method": "flickr.photos.search",
        "api_key": "7a7fca6415a7e9515e2d5a809ee4b4d6",
        "text": query,
        "sort": "relevance",
        "per_page": images,
        "page": page,
        "format": "json",
        "nojsoncallback": 1,                          # Ensures raw JSON is returned instead of a function wrapper
        "extras": "url_k"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise error for bad responses
        data = response.json()

        # Check if the API request was successful according to Flickr
        if data.get("stat") == "ok":
            photos = data["photos"]["photo"]

            image_urls = []
            for photo in photos:
                # Use large image url if available, otherwise fallback to medium
                img_url = photo.get("url_k")
                if img_url:
                    image_urls.append(img_url)
            return image_urls
        else:
            print(f"Flickr API Error: {data.get('message')}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        print(response.text)
        return []


# In[ ]:


with open("unspl_links.txt", "r") as f:
    unsplash_topics = [x.split("/")[-1].strip().replace("-", " ") for x in f.readlines()]


# In[ ]:


from concurrent.futures import ThreadPoolExecutor
import time

def work(topic, target_path):
    results = search_flickr_images(topic, 100, 1)
    print(topic, len(results))
    if len(results) > 0:
        with open(target_path, "w") as f:
            for url in results:
                f.write(url+"\n")

with ThreadPoolExecutor(max_workers=10) as executor:
    for topic in unsplash_topics:
        target_path = os.path.join(dirname, topic.replace(" ", "-"))
        if os.path.exists(target_path):
            print("skip", target_path)
            continue

        executor.submit(work, topic, target_path)
        time.sleep(0.5)



# In[ ]:




