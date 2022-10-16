# Краткое описание

Программа предназначена для парсинга (скачивания) сканов (картинок).

Для использования определенных сайтов требуется наличие Google Chrome (или Chromium) и [драйвера]( https://chromedriver.chromium.org/downloads) к нему. 
Драйвер должен быть той же версии, что и браузер.

Может после скачивания склеить картинки, а также заархивировать их (временно отключено). 

В разработке - заливка на гугл-диск, waifu2x.

Для скачивания с некоторых сайтов может потребоваться предварительная авторизация на этих сайтах.

# Поддерживаемые сайты
- ac.qq.com
- bomtoon.com
- comic.naver.com
- comiko.kr
- fanfox.net
- kuaikanmanhua.com
- king-manga.com
- manga.bilibili.com
- mangakalot.com
- mangareader.com
- manhuadb.com
- mechacomic.jp
- page.kakao.com
- rawdevart.com
- ridibooks.com
- scansnelo.com
- webmota.com
- webtoons.com

# Установка
Установить Python. Программа разрабатывалась на версии 3.8. 
Скачать архив с кодом, установить зависимости `pip install -r requirements.txt`.
Положить в папку с исполняемым файлом `chromedriver.exe`. Отредактировать `config.py`, прописав свои пути.
Запустить `python3 main.py`. 