import os

CWD = os.getcwd() + os.path.sep
DWD = os.getcwd() + os.path.sep + "data" + os.path.sep

WINDRIVER = DWD + "drivers/chromedriver_win32/chromedriver.exe"
UXDRIVER = DWD + "drivers/chromedriver_linux64/chromedriver"


LOGIN_ID = "8861375355"
LOGIN_PWD = "wasdrqe156!%^f"
URL = "https://jobs.zeetechmanagement.com/Candidate/MyProject.aspx"

PROFILE = {
    "plugins.plugins_list": [{"enabled": False,
                              "name": "Chrome PDF Viewer"}],
    "download.default_directory": os.getcwd()+os.path.sep+"data",
    "download.extensions_to_open": "",
    "plugins.always_open_pdf_externally": True,
}

FORMINPUTS = [
    'input',
    'select',
    'textarea'
]

ROUTER = {
    "Login" : "",
    "MyProject" : "",
    "DataFiles" : "",
    }


PARAMS = {
    "values": 0,
    "label": 0,
    "select": 2,
    "input": 3,
    "textarea": 3
}
