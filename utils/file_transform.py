from os import listdir, pardir
from os.path import split, join, abspath

import patoolib
from PIL import Image

from utils.logging import log


@log
def archivate(save_folder, title):
    """ Archive files (images) to zip-file. """
    save_folder = split(save_folder)[0]
    name = gen_correct_name(title)
    patoolib.create_archive(join(save_folder, name + '.zip'), [save_folder])

@log
def merge_images(save_folder):
    """ Merge images into one PNG. """
    name = gen_correct_name(split(save_folder)[-1])
    dir_imgs = listdir(save_folder)
    suffix = dir_imgs[0].split('.')[-1]
    total = len(dir_imgs)
    height = 0
    imgs = []

    for i in range(1, total + 1):
        img = Image.open(join(save_folder, str(i) + '.' + suffix))
        imgs.append(img)
        height += img.height

    width = imgs[0].width
    save_folder = abspath(join(save_folder, pardir))
    file_name = join(save_folder, name + '_MERGED.png')
    res_img = Image.new('RGB', (width, height), 'white')

    t_height = 0
    for img in imgs:
        res_img.paste(img, (0, t_height))
        t_height += img.height
        img.close()

    res_img.save(file_name)
    res_img.close()

def gen_correct_name(name: str) -> str:
    """ Return the correct name of the destination folder without restricted symbols. """
    return ''.join([el for el in name if not el in ' .|/\\?*><:"!^;,№'])
