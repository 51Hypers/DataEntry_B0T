
from src.Utils import *

# * Final values dict : keys -> record value ->

final_labellist = ['Application Type', 'License No.', 'Firm Type', 'Type of Ownership of Business Premises',
                  'Applicant Name', "Father's Name", 'Mobile No.', 'Applicant Address', 'Name of Business',
                  ' Nature of Business/Brief Description of Business', ' Date of Establishment', ' Business Address', ' Total Area (Sq.Ft.)']

final_labellist = Utils.cleanList(final_labellist, "label")
print(final_labellist)

# pdfpath = DWD + "ReadPDFStream.pdf"
# images = convert_from_path(pdfpath)
# images[0].save(DWD + "page.jpg", "JPEG")
# pagepath = DWD + "page.jpg"
#
# s = time.time()
# reader = easyocr.Reader(['en'])
# res = reader.readtext(pagepath, paragraph="False")
# pdf_values = [i[1] for i in res]
# e = time.time()
# print("\n")
# print(pdf_values)
# print("\n")
# Utils.uniquify(pdf_values)
# print(pdf_values)
# print(s-e)
#
# pdf_values = Utils.cleanList(pdf_values, "0")
