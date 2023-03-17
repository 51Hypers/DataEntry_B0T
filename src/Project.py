import time
import random

from src.Form import *
from selenium.webdriver.common.alert import Alert

class Project:
    def __init__(self,driver: webdriver.Chrome, filecount: int):
        self.driver = driver
        self.total_filecount = filecount
        self.files_completed = 0
        self.cycles = 0
        self.cycle_filecount = 0
        self.state = True

    def openFile(self):
        viewfile = self.driver.find_element(
            By.XPATH, "//*[@id='div_data_file']/tr[1]/td[2]/a"
        )

        self.driver.execute_script("arguments[0].click();", viewfile)

    def realizeFile(self):
        p = Form(self.driver)

        print("Creating A Form")

        p.getPdf()
        print("Got PDF")

        time.sleep(3)

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
        print("validating")
        p.validateForm()

    def submitFile(self):
        subm = self.driver.find_element(By.XPATH, '//*[@id="btn_save_bottom"]')
        self.driver.execute_script("arguments[0].click();", subm)
        self.files_completed += 1

    def executeCycle(self):
        self.openFile()
        self.realizeFile()
        pause = random.randint(12,19)
        time.sleep(pause)
        self.submitFile()
        self.cycle_filecount +=1
        print(f"Cycle Files done : {self.cycle_filecount}")

    def loopCycle(self):
        try:
            for _ in range(20):
                self.executeCycle()
                time.sleep(3)

            self.cycles +=1
            self.cycle_filecount = 0
            self.state = False
            print(f"Cycles : {self.cycles}")
        except:
            self.state = False
            self.regenerateData()

    def regenerateData(self):
        if not self.state:
            print("Regenerating Data")
            b = self.driver.find_element(
                By.XPATH, '//*[@id="btn_get_data"]'
            )
            self.driver.execute_script("arguments[0].click();", b)
            print("Accepting Alert")
            Alert(self.driver).accept()


        self.state = True
        print("Data regenerated")
        print("Looping cycle")

        self.loopCycle()
