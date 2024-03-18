import json
import math
import os

import requests
from datetime import datetime

from itv_parser.AvtoDom.config import cookies, headers

current_date = datetime.now().strftime("%Y-%m-%d")

# Путь к папке, которую вы хотите создать
folder_path = f"AvtoDom/data_{current_date}"

# Проверяем существование папки
if not os.path.exists(folder_path):
    # Если папка не существует, создаем её
    os.makedirs(folder_path)
    print(f"Папка '{folder_path}' успешно создана.")
else:
    print(f"Папка '{folder_path}' уже существует.")


def get_html():
    # for i in range(1, 11):
    response = requests.get(
        'https://avtodom.ru/v1/catalog/16/15?holdingId=1&city=msk&condition=used&transportType=cars&sort=popular-desc',
        cookies=cookies,
        headers=headers,
    ).json()

    pages = response['data']['total']
    print(f'[INFO] Total pages: {pages}')
    page = math.ceil(int(pages) / 16)

    for i in range(1, page+1):
        print(f'[INFO] Page {i} of {pages}')
        res = requests.get(
            f'https://avtodom.ru/v1/catalog/16/{i}?holdingId=1&city=msk&condition=used&transportType=cars&sort=popular-desc',
            cookies=cookies,
            headers=headers,
        ).json()

        item_list = dict()
        for d in res['data']['data']:
            car_id = d.get('carId')
            color = d.get('color')
            concatName = d.get('concatName')
            disprice = d.get('disprice')
            images = d.get('images')
            id_item = d.get('id')
            for url in images:
                url_img = url.get('source').get('url')
                item_list.update({
                    'catId': car_id,
                    'Цвет': color,
                    'Модель': concatName,
                    'Цена': disprice,
                    'Фото': url_img,
                    'Карточка товара': f'https://avtodom.ru/v1/catalog/{id_item}?holdingId=1&city='
                })
            r = requests.get(f'https://avtodom.ru/v1/catalog/{id_item}').json()
            with open(f'AvtoDom/data_{current_date}/{car_id}_{concatName}.json', 'w', encoding='utf-8') as file_json:
                json.dump(r, file_json, ensure_ascii=False, indent=4)
        with open(f'AvtoDom/cars_{current_date}.json', 'a', encoding='utf-8') as file:
            json.dump(res, file, ensure_ascii=False, indent=4)


def main():
    get_html()


if __name__ == '__main__':
    main()
