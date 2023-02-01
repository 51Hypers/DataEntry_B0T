import os

LOGIN_ID = "8861375355"
LOGIN_PWD = "wasdrqe156!%^f"
URL = "https://jobs.zeetechmanagement.com/Candidate/MyProject.aspx"

PROFILE = {
    "plugins.plugins_list": [{"enabled": False,
                              "name": "Chrome PDF Viewer"}],
    "download.default_directory": f"{os.getcwd()}/",
    "download.extensions_to_open": "",
    "plugins.always_open_pdf_externally": True,
}