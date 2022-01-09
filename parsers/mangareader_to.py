def parse(url, timeout, save_folder, redownload_numbers, do_archive, try_next):
    from parsers.basic_functions import download_images, archivate, rebuild_redownload_images
    from bs4 import BeautifulSoup as bs
    import time, sys, os
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
    try:
        browser.get(url)
        while True:
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

            save_folder = os.path.join(save_folder, title)
            save_folder = save_folder.replace(' ', '_').replace('.', '').replace('|', '-')

            if not os.path.exists(save_folder):
                os.mkdir(save_folder)

            if redownload_numbers != '':
                urls = rebuild_redownload_images(redownload_numbers, urls)

            download_images(urls, save_folder, url, timeout)

            if do_archive:
                archivate(save_folder)

            if try_next:
                browser.execute_script('nextChapterVolume();')
                save_folder = true_save_folder
                old_title = title
            else:
                break
    finally:
        browser.close()