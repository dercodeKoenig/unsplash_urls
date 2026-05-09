#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import requests
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

urls_dir = "unsplash_urls"
output_dir = "unsplash_images"

os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}


existing_files = {f for f in os.listdir(output_dir) if not f.endswith('.tmp')}

def get_file_name(url):
    return url.split("/")[-1].split("?")[0]

# 2. Collect URLs that aren't already in the folder
urls_to_download = set()
for urls_file in tqdm(os.listdir(urls_dir)):
    with open(os.path.join(urls_dir, urls_file), 'r') as file:
        for line in file:
            url = line.strip()
            if not url:
                continue
            if("premium_photo") in url:
                # has watermarks
                continue 

            filename = get_file_name(url)
            if filename not in existing_files:
                urls_to_download.add(url)


urls_to_download = list(urls_to_download)
if len(sys.argv) == 2:
    limit = int(sys.argv[1])
    urls_to_download = urls_to_download[:limit]
print("to download:", len(urls_to_download))
random.shuffle(urls_to_download)


def download_url(url):
    filename = get_file_name(url)
    filepath = os.path.join(output_dir, filename)
    tmp_filepath = filepath + ".tmp"

    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            # Write to the temporary file first
            with open(tmp_filepath, 'wb') as f:
                f.write(response.content)
            os.replace(tmp_filepath, filepath)
            return f"Downloaded {url}"
        else:
            return f"Failed {url}: {response.status_code}"

    except Exception as e:
        if os.path.exists(tmp_filepath):
            try:
                os.remove(tmp_filepath)
            except OSError:
                pass
        return f"Error {url}: {e}"


with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(download_url, url): url for url in urls_to_download}
    for future in tqdm(as_completed(futures), total=len(futures)):
        pass


# In[ ]:




