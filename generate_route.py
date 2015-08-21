#script to generate routes ( vehicles )
#coded by sayf eddine 30/07/2015
########################################
import random
#define vehicles' probabilities
pWE = 1./7
pSN = 1./3
pNS = 1./2
pEW = 1./7
pWCSN = -1./7
N = 20


def generate():
	with open("hello.rou.xml", "w") as routes:
		print >>routes, """<routes>
	<vType guiShape="passenger/hatchback" accel="1.0" decel="5.0" id="Car1" length="4.0" maxSpeed="100.0" sigma="0.0" />

	<route id="routewe" edges="3to1 1to2" />
	<route id="routesn" edges="5to1 1to4" />
	<route id="routens" edges="4to1 1to5" />
	<route id="routeew" edges="2to1 1to3" />
	<route id="routeWCSN" edges="3to1 1to5 5to1 1to4" />
	<vehicle depart="0" id="we" route="routewe" type="Car1" />"""
		#generate vehicle
		counter = 0
		for i in range(N):
			if random.uniform(0,1) < pWE:
				print >>routes, """<vehicle depart="%s" id="we_%s" route="routewe" type="Car1" />""" %(i, counter)
				counter+=1
			if random.uniform(0,1) < pSN:
				print >>routes, """<vehicle depart="%s" id="sn_%s" route="routesn" type="Car1" />""" %(i, counter)
				counter+=1
			if random.uniform(0,1) < pNS:
				print >>routes, """<vehicle depart="%s" id="ns_%s" route="routens" type="Car1" />""" %(i, counter)
				counter+=1
			if random.uniform(0,1) < pEW:
				print >>routes, """<vehicle depart="%s" id="ew_%s" route="routeew" type="Car1" />""" %(i, counter)
				counter+=1
			if random.uniform(0,1) < pWCSN:
				print >>routes, """<vehicle depart="%s" id="wecn_%s" route="routeWCSN" type="Car1" />""" %(i, counter)
				counter+=1


		print >>routes, "</routes>"
		print "Success"
		return counter+1
print generate()