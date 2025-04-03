import vk_api
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor
from cfg import TOKEN_PROFILE, TOKEN_COMMUNITY

# Инициализация VK API
vk = vk_api.VkApi(token=TOKEN_PROFILE)
vk.get_api()

vk_public = vk_api.VkApi(token=TOKEN_COMMUNITY)
vk_public._auth_token()
vk_public.get_api()

# Списки для хранения вложений VK
ecmwf00z = []
gfs00z = []
aifs00z = []
icon00z = []
ecmwf12z = []
gfs12z = []
aifs12z = []
icon12z = []

# URL карт погоды
urls_gfs00z = [
    'https://www.wetterzentrale.de/maps/GFSOPEU00_0_2.png', # 1
    'https://www.wetterzentrale.de/maps/GFSOPEU00_24_2.png', # 2
    'https://www.wetterzentrale.de/maps/GFSOPEU00_48_2.png', # 3
    'https://www.wetterzentrale.de/maps/GFSOPEU00_72_2.png', # 4
    'https://www.wetterzentrale.de/maps/GFSOPEU00_96_2.png', # 5
    'https://www.wetterzentrale.de/maps/GFSOPEU00_120_2.png', # 6
    'https://www.wetterzentrale.de/maps/GFSOPEU00_144_2.png', # 7
    'https://www.wetterzentrale.de/maps/GFSOPEU00_168_2.png', # 8
    'https://www.wetterzentrale.de/maps/GFSOPEU00_192_2.png', # 9
    'https://www.wetterzentrale.de/maps/GFSOPEU00_216_2.png', # 10
]

urls_aifs00z = [
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_0_2.png', # 11
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_24_2.png', # 12
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_48_2.png', # 13
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_72_2.png', # 14
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_96_2.png', # 15
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_120_2.png', # 16
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_144_2.png', # 17
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_168_2.png', # 18
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_192_2.png', # 19
    'https://www.wetterzentrale.de/maps/AIFSOPEU00_216_2.png', # 20
]

urls_ecmwf00z = [
    'https://www.wetterzentrale.de/maps/ECMOPEU00_0_2.png',  # 21
    'https://www.wetterzentrale.de/maps/ECMOPEU00_24_2.png', # 22
    'https://www.wetterzentrale.de/maps/ECMOPEU00_48_2.png', # 23
    'https://www.wetterzentrale.de/maps/ECMOPEU00_72_2.png', # 24
    'https://www.wetterzentrale.de/maps/ECMOPEU00_96_2.png', # 25
    'https://www.wetterzentrale.de/maps/ECMOPEU00_120_2.png', # 26
    'https://www.wetterzentrale.de/maps/ECMOPEU00_144_2.png', # 27
    'https://www.wetterzentrale.de/maps/ECMOPEU00_168_2.png', # 28
    'https://www.wetterzentrale.de/maps/ECMOPEU00_192_2.png', # 29
    'https://www.wetterzentrale.de/maps/ECMOPEU00_216_2.png', # 30
]

urls_icon00z = [
    'https://www.wetterzentrale.de/maps/ICOOPEU00_0_2.png', # 31
    'https://www.wetterzentrale.de/maps/ICOOPEU00_24_2.png', # 32
    'https://www.wetterzentrale.de/maps/ICOOPEU00_48_2.png', # 33
    'https://www.wetterzentrale.de/maps/ICOOPEU00_72_2.png', # 34
    'https://www.wetterzentrale.de/maps/ICOOPEU00_96_2.png', # 35
    'https://www.wetterzentrale.de/maps/ICOOPEU00_120_2.png', # 36
    'https://www.wetterzentrale.de/maps/ICOOPEU00_144_2.png', # 37
    'https://www.wetterzentrale.de/maps/ICOOPEU00_168_2.png', # 38
]

urls_gfs12z = [
    'https://www.wetterzentrale.de/maps/GFSOPEU12_0_2.png', # 39
    'https://www.wetterzentrale.de/maps/GFSOPEU12_24_2.png', # 40
    'https://www.wetterzentrale.de/maps/GFSOPEU12_48_2.png', # 41
    'https://www.wetterzentrale.de/maps/GFSOPEU12_72_2.png', # 42
    'https://www.wetterzentrale.de/maps/GFSOPEU12_96_2.png', # 43
    'https://www.wetterzentrale.de/maps/GFSOPEU12_120_2.png', # 44
    'https://www.wetterzentrale.de/maps/GFSOPEU12_144_2.png', # 45
    'https://www.wetterzentrale.de/maps/GFSOPEU12_168_2.png', # 46
    'https://www.wetterzentrale.de/maps/GFSOPEU12_192_2.png', # 47
    'https://www.wetterzentrale.de/maps/GFSOPEU12_216_2.png', # 48
]

urls_aifs12z = [
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_0_2.png', # 49
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_24_2.png', # 50
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_48_2.png', # 51
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_72_2.png', # 52
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_96_2.png', # 53
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_120_2.png', # 54
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_144_2.png', # 55
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_168_2.png', # 56
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_192_2.png', # 57
    'https://www.wetterzentrale.de/maps/AIFSOPEU12_216_2.png', # 58
]

urls_ecmwf12z = [
    'https://www.wetterzentrale.de/maps/ECMOPEU12_0_2.png', # 59
    'https://www.wetterzentrale.de/maps/ECMOPEU12_24_2.png', # 60
    'https://www.wetterzentrale.de/maps/ECMOPEU12_48_2.png', # 61
    'https://www.wetterzentrale.de/maps/ECMOPEU12_72_2.png', # 62
    'https://www.wetterzentrale.de/maps/ECMOPEU12_96_2.png', # 63
    'https://www.wetterzentrale.de/maps/ECMOPEU12_120_2.png', # 64
    'https://www.wetterzentrale.de/maps/ECMOPEU12_144_2.png', # 65
    'https://www.wetterzentrale.de/maps/ECMOPEU12_168_2.png', # 66
    'https://www.wetterzentrale.de/maps/ECMOPEU12_192_2.png', # 67
    'https://www.wetterzentrale.de/maps/ECMOPEU12_216_2.png', # 68
]

urls_icon12z = [
    'https://www.wetterzentrale.de/maps/ICOOPEU12_0_2.png', # 69
    'https://www.wetterzentrale.de/maps/ICOOPEU12_24_2.png', # 70
    'https://www.wetterzentrale.de/maps/ICOOPEU12_48_2.png', # 71
    'https://www.wetterzentrale.de/maps/ICOOPEU12_72_2.png', # 72
    'https://www.wetterzentrale.de/maps/ICOOPEU12_96_2.png', # 73
    'https://www.wetterzentrale.de/maps/ICOOPEU12_120_2.png', # 74
    'https://www.wetterzentrale.de/maps/ICOOPEU12_144_2.png', # 75
    'https://www.wetterzentrale.de/maps/ICOOPEU12_168_2.png' # 76
]

def download_image(url, index):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(f'GENERAL/map_{index}.png', 'wb') as file:
            file.write(response.content)
        print(f'Файл map_{index}.png сохранён')
    except Exception as e:
        print(f'Ошибка при загрузке {url}: {e}')

def download_maps(upload_list, start_index):
    """Загружает карты параллельно"""
    os.makedirs('GENERAL', exist_ok=True)
    tasks = [(url, start_index + i) for i, url in enumerate(upload_list)]
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda args: download_image(*args), tasks)

def upload_photos(start, end, photo_list):
    """Загружает фото на сервер VK"""
    for i in range(start, end):
        try:
            
            # Для публичной страницы
            upload_server_public = vk_public.method("photos.getMessagesUploadServer", {'group_id': 229873541})
            
            # Загрузка фото (используем публичную страницу)
            with open(f'GENERAL/map_{i}.png', 'rb') as f:
                response = requests.post(upload_server_public['upload_url'], files={'photo': f}).json()
            
            # Сохранение фото
            saved_photo = vk_public.method('photos.saveMessagesPhoto', {
                'photo': response['photo'],
                'server': response['server'],
                'hash': response['hash']
            })[0]
            
            photo_attachment = f"photo{saved_photo['owner_id']}_{saved_photo['id']}"
            photo_list.append(photo_attachment)
            
        except vk_api.exceptions.Captcha as captcha:
            print(f"Требуется ввод капчи: {captcha.get_url()}")
            captcha.try_again(input("Введите текст с капчи: "))
        except Exception as e:
            print(f"Ошибка при загрузке фото {i}: {e}")
    
    print(f'Загружено фото {start}-{end-1}')
    return photo_list

def send_messages(start, end, model, model_name, utc):
    """Отправляет сообщения с картами"""
    for chat_id in range(1, 101):
        try:
            peer_id = 2000000000 + chat_id
            vk_public.method('messages.send', {
                'peer_id': peer_id,
                'message': f'Модель: {model_name}\nСрок: {utc}z (UTC+3)\nРазработчик: @obsrvarnd\nРедактор: @uporotyj_meteorolog',
                'attachment': ','.join(model),
                'random_id': 0
            })
            print(f"Сообщение отправлено в чат {peer_id}")
        except Exception as e:
            print(f"Ошибка при отправке в чат {peer_id}: {e}")

def process_model(url_list, start_idx, model_list, model_name, utc):
    """Полный процесс обработки модели"""
    print(f"\n=== Обработка {model_name} {utc}z ===")
    
    # 1. Загрузка карт
    download_maps(url_list, start_idx)
    
    # 2. Загрузка фото в VK
    upload_photos(start_idx, start_idx + len(url_list), model_list)
    
    # 3. Отправка сообщений
    send_messages(start_idx, start_idx + len(url_list), model_list, model_name, utc)
    
    # Очистка списка для следующего цикла
    model_list.clear()

def main_loop():
    """Основной цикл работы"""
    while True:
        try:
            # 00z модели
            process_model(urls_gfs00z, 1, gfs00z, 'GFS', '00')
            time.sleep(1500)
            
            process_model(urls_aifs00z, 11, aifs00z, 'AIFS', '00')
            time.sleep(1500)
            
            process_model(urls_ecmwf00z, 21, ecmwf00z, 'ECMWF', '00')
            time.sleep(1500)
            
            process_model(urls_icon00z, 31, icon00z, 'ICON', '00')
            time.sleep(38700)
            
            # 12z модели
            process_model(urls_gfs12z, 39, gfs12z, 'GFS', '12')
            time.sleep(1500)
            
            process_model(urls_aifs12z, 49, aifs12z, 'AIFS', '12')
            time.sleep(1500)
            
            process_model(urls_ecmwf12z, 59, ecmwf12z, 'ECMWF', '12')
            time.sleep(1500)
            
            process_model(urls_icon12z, 69, icon12z, 'ICON', '12')
            time.sleep(38700)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            continue

if __name__ == '__main__':
    main_loop()
