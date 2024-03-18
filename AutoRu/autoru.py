import requests
from bs4 import BeautifulSoup

from itv_parser.AutoRu.config import cookies, headers


def autoru(url, cookies, headers):
    # r = requests.get(url)

    response = requests.get(url=url, cookies=cookies, headers=headers).text
    with open('auto.html', 'w', encoding='utf-8') as file:
        file.write(response)


# def get_html():
    soup = BeautifulSoup(response, 'html.parser')
    url_link = soup.find_all('div', class_='ListingItemExp__snippet-JkcCW')
    for link in url_link:
        print(link.find('a').get('href'))


def main():
    autoru('https://auto.ru/moskovskaya_oblast/cars/all/engine-electro/', cookies=cookies, headers=headers)


if __name__ == '__main__':
    main()
