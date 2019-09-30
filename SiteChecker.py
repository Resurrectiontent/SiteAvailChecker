import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SiteChecker:

    _USERNAME = 'st035540'
    _PASSWORD = 'X8YemZRn'
    _SAFE_URL = r'https://www.random.org'
    browser = ''

    @staticmethod
    def check_connection():
        """Checks internet connection by accessing to random.org"""

        timer = time.time()
        while True:
            try:
                SiteChecker.browser = webdriver.Firefox()
                SiteChecker.browser.get(SiteChecker._SAFE_URL)
                WebDriverWait(SiteChecker.browser, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="True Random Number Service"]'))
                )
                return {'value': True, 'cause': 'Internet connected.'}
            except:
                SiteChecker.browser.close()
                if time.time() - timer >= 75:
                    return {'value': False, 'cause': 'Internet connection timeout.'}
                else:
                    pass

    @staticmethod
    def check_site(url):
        """Checks workability of given site"""
        is_connected = SiteChecker.check_connection()
        if is_connected['value']:
            try:
                SiteChecker.browser.get(url)
                WebDriverWait(SiteChecker.browser, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="username"]'))
                )
                un = SiteChecker.browser.find_element_by_xpath('//input[@id="username"]')
                pw = SiteChecker.browser.find_element_by_xpath('//input[@id="password"]')

                un.click()
                un.send_keys(SiteChecker._USERNAME)
                un.send_keys(Keys.TAB)
                pw.send_keys(SiteChecker._PASSWORD)
                pw.send_keys(Keys.RETURN)

                WebDriverWait(SiteChecker.browser, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Оценка"]'))
                )
                SiteChecker.browser.close()
                return {'value': True, 'cause': ''}
            except:
                SiteChecker.browser.close()
                return {'value': False, 'cause': 'Server answer failure.'}
        else:
            return is_connected

    @staticmethod
    def onclose():
        """Emergency closes webdriver"""
        try:
            SiteChecker.browser.close()
            SiteChecker.browser.quit()
        except:
            pass
