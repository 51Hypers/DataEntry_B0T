import difflib
import re

import easyocr
from pdf2image import convert_from_path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.Consts import *
from webdriver_manager.chrome import ChromeDriverManager


class Form:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.form = self.driver.find_element(
            By.XPATH, '//form/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]'
        )

        self.pdfpath = ""           # Path to PDF
        self.pagepath = ""          # Path to Converted Page

        self.pdf_values = []        # Values from PDF
        self.mapped_values = {}     # Dict mapping PDF Values to Form Labels

    def getPdf(self):

        """
        Download the PDF linked to the form.

        :return: None
        """

        pdflink = self.driver.find_element(By.XPATH, "//object").get_attribute("data")
        (
            self.driver.get(
                pdflink
            )
        )
        self.pdfpath = DWD + "ReadPDFStream.pdf"

    def getFormLabels(self):

        """
        Get all the Labels of the form.

        :return: List of form labels
        """

        labeldivs = self.form.find_elements(By.XPATH, "//div[@class='col-sm-4")

        return [
            label.find_element(By.TAG_NAME, "label").text[3:-1]
            for label in labeldivs
        ]

    def readPDF(self):

        """
        Get all values from the PDF.

        :return: Nothing
        """
        images = convert_from_path(self.pdfpath)
        images[0].save(DWD + "page.jpg", "JPEG")
        self.pagepath = DWD + "page.jpg"

        reader = easyocr.Reader(['en'])
        res = reader.readtext(self.pagepath, paragraph="False")
        self.pdf_values = [i[1] for i in res]

    def getInputIDs(self, element: str):

        """
        Return a list of either the SELECT IDs, INPUT IDs, or TEXTAREA IDs.

        :param element: ID Type to be returned
        :return: list of IDs
        """

        if element not in FORMINPUTS:
            raise ValueError("Element must be one of %r" % FORMINPUTS)

        return [
            i.get_attribute("id") for i in self.form.find_elements(
                By.XPATH, f'//div/div[@class="form-group"]//{element}'
            )
        ]

    def generateInitialDict(self):
        for i in self.getFormLabels():
            for j in self.pdf_values:
                if i == j:
                    self.mapped_values.update(
                        {i: self.pdf_values[self.pdf_values.index(i) + 1]}
                    )

    def generateFinalDict(self):
        for element in self.pdf_values:
            inputvar = difflib.get_close_matches(
                element, self.cleanList(self.pdf_values), 1, 0.7
            )
            selectvar = difflib.get_close_matches(
                element, self.cleanList(

                ), 1, 0.7
            )

