# This filter subsides the land - caves collapse
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *

inputs = (
  ("This filter subsides the land - caves collapse", "label"),
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


def Subside(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Subside"
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	# Pass 1 - mark and replace
	for iterX in xrange(box.minx, box.maxx):
		print '%s: Subside %s of %s' % (method, iterX-box.minx, width-1)
		for iterZ in xrange(box.minz, box.maxz):
			# Pass 1, fall
			iterY = box.miny
			lastSolidY = iterY-1
			
			x = iterX - box.minx - centreWidth
			z = iterZ - box.minz - centreDepth
			
			if x*x + z*z < centreDepth*centreWidth:
				lastSolidY = lastSolidY+1 # hunt for next available position, start above the block just placed
				keepGoing = 1
				while keepGoing == 1:
					if level.blockAt(iterX, lastSolidY, iterZ) == 0:
						lastSolidY = lastSolidY-1
						keepGoing = 0
					lastSolidY = lastSolidY+1
					if lastSolidY == box.maxy: # No air?
						keepGoing = 0 # give up, no free air found within the current pile.			
					else: # There is air
						while iterY < box.maxy:
							tempB = level.blockAt(iterX,iterY,iterZ)
							if (tempB <> 0 and level.blockAt(iterX,iterY-1,iterZ) == 0):
								# print '%s: Fall %s of %s at block %s' % (method, iterY, box.maxy, tempBlock)
								# fall! Where to?				
								if iterY > lastSolidY:
									tempBlock = (tempB, level.blockDataAt(iterX,iterY,iterZ))
									setBlockIfEmpty(level, tempBlock, iterX, lastSolidY, iterZ) # Place block at lowest air position
									setBlock(level, AIR, iterX, iterY, iterZ) # Replace original block position with AIR						
									level.markDirtyBox(box)
									lastSolidY = lastSolidY+1 # hunt for next available position, start above the block just placed
									keepGoing = 1
									while keepGoing == 1:
										if level.blockAt(iterX, lastSolidY, iterZ) == 0:
											lastSolidY = lastSolidY-1	
											keepGoing = 0
										lastSolidY = lastSolidY+1
										if lastSolidY == box.maxy:
											keepGoing = 0 # give up, no free air found within the current pile.
											iterY = box.maxy # break hunt
								# else:
								#	print 'Subside error - air block was missed! %s %s %s' % (iterY, lastSolidY, iterZ)
							iterY = iterY + 1


def perform(level, box, options):
	''' This script is used to erode the contents of a selected box. Feedback to abrightmoore@yahoo.com.au '''

	Subside(level, box, options)		
	
	level.markDirtyBox(box)