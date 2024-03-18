import requests

cookies = {
    'stickounet': '1708265233.115.17696.916034|db2cac49ccc998c0c6912941ae0ac4e1',
    'siteCityCode': 'msk',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://avtodom.ru/cars/used/',
    'Connection': 'keep-alive',
    # 'Cookie': 'stickounet=1708265233.115.17696.916034|db2cac49ccc998c0c6912941ae0ac4e1; siteCityCode=msk',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'DNT': '1',
    'Sec-GPC': '1',
}

