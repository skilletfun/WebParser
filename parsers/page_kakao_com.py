def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count, path_to_browser):
    from parsers.basic_functions import download_images, archivate, rebuild_redownload_images, prepare_save_folder
    import time, sys
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()

    options.add_argument('--blink-settings=imagesEnabled=false')

    options.add_argument("--disable-features=VizDisplayCompositor")

    options.add_argument("--user-data-dir=" + path_to_browser)

    if not sys.platform.startswith("linux"):
        ex_path = 'chromedriver.exe'
    else:
        ex_path = 'chromedriver'

    browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
    browser.minimize_window()

    true_save_folder = save_folder
    old_title = ''

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1

    try:
        browser.execute_script('window.stop();')
        browser.get(url)
        while True:
            chapter_count -= step

            check = browser.execute_script('return document.getElementsByClassName(\'css-88gyaf\')[0];')

            if check is None:
                time.sleep(1)
                continue

            urls = browser.execute_script(
                'return document.getElementsByClassName(\'css-88gyaf\')[0].getElementsByTagName(\'img\');')

            urls = [el.get_attribute('src') for el in urls]

            title = browser.title
            if title == old_title: break

            save_folder = prepare_save_folder(save_folder, title)

            if redownload_numbers != '':
                urls = rebuild_redownload_images(redownload_numbers, urls)

            download_images(urls, save_folder, url, timeout)

            if do_archive:
                archivate(save_folder)

            if chapter_count > 0:
                next_btn = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/span[4]')

                if next_btn is None: break
                else:
                    next_btn.click()
                    save_folder = true_save_folder
                    old_title = title
                    max_wait = 10

                    while title == old_title and max_wait > 0:
                        title = browser.title
                        max_wait -= 1
                        time.sleep(1)
            else:
                break
    finally:
        browser.close()
        browser.quit()