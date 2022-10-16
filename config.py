# Заголовки для запросов, менять не рекомендуется
HEADERS = {
    "Accept": "image/webp,*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    'Host': '',
    "DNT": "1",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

# Если у вас Windows, установите число 8, если Linux, установите число 7
SYMBOLS_FOR_DELETE = 8

# Папка для сохранения сканов
# Внутри указанной папки будет создана еще папка(-и) с названием скачиваемой главы
SAVE_FOLDER = "C:\\Users\\user\\Downloads"

# Путь до папки <User Data> браузера на движке Chromium (Chrome, Chromium, Canary, Vivaldi...)
PATH_TO_BROWSER = "C:\\Users\\user\\AppData\\Local\\Chromium\\User Data"

# Посылать ли уведомленя о завершении работы (True / False)
NOTIFY = False

# Сколько за раз запрашивается сканов
REQUESTS_LIMIT = 10

# Сколько раз программе пытаться скачать один и тот же скан при ошибке 
DOWNLOAD_TRIES = 10

# Задержка в секундах для скролла страницы
SCROOL_DELAY = 0.7

# Используется ли в браузере новый интерфейс реманги или старый (True / False)
NEW_REMANGA = True

# Версия программы
VERSION = "v1.8"