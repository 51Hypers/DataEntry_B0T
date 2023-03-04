#  Imports

from selenium.webdriver.common.alert import Alert

from src.Form import *
from src.Project import *


class Zeetech:
    def __init__(self):
        print("Init started")
        self.driver = Utils.get_driver()
        self.driver.get(URL)
        self.driver.implicitly_wait(15)

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

    def navigatetoProj(self):
        # * Click View File
        Viewfilebutton = self.driver.find_element(By.XPATH, '//*[@id="grdv_project_link_view_file_0"]')

        self.driver.execute_script("arguments[0].click();",Viewfilebutton)

    #     # * Click MyProjects Button
    #     try:
    #         (
    #             self.driver
    #             .execute_script(
    #                 "arguments[0].click();",
    #                 self.driver.find_element(By.XPATH, "//a[@href='MyProject.aspx']")
    #             )
    #         )
    #         self._currentpage = "MyProject"
    #     except:
    #         attendance_button = self.driver.find_element(
    #             By.XPATH,
    #             "/html/body/form/div[4]/div[2]/div/div[2]/div/div[1]/div/div[1]/input"
    #         )
    #         self.driver.execute_script("arguments[0].click();", attendance_button)
    #         alert = Alert(self.driver)
    #         alert.accept()
    #         (
    #             self.driver
    #             .execute_script(
    #                 "arguments[0].click();",
    #                 self.driver.find_element(By.XPATH, "//a[@href='MyProject.aspx']")
    #             )
    #         )
    #         self._currentpage = "MyProject"

    def startProject(self):
        filecount = int(self.driver.find_element(
            By.XPATH, "//div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[4]/span"
        ).get_attribute("innerHTML"))

        self.driver.find_element(
            By.XPATH, "//div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[8]/a[1]"
        ).click()

        proj = Project(self.driver, filecount)
        proj.loopCycle()






