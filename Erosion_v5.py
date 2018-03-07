# This filter erodes the environment
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *

inputs = (
  ("Depth of erosion", 5),
  ("Main Material:", "blocktype"),
  ("Secondary Material:", "blocktype"),
  ("Highlight Material:", "blocktype"),
)

# Utility methods

def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt(x,y,z)
    if tempBlock == 0:
	setBlock(level, (block, data), x, y, z)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
    	level.setBlockDataAt(x, y, z, data)


def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, y):
    	setBlockIfEmpty(level, (block, data), x, iterY, z)
    	

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def fix(angle):
	while angle > pi:
		angle = angle - 2 * pi
	while angle < -pi:
		angle = angle + 2 * pi
	return angle

def Erode(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = "Erode"
	PROBABILITY = options["Depth of erosion"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	stepRadiusWidth = (float)(centreWidth/100.0)
	stepRadiusDepth = (float)(centreDepth/100.0)
	stepHeight = (float)(height/100.0)
	AIR = (0,0)
	# END CONSTANTS

	# Pass 1 - mark and replace
	for iterX in xrange(box.minx, box.maxx):
		print '%s: Erode %s of %s' % (method, iterX-box.minx, width)
		for iterZ in xrange(box.minz, box.maxz):
			erodedepth = randint(0,PROBABILITY)
			minY = box.maxy-1
			iterY = box.maxy-1
			while iterY >= box.miny:		
				tempBlock = (level.blockAt(iterX,iterY,iterZ), level.blockDataAt(iterX,iterY,iterZ))
				if tempBlock <> AIR:
					dice = randint(0,100) # Replace to limit
					if dice >= 50:
						block = materialMain
					elif randint(0,100) <= 10:
						block = materialSecondary
					else:
						block = materialHighlight
					setBlock(level, block, iterX, iterY, iterZ) # Replace original block position with AIR
					erodedepth = erodedepth - 1
					if erodedepth <= 0:
						minY = iterY
						iterY = box.miny # stop
				iterY = iterY -1
			level.markDirtyBox(box) # Testing if there's a caching/timing thing going on
			
			# Pass 2, fall
			lastSolidY = box.miny
			iterY = box.miny
			while iterY < box.maxy:
				tempBlock = (level.blockAt(iterX,iterY,iterZ), level.blockDataAt(iterX,iterY,iterZ))
				if (tempBlock == materialMain and materialMain <> AIR) or (tempBlock == materialSecondary and materialSecondary <> AIR) or (tempBlock == materialHighlight and materialHighlight <> AIR) and (level.blockAt(iterX,iterY-1,iterZ) == 0):
					# print '%s: Fall %s of %s at block %s' % (method, iterY, box.maxy, tempBlock)
					# fall! Where to?				
					if iterY > lastSolidY:
						setBlockIfEmpty(level, tempBlock, iterX, lastSolidY, iterZ) # Place block at lowest air position
						setBlock(level, AIR, iterX, iterY, iterZ) # Replace original block position with AIR						
						lastSolidY = lastSolidY+1 # hunt for next available position, start above the block just placed
						keepGoing = 1
						while keepGoing == 1:
							if level.blockAt(iterX, lastSolidY, iterZ) == 0:
								keepGoing = 0
							lastSolidY = lastSolidY+1
							if lastSolidY == box.maxy:
								keepGoing = 0 # give up, no free air found within the current pile.
								iterY = box.maxy # break hunt
				iterY = iterY + 1

	# Pass 3 - determine a connection graph to the ground. Remove anything not connected in some way to ground
	# Initialise the connected array
	conn = zeros((width,height,depth))
				
	for passcounter in xrange(0,2): # Do this twice. First pass is setup the first layer and direct vertical connections, second pass is deeper evaluation
		for iterY in xrange(box.miny, box.maxy): # start from the bottom
			print '%s: Connect check %s %s of %s' % (method, passcounter, iterY-box.miny, height)
			for iterX in xrange(box.minx, box.maxx):
				for iterZ in xrange(box.minz, box.maxz):
					
					if iterY == box.miny: # first layer is considered connected if a non-air block is below. Sides aren't currently checked
						if level.blockAt(iterX, iterY-1, iterZ) <> 0:
							print '%s: array %s of %s' % (method, iterZ,box.minz)
							
							conn[   iterX-box.minx,
								iterY-box.miny,
								iterZ-box.minz] = 1
								
					else: # work out if a colleague is connected
						if level.blockAt(iterX, iterY, iterZ) <> 0: # current block is not air
							blockcount = 0
							for iter in xrange(-1,1):
								if iterX > box.minx and iterX < box.maxx-1:
									if iter <> 0 and conn[iterX+iter-box.minx, iterY-box.miny, iterZ-box.minz] == 1: # Count the not-air blocks
										blockcount = blockcount + 1
							for iter in xrange(-1,1):
								if iterY > box.miny and iterY < box.maxy-1:
									if iter <> 0 and conn[iterX-box.minx, iterY+iter-box.miny, iterZ-box.minz] == 1: # Count the not-air blocks
										blockcount = blockcount + 1
							for iter in xrange(-1,1):
								if iterZ > box.minz and iterZ < box.maxz-1:
									if iter <> 0 and conn[iterX-box.minx, iterY-box.miny, iterZ+iter-box.minz] == 1: # Count the not-air blocks
										blockcount = blockcount + 1
							if blockcount > 0: # a known path to the ground exists
								conn[iterX-box.minx,iterY-box.miny,iterZ-box.minz] = 1
						else:
							conn[iterX-box.minx,iterY-box.miny,iterZ-box.minz] = 0 # block is air, not connected nor connectable

	# Purge!
	for iterY in xrange(box.miny, box.maxy): # start from the bottom
		for iterX in xrange(box.minx, box.maxx):
			for iterZ in xrange(box.minz, box.maxz):
				if conn[iterX-box.minx,iterY-box.miny,iterZ-box.minz] == 0:
					setBlock(level, AIR, iterX, iterY, iterZ)



def perform(level, box, options):
	''' This script is used to erode the contents of a selected box. Feedback to abrightmoore@yahoo.com.au '''

	Erode(level, box, options)		
	
	level.markDirtyBox(box)