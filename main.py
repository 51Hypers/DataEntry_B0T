from src.Zeetech import *
from src.testPDF import *
from src.Consts import *
def testpdf():
    readPDF(DWD + "ReadPDFStream.pdf")

def main():
    z = Zeetech()
    z.login(LOGIN_ID, LOGIN_PWD)
    z.navigatetoProj()
    z.startProject()


testpdf()
#
# if __name__ == '__main__':
#     main()
