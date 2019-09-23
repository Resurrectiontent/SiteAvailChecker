from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SiteChecker:

    _USERNAME = 'st035540'
    _PASSWORD = 'X8YemZRn'

    def __init__(self, url):
        self.URL = url
        self._browser = webdriver.Firefox()

    def check_site(self):
        self._browser.get(self.URL)
        try:
            WebDriverWait(self._browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'div'))
            )
            un = self._browser.find_element_by_xpath('//input[@id="username"]')
            pw = self._browser.find_element_by_xpath('//input[@id="password"]')

            un.send_keys(self._USERNAME)
            un.send_keys(Keys.TAB)
            pw.send_keys(self._PASSWORD)
            pw.send_keys(Keys.RETURN)

            WebDriverWait(self._browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@value="Искать"]'))
            )
            self._browser.close()
            return True
        except:
            return False
