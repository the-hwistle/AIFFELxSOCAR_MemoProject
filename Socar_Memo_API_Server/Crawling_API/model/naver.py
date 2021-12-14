from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time


class Naver_Crawler:
    def __init__(self, implicitly_wait_time=10):
        self.implicitly_wait_time = implicitly_wait_time
        self.reset_driver()

    def reset_driver(self):
        print("reset driver!")

        chrome_driver_path = os.path.join(os.getcwd(), "chromedriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
        self.driver.implicitly_wait(self.implicitly_wait_time)

    def search(self, word):
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={quote_plus(word)}"
        self.driver.get(url)

        page_html = self.driver.page_source
        page_soup = BeautifulSoup(page_html, "html.parser")
        result = []

        total_tit = page_soup.select(".total_tit")

        if total_tit == None or len(total_tit) == 0:
            self.driver.quit()
            time.sleep(2)
            self.reset_driver()
            time.sleep(2)

        api_txt_lines = page_soup.select(".api_txt_lines")

        if api_txt_lines == None or len(api_txt_lines) == 0:
            self.driver.quit()
            time.sleep(2)
            self.reset_driver()
            time.sleep(2)

        for total_tit in total_tit:
            result.append(total_tit.text.strip())

        for api_txt_lines in page_soup.select(".api_txt_lines"):
            result.append(api_txt_lines.text.strip())

        return result
