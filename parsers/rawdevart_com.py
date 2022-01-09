import os
from parsers.basic_functions import find_images, rebuild_redownload_images, download_images, get_response


def parse(url, timeout, save_folder, redownload_numbers, do_archive, try_next):
    src = get_response(url)

    title_page, images = find_images(src, 'div', 'id', 'img-container')

    if redownload_numbers != '':
        images = rebuild_redownload_images(redownload_numbers, images)

    save_folder = os.path.join(save_folder, title_page)
    save_folder = save_folder.replace(' ', '_').replace('.', '').replace('|', '-')

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    images = [img.get('data-src') for img in images]

    download_images(images, save_folder, url, timeout)

    if do_archive:
        import patoolib
        patoolib.create_archive(os.path.join(save_folder, save_folder + '.zip'), [save_folder])