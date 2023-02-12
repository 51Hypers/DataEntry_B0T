import difflib
import os
import re

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

    # ? What should the Project class be handling?











