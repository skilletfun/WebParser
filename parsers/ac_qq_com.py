from parsers.basic_functions import find_images, rebuild_redownload_images, download_images, find_element, archivate, prepare_save_folder
import sys, time

def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):
    true_save_folder = save_folder

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1
        
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("window-size=900,600")

    if not sys.platform.startswith("linux"):
        ex_path = 'chromedriver.exe'
    else:
        ex_path = 'chromedriver'
    
    browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
    
    try:
        while True:
            chapter_count -= step
            browser.get(url)
            
            time.sleep(2)
            
            script = 'document.getElementById(\'comicContain\').getElementsByTagName(\'img\')'
            
            l = int(browser.execute_script('return ' + script + '.length;'))
            images = []
            
            for i in range (l):
                browser.execute_script(script + f'[{i}].scrollIntoView();')
                time.sleep(0.5)
            
            for i in range (l):
                browser.execute_script(script + f'[{i}].scrollIntoView();')
                while browser.execute_script('return ' + script + f'[{i}].src;').endswith('pixel.gif'):
                    continue
                images.append(browser.execute_script('return ' + script + f'[{i}].src;'))
            
            title = browser.title
            images = images[:1] + images[2:]
                       
            if redownload_numbers != '':
                images = rebuild_redownload_images(redownload_numbers, images)

            save_folder = prepare_save_folder(save_folder, title)
            
            download_images(images, save_folder, url, timeout)

            if do_archive:
                archivate(save_folder)

            if chapter_count > 0:
                url = browser.execute_script('return document.getElementById(\'nextChapter\').href;')
                save_folder = true_save_folder
            else:
                break
    finally:
        browser.close()
        browser.quit()
