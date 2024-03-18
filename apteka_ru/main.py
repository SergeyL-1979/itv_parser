import csv
import time
from itertools import chain

import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_stealth import stealth

from fake_useragent import UserAgent


ua = UserAgent()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--disable-blink-features=AutomationControlled')

# run in headless mode = фоновый режим запуска браузера
# options.add_argument("--headless")
# disable the AutomationControlled feature of Blink rendering engine
options.add_argument('--disable-blink-features=AutomationControlled')
# disable pop-up blocking
options.add_argument('--disable-popup-blocking')
# start the browser window in maximized mode
options.add_argument('--start-maximized')
# disable extensions
options.add_argument('--disable-extensions')
# disable sandbox mode
options.add_argument('--no-sandbox')
# disable shared memory usage
options.add_argument('--disable-dev-shm-usage')
# options.add_argument(f'user-agent={ua.random}')

driver = uc.Chrome(headless=True, use_subprocess=False)
# driver = webdriver.Chrome(options=options, )

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.random})

stealth(driver,
        user_agent=ua.random,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


def get_data_selenium():
    try:
        print("Вызов URL")
        driver.get(url="https://apteka.ru/category/orvi/antiviral_action/")
        # driver.get(url='https://nowsecure.nl')
        # driver.get(url='https://exchange.konomik.com/authorization/login')
        time.sleep(5)
        driver.save_screenshot('nowsecure.png')
        time.sleep(5)

        get_html = driver.page_source
        with open("nowsecure.html", "w", encoding="utf-8") as f:
            f.write(get_html)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        print("Сбор закончен")


def get_data_html():
    with open("nowsecure.html", "r", encoding="utf-8") as f:
        data_html = f.read()

    soup = BeautifulSoup(data_html, "html.parser")
    cards_product = soup.find_all("div", class_="catalog-card card-flex")

    # links_list = list()
    with open("links_list.txt", "w", encoding="utf-8", newline='') as f:
        for card in cards_product:
            card_photo = card.find('a', class_='catalog-card__photos').get('href')
            # links_list.append(card_photo)
            f.write(f"{card_photo}\n")


def main():
    # get_data_selenium()
    get_data_html()


if __name__ == '__main__':
    main()
