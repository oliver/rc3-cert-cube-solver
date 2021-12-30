#!/usr/bin/env python3

#
# Creates a Dot graph of the rooms in the rc3 CERT Cube maze.
# Also, prints some statistics about the room graph.
#

import graphviz
import json
import sys


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: %s <room graph JSON file> <Dot graph output file>" % sys.argv[0])
        sys.exit(1)

    inFile = sys.argv[1]
    outFile = sys.argv[2]

    with open(inFile) as fp:
        rooms = json.load(fp)
    print("loaded %d rooms" % len(rooms))

    dot = graphviz.Digraph()

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

    print("have %d room connections" % numEdges)

    # display how many rooms and directions have been explored so far:
    for i in range(5):
        print("%d directions explored: %d rooms (%s)" % (i, len(buckets[i]), buckets[i]))

    with open(outFile, "w") as fp:
        fp.write(dot.source)

    print("Convert to PNG image eg. with:")
    print("  sfdp -x -Goverlap=scale -Tpng %s > graph.png" % outFile)
