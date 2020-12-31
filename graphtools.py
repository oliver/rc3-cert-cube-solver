#!/usr/bin/env python

#import graphviz
from collections import deque
import json
import sys

#pathCache = []

def find_shortest_path(graph, start, end):
    dist = {start: [start]}
    q = deque([start])
    while len(q):
        at = q.popleft()
        for (next,d) in graph[at]:
            if next not in dist:
                #dist[next] = [(dist[at],d), (next,d)]
                dist[next] = [dist[at], (next, d)]
                q.append(next)
    return dist.get(end)

#def find_path(graph, start, end, path=[]):
    #path = path + [start]
    #if start == end:
        #return path
    #if not graph.has_key(start):
        #return None
    #for node in graph[start]:
        #if node not in path:
            #newpath = find_path(graph, node, end, path)
            #if newpath: return newpath
    ##for d in graph[start]:
        ##node = graph[start][d]
        ##if node not in path:
            ##newpath = find_path(graph, node, end, path)
            ##if newpath: return newpath
    #return None

#def loadGraph()

#def unwrapPath

if __name__ == "__main__":
    inFile = sys.argv[1]
    #outFile = sys.argv[2]
    startRoom = int(sys.argv[2])
    targetRoom = int(sys.argv[3])

    fp = open(inFile)
    #rooms = json.load(fp)
    rooms = {}
    loadedRooms = json.load(fp)
    for rId in loadedRooms:
        #rooms[int(rId)] = {}
        rooms[int(rId)] = []
        for d in loadedRooms[rId]:
            #rooms[int(rId)][d] = loadedRooms[rId][d]
            #rooms[int(rId)].append(loadedRooms[rId][d])
            rooms[int(rId)].append( (loadedRooms[rId][d], d) )

    fp.close()
    print "loaded %d rooms" % len(rooms)
    #print rooms

    #paths = {}
    #for r1 in rooms:
        #for r2 in rooms:
            #find_path(rooms, r1, r2)

    #path = find_path(rooms, startRoom, targetRoom)
    path = find_shortest_path(rooms, startRoom, targetRoom)
    #print path
    
    def unwrap(p):
        if isinstance(p, list):
            #return unwrap(p[0]) + [ tuple(p[1:]) ]
            return unwrap(p[0]) + p[1:]
        else:
            return [ p ]
    
    path = unwrap(path)
    print "path has %d steps" % len(path)
    for el in path[1:]:
        sys.stdout.write("%s (zu %s); " % (el[1], el[0]))

    print ""

    #for el in path:
        #while isinstance(el, list):
        ##while len(el) > 1:
            #el = el[0]
        #print el
