from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib import parse
import re
import time
import os
import math
import unicodedata
import sys
import requests


class webdriver_functions(object):
    def __init__(self):
        options = Options()

        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.delete_all_cookies()


    def check_if_xpath_exists(self, xpath, interval=0) -> object:

        time.sleep(interval)
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    def click_on_xpath(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, 100):

            try:
                self.driver.find_element(By.XPATH, xpath).click()
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def count_xpath(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, 100):

            try:
                count = len(self.driver.find_elements(By.XPATH, xpath))
                return count

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def get_text_from_xpath(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                text = self.driver.find_element(By.XPATH, xpath).text
                return text

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def open_website(self, link):

        self.driver.get(link)
        time.sleep(1)

    def send_keys_to_text_box(self, xpath, text, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, 100):

            try:
                text_box = self.driver.find_element(By.XPATH, xpath)
                text_box.send_keys(text)
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def send_enter_key(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, 100):

            try:
                text_box = self.driver.find_element(By.XPATH, xpath)
                text_box.send_keys(Keys.RETURN)
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def get_xpath_attribute(self, xpath, attribute, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, 100):

            try:
                element = self.driver.find_element(By.XPATH, xpath)
                attr = element.get_attribute(attribute)
                return attr

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def switch_tabs(self, tab_index=-1, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, 100):

            try:
                self.driver.switch_to.window(self.driver.window_handles[tab_index])
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def quit_driver(self):

        self.driver.quit()
        return "Driver closed"

    def get_html_of_link(self, link):
        html = requests.get(link)
        return html.text

def latest_download_file_rename(new_name):
    path = r'C:\Users\konra\Downloads'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    try:
        os.rename(f"C:/Users/konra/Downloads/{newest}",
                  f"C:/Users/konra/Downloads/{new_name}.{newest.split(sep='.')[1]}")
    except:
        print(new_name)
        pass
