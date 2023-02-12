import os
import re

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.Consts import *
from src.Form import *


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

    def submitFile(self):
        subm = self.driver.find_element(By.XPATH, '//*[@id="btn_save_bottom"]')
        self.driver.execute_script("arguments[0].click();", subm)
        self.files_completed += 1

    def executeCycle(self):
        self.openFile()
        self.realizeFile()
        self.submitFile()
        self.cycle_filecount +=1
        print(f"Cycle Files done : {self.cycle_filecount}")

    def loopCycle(self):
        try:
            while self.state:
                for _ in range(20):
                    self.executeCycle()
                    time.sleep(10)

                self.cycles +=1
                self.cycle_filecount = 0
                self.state = False
            print(f"Cycles : {self.cycles}")
        except:
            self.regenerateData()

    def regenerateData(self):
        if not self.state:
            print("Regenerating Data")
            b = self.driver.find_element(
                By.XPATH, '//*[@id="btn_get_data"]'
            )
            self.driver.execute_script("arguments[0].click();", b)

        self.state = True
        self.loopCycle()











