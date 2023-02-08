import os
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
import pdb
from pdf2image import convert_from_path
import os
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
from pdf2image.exceptions import PDFPageCountError
import re
import difflib
from collections import Counter 
from itertools import tee, count
import tempfile

URL = "https://jobs.zeetechmanagement.com/Candidate/MyProject.aspx"
LOGINID = input("Enter the Login ID:")
LOGINPWD = input("Enter the Password:")

def strip_dict(d):
    return dict((k.strip(), v.strip()) for k, v in d.items())

def main():
    
    #--------------------------------------------------Inputing the detials to the website--------------------------------------------------#

    chrome_options = Options()

    # Disabling Chrome's PDF Viewer inorder to trigger the auto-download of the PDF 
    profile = {
                "plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
                "download.default_directory": f"{os.getcwd()}/",
                "download.extensions_to_open": "",
                "plugins.always_open_pdf_externally": True,
    }
    chrome_options.add_experimental_option("prefs", profile)
    chrome_options.add_experimental_option("detach", True)

    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    browser.implicitly_wait(5)

    browser.get(URL)
    print("Opened Zeetech")

    browser.find_element(By.ID, "txt_user").send_keys(LOGINID)
    print("Entered Username")

    browser.find_element(By.ID, "txt_pass").send_keys(LOGINPWD)
    print("Entered Password")

    browser.find_element(By.ID, "chk_accept_cookie_policy").click()
    browser.find_element(By.ID, "btn_log").click()

    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------Navigating to the Forms Page--------------------------------------------------#

    try:

        my_projects_button = browser.find_element(By.XPATH, "//a[@href='MyProject.aspx']")
        
        # Click the MyProjects button as it is embedded in the side bar
        browser.execute_script("arguments[0].click();", my_projects_button)
        # n = browser.find_element(By.XPATH,"/html/body/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[4]/span").get_attribute("innerHTML")
        browser.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[8]/a[1]").click()
    except:
        attendance_button = browser.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div[2]/div/div[1]/div/div[1]/input")
        browser.execute_script("arguments[0].click();", attendance_button)
        alert = Alert(browser)
        alert.accept()
        my_projects_button = browser.find_element(By.XPATH, "//a[@href='MyProject.aspx']")
        browser.execute_script("arguments[0].click();", my_projects_button)
        # n = browser.find_element(By.XPATH,"/html/body/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[4]/span").get_attribute("innerHTML")
        browser.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[8]/a[1]").click()

    # Loop created to iterate through the number of files remaining
    # for i in range(int(n)+1):
    #     I_D = "grdv_project_link_view_file_"
    #     r = str(i)
    #     I_D = I_D + r
    #     browser.find_element(By.ID, I_D).click()
    #     browser.find_element(By.XPATH, "//table/tbody/tr[1]/td[3]/a").click()
    for i in range(20):
        view_file_button = browser.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div[2]/div/div[2]/div/div/table/tbody/tr[1]/td[2]/a")
        browser.execute_script("arguments[0].click();", view_file_button)

    # Delete PDF because all of them are saved with the same name ease of functionability
        try:
            os.remove(os.path.join(rf'{os.getcwd()}\ReadPDFStream.pdf'))
            os.remove(os.path.join(rf'{os.getcwd()}\page.jpg'))
        except:
            pass
    
    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------Operations on the PDF--------------------------------------------------#

    # Get PDF
        pdflink = browser.find_element(By.XPATH, "//object").get_attribute("data")
        print(pdflink)
        browser.get(pdflink)

    # Get Form Labels
        final_labellist = []
        form = browser.find_element(By.XPATH, "//form/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]")
        labeldivs = form.find_elements(By.XPATH, '//div[@class="col-sm-4"]')

        labellist = [label.find_element(By.TAG_NAME, "label").text for label in labeldivs[:-1]]
        for i in labellist:
            s = i[3:-1]
            final_labellist.append(s)
        copy_final_labellist = final_labellist.copy()
    
    # Converting PDF to Imagine using easyOCR
        with tempfile.TemporaryDirectory() as path:
            file_path = rf"{os.getcwd()}\ReadPDFStream.pdf"
            images = convert_from_path(file_path , output_folder=path)
            images[0].save("page.jpg", "JPEG")

    # Scraping the image using OCR AI B0T
        IMAGE_PATH = rf"{os.getcwd()}\page.jpg"
        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH,paragraph="True")
        values = []
        for i in result:
            values.append(i[1])
    
    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------Getting informatio from the HTML form--------------------------------------------------#

    # Loop to check the params from the FORM giving on the web-page
        final_dict = {}
        for i in final_labellist:
            for j in values:
                if (i == j):
                    final_dict.update({i : values[values.index(i)+1]})

    # Getting labels of the params from the HTML form
        input_ids = []
        select_ids = []
        textarea_ids = []
        form = browser.find_element(By.XPATH, "//form/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]")
        labeldivs_input = form.find_elements(By.XPATH, '//div/div[@class="form-group"]//input')
        labeldivs_select = form.find_elements(By.XPATH, '//div/div[@class="form-group"]//select')
        labeldivs_textarea = form.find_elements(By.XPATH, '//div/div[@class="form-group"]//textarea')
        for i in labeldivs_input:
            input_ids.append(i.get_attribute("id"))
        for i in labeldivs_select:
            select_ids.append(i.get_attribute("id"))
        for i in labeldivs_textarea:
            textarea_ids.append(i.get_attribute("id"))
            
    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------LABELS & IDs--------------------------------------------------#

    # Matching the labelist and the ids
        final_ids_dict = {}
        truncated_final_labellist = []
        truncated_select_ids = []
        truncated_input_ids = []
        truncated_textarea_ids = []
        
    # Truncating the lists off special characters, spaces and HTML framework codes
        for i in final_labellist:
            truncated_final_labellist.append(re.sub("[^A-Z]", "",i,0,re.IGNORECASE).casefold())
        for i in select_ids:
            truncated_select_ids.append(re.sub("[^A-Z]", "",i,0,re.IGNORECASE).casefold()[2:])
        for i in input_ids:
            truncated_input_ids.append(re.sub("[^A-Z]", "",i,0,re.IGNORECASE).casefold()[3:])
        for i in textarea_ids:
            truncated_textarea_ids.append(re.sub("[^A-Z]", "",i,0,re.IGNORECASE).casefold()[3:])
        
    # Loop to match and ids and labels and putting them into a dictionary
        for i in truncated_final_labellist:
            try:
                var = difflib.get_close_matches(i, truncated_input_ids, 1, 0.7)
                final_ids_dict.update({final_labellist[truncated_final_labellist.index(i)] : input_ids[truncated_input_ids.index(var[0])]})
            except:
                continue
        for i in truncated_final_labellist:
            try:
                var = difflib.get_close_matches(i, truncated_select_ids)
                final_ids_dict.update({final_labellist[truncated_final_labellist.index(i)] : select_ids[truncated_select_ids.index(var[0])]})
            except:
                continue
        for i in truncated_final_labellist:
            try:
                var = difflib.get_close_matches(i, truncated_textarea_ids, 1, 0.7)
                final_ids_dict.update({final_labellist[truncated_final_labellist.index(i)] : textarea_ids[truncated_textarea_ids.index(var[0])]})
            except:
                continue
        
        # Loop to correct the final params that are remaining from the above loop
        d=select_ids+input_ids+textarea_ids
        for i in final_labellist:
            x=difflib.get_close_matches(i,d,2,0.3)
            final_ids_dict.update({i:x[0]})
        
        # Pre-defining for now
        final_ids_dict.update({'Name of Business': 'txt_business_name'})
    
    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------LABELS & VALUES--------------------------------------------------#
    
    # Function to make the addresses unique as the applicant and the buisness address just appear address
        def uniquify(seq, suffs = count(1)):
            not_unique = [k for k,v in Counter(seq).items() if v>1] 
            suff_gens = dict(zip(not_unique, tee(suffs, len(not_unique))))  
            for idx,s in enumerate(seq):
                try:
                    suffix = str(next(suff_gens[s]))
                except KeyError:
                    # s was unique
                    continue
                else:
                    seq[idx] += suffix

        uniquify(values)

    # Block to change the first adress to Applicant adress if the first title in the PDF is Applicant
        a=['Applicant', 'Application']
        if any(ext in values[0] for ext in a):
            values = list(map(lambda x: x.replace('Address1', 'Applicant Address'), values))
            values = list(map(lambda x: x.replace('Address2', 'Business Address'), values))
        else:
            values = list(map(lambda x: x.replace('Address2', 'Applicant Address'), values))
            values = list(map(lambda x: x.replace('Address1', 'Business Address'),values))

    # Block to change the first instance of Name to Applicant name as Father and Buisness name is defined properly but not Applicant name
        print(values)
        for i in values:
            x=values.index(i)
            if i[-1]=="1" and i not in [' Date of Establishment','License No.','Mobile No.']:
                values[x]=i[:-1]

        n = values.index("Name")
        values[n] = "Applicant Name"

    # Loop to truncate the values list to implement get() function
        truncated_values = []
        for i in values:
            truncated_values.append(re.sub("[^A-Z]", "",i,0,re.IGNORECASE).casefold())

    # Updating final dict with the LABELS as KEYS and VALUES from the OCR as the VALUES
        final_values_dict = {}
        for i in truncated_final_labellist:
                    try:
                        var = difflib.get_close_matches(i, truncated_values, 1, 0.7)
                        final_values_dict.update({final_labellist[truncated_final_labellist.index(i)] : values[truncated_values.index(var[0]) + 1]})
                    except:
                        continue 
    
    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------Correcting the Values to be entered as PAYLOAD--------------------------------------------------#

    # This is to remove the "Email Id" and the "Street Name" from the outputed OCR values
        for i in final_values_dict.keys():
            d=final_values_dict.get(i)
            if i == "Applicant Address":
                if "street name" in d.casefold():
                    d=d[0:d.casefold().index("street name")]
                    final_values_dict.update({i:d})
            elif i == "Applicant Address":
                if "email id" in d.casefold():
                    d=d[0:d.casefold().index("email id")]
                    final_values_dict.update({i:d})

    # This is loop to touble shoot the random 1 appearing at the end of the OCR reading
        for i in final_values_dict.keys():
            d=final_values_dict.get(i)
            if i == " Date of Establishment" and len(d)>10:
                d=d[:-1]
                final_values_dict.update({i:d})
            elif i == 'License No.' and len(d)>17:
                d=d[:-1]
                final_values_dict.update({i:d})
            elif i == 'Mobile No.' and len(d)>10:
                d=d[:-1] 
                final_values_dict.update({i:d})

    # This loop is to check for the 1 appearing in Names
        for i in final_labellist:
            param_value_check = final_values_dict[i]
            if(i.strip() == "Applicant Name"):
                stripped_applicant_name = i[-1::]
                if(stripped_applicant_name.isnumeric()):
                    final_values_dict.update({i : param_value_check.replace(stripped_applicant_name, "")})

            if(i.strip() == "Buisness Name"):
                stripped_applicant_name = i[-1::]
                if(stripped_applicant_name.isnumeric()):
                    final_values_dict.update({i : param_value_check.replace(stripped_applicant_name, "")}) 

            if(i.strip() == "Applicant Address"):
                stripped_applicant_name = i[-1::]
                if(stripped_applicant_name.isnumeric()):
                    final_values_dict.update({i : param_value_check.replace(stripped_applicant_name, "")}) 

            if(i.strip() == "Buisness Address"):
                stripped_applicant_name = i[-1::]
                if(stripped_applicant_name.isnumeric()):
                    final_values_dict.update({i : param_value_check.replace(stripped_applicant_name, "")}) 

    # This is to change the '-' in the date element to '/' as it is the format in which it is accepted in the payload
        for i in final_labellist:
            if(i.strip() == "Date of Establishment"):
                final_values_dict.update({i : final_values_dict[i].replace('-', '/')})

    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------Entering the Payload--------------------------------------------------#

        for i in final_labellist:
            param_id = final_ids_dict[i]
            param_value = final_values_dict[i]
            browser.find_element(By.ID, param_id).send_keys(param_value)

    # This exception creater for the total area as the drop down is in the form of options according to given divisions
            if(i.strip() in "Total Area (Sq.Ft.)"):
                param_id = final_ids_dict[i]
                param_value = int(final_values_dict[i])
                drop_down = Select(browser.find_element(By.ID, param_id))
                if(param_value <= 250):
                    drop_down.select_by_index(0)
                elif(param_value > 250 and param_value <= 500):
                    drop_down.select_by_index(1)
                elif(param_value > 500 and param_value <= 750):
                    drop_down.select_by_index(2)
                elif(param_value > 750 and param_value <= 1000):
                    drop_down.select_by_index(3)
                elif(param_value > 1000 and param_value <= 1500):
                    drop_down.select_by_index(4)
                elif(param_value > 1500 and param_value <= 2000):
                    drop_down.select_by_index(5)
                elif(param_value > 2000):
                    drop_down.select_by_index(6)
            
    # This loop is for APPLICATION TYPE having a select tag in the framework
            if(i.strip() == "Application Type"):
                param_id = final_ids_dict[i]
                param_value = final_values_dict[i].casefold()
                drop_down = Select(browser.find_element(By.ID, param_id))
                if("license" in param_value):
                    drop_down.select_by_index(0)
                elif("renew" in param_value):
                    drop_down.select_by_index(1)
    
    # This loop is for the FIRM TYPE having a select tag in the framework
            if(i.strip() == "Firm Type"):
                param_id = final_ids_dict[i]
                param_value = final_values_dict[i].casefold()
                drop_down = Select(browser.find_element(By.ID, param_id))
                if("proprie" in param_value):
                    drop_down.select_by_index(0)
                elif("partner" in param_value):
                    drop_down.select_by_index(1)
                elif("ngo" in param_value):
                    drop_down.select_by_index(2)
                elif("opc" in param_value):
                    drop_down.select_by_index(3)
                elif("private" in param_value):
                    drop_down.select_by_index(4)
                elif("public" in param_value):
                    drop_down.select_by_index(5)
                else:
                    drop_down.select_by_index(6)

    # This loop is for the TYPE OF OWNERSHIP select tag
            if(i.strip() == "Type of Ownership of Business Premises"):
                param_id = final_ids_dict[i]
                param_value = final_values_dict[i].casefold()
                drop_down = Select(browser.find_element(By.ID, param_id))
                if("rent" in param_value):
                    drop_down.select_by_index(0)
                elif("lease" in param_value):
                    drop_down.select_by_index(1)
                elif("own" in param_value):
                    drop_down.select_by_index(2)

    # This loop is there to remove all the previous data that is there in the data txt area so that it can be re-entered as payload
            if(i.strip() == "Date of Establishment"):
                for i in range(20):
                    date_button = browser.find_element(By.ID, param_id)
                    date_button.send_keys(Keys.BACKSPACE)
                date_button.send_keys(param_id, param_value)

        pdb.set_trace()
    
    #--------------------------------------------------LEEF--------------------------------------------------#

    #--------------------------------------------------Exception Handling--------------------------------------------------#
    
        submit_button = browser.find_element(By.XPATH, "/html/body/form/div[4]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[41]/div/input")

        # This TRY BLOCK is for the first deafult try to check whether the inputed payload can be entered into the HTML form
        try:
            browser.execute_script("arguments[0].click()", submit_button)
    
    # FIRST EXCEPTION --> giving value error with name as an "attribute"
    # This EXCEPT is replicating the payload inputing function with default values for FAULTY PDFs
        except ValueError:
            final_values_dict = {'Application Type': 'New Licence', 'License No.': 'RAN22020119159408', 'Firm Type': 'Proprietary',
            'Type of Ownership of Business Premises': 'On Rent', 'Applicant Name': 'FAULTY PDF', "Father's Name": 'RAM',
            'Mobile No.': '9576131033', 'Applicant Address': 'ADRESSS', 'Name of Business': 'BUISNESS',
            ' Nature of Business/Brief Description of Business': 'SHOP', ' Date of Establishment': '05-01-2019',
            ' Business Address': 'INDIA', ' Total Area (Sq.Ft.)': '300'}
            for i in final_labellist:
                param_id = final_ids_dict[i]
                param_value = final_values_dict[i]
                browser.find_element(By.ID, param_id).send_keys(param_value)

    # This exception creater for the total area as the drop down is in the form of options according to given divisions
                if(i.strip() in "Total Area (Sq.Ft.)"):
                    param_id = final_ids_dict[i]
                    param_value = int(final_values_dict[i])
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if(param_value <= 250):
                        drop_down.select_by_index(0)
                    elif(param_value > 250 and param_value <= 500):
                        drop_down.select_by_index(1)
                    elif(param_value > 500 and param_value <= 750):
                        drop_down.select_by_index(2)
                    elif(param_value > 750 and param_value <= 1000):
                        drop_down.select_by_index(3)
                    elif(param_value > 1000 and param_value <= 1500):
                        drop_down.select_by_index(4)
                    elif(param_value > 1500 and param_value <= 2000):
                        drop_down.select_by_index(5)
                    elif(param_value > 2000):
                        drop_down.select_by_index(6)
                
    # This loop is for APPLICATION TYPE having a select tag in the framework
                if(i.strip() == "Application Type"):
                    param_id = final_ids_dict[i]
                    param_value = final_values_dict[i].casefold()
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if("license" in param_value):
                        drop_down.select_by_index(0)
                    elif("renew" in param_value):
                        drop_down.select_by_index(1)
        
    # This loop is for the FIRM TYPE having a select tag in the framework
                if(i.strip() == "Firm Type"):
                    param_id = final_ids_dict[i]
                    param_value = final_values_dict[i].casefold()
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if("proprie" in param_value):
                        drop_down.select_by_index(0)
                    elif("partner" in param_value):
                        drop_down.select_by_index(1)
                    elif("ngo" in param_value):
                        drop_down.select_by_index(2)
                    elif("opc" in param_value):
                        drop_down.select_by_index(3)
                    elif("private" in param_value):
                        drop_down.select_by_index(4)
                    elif("public" in param_value):
                        drop_down.select_by_index(5)
                    else:
                        drop_down.select_by_index(6)

    # This loop is for the TYPE OF OWNERSHIP select tag
                if(i.strip() == "Type of Ownership of Business Premises"):
                    param_id = final_ids_dict[i]
                    param_value = final_values_dict[i].casefold()
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if("rent" in param_value):
                        drop_down.select_by_index(0)
                    elif("lease" in param_value):
                        drop_down.select_by_index(1)
                    elif("own" in param_value):
                        drop_down.select_by_index(2)

    # Pressing the submit button after the exception handling
            browser.execute_script("arguments[0].click();", submit_button)

    # SECOND EXCEPTION --> where the mobile number is usualy in "alnum" form where it must be in "numeric"
    # This EXCECPT BLOCK is created to deal when an element is out of its DATA TYPE and an alert box pops up
        except UnexpectedAlertPresentException:
            browser.switch_to().alert().accept()
            
            final_values_dict = {'Application Type': 'New Licence', 'License No.': 'RAN22020119159408', 'Firm Type': 'Proprietary',
            'Type of Ownership of Business Premises': 'On Rent', 'Applicant Name': 'FAULTY PDF', "Father's Name": 'RAM',
            'Mobile No.': '9576131033', 'Applicant Address': 'ADRESSS', 'Name of Business': 'BUISNESS',
            ' Nature of Business/Brief Description of Business': 'SHOP', ' Date of Establishment': '05-01-2019',
            ' Business Address': 'INDIA', ' Total Area (Sq.Ft.)': '300'}
            for i in final_labellist:
                param_id = final_ids_dict[i]
                param_value = final_values_dict[i]
                browser.find_element(By.ID, param_id).send_keys(param_value)

    # This exception creater for the total area as the drop down is in the form of options according to given divisions
                if(i.strip() in "Total Area (Sq.Ft.)"):
                    param_id = final_ids_dict[i]
                    param_value = int(final_values_dict[i])
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if(param_value <= 250):
                        drop_down.select_by_index(0)
                    elif(param_value > 250 and param_value <= 500):
                        drop_down.select_by_index(1)
                    elif(param_value > 500 and param_value <= 750):
                        drop_down.select_by_index(2)
                    elif(param_value > 750 and param_value <= 1000):
                        drop_down.select_by_index(3)
                    elif(param_value > 1000 and param_value <= 1500):
                        drop_down.select_by_index(4)
                    elif(param_value > 1500 and param_value <= 2000):
                        drop_down.select_by_index(5)
                    elif(param_value > 2000):
                        drop_down.select_by_index(6)
                
    # This loop is for APPLICATION TYPE having a select tag in the framework
                if(i.strip() == "Application Type"):
                    param_id = final_ids_dict[i]
                    param_value = final_values_dict[i].casefold()
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if("license" in param_value):
                        drop_down.select_by_index(0)
                    elif("renew" in param_value):
                        drop_down.select_by_index(1)
        
    # This loop is for the FIRM TYPE having a select tag in the framework
                if(i.strip() == "Firm Type"):
                    param_id = final_ids_dict[i]
                    param_value = final_values_dict[i].casefold()
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if("proprie" in param_value):
                        drop_down.select_by_index(0)
                    elif("partner" in param_value):
                        drop_down.select_by_index(1)
                    elif("ngo" in param_value):
                        drop_down.select_by_index(2)
                    elif("opc" in param_value):
                        drop_down.select_by_index(3)
                    elif("private" in param_value):
                        drop_down.select_by_index(4)
                    elif("public" in param_value):
                        drop_down.select_by_index(5)
                    else:
                        drop_down.select_by_index(6)

    # This loop is for the TYPE OF OWNERSHIP select tag
                if(i.strip() == "Type of Ownership of Business Premises"):
                    param_id = final_ids_dict[i]
                    param_value = final_values_dict[i].casefold()
                    drop_down = Select(browser.find_element(By.ID, param_id))
                    if("rent" in param_value):
                        drop_down.select_by_index(0)
                    elif("lease" in param_value):
                        drop_down.select_by_index(1)
                    elif("own" in param_value):
                        drop_down.select_by_index(2)

    # Submitting the payload after the EXCEPTION has been handled
        browser.execute_script("arguments[0].click()", submit_button)

    #--------------------------------------------------LEEF--------------------------------------------------#   
        



main()
