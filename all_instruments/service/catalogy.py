import requests
import json

from config import cookies, headers

from typing import Optional
from pydantic import BaseModel


class Param(BaseModel):
    id: Optional[str] = None


def get_json():
    for i in range(1, 33):
        params = Param(id=str(i))
        params_dict = params.dict(exclude_none=True)  # Преобразовать объект Param в словарь
        params_dict.update({'activeRegionId': '1'})  # Добавить дополнительные параметры

        response = requests.get(
            'https://bff.vseinstrumenti.ru/api/catalog/categories',
            params=params_dict, cookies=cookies, headers=headers
        ).json()
        if response:  # Проверяем наличие данных в ответе
            with open(f'data/data_json_{i}.json', 'w', encoding='utf-8') as outfile:
                json.dump(response, outfile, ensure_ascii=False, indent=4)

        print(f"[INFO] Page {i} of {33} complete")


def main():
    get_json()


if __name__ == '__main__':
    main()
