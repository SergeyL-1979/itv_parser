import math
import os
from datetime import datetime

import requests
import requests_cache
import json

from itv_parser.AvtoSpot.autospot_config import cookies

current_date = datetime.now().strftime("%Y-%m-%d")


# Путь к папке, которую вы хотите создать
folder_path = f"AvtoSpot/auto_spot_{current_date}"

# Проверяем существование папки
if not os.path.exists(folder_path):
    # Если папка не существует, создаем её
    os.makedirs(folder_path)
    print(f"Папка '{folder_path}' успешно создана.")
else:
    print(f"Папка '{folder_path}' уже существует.")


def get_auto_spot():
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6ImUxODRlNWZhZDlkNzk4MjJmMmIyN2UxYzJjNTc5ZTc0YjA3ZGQxMzEiLCJqdGkiOiJlMTg0ZTVmYWQ5ZDc5ODIyZjJiMjdlMWMyYzU3OWU3NGIwN2RkMTMxIiwiaXNzIjoiIiwiYXVkIjoiY2xpZW50LWxrIiwic3ViIjpudWxsLCJleHAiOjE3MDg5NDMwNzUsImlhdCI6MTcwODg1NjY3NSwidG9rZW5fdHlwZSI6ImJlYXJlciIsInNjb3BlIjoiY29tbW9uIn0.CzwG_dOhyfptAg_2K96x4kaf5mzekPuN4083jMKPOS_uAS57562q_07lDWl2GXSU40u74grXXjURkfB91VuJOSJIl_tl1D62j2t6FgEU0Idg9vMOzGwXBtSQl9eHwFvDZDkCnophUsOReK4XzqZMdlJlwaafxB5cCgpQAUHaN9q68Rr3FsILPVz8hu745L5320TSwbmuofCphmX-8DvzBmdq0cfM7_xi-adHo6h-hzwrCAWiEU2Faw0m2HNDgdIpTjY6YRmBuWiL8sz5tRt4k2-lI8ope_Il2PMN7Fj5kEmpOgFBJNzWYHZt7UGgBKld75IOM1hFTOsLERs1kukC_Q'
    }
    session = requests.Session()

    params = {
        'sort': '-percent_discount',
        'limit': '12',
        'page': '1',
        'city_ids[0]': '3',
        # 'radius': '0',
        # 'picture_exp': '1',
    }

    response = session.get('https://api.autospot.ru/rest/filter/cars-with-parallel-import/',
                           verify=False, params=params, headers=headers,
                           ).json()
    print(response)
    page_total = response['meta']['totalCount']
    pages = math.ceil(int(page_total) / response['meta']['perPage'])

    for page in range(1, pages + 1):
        print(f'[INFO] Page {page} of {pages}')
        params = {
            'sort': '-percent_discount',
            'limit': '12',
            f'page': {page},
            'city_ids[0]': '3',
            'radius': '0',
            'picture_exp': '1',
        }

        res = session.get('https://api.autospot.ru/rest/filter/cars-with-parallel-import/',
                          verify=False, params=params, cookies=cookies, headers=headers,
                          ).json()

        cars_dict = list()
        for item in res['items']:
            car_id = item['car_id']
            offer_id = item['offer_id']
            url = item['url']
            brand_name = item['brand_name']
            city_name = item['city_name']
            equipment_group = item['equipment_group']
            body_type_name = item['body_type_name']
            year = item['year']
            color_name = item['color_name']
            prices = item['prices']
            img_url = item['slider']

            cars_dict.append({
                'car_id': car_id,
                'offer_id': offer_id,
                'url': url,
                'brand_name': brand_name,
                'city_name': city_name,
                'equipment_group': equipment_group,
                'body_type_name': body_type_name,
                'year': year,
                'color_name': color_name,
                'prices': prices,
                'picture_url': img_url,
            })

            with open(f'AvtoSpot/auto_spot_{current_date}/auto_{page}.json', 'w', encoding='utf-8') as f:
                json.dump(cars_dict, f, indent=4, ensure_ascii=False)


def main():
    get_auto_spot()


if __name__ == '__main__':
    main()
