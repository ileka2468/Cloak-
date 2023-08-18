import os
import platform
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from subprocess import CREATE_NO_WINDOW


def parseFile(appList):
    inputs = appList
    return inputs


def osIs():
    if platform.system() == "Darwin":
        return "Mac"
    elif platform.system() == "Linux":
        return "Linux"
    elif platform.system() == "Windows":
        return "Windows"


class RewriteAutomate:
    def __init__(self, outputFileName):

        self.currentOs = osIs()
        self.output_file_name = outputFileName
        print(f"Current OS detected: {self.currentOs}")

        # script_dir = os.getcwd()
        #
        # print(f"alleged current working directory: {script_dir}")
        # # default mac output for prod
        # self.output_dir = os.path.join(script_dir, 'Desktop/AutomatorOutput')
        #
        # # running locally in pycharm or windows
        # if devMode:
        #     self.output_dir = f"{script_dir}/DebugOutput"
        #     if not os.path.exists(self.output_dir):
        #         os.mkdir(self.output_dir)
        # else:
        #     if not os.path.exists(self.output_dir):
        #         os.mkdir(self.output_dir)

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-infobars')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.serv = ChromeService(ChromeDriverManager().install())
        self.serv.creationflags = CREATE_NO_WINDOW
        self.LINK = "--REDACTED-FOR-EDUCATIONAL-PURPOSES--"

    def login(self):
        driver = None
        for i in range(4):
            try:
                driver = webdriver.Chrome(service=self.serv, options=self.options)
                driver.get(self.LINK)
                break  # If driver.get() succeeds, exit the loop
            except WebDriverException:
                print("Attempt", i + 1, "failed. Retrying...")
        if driver is None:
            print("Could not launch browser after 4 attempts.")

        if getattr(sys, 'frozen', False):
            Current_Path = os.path.dirname(sys.executable)
        else:
            Current_Path = str(os.path.dirname(__file__))
        file = open(f'{Current_Path}/Info/key.txt', 'r').read().split('\n')
        email = file[1]
        password = file[-1]

        try:
            myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="__next"]/div[2]/section/div/div[2]/div/form/button[1]')))
            print("Attempting to login")
        except NoSuchElementException:
            print('The application failed to log you in, please try again.')
            driver.close()
        emailBox = driver.find_element(By.ID, "signInInput1-1")
        emailBox.click()
        for char in email:
            emailBox.send_keys(char)

        passwordBox = driver.find_element(By.ID, "signInInput1-2")
        passwordBox.click()
        for char in password:
            passwordBox.send_keys(char)

        # click login

        signInButton = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/section/div/div[2]/div/form/button[1]')
        signInButton.click()

        # go to enhancer

        try:
            myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[1]/div/div/div[1]/div/button[2]')))
            print("Checking levels of ai generated content")
        except TimeoutException:
            print("Timed Out checking levels of ai generated content")
            driver.close()

        ehrbutton = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[1]/div/div/div[1]/div/button[2]')
        ehrbutton.click()

        return driver

    def start(self, inputs, driver):
        progress = 0

        for text in inputs:
            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[2]/div/div[1]/div[2]/button')))

            except TimeoutException:
                print("Initializing rewriter")
                driver.close()
            checkButton = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[1]/div/main/div[2]/div/div[1]/div[2]/button')
            textbox = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[2]/div/div[2]/div[2]/div/div/div')
            textbox.click()

            textbox.send_keys(text)
            checkButton.click()

            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[2]/div[1]/div/div[3]/div[1]/strong')))
                driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[2]/div[2]/div[2]/button[1]').click()
            except TimeoutException:
                print("Timed out while processing your request")
                driver.close()

            try:
                while driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/div[1]/div/div'):
                    pass

            except NoSuchElementException:
                print("Rewrite done!")

            newTextbox = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[2]/div[2]/div[1]/div/div[2]/div/div/div')

            # if self.currentOs == "Windows" or self.currentOs == "Linux":
            #     newTextbox.send_keys(Keys.CONTROL + 'a')
            #     newTextbox.send_keys(Keys.CONTROL + 'c')
            # else:
            #     newTextbox.send_keys(Keys.COMMAND + 'a')
            #     newTextbox.send_keys(Keys.COMMAND + 'c')

            # text = pyperclip.paste()

            innerHtmlTextBox = newTextbox.get_attribute('innerHTML')
            print(innerHtmlTextBox)

            soup = BeautifulSoup(innerHtmlTextBox, 'html.parser')

            print(f"Processed: {soup.get_text()}")

            with open(os.path.join(self.output_file_name), 'a') as f:
                f.write(soup.get_text() + "\n\n")

            ehrbutton = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div/main/div[1]/div/div/div[1]/div/button[2]')
            ehrbutton.click()
            progress += 1
            print(f"Progress {progress}/{len(inputs)}")
        driver.close()


if __name__ == '__main__':
    pass
