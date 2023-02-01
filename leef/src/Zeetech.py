#  Imports

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.consts import *
from webdriver_manager.chrome import ChromeDriverManager


class Zeetech:
    def __init__(self):
        print("Init started")
        self.driver = self._get_driver()
        self.driver.get(URL)
        self.driver.implicitly_wait(5)

        self.currentpage = ""


    def _get_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", PROFILE)
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        return driver

    def login(self, loginid: str, loginpwd: str):
        # Login ID

        self.driver.find_element(By.ID, "txt_user").send_keys(loginid)
        print("Entered login id")

        # Login PWD
        self.driver.find_element(By.ID, "txt_pass").send_keys(loginpwd)
        print("Entered login password")

        # Accept Cookies
        self.driver.find_element(By.ID, "chk_accept_cookie_policy").click()
        self.driver.find_element(By.ID, "btn_log").click()

        print("Logged in")

    def start_project(self):
        # Click MyProjects Button
        (

        )


