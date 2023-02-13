from src.Zeetech import *


def main():
    z = Zeetech()
    z.login(LOGIN_ID, LOGIN_PWD)
    z.navigatetoProj()
    z.startProject()


if __name__ == '__main__':
    main()
