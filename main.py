from src.Consts import LOGIN_ID,LOGIN_PWD,URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.Zeetech import *


def main():
    z = Zeetech()
    z.login(LOGIN_ID,LOGIN_PWD)


if __name__ == '__main__':
    main()
