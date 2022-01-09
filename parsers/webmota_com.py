import os
from parsers.basic_functions import find_images, rebuild_redownload_images, download_images, \
    get_response, find_element, archivate, prepare_save_folder


def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):
    true_save_folder = save_folder

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1

    while True:
        chapter_count -= step
        src = get_response(url)

        title, images = find_images(src, 'div', 'class', 'comic-contain')

        if redownload_numbers != '':
            images = rebuild_redownload_images(redownload_numbers, images)

        save_folder = prepare_save_folder(save_folder, title)

        images = [img.get('src') for img in images]

        download_images(images, save_folder, url, timeout)

        if do_archive:
            archivate(save_folder)

        if chapter_count > 0:
            res = find_element(src, 'div', 'class', 'bottom-bar-tool').find_all('a')[3]
            url = res.get('href')
            if not url is None:
                url = res.get('href')
                save_folder = true_save_folder
            else:
                break
        else:
            break