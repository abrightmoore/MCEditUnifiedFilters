# This filter duplicates the selection box in the direction specified for a number of instances you define.
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *

inputs = (
  ("REPEAT by abrightmoore@yahoo.com.au (http://brightmoore.net)", "label"), # Thanks InHaze for the usage tips!
  ("Select a region then choose the number of copies to make, and which direction to make them in.", "label"), # Suggested by http://www.reddit.com/user/PinkiePieladin, Thread: http://www.reddit.com/r/Minecraft/comments/14zo30/oceana/c7i0gg5
  ("Number of instances", 5),
  ("Direction", ("Up", "Down", "Shake it all around", "North", "South", "East", "West")),
  
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

def Repeat(level, box, options):
	# CONSTANTS AND VARIABLES
	NUMBER_OF_INSTANCES = options["Number of instances"]
	DIRECTION = options["Direction"]
	method = "Repeaterificational"

	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	UP_DOWN = 0
	SHAKEITALLAROUND = 0
	NORTH_SOUTH = 0
	EAST_WEST = 0
	
	if DIRECTION == "Up":
		UP_DOWN = 1
	elif DIRECTION == "Down":
		UP_DOWN = -1
	elif DIRECTION == "North":
		NORTH_SOUTH = 1
	elif DIRECTION == "South":
		NORTH_SOUTH = -1
	elif DIRECTION == "East":
		EAST_WEST = 1
	elif DIRECTION == "West":
		EAST_WEST = -1
	elif DIRECTION == "Shake it all around":
		SHAKEITALLAROUND = 1

	
	# Copy the selected box in the specified direction for the nominated number of times.
	for iterX in xrange(box.minx, box.maxx):
		print '%s: %s of %s' % (method, iterX-box.minx, width-1)
		for iterY in xrange(box.miny, box.maxy):
			for iterZ in xrange(box.minz, box.maxz):
				for iterInstances in xrange(1, NUMBER_OF_INSTANCES+1):
					
					setBlock(level, 
						 (level.blockAt(iterX,iterY,iterZ), level.blockDataAt(iterX,iterY,iterZ)),
						 iterX + EAST_WEST*iterInstances*width + SHAKEITALLAROUND*(randint(-NUMBER_OF_INSTANCES,NUMBER_OF_INSTANCES)),
						 iterY + UP_DOWN*iterInstances*height + SHAKEITALLAROUND*(randint(-NUMBER_OF_INSTANCES,NUMBER_OF_INSTANCES)),
						 iterZ + NORTH_SOUTH*iterInstances*depth + SHAKEITALLAROUND*(randint(-NUMBER_OF_INSTANCES,NUMBER_OF_INSTANCES))
						)


def perform(level, box, options):
	''' This script is used to erode the contents of a selected box. Feedback to abrightmoore@yahoo.com.au '''

	Repeat(level, box, options)		
	
	level.markDirtyBox(box)