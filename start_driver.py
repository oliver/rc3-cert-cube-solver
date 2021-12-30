#!/usr/bin/env python3

#
# Starts Selenium Chrome webdriver (ie. opens a Chrome window which remains open).
# Opens the maze website in that browser window, so that the user can manually log in etc.
#
# The Selenium connection details of the browser window are displayed on terminal,
# and can be manually passed to the actual bot script which will then use this browser window.
#


import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s <URL for some room in the maze>" % sys.argv[0])
        sys.exit(1)

    startUrl = sys.argv[1]

    # disable camera, microphone etc. (to prevent popups asking for permission):
    opt = Options()
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2
    })
    opt.add_experimental_option("detach", True) # keep browser window open after this script has exited

    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=opt)
    driver.get(startUrl)

    print("driver URL: %s" % driver.command_executor._url)
    print("driver session: %s" % driver.session_id)
