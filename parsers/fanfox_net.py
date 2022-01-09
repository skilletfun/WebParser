def parse(url, timeout, save_folder, redownload_numbers, do_archive, try_next):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time, sys, os
    from parsers.basic_functions import download_images, archivate, rebuild_redownload_images

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
    try:
        while url != 'https://fanfox.net':
            urls = []
            browser.get(url)

            time.sleep(5)

            image = browser.find_element_by_xpath('/html/body/div[7]/img')
            n = int(browser.execute_script('return imagecount'))

            title = browser.execute_script('return document.title')
            save_folder = os.path.join(true_save_folder, title)

            if not os.path.exists(save_folder):
                os.mkdir(save_folder)

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

            if try_next:
                url = 'https://fanfox.net' + browser.execute_script('return nextchapterurl')
            else: break
    finally:
        browser.close()
