import re
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.Consts import *
from webdriver_manager.chrome import ChromeDriverManager
from itertools import tee, count
from collections import Counter


class Utils:
    @staticmethod
    def cleanList(oldlist: list, param: str):
        if param not in PARAMS.keys():
            raise ValueError("Wrong Parameter. Must be one of %r " % PARAMS)

        newlist = []
        for i in oldlist:
            newlist.append(
                re.sub("[^A-Z]", "", i, 0, re.IGNORECASE).casefold()[PARAMS[param]:]
            )

        return newlist

    @staticmethod
    def checkDriver():
        if os.path.isfile(WINDRIVER) and os.path.isfile(UXDRIVER):
            return True

        return False

    @staticmethod
    def get_driver():
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", PROFILE)
        chrome_options.add_experimental_option("detach", True)

        # * Get OS and assign corresponding driver
        #
        # if Utils.checkDriver():
        #     if sys.platform == "win32":
        #         driver = webdriver.Chrome(
        #             service=Service(WINDRIVER),
        #             options=chrome_options
        #         )
        #     elif sys.platform == "linux":
        #         driver = webdriver.Chrome(
        #             service=Service(UXDRIVER),
        #             options=chrome_options
        #         )
        #     else:
        #         driver = webdriver.Chrome(
        #             service=Service(ChromeDriverManager().install()),
        #             options=chrome_options
        #         )
        # else:
        #     driver = webdriver.Chrome(
        #         service=Service(ChromeDriverManager().install()),
        #         options=chrome_options
        #     )
        driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )

        return driver

    @staticmethod
    def uniquify(seq, suffs=count(1)):

        not_unique = [k for k, v in Counter(seq).items() if v > 1]
        suff_gens = dict(zip(not_unique, tee(suffs, len(not_unique))))
        for idx, s in enumerate(seq):
            try:
                suffix = str(next(suff_gens[s]))
            except KeyError:
                # s was unique
                continue
            else:
                seq[idx] += suffix
