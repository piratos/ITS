"""
Lane class
coded by sayfeddine
"""

class Lane:
	def __init__(self, id1):
		self.id = id1
		self.Ql = 0         # Queue length
		self.Awt = 0        # average waiting time for the queue
		self.Tin = []       # instance where vehicles enter lane queue, instance is on form (step)
		self.Tout = []      # instance where vehicle leave lane queue, instance is on form (step)

	def getPriority(self, step):
		return self.getAwt(step) + self.getQl(step)

	def getTinBefore(self, step):
		return [i for i in self.Tin if i <= step]

	def getQl(self, step):
		return len(self.Tin) - len(self.leave_at_step(step))

	def leave_at_step(self, step):
				return [ i for i in self.Tout if i <= step ]

	def getAwt(self, step): #returning the sum for now #equation down is the sum of the wainting time for each vec until step
		return (len( self.Tin[ len(self.leave_at_step(step) ) : ] )*step - sum( self.getTinBefore(step)[ len(self.leave_at_step(step) ) : ] ))/(max(float(self.getQl(step)), 1.00))

if __name__ == "__main__":
	l = Lane("l1")
	l.Tin = [1,2,3,4,5]
	l.Tout = [5, 6]
