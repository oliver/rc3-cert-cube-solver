#!/usr/bin/env python
# coding: utf-8

#
# Prints the shortest path between two rooms in the rc3 CERT Cube room graph.
#


from collections import deque
import json
import sys


def findShortestPath(roomGraph, start, end):
    """
    Returns the shortest (?) path between two nodes in the room graph.
    Each path element is a tuple of two elements:
    - the next room number
    - the direction to take to get into that room

    Based on the code by Eryk Kopczyński from https://www.python.org/doc/essays/graphs/
    """
    dist = {start: [(start, "")]}
    q = deque([start])
    while len(q):
        at = q.popleft()
        for d in roomGraph[at]:
            next = roomGraph[at][d]
            if next not in dist:
                dist[next] = [dist[at], (next, d) ]
                q.append(next)

    # path is now a nested list of path elements; "unwrap" it into a flat list:
    def unwrap(p):
        if isinstance(p, list):
            return unwrap(p[0]) + p[1:]
        else:
            return [ p ]

    return unwrap(dist.get(end))


def toReadableDirection (d):
    directionNames = {
        "u": "up",
        "d": "down",
        "l": "left",
        "r": "right"
    }
    return directionNames[d]


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: %s <room graph JSON file> <id of start room> <id of target room>" % sys.argv[0]
        sys.exit(1)

    inFile = sys.argv[1]
    startRoom = int(sys.argv[2])
    targetRoom = int(sys.argv[3])

    # load room graph from JSON file
    rooms = {}
    with open(inFile) as fp:
        loadedRooms = json.load(fp)
        for rId in loadedRooms:
            # convert JSON keys (which are strings) into integers:
            rooms[int(rId)] = loadedRooms[rId]
    print "loaded %d rooms" % len(rooms)

    path = findShortestPath(rooms, startRoom, targetRoom)

    print "path from %d to %d has %d steps:" % (startRoom, targetRoom, len(path))
    for el in path[1:]:
        sys.stdout.write("%s (into %s); " % (toReadableDirection(el[1]), el[0]))
    print ""
