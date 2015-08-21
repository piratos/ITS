#!/usr/bin/python
#####################################################
#script to control sumo's traffic lights on port 8813
#coded by sayfeddine 30/07/2015
#####################################################
import os
import sys
import optparse
import subprocess
import random
import generate_route
from prettytable import PrettyTable
from Lane import Lane
from Intersection import Intersection
from bokeh.plotting import figure, output_file, show

SUMO_HOME = "/home/piratos/Desktop/sumo-0.23.0/" #os.environ.get("SUMO_HOME")
if SUMO_HOME == None:
	print "[-] please define the sumo home directory that contains bin and tools in $SUMO_HOME"
	sys.exit()
sys.path.append(os.path.join(SUMO_HOME, 'tools/'))

import traci
from sumolib import checkBinary
PORT = 8813
MAX_STEP = 500
cnt = 124 #generate_route.generate()
seq1 = ["GGGGrrrrrrrrrrrr", "yyyyrrrrrrrrrrrr",
       "rrrrGGGGrrrrrrrr", "rrrryyyyrrrrrrrr",
       "rrrrrrrrGGGGrrrr", "rrrrrrrryyyyrrrr",
       "rrrrrrrrrrrrGGGG", "rrrrrrrrrrrryyyy"]

seq = ["GGGGGrrrGGGGGrrr", "GyyyGrrrGyyyGrrr",
        "GrrrGGGGGrrrGGGG", "GrrrGyyyGrrrGyyy",]

seq12 = ["GGGGGrrrGrrrGrrr", "GyyyGrrrGrrrGrrr",
       "GrrrGGGGGrrrGrrr", "GrrrGyyyGrrrGrrr",
       "GrrrGrrrGGGGGrrr", "GrrrGrrrGyyyGrrr",
       "GrrrGrrrGrrrGGGG", "GrrrGrrrGrrrGyyy"]

c = len(seq)

######################################################
#helpers

def numberv(lane):
    """ return the number of vehicle in a given lane
    lane : lane identifier ( XtoY_id )
    """
    nb = []
    for k in traci.lane.getLastStepVehicleIDs(lane):
        pos = traci.vehicle.getLanePosition(k)
        if pos >= 100:
            nb.append(pos)
    return len(nb)

def lanes_id():
    """ return a list of all lane identificator """
    lanes = []
    for id_lane in ["_0"]: # right turn protected for now else use ["_0", "_1", "_2"]
        for edg in ["2to1", "3to1", "4to1", "5to1"]:
            lanes.append(edg+id_lane)
    return lanes

def get_light_command(lights, light):
    for interval in lights:
        if light >= interval[0] and light <= interval[1]: 
            return lights[interval]


def plot(waiting):
    colors = ("red", "yellow", "green", "blue")
    x = [i for i in range(0, 350, 10)]
    output_file("classic.html")
    p = figure(title="average waiting time per direction", x_axis_label='step (seconds)', y_axis_label='avg waiting time')
    for lane in waiting:
        p.line(x, waiting[lane], legend=lane+str(sum(waiting[lane])), line_width=2, line_color=colors[waiting.keys().index(lane)])
    show(p)
########################################################
table = PrettyTable(["Step", "from_east", "from_west", "from_north", "from_south"])
lane_table = PrettyTable(["Lane", "Q length", "Awt"])
lanevar_table = PrettyTable(["Lane", "Tin", "Tout"])
data = {
	"east": 0,
	"west": 0,
	"north": 0,
	"south": 0,
}

#initiate lanes' objects
ln, ls, le, lw = Lane("north"), Lane("south"), Lane("east"), Lane("west")
lanes = [le, lw, ln, ls]
lanes = {
    "east": le,
    "west": lw,
    "north":ln,
    "south": ls,
}
#initiate variables
lane_data = {
    "east": 0,
    "west": 0,
    "north": 0,
    "south": 0,
}
inter = Intersection("Intersection 1")
inter.attach(lanes)
lights = {
            (0, 30):   "rrrrggggrrrrgggg",
            (30, 60):  "ggggrrrrggggrrrr",
        }


def run():
    global lanes, vec_sum, lane_data, intersection, lights
    traci.init(PORT)
    step = 0
    data_count = inter.cycle
    while step < MAX_STEP:
        traci.simulationStep()
        data =  dict(zip( [key for key in ["east", "west", "north", "south"]], [ value for value in [ numberv(i) for i in lanes_id()]]))
        for i in ["east", "west", "north", "south"]:
            if data[i] > lane_data[i]:
                inter.lanes[i].Tin += [step]*(data[i] - lane_data[i])
            else:
                inter.lanes[i].Tout += [step]*(lane_data[i] - data[i])
        lane_data = data
        step += 1
        data_count -= 1
        """
        light = get_light_command(lights, data_count)
        #traci.trafficlights.setRedYellowGreenState("1", light)
        if data_count ==0:
            lights = inter.getCommand(step) # update the light cycle
            print lights
            data_count = inter.cycle    # update the cycle
            print "cycle updated ",data_count
        """
    traci.close()
    for lane in inter.lanes:
        print "lane ", inter.lanes[lane].id, len(inter.lanes[lane].Tin), len(inter.lanes[lane].Tout)
        print inter.lanes[lane].Tin
        print inter.lanes[lane].Tout
    print "========================"
    waiting = {
    "east": [],
    "west": [],
    "north":[],
    "south":[]
    }
    for lane in inter.lanes:
        for i in range(0, 350, 10):
            #print "lane ", inter.lanes[lane].id, "step", i, inter.lanes[lane].getQl(i), inter.lanes[lane].getAwt(i)
            waiting[lane].append(inter.lanes[lane].getAwt(i))
    plot(waiting)
    print "real number is :",cnt







# this is the main entry point of this script
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    print "[+] starting"
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo')
    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    sumoProcess = subprocess.Popen([sumoBinary, "-c", "hello.sumo.cfg", "-a", "hello.indloop.xml", "--queue-output", "queue.xml", "--remote-port", str(PORT)], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb')) #stdout=sys.stdout, stderr=sys.stderr)
    run()
    sumoProcess.wait()
