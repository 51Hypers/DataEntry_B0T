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
    def __init__(self, driver : webdriver.Chrome):
        self.driver = driver
        self.form = self.driver.find_element(
            By.XPATH, "//form/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]"
        )

    def get