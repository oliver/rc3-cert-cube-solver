#!/usr/bin/env python

import datetime
import json
import random
import re
import shutil
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

#cookieFile = "try2/cookies.json"
#if not(os.path.exists(cookieFile)):

#fp = open("cookies.json")
#cookies = json.load(fp)
#fp.close()

opt = Options()
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2
})

driver = webdriver.Chrome(chrome_options=opt)

startUrl = "https://visit.at.rc3.world/as/cert/jfFyq6m28LUCJNDhGnPnWD/_/global/cert.maps.at.rc3.world/cube/okmvqn-8669b66f-9045-4e28-a4bd-9da70d8b31e8-eukf595.json"
driver.get(startUrl)

print "driver URL: %s" % driver.command_executor._url
print "driver session: %s" % driver.session_id

#while True:
    #print "press Ctrl+C to terminate this driver"
    #raw_input()
