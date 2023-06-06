import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class ScrapUtils:

    @staticmethod
    def scroll_max(driver):
        SCROLLS = 0
        SCROLL_PAUSE_TIME = 1

        while SCROLLS < 32:
            driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
            time.sleep(SCROLL_PAUSE_TIME)
            SCROLLS += 1

    @staticmethod
    def clicks(driver):
        counts = 0
        SCROLL_PAUSE_TIME = 8

        ScrapUtils.accept_cookie(driver)

        while counts < 10:
            el = driver.find_element(By.CSS_SELECTOR, 'div.topic__loadmore__2s1t0').find_element(By.TAG_NAME, 'button')
            el.click()
            time.sleep(SCROLL_PAUSE_TIME)
            counts += 1

    @staticmethod
    def accept_cookie(driver):
        try:
            el = driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
            el.click()
        except:
            pass
