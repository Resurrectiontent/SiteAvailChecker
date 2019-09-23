from itertools import combinations
from random import choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize(url):
    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get(url)
    return browser


def login(browser, login, password):
    un = browser.find_element_by_xpath('//input[@id="username"]')
    pw = browser.find_element_by_xpath('//input[@id="password"]')
    
    un.send_keys(login)
    un.send_keys(Keys.TAB)
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)

def ini_page(browser, wait):
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'div'))
    )
    for i in range(wait):
        print(i)
        time.sleep(1)
    return browser.find_elements_by_tag_name('div')

def click_all(browser):
    wait = 5
    to_click = 1
    while not len(browser.find_elements_by_xpath('//h2[@class="traceback"]')):
        context = ini_page(browser, wait)
        wait = 5
        to_click = choice(context)
        try:
            to_click.click()
            tabs = browser.current_window_handle()
            browser.switch_to_window(browser.window_handles[5])
        except:
            wait = 0
            pass
    err_el = [x for x in to_click]
    raise Exception('Error clicking element: {0}'.format(err_el))

if __name__ == '__main__':
    browser = initialize(r'http://v.dltc.spbu.ru:5000')
    login(browser, 'st035540', 'X8YemZRn')

    click_all(browser)