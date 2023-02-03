import os

CWD = os.getcwd() + os.path.sep
DWD = os.getcwd() + os.path.sep + "data" + os.path.sep

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

ROUTER = {
    "Login" : "",
    "MyProject" : "",
    "DataFiles" : "",
    }