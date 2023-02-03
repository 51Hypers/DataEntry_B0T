import os
import easyocr
from pdf2image import convert_from_path


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.Consts import *
from webdriver_manager.chrome import ChromeDriverManager

'''
Project -> 
'''

class Project:
    def __init__(self,driver: webdriver.Chrome, filecount: int):
        self.driver = driver
        self.filecount = filecount

        self.pdfpath = ""
        self.pagepath = ""

        self.form_labels = []
        self.pdf_values = []
        self.mapped_values = {}

    def getPdf(self):
        # Download pdf
        pdflink = self.driver.find_element(By.XPATH, "//object").get_attribute("data")
        (
            self.driver.get(
                pdflink
            )
        )
        self.pdfpath = DWD + "ReadPDFStream.pdf"

    def getFormLabels(self):
        #Get the form
        form = self.driver.find_element(
            By.XPATH, "//form/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]"
        )
        labeldivs = form.find_elements(By.XPATH, "//div[@class='col-sm-4")

        self.form_labels = [label.find_element(By.TAG_NAME, "label").text[3:-1] for label in labeldivs]


    def readPDF(self):
        images = convert_from_path(self.pdfpath)
        images[0].save(DWD + "page.jpg", "JPEG")
        self.pagepath = DWD + "page.jpg"

        reader = easyocr.Reader(['en'])
        res = reader.readtext(self.pagepath, paragraph="False")
        values = [i[1] for i in res]

    def validateParams(self):
        pass