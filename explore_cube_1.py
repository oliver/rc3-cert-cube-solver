#!/usr/bin/env python

import datetime
import json
import random
import re
import shutil
import sys
import time

from collections import deque

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

DIR_UP = "u"
DIR_DOWN = "d"
DIR_LEFT = "l"
DIR_RIGHT = "r"

class CubeRooms:
    def __init__ (self, jsonFile):
        self.jsonFile = jsonFile
        self.rooms = {}

        try:
            fp = open(self.jsonFile)
            loadedRooms = json.load(fp)
            fp.close()
            for rId in loadedRooms:
                self.rooms[int(rId)] = {}
                for d in loadedRooms[rId]:
                    if False and loadedRooms[rId][d] == int(rId):
                        print "(discarding %d,%s -> %d)" % (int(rId), d, int(rId))
                    else:
                        self.rooms[int(rId)][d] = loadedRooms[rId][d]
        except:
            print "no rooms loaded"
            pass
        else:
            print "loaded %d start rooms" % len(self.rooms)
            self.save()

    def addRoom (self, startRoom, direction, resultRoom):
        if not(self.rooms.has_key(startRoom)):
            self.rooms[startRoom] = {}
        if self.rooms[startRoom].has_key(direction):
            print "this result (%d,%s -> %d) already exists" % (startRoom, direction, resultRoom)
            #assert self.rooms[startRoom][direction] == resultRoom, "new result must match previously found result (otherwise the cube is not reproducable)"
            if self.rooms[startRoom][direction] != resultRoom:
                print "WARNING: new result (%d,%s -> %d) does not match previous result (%d,%s -> %d)! Overwriting old result." % (startRoom, direction, resultRoom, startRoom, direction, self.rooms[startRoom][direction])
                sys.exit(1)
            else:
                return

        self.rooms[startRoom][direction] = resultRoom
        self.save()

    def get (self, room):
        if not(self.rooms.has_key(room)):
            return {}
        return self.rooms[room]

    def save(self):
        fp = open(self.jsonFile, "w")
        json.dump(self.rooms, fp, indent=4)
        fp.close()

        backupName = "%s.%s.json" % (self.jsonFile, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        shutil.copyfile(self.jsonFile, backupName)

    def find_shortest_path(self, start, end):
        dist = {start: [start]}
        q = deque([start])
        while len(q):
            at = q.popleft()
            #for (next,d) in graph[at]:
            for d in self.rooms[at]:
                next = self.rooms[at][d]
                if next not in dist:
                    #dist[next] = [(dist[at],d), (next,d)]
                    dist[next] = [dist[at], (next, d) ]
                    q.append(next)
        return dist.get(end)

    def getPathToNextIncomplete(self, startRoom):
        for targetRoom in self.rooms:
            if len(self.rooms[targetRoom]) < 4:
                break
        else:
            print "all rooms are complete!"
            return None

        print "next incomplete room: %d" % targetRoom
        path = self.find_shortest_path(startRoom, targetRoom)

        def unwrap(p):
            if isinstance(p, list):
                return unwrap(p[0]) + p[1:]
            else:
                return [ p ]

        unwrappedPath = unwrap(path)
        return unwrappedPath[1:]

    def getPathToNextIncomplete2(self, startRoom):
        def unwrap(p):
            if isinstance(p, list):
                return unwrap(p[0]) + p[1:]
            else:
                return [ p ]

        #targets = []
        targetPath = None
        for targetRoom in self.rooms:
            if len(self.rooms[targetRoom]) < 4:
                print "candidate: %d" % targetRoom
                path = unwrap(self.find_shortest_path(startRoom, targetRoom))[1:]
                #targets.append( (targetRoom, path) )
                if path and (targetPath is None or len(path) < len(targetPath)):
                    targetPath = path
        #if not targets:
        if targetPath is None:
            print "all rooms are complete!"
            return None

        #print "have %d incomplete rooms: %s" % (len(targets), targets)
        #for 
        print "shortest path ton incomplete room: %s" % targetPath
        return targetPath

        #for targetRoom in targets:
            #path = self.find_shortest_path(startRoom, targetRoom)
            #unwrappedPath = unwrap(path)
        #return unwrappedPath[1:]

    def getPathToNextIncomplete3(self, startRoom):
        def unwrap(p):
            if isinstance(p, list):
                return unwrap(p[0]) + p[1:]
            else:
                return [ p ]

        targetRoom = 1683
        path = unwrap(self.find_shortest_path(startRoom, targetRoom))[1:]
        return path

        ##targets = []
        #targetPath = None
        #for targetRoom in self.rooms:
            #if len(self.rooms[targetRoom]) < 4:
                #print "candidate: %d" % targetRoom
                #path = unwrap(self.find_shortest_path(startRoom, targetRoom))[1:]
                ##targets.append( (targetRoom, path) )
                #if path and (targetPath is None or len(path) < len(targetPath)):
                    #targetPath = path
        ##if not targets:
        #if targetPath is None:
            #print "all rooms are complete!"
            #return None

        ##print "have %d incomplete rooms: %s" % (len(targets), targets)
        ##for 
        #print "shortest path ton incomplete room: %s" % targetPath
        #return targetPath

        #for targetRoom in targets:
            #path = self.find_shortest_path(startRoom, targetRoom)
            #unwrappedPath = unwrap(path)
        #return unwrappedPath[1:]


driverUrl = sys.argv[1]
driverSession = sys.argv[2]

#cookieFile = "try2/cookies.json"
#if not(os.path.exists(cookieFile)):

#fp = open("cookies.json")
#cookies = json.load(fp)
#fp.close()

#opt = Options()
#opt.add_experimental_option("prefs", {
    #"profile.default_content_setting_values.media_stream_mic": 2,
    #"profile.default_content_setting_values.media_stream_camera": 2,
    #"profile.default_content_setting_values.geolocation": 2,
    #"profile.default_content_setting_values.notifications": 2
#})

#driver = webdriver.Chrome(chrome_options=opt)

rooms = CubeRooms("try2/rooms.json")

#url_1411 = "https://visit.at.rc3.world/as/cert/jt6BuM1QvbtjdciJriVHWe/_/global/cert.maps.at.rc3.world/cube/cvsszz-b736bfd3-b883-45d0-af44-649af3220d7b-psqe1411.json"
#driver.get(url_1411)

#for c in cookies:
    #driver.add_cookie(c)


driver = webdriver.Remote(command_executor=driverUrl, desired_capabilities={})
driver.close()   # this prevents the dummy browser
driver.session_id = driverSession


#driver.get(url_1411)

#body = driver.find_element_by_tag_name("body")

#body.send_keys(Keys.ENTER)

#time.sleep(2)
#body.send_keys(Keys.ENTER)

#time.sleep(2)
cv = driver.find_element_by_tag_name("canvas")

actionChains = {}

actionChains[DIR_UP] = ActionChains(driver)
actionChains[DIR_UP].click(cv).key_down(Keys.ARROW_UP)
actionChains[DIR_DOWN] = ActionChains(driver)
actionChains[DIR_DOWN].click(cv).key_down(Keys.ARROW_DOWN)
actionChains[DIR_LEFT] = ActionChains(driver)
actionChains[DIR_LEFT].click(cv).key_down(Keys.ARROW_LEFT)
actionChains[DIR_RIGHT] = ActionChains(driver)
actionChains[DIR_RIGHT].click(cv).key_down(Keys.ARROW_RIGHT)

#actionsR = ActionChains(driver)
#actionsR.click(cv).key_down(Keys.ARROW_RIGHT)

#actionsL = ActionChains(driver)
#actionsL.click(cv).key_down(Keys.ARROW_LEFT)

def getPageId(url):
    return int(re.search(r"(\d+)\.json", url).group(1))

while True:
    oldUrl = driver.current_url
    print "start URL: %s" % oldUrl
    startId = getPageId(oldUrl)
    print "old room: %d" % startId

    knownResults = rooms.get(startId)
    print "have already explored %d directions from here (%s)" % (
        len(knownResults), ",".join(knownResults.keys()))
    nextDir = None
    for d in (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT):
        if not knownResults.has_key(d):
            nextDir = d
            break
    if nextDir is None:
        print "have already explored all directions of %d!" % startId

        path = rooms.getPathToNextIncomplete2(startId)
        print "path to next goal: %s" % path

        nextDir = path[0][1]

        #sys.exit(1)

        #print "choosing a random direction..."
        #while True:
            #nextDir = random.choice( (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) )
            #if knownResults[nextDir] != startId:
                #break
            #print "choosing again (because '%s' would lead to this room again" % nextDir
        ## TODO: better: go to a room that needs to be explored yet

    print "next direction: '%s'" % nextDir
    actionChains[nextDir].perform()

    #actionsR.perform()
    #actionsL.perform()

    for i in range(10):
        time.sleep(0.5)
        newUrl = driver.current_url
        #print "newUrl: %s" % newUrl
        print "new room: %d" % getPageId(newUrl)
        if newUrl != oldUrl:
            break
        print "waiting a bit more..."
        #actionChains[nextDir].perform()
    else:
        print "%d,%s leads again to %d!" % (startId, nextDir, startId)
        sys.exit(1)

    rooms.addRoom(getPageId(oldUrl), nextDir, getPageId(newUrl))

    #print "press Enter to continue"
    #raw_input()
    time.sleep(0.5)

#actionsL.perform()

#actionsR.perform()



#print "press Enter to close"
#raw_input()

#driver.close()

