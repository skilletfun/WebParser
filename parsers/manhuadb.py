import requests, os
from bs4 import BeautifulSoup as bs
from parsers.basic_functions import download_images, archivate, rebuild_redownload_images, prepare_save_folder

def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):

    true_url = url
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
    soup = download(url, headers, save_folder, redownload_numbers, do_archive, timeout)

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1

    chapter_count -= 1

    if chapter_count > 0:
        chapter_count -= step
        chapters_urls = soup.find('ol', {'class': 'links-of-books'}).find_all('a')
        l = len(chapters_urls)

        for i in range(l):
            if chapters_urls[i].get('href') in true_url:
                if not i + 1 >= l:
                    chapters_urls = ['https://www.manhuadb.com' + el.get('href') for el in chapters_urls[i + 1:]]
                    for url in chapters_urls:
                        download(url, headers, save_folder, redownload_numbers, do_archive, timeout)


def download(url, headers, save_folder, redownload_numbers, do_archive, timeout):
    urls = []
    tries = 3

    if not url[:-5].endswith('_p1'):
        url = url[:-5] + '_p1.html'

    response = requests.get(url, headers=headers)
    soup = bs(response.text, "lxml")
    title = soup.find('title').text

    while tries > 0:
        response = requests.get(url, headers=headers)
        if response.ok:
            src = response.text
            soup = bs(src, "lxml")
            img = soup.find('img', {'class': 'show-pic'})

            if img != None:
                urls.append(img.get('src'))
                url = url[:url.rfind('_') + 2] + str(int(url[url.rfind('_') + 2: -5]) + 1) + '.html'
                tries = 3
            else:
                break
        else:
            tries -= 1

    save_folder = prepare_save_folder(save_folder, title)

    if redownload_numbers != '':
        urls = rebuild_redownload_images(redownload_numbers, urls)

    download_images(urls, save_folder, 'https://www.manhuadb.com/', timeout)

    if do_archive:
        archivate(save_folder)

    return soup




