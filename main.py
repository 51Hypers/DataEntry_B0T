from src.Zeetech import *
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime}::{levelname:<4}::{message}",
    style="{",
    filename='testlog.txt',
    filemode='w'
)

def main():
    z = Zeetech()
    #logging.info('Started')
    z.login(LOGIN_ID, LOGIN_PWD)
    #logging.info('logged in')
    z.navigatetoProj()
    z.startProject()


if __name__ == '__main__':
    main()
