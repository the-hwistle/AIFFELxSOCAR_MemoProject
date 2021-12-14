from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time


class Google_Crawler:
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

    def get_page_soup(self, url):
        self.driver.get(url)

        page_html = self.driver.page_source
        page_soup = BeautifulSoup(page_html, "html.parser")

        return page_soup

    def search(self, word):
        url = f"https://www.google.com/search?q={quote_plus(word)}"
        page_soup = self.get_page_soup(url)
        result = []
        g_tags = page_soup.select(".g")

        if g_tags == None or len(g_tags) == 0:
            self.driver.quit()
            time.sleep(2)
            self.reset_driver()
            time.sleep(2)

        for g in g_tags:
            if g.find("div", attrs={"class": "LC20lb"}):
                result.append(g.select_one(".LC20lb").text.strip())  # 타이틀
            if g.find("div", attrs={"class": "VwiC3b"}):
                result.append(g.select_one(".VwiC3b").text.strip())  # 내용

        return result

    def search_highlighted(self, word):
        url = f"https://www.google.com/search?q={quote_plus(word)}"
        page_soup = self.get_page_soup(url)
        modifier = page_soup.select_one("a.gL9Hy")

        if modifier:
            word = modifier.text
            url = f"https://www.google.com/search?q={quote_plus(word)}"
            page_soup = self.get_page_soup(url)

        data = page_soup.find_all("em")
        if not data:
            self.driver.quit()
            sleep(3)
            self.reset_driver()
            return self.search_highlighted(word, True)

        result = []
        for element in data:
            result.extend(element.text.split())

        return result, word
