import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Browser():
    # Class to control the browser

    # Constructor
    def __init__(self):
        chrome_install = ChromeDriverManager().install()
        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
        self.service = webdriver.ChromeService(chromedriver_path)
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches",["enable-automation"])
        self.options.add_extension('./_internal/src/extensions/Buster-Captcha-Solver.crx')
        self.options.add_extension('./_internal/src/extensions/hCaptcha-Solver.crx')
        self.browser = None
        self.browser_process = "chrome.exe"

    # Function to open the browser
    def open(self, url: str):
        try:
            self.browser = webdriver.Chrome(service=self.service, options=self.options)
            self.browser.get(url)
            self.browser.execute_script("window.focus();")
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            return True
        finally:
            pass

    def change_url(self, url):
        try:
            self.browser.get(url)
        except Exception as e:
            print(f"An error occurred: {e}")     

    def maximize(self):
        self.browser.maximize_window()

    def minimize(self):
        self.browser.minimize_window()
            

    # Function to close the browser
    def close(self):
        try:
            self.browser.quit()
            self.browser.close()
            self.browser = None
        except Exception as e:
            print(f"An error occurred: {e}")
    # Function to send text to an element by xpath
    def send(self, xpath: str, text: str):
        print(f"Sending {text} to {xpath}")
        self.browser.find_element('xpath', fr'{xpath}').send_keys(text)
        

    # Function to receive an element by xpath
    def receive(self, xpath: str):
        return self.browser.find_element('xpath', xpath)

    # Function to click on an element by xpath
    def click(self, xpath: str):
        print(f"Clicking on {xpath}")
        self.browser.find_element('xpath', xpath).click()