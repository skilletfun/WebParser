import os
from parsers.basic_functions import find_images, rebuild_redownload_images, download_images, get_response, find_element, archivate


def parse(url, timeout, save_folder, redownload_numbers, do_archive, try_next):
    true_save_folder = save_folder
    while True:
        src = get_response(url)

        title_page, images = find_images(src, 'div', 'class', 'comic-contain')

        if redownload_numbers != '':
            images = rebuild_redownload_images(redownload_numbers, images)

        save_folder = os.path.join(save_folder, title_page)
        save_folder = save_folder.replace(' ', '_').replace('.', '').replace('|', '-')

        if not os.path.exists(save_folder):
            os.mkdir(save_folder)

        images = [img.get('src') for img in images]

        download_images(images, save_folder, url, timeout)

        if do_archive:
            archivate(save_folder)

        if try_next:
            res = find_element(src, 'div', 'class', 'bottom-bar-tool').find_all('a')[3]
            url = res.get('href')
            if not url is None:
                url = res.get('href')
                save_folder = true_save_folder
            else:
                break
        else:
            break