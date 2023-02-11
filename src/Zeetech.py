#  Imports

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from src.Consts import *
from webdriver_manager.chrome import ChromeDriverManager
from src.Project import *


class Zeetech:
    def __init__(self):
        print("Init started")
        self.driver = self._get_driver()
        self.driver.get(URL)
        self.driver.implicitly_wait(5)

        self._currentpage = "Login"

    @staticmethod
    def navigate(self, link : str):
        pass

    def _get_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", PROFILE)
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        return driver

    def navigate(self,page: str):
        pass
        #self.driver.get()

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
        self._currentpage = "DailyAttendance"

    def start_project(self):
        # Click MyProjects Button
        (
            self.driver
            .execute_script(
                "arguments[0].click();",
                self.driver.find_element(By.XPATH, "//a[@href='MyProject.aspx']")
            )
        )
        self._currentpage = "MyProject"

        filecount = int(self.driver.find_element(
            By.XPATH, "//div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[4]/span"
        ).get_attribute("innerHTML"))

        self.driver.find_element(
            By.XPATH, "//div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[8]/a[1]"
        ).click()

        p = Project(self.driver, filecount)

        #  ! Ignore later
        view_file_button = self.driver.find_element(
            By.XPATH, "//div[4]/div[2]/div/div[2]/div/div[2]/div/div/table/tbody/tr[1]/td[2]/a")

        self.driver.execute_script("arguments[0].click();", view_file_button)

        #
        




