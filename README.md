# rc3 CERT Cube Solver

This is a solver for the "CERT Cube", a maze in the virtual world at [rc3 event 2020](https://events.ccc.de/2020/09/04/rc3-remote-chaos-experience/).

The solver works by using [Selenium](https://www.selenium.dev/) to remote-control a web browser window, and walk through all rooms to explore the maze.
This is used to create a graph of all rooms and their exits, which is saved as JSON file.
Afterwards the graph information can be used to find the shortest path through the maze.

Note that exploring the maze can take several hours.
In my successful run the bot explored 126 rooms and 499 connections until it found the exit.
The first ca. 80 rooms were explored within maybe an hour or less, because they were closely connected.
The remaining rooms took a long time, because they required repeatedly walking through long one-way connections.


## Installation
- install Python packages:
```
virtualenv venv
source venv/bin/activate
pip install selenium graphviz webdriver-manager
```

## Usage

- create directory for results:  
`mkdir run1`

- start Selenium browser window (in background):  
`./start_driver.py https://visit.at.rc3.world/as/cert &`

- start the explorer script (use the "driver URL" and "driver session" printed by `start_driver.py`):  
`./explore_cube.py run1/rooms.json http://127.0.0.1:46079 da974f8e950add8979c15aaca8c4842f`

While running, the explorer code will add newly collected room information to the supplied JSON file.
It will also create backup files of the JSON file whenever new information is discovered (to avoid loosing all data if the JSON file gets broken by the script).
The backup files will be created in the same directory where the main JSON file is created.

You can view the gathered room information like this:  
```
./create_dot_graph.py run1/rooms.json run1/rooms.dot
sfdp -x -Goverlap=scale -Tpng run1/rooms.dot > run1/rooms.png
```

When the exit room has been found, the bot will quit with an error (but unfortunately it will not add the final room to the JSON file).
Therefore you have to edit the JSON file manually and add an entry for the exit room (without any directions).
Then use `find_path.py` to show the full path from any room to any other room, eg.:  
`./find_path.py run1/rooms.json 1190 1683`


## Known Problems
There a some cases which the explorer code doesn't cannot handle, and where it will therefore quit:
- if a room exit leads into the same room again (since the explorer code waits for the room number to change, it will keep walking through that exit)
    - the script will give up after a few seconds and will quit
    - solution: manually edit the room JSON file and add this connection, the restart the script
- if a "connection lost..." screen appears, which may occur if the backend is too slow
    - again, the script will give up after a few seconds and will quit
    - solution: restart the script once the backend is less overloaded
- when the exit room is found, the bot cannot reach any other room and will again quit. See the Usage section for details.

Also, I haven't tested the code after cleaning it up (cardinal sin, I know; but the maze server was already shut down).
Therefore the current code might have bugs that were introduced during cleanup.
If unsure, check out the very first commit; that code was actually used successfully (but is difficult to use).


## Results for Successful Run on "okmvqn" Maze Iteration
The room graph for the last successful run in the last rc3 maze setup (with identifier "okmvqn") are stored in results-okmvqn/ subdirectory.
The exit room in that setup has ID 1683.
