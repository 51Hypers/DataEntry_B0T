import easyocr
from pdf2image import convert_from_path

from src.Consts import *

def readPDF(pdfpath):
    """
    Get all values from the PDF.

    :return: Nothing
    """
    images = convert_from_path(pdfpath)
    images[0].save(DWD + "page.jpg", "JPEG")
    pagepath = DWD + "page.jpg"

    reader = easyocr.Reader(['en'])
    res = reader.readtext(pagepath, paragraph="False")

    pdf_values = [i[1] for i in res]
    indices = [i for i, x in enumerate(pdf_values) if x == "Address"]
    a = ['Applicant', 'Application']

    if any(ext in pdf_values[0] for ext in a):
        pdf_values[indices[0]] = 'Applicant Address'
        pdf_values[indices[1]] = 'Business Address'
    else:
        pdf_values[indices[1]] = 'Applicant Address'
        pdf_values[indices[0]] = 'Business Address'

    for i in pdf_values:
        x = pdf_values.index(i)
        if i[-1] == "1" and i not in [' Date of Establishment', 'License No.', 'Mobile No.']:
            pdf_values[x] = i[:-1]

    n = pdf_values.index("Name")
    pdf_values[n] = "Applicant Name"

    print(pdf_values)
