#  Imports
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from src.Consts import *
from webdriver_manager.chrome import ChromeDriverManager
from src.Project import *
from src.Utils import *
from src.Form import *


class Zeetech:
    def __init__(self):
        print("Init started")
        self.driver = Utils.get_driver()
        self.driver.get(URL)
        self.driver.implicitly_wait(5)

        self._currentpage = "Login"

    def navigate(self, page: str):
        pass
        # self.driver.get()

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
        # * Click MyProjects Button
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

        proj = Project(self.driver, filecount)

        # TODO : INTEGRATE INTO PROJECT CLASS TO BE ABLE TO DO MULTIPLE FILES
        viewfile = self.driver.find_element(
            By.XPATH, "//*[@id='div_data_file']/tr[1]/td[2]/a"
        )

        self.driver.execute_script("arguments[0].click();", viewfile)

        p = Form(self.driver)

        print("Creating A Form")

        p.getPdf()
        print("Got PDF")

        time.sleep(5)

        print("Reading PDF")
        p.readPDF()
        print("Finished Reading PDF")

        print("generating IDs")
        p.generateIDDict()

        print("generatign payload")
        p.generatePayload()

        print("\n")
        print(p.mapped_payload)

        print("Entering Payload")
        p.enterPayload()

        subm = self.driver.find_element(By.XPATH, '//*[@id="btn_save_bottom"]')
        self.driver.execute_script("arguments[0].click();", subm)



