import difflib
import os.path
import re

import easyocr
from pdf2image import convert_from_path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from src.Consts import *
from src.Utils import *


class Form:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.form = self.driver.find_element(
            By.XPATH, '//form/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]'
        )

        self.pdfpath = ""           # Path to PDF
        self.pagepath = ""          # Path to Converted Page

        self.form_labels = self.getFormLabels()
        self.input_IDs = self.getInputIDs("input")
        self.select_IDs = self.getInputIDs("select")
        self.textarea_IDs = self.getInputIDs("textarea")

        self.pdf_values = []        # Values from PDF

        self.mapped_payload = {}     # Dict mapping PDF Values to Form Labels
        self.mapped_ids = {}

    def getPdf(self):
        """
        Download the PDF linked to the form.

        :return: None
        """

        if os.path.isfile(DWD+"ReadPDFStream.pdf"):
            print("PDF already exists, deleting")
            os.remove(DWD + "ReadPDFStream.pdf")

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

        labeldivs = self.form.find_elements(By.XPATH, '//div[@class="col-sm-4"]')

        return [
            label.find_element(By.TAG_NAME, "label").text[3:-1]
            for label in labeldivs[:-1]
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
        Utils.uniquify(self.pdf_values)

        a = ['Applicant', 'Application']
        if any(ext in self.pdf_values[0] for ext in a):
            self.pdf_values = list(map(lambda x: x.replace('Address1', 'Applicant Address'), self.pdf_values))
            self.pdf_values = list(map(lambda x: x.replace('Address2', 'Business Address'), self.pdf_values))
        else:
            self.pdf_values = list(map(lambda x: x.replace('Address2', 'Applicant Address'), self.pdf_values))
            self.pdf_values = list(map(lambda x: x.replace('Address1', 'Business Address'), self.pdf_values))

        for i in self.pdf_values:
            x = self.pdf_values.index(i)
            if i[-1] == "1" and i not in [' Date of Establishment', 'License No.', 'Mobile No.']:
                self.pdf_values[x] = i[:-1]

        n = self.pdf_values.index("Name")
        self.pdf_values[n] = "Applicant Name"

        # Loop to truncate the values list to implement get() function

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

    def generateIDDict(self):
        cleaned_labels = Utils.cleanList(self.form_labels, "label")
        for element in cleaned_labels:
            cleanedinput = Utils.cleanList(self.input_IDs, "input")
            inputvar = difflib.get_close_matches(
                element, cleanedinput, 1, 0.7
            )

            cleanedselect = Utils.cleanList(self.select_IDs, "select")
            selectvar = difflib.get_close_matches(
                element, cleanedselect, 1, 0.7
            )

            print(f"text area ids = {self.textarea_IDs} \n")

            cleanedtextarea = Utils.cleanList(self.textarea_IDs, "textarea")

            print(f"cleaned text area ids = {cleanedtextarea} \n")
            print(f"element : {element}")
            textvar = difflib.get_close_matches(
                element, cleanedtextarea, 1, 0.7
            )
            print(f"text var = {textvar} \n")
            try:
                self.mapped_ids.update(
                    {self.form_labels[cleaned_labels.index(element)]: self.input_IDs[cleanedinput.index(inputvar[0])]}
                )
                self.mapped_ids.update(
                    {self.form_labels[cleaned_labels.index(element)]: self.select_IDs[cleanedselect.index(selectvar[0])]}
                )
                self.mapped_ids.update(
                    {self.form_labels[cleaned_labels.index(element)]: self.textarea_IDs[cleanedtextarea.index(textvar[0])]}
                )
            except IndexError:
                continue

        # * Correct the Final Params
        d = self.select_IDs + self.input_IDs + self.textarea_IDs
        for ele in self.form_labels:
            x = difflib.get_close_matches(ele, d, 2, 0.3)
            self.mapped_ids.update({ele: x[0]})

        # ? Predefining for now, find some way to not for later
        self.mapped_ids.update({'Name of Business': 'txt_business_name'})

    def generatePayload(self):
        cleaned_labels = Utils.cleanList(self.form_labels,"label")
        cleaned_pdfval = Utils.cleanList(self.pdf_values, "values")
        for element in cleaned_labels:
            var = difflib.get_close_matches(element, Utils.cleanList(self.pdf_values, "values"), 1, 0.7)

            self.mapped_payload.update(
                {self.form_labels[cleaned_labels.index(element)]: self.pdf_values[cleaned_pdfval.index(var[0]) + 1]}
            )

        for i in self.mapped_payload.keys():
            d = self.mapped_payload.get(i)

            if i == "Applicant Address":
                if "street name" in d.casefold():
                    d = d[0:d.casefold().index("street name")]
                    self.mapped_payload.update({i: d})

                if "email id" in d.casefold():
                    d = d[0:d.casefold().index("email id")]
                    self.mapped_payload.update({i: d})

            if i == " Date of Establishment" and len(d) > 10:
                d = d[:-1]
                self.mapped_payload.update({i: d})

            if i == 'License No.' and len(d) > 17:
                d = d[:-1]
                self.mapped_payload.update({i: d})

            if i == 'Mobile No.' and len(d) > 10:
                d = d[:-1]
                self.mapped_payload.update({i: d})

        for ele in self.form_labels:
            param_value_check = self.mapped_payload[ele]

            if ele.strip() == "Applicant Name":
                if ele[-1::].isnumeric():
                    self.mapped_payload.update({ele: param_value_check.replace(ele[-1::], "")})

            # ! Is Buisness the Right thing
            # TODO : Change to correct spelling later if not right

            if ele.strip() == "Buisness Name":
                if ele[-1::].isnumeric():
                    self.mapped_payload.update({ele: param_value_check.replace(ele[-1::], "")})

            if ele.strip() == "Applicant Address":
                if ele[-1::].isnumeric():
                    self.mapped_payload.update({ele: param_value_check.replace(ele[-1::], "")})

            # ! Is Buisness the Right thing

            if ele.strip() == "Buisness Address":
                if ele[-1::].isnumeric():
                    self.mapped_payload.update({ele: param_value_check.replace(ele[-1::], "")})

        # * Replace - with /
        for i in self.form_labels:
            if i.strip() == "Date of Establishment":
                self.mapped_payload.update({i: self.mapped_payload[i].replace('-', '/')})

    def enterPayload(self):
        for i in self.form_labels:
            param_id = self.mapped_ids[i]
            param_value = self.mapped_payload[i]

            self.driver.find_element(By.ID, param_id).send_keys(param_value)

            if (i.strip() in "Total Area (Sq.Ft.)"):
                param_id = self.mapped_ids[i]
                param_value = int(self.mapped_payload[i])
                drop_down = Select(self.driver.find_element(By.ID, param_id))
                if param_value <= 250:
                    drop_down.select_by_index(0)
                elif (param_value > 250 and param_value <= 500):
                    drop_down.select_by_index(1)
                elif (param_value > 500 and param_value <= 750):
                    drop_down.select_by_index(2)
                elif (param_value > 750 and param_value <= 1000):
                    drop_down.select_by_index(3)
                elif (param_value > 1000 and param_value <= 1500):
                    drop_down.select_by_index(4)
                elif (param_value > 1500 and param_value <= 2000):
                    drop_down.select_by_index(5)
                elif (param_value > 2000):
                    drop_down.select_by_index(6)

            # This loop is for APPLICATION TYPE having a select tag in the framework
            if i.strip() == "Application Type":
                param_id = self.mapped_ids[i]
                param_value = self.mapped_payload[i].casefold()
                drop_down = Select(self.driver.find_element(By.ID, param_id))
                if "license" in param_value:
                    drop_down.select_by_index(0)
                elif "renew" in param_value:
                    drop_down.select_by_index(1)

            # This loop is for the FIRM TYPE having a select tag in the framework
            if i.strip() == "Firm Type":
                param_id = self.mapped_ids[i]
                param_value = self.mapped_payload[i].casefold()
                drop_down = Select(self.driver.find_element(By.ID, param_id))
                if "proprie" in param_value:
                    drop_down.select_by_index(0)
                elif "partner" in param_value:
                    drop_down.select_by_index(1)
                elif "ngo" in param_value:
                    drop_down.select_by_index(2)
                elif "opc" in param_value:
                    drop_down.select_by_index(3)
                elif "private" in param_value:
                    drop_down.select_by_index(4)
                elif "public" in param_value:
                    drop_down.select_by_index(5)
                else:
                    drop_down.select_by_index(6)

            # This loop is for the TYPE OF OWNERSHIP select tag
            if i.strip() == "Type of Ownership of Business Premises":
                param_id = self.mapped_ids[i]
                param_value = self.mapped_payload[i].casefold()
                drop_down = Select(self.driver.find_element(By.ID, param_id))
                if "rent" in param_value:
                    drop_down.select_by_index(0)
                elif "lease" in param_value:
                    drop_down.select_by_index(1)
                elif "own" in param_value:
                    drop_down.select_by_index(2)

            # This loop is there to data that is there in the data txt area so that it can be re-entered as payload
            if i.strip() == "Date of Establishment":
                date_button = self.driver.find_element(By.ID, param_id)
                for _ in range(20):
                    date_button.send_keys(Keys.BACKSPACE)
                date_button.send_keys(param_id, param_value)






