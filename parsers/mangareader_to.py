def parse(url, timeout, save_folder, redownload_numbers, do_archive, chapter_count):
    from parsers.basic_functions import download_images, archivate, rebuild_redownload_images, prepare_save_folder
    from bs4 import BeautifulSoup as bs
    import time, sys
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("window-size=900,600")

    if not sys.platform.startswith("linux"):
        ex_path = 'chromedriver.exe'
    else:
        ex_path = 'chromedriver'

    browser = webdriver.Chrome(chrome_options=options, executable_path=ex_path)
    true_save_folder = save_folder
    old_title = ''

    if chapter_count != '*':
        chapter_count = int(chapter_count)
        step = 1
    else:
        step = 0
        chapter_count = 1

    try:
        browser.get(url)
        while True:
            chapter_count -= step
            check = browser.execute_script('return document.getElementsByClassName(\'rtl-row mode-item\')[0];')

            if not check is None:
                browser.execute_script('document.getElementsByClassName(\'rtl-row mode-item\')[0].click();')

            time.sleep(5)
            html = browser.execute_script(
                'return document.getElementsByClassName(\'container-reader-chapter\')[0].innerHTML;')

            soup = bs(html, 'lxml')
            title = str(browser.current_url).split('/')[-1]
            if title == old_title: break
            urls = [el['data-url'] for el in soup.find_all('div', {'class': 'iv-card'})]

            save_folder = prepare_save_folder(save_folder, title)

            if redownload_numbers != '':
                urls = rebuild_redownload_images(redownload_numbers, urls)

            download_images(urls, save_folder, url, timeout)

            if do_archive:
                archivate(save_folder)

            if chapter_count > 0:
                browser.execute_script('nextChapterVolume();')
                save_folder = true_save_folder
                old_title = title
            else:
                break
    finally:
        browser.close()