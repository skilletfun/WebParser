def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time, sys, os
    from parsers.basic_functions import download_images, archivate, rebuild_redownload_images, prepare_save_folder

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("window-size=900,600")

    if not sys.platform.startswith("linux"):
        ex_path = 'chromedriver.exe'
    else:
        ex_path = 'chromedriver'

    browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)

    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
    true_save_folder = save_folder

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1

    try:
        while url != 'https://fanfox.net':
            chapter_count -= step
            urls = []
            browser.get(url)

            time.sleep(5)

            image = browser.find_element_by_xpath('/html/body/div[7]/img')
            n = int(browser.execute_script('return imagecount'))

            title = browser.execute_script('return document.title')

            save_folder = prepare_save_folder(save_folder, title)

            url_img = image.get_attribute('src')

            url = url_img.split('?')[0]

            if url[-9] == '/':
                left_url = url[:-7]
                num = '000'
            else:
                pos = url.rfind('_') + 1
                left_url = url[:pos]
                num = str(url[pos:-4])

            for _ in range(n + 1):
                if len(num) < 3:
                    num = (3 - len(num)) * '0' + num

                urls.append(left_url + num + '.jpg')
                num = str(int(num) + 1)

            if redownload_numbers != '':
                images = rebuild_redownload_images(redownload_numbers, images)

            download_images(urls, save_folder, url, timeout, _headers=headers)

            if do_archive:
                archivate(save_folder)

            if chapter_count > 0:
                url = 'https://fanfox.net' + browser.execute_script('return nextchapterurl')
                save_folder = true_save_folder
            else: break
    finally:
        browser.close()
