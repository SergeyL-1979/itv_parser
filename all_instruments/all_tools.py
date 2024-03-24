import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth

from fake_useragent import UserAgent

useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
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

driver = webdriver.Chrome(options=options, )
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": useragent.random})

stealth(driver,
        user_agent=useragent.random,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


def get_all_tools():
    try:
        print("Вызов URL")
        # TODO = Сделать пагинацию по страницам
        driver.get(url="https://www.vseinstrumenti.ru/category/akkumulyatornyj-instrument-2392/page1/")
        time.sleep(10)

        get_html = driver.page_source
        with open("all_page.html", "w", encoding="utf-8") as f:
            f.write(get_html)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        print("Сбор закончен")


def get_all_data_html():
    with open("all_page.html", "r", encoding="utf-8") as f:
        data_html = f.read()

    soup = BeautifulSoup(data_html, "html.parser")
    cards_product = soup.find_all("div", attrs={"data-qa": "products-tile"})

    list_product = list()
    for card in cards_product:
        code_product = card.find("p").text.strip().replace("код: ", "")
        link_product = card.find("a", attrs={"data-qa": "product-name"}).get("href")
        name_product = card.find("a", attrs={"data-qa": "product-name"}).text.strip()
        price_product = card.find("p", attrs={"data-qa": "product-price-current"}).text.strip().replace("\xa0", " ")
        list_product.append({
            "Артикул": code_product,
            "Ссылка": link_product,
            "Наименование": name_product,
            "Цена товара": price_product,
        })

    # print(list_product)
    with open("all_data.json", "w", encoding="utf-8") as file:
        json.dump(list_product, file, ensure_ascii=False, indent=4)


def main():
    get_all_tools()
    get_all_data_html()


if __name__ == '__main__':
    main()
