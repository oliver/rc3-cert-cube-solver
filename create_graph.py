#!/usr/bin/env python

import graphviz
import json
import sys

if __name__ == "__main__":
    inFile = sys.argv[1]
    outFile = sys.argv[2]

    fp = open(inFile)
    rooms = json.load(fp)
    fp.close()
    print "loaded %d rooms" % len(rooms)

    dot = graphviz.Digraph()
    
    #buckets = range(5)
    buckets = []
    for i in range(5):
        buckets.append([])

    numEdges = 0
    for key in rooms:
        startRoom = int(key)
        dot.node(str(startRoom))
        
        numDirs = len(rooms[key])
        buckets[numDirs].append(startRoom)

        for d in rooms[key]:
            resultRoom = rooms[key][d]
            dot.edge(str(startRoom), str(resultRoom), label=d)
            numEdges+=1

    print "have %d edges" % numEdges
    #for b in buckets:
    for i in range(5):
        print "%d directions explored: %d rooms (%s)" % (i, len(buckets[i]), buckets[i])

    fp = open(outFile, "w")
    fp.write(dot.source)
    fp.close()
