#Intersection class, the processing unit where traffic light control takes place
#coded by sayfeddine

DEFAULT_CYCLE = 60 # default cycle length to start with ( in seconds or "step" for SUMO)
"""
cycle length formula : 
C = (1.5*L + 5)/(1.0 - SYi))
C : optimum cycle length that minimise the delay
cycle is always between 0.75*C and 1.5*C
L = Unusable time per cycle in seconds usually taken as a sum of the vehicle signal change intervals.
SYi = critical lane volume each phase/saturation flow
"""

class Intersection:
	"""
	For each intersection there will be an Intersection object instaciated
	attach method is used to add the lanes correspoding to the intersection
	the result for each cycle are accessible throught the getCommand() method
	"""

	def __init__(self, idIn):
		self.id = idIn				 # Intersection identification used if the problem is containing more than one intersection
		self.cycle = DEFAULT_CYCLE   # the cycle length starting with the DEFAULT value then adjusted by the algorithm
		self.lanes = []              # contains the list of all the lane connected to the intersection point
		self.right_protected = False # if set true then the right turn will be desattached ( protected mode)


	def attach(self, lanes):
		""" attach lanes of the Intersection to the object"""
		self.lanes = lanes


	def getCommand(self, step):
		"""Execute the algorithm then decide the cylce length and the signaling phases"""
		
		west = self.lanes["west"].getPriority(step)
		north = self.lanes["north"].getPriority(step)
		if (west + north) == 0:
			west, north = 0, 0
		else:
			west,north = west/(west+north), north/(west+north)

		east = self.lanes["east"].getPriority(step)
		south = self.lanes["south"].getPriority(step)
		
		if (east + south) == 0:
			east, south = 0, 0
		else:
			east, south = east/(east+south), south/(east+south)

		max_ph1, max_ph2 = max(west, east), max(north, south)
		if max_ph1>max_ph2:
			ring = max_ph1
		else:
			ring = 1-max_ph2


		self.cycle = DEFAULT_CYCLE # adjusting cycle length
		lights = {
			(0, self.cycle*ring): 			"rrrrggggrrrrgggg",
			(self.cycle*ring, self.cycle): 	"ggggrrrrggggrrrr",
		}
		return lights