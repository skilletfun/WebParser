from parsers.basic_functions import find_images, rebuild_redownload_images, download_images, find_element, archivate, prepare_save_folder

import requests

def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):
    true_save_folder = save_folder
    
    if 'weekday' in url:
        url = url[:url.find('weekday') - 1]

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1
        
    while True:
        chapter_count -= step
        
        headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
        response = requests.get(url, headers=headers)
                
        if 'list?titleId' in response.url:
            break
            
        src = response.text
        
        title, images = find_images(src, 'div', 'class', 'wt_viewer')
        
        title += str(int(url[url.rfind('=') + 1:]))

        if redownload_numbers != '':
            images = rebuild_redownload_images(redownload_numbers, images)

        save_folder = prepare_save_folder(save_folder, title)

        images = [img.get('src') for img in images]

        download_images(images, save_folder, url, timeout)

        if do_archive:
            archivate(save_folder)

        if chapter_count > 0:
            url = url[:url.rfind('=') + 1] + str(int(url[url.rfind('=') + 1:]) + 1)
            save_folder = true_save_folder
        else:
            break
