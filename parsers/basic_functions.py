import requests
import os
import time
import multiprocessing as mp
from bs4 import BeautifulSoup as bs

# =====================================================================#
# Download function. Declare single because of async
# =====================================================================#
def download(url, _headers, name, save_folder):
    img = requests.get(url, headers=_headers)
    tries = 10

    while (not img.status_code == 200) and tries > 0:
        img = requests.get(url, headers=_headers)
        tries -= 1

    if img.status_code == 200:
        with open(os.path.join(save_folder, name + '.jpg'), "wb") as f:
            f.write(img.content)


# =====================================================================#
# Find element
# =====================================================================#
def find_element(src, tag, type, value):
    soup = bs(src, "lxml")
    res = soup.find(tag, {type: value})
    return res


# =====================================================================#
# Get response and return text
# =====================================================================#
def get_response(url, headers=None):
    if headers is None:
        headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
    response = requests.get(url, headers=headers)
    src = response.text
    return src


# =====================================================================#
# Prepare save folder
# =====================================================================#
def prepare_save_folder(save_folder, title):
    save_folder = os.path.join(save_folder, title)
    save_folder = save_folder.replace(' ', '_').replace('.', '').replace('|', '-')

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    return save_folder


# =====================================================================#
# Parse html and find urls
# =====================================================================#
def find_images(src, tag_type, tag_type_for_search, value_of_ttfs):
    soup = bs(src, "lxml")
    title_page = soup.find('title').text

    images = soup.find(tag_type, {tag_type_for_search: value_of_ttfs})
    images = images.find_all('img')

    return title_page, images


# =====================================================================#
# Rebuild array with urls
# =====================================================================#
def rebuild_redownload_images(numbers, images):
    numbers = numbers.split()
    numbers = [int(i) - 1 for i in numbers]

    return [images[i] for i in numbers]


# =====================================================================#
# Download images by urls
# =====================================================================#
def download_images(images, save_folder, url, timeout, _headers=None, name_of_files=None):
    if _headers is None:
        _headers = {
            "Accept": "image/webp,*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            'Host': '',
            "DNT": "1",
            "Referer": url,
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
        }

    if name_of_files is None:
        name_of_files = range(len(images))

    pool = mp.Pool(mp.cpu_count())

    i = 0

    for img_url in images:
        temp_url = img_url

        if 'Host' in _headers:
            _headers['Host'] = temp_url.replace('http://', '').replace('https://', '').split('/')[0]

        pool.apply_async(download, args=(img_url, _headers, str(name_of_files[i] + 1), save_folder))

        i += 1
        time.sleep(timeout)

    pool.close()
    pool.join()

# =====================================================================#
# Archive images to zip
# =====================================================================#
def archivate(save_folder):
    import patoolib
    patoolib.create_archive(os.path.join(save_folder, save_folder + '.zip'), [save_folder])