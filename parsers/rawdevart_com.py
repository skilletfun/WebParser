import os
from parsers.basic_functions import find_images, rebuild_redownload_images, download_images, get_response, prepare_save_folder


def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):
    src = get_response(url)

    title, images = find_images(src, 'div', 'id', 'img-container')

    if redownload_numbers != '':
        images = rebuild_redownload_images(redownload_numbers, images)

    save_folder = prepare_save_folder(save_folder, title)

    images = [img.get('data-src') for img in images]

    download_images(images, save_folder, url, timeout)

    if do_archive:
        import patoolib
        patoolib.create_archive(os.path.join(save_folder, save_folder + '.zip'), [save_folder])