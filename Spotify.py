from Browser import Browser
from Utils import Utils
from dotenv import load_dotenv
from config import *
import os
from time import sleep
from selenium.common.exceptions import WebDriverException
load_dotenv()

class Spotify():
    
    def __init__(self, url):
        self.url = url
        self.player_status = False
        self.browser = Browser()
        self.start()
        sleep(10)
        self.click_play()

    def start(self):
        if not self.player_status:
            self.player_status = self.__open_and_login()

    def end(self):
        try:
            self.browser.browser.quit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_maximize(self):
        try:
            try:
                self.browser.minimize()
            except:
                pass
            self.browser.maximize()
        except WebDriverException:
            return "closed"
        finally:
            return "other"



    def on_minimize(self):
        self.browser.minimize()
        
    def __open_and_login(self):

        def __login(self):
            self.browser.send(SPOTIFY_LOGIN_INPUT, os.getenv("ACCOUNT_USERNAME"))
            self.browser.send(SPOTIFY_PASSWORD_INPUT, os.getenv("SPOTIFY_PASSWORD"))
            self.browser.click(SPOTIFY_ACCESS_BUTTON)

        try:
            self.browser.open(self.url)
            __login(self)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        else:
            return True

    def click_play(self):
        try:
            self.browser.click(SPOTIFY_PLAY_BUTTON)
            sleep(5)
            self.on_minimize()
        except Exception as e:
            print(f"An error occurred: {e}")
            