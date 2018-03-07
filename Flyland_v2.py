# This filter uses the selection box to create a floating island from the land within it.
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from pymclevel import alphaMaterials
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *


inputs = (
	  ("FLYLAND abrightmoore@yahoo.com.au http://brightmoore.net", "label"),
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

def Flyland(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Flyland"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	# The scan region is a vertical cylinder in the selection box

	ANGLESTEPSIZEX = pi/width 	# I like to shout when it comes to constants. For each step in the width direction, this is how much rotation around a unit circle occurs

	# Step 1 - find the maximum height of the blocks in the area. The difference between that height and the top of the box is how much the blocks will be moved.
	myBox = zeros( (width,height,depth,2) )
	surfaceLayer = height
	lastBlockCount = 0
	currentBlockCount = 0
	highestBlockLayer = 0

	iterY = height-1
	while iterY >= 0:
		currentBlockCount = 0

		for iterX in xrange(0, width):

			angleX = ANGLESTEPSIZEX*iterX
			minMaxZ = (int)(sin(angleX)*centreDepth)
			
			iterZ = -minMaxZ
			while iterZ < minMaxZ:  # This method is slightly better than rotation mapping for speed and leaving no holes due to rounding

				(block, blockData) = (level.blockAt(box.minx + iterX, box.miny + iterY, box.minz + centreDepth + iterZ), level.blockDataAt(box.minx + iterX, box.miny + iterY, box.minz + centreDepth + iterZ))
				myBox[iterX, iterY, iterZ+centreDepth, 0] = block
				myBox[iterX, iterY, iterZ+centreDepth, 1] = blockData # cache a copy. We'll bring it back when wrenching it from the ground into the sky later.
				# print 'Block = %s, BlockData = %s' % (myBox[iterX, iterY, iterZ+centreDepth,0], myBox[iterX, iterY, iterZ+centreDepth,1])
				if block != 0:
					currentBlockCount = currentBlockCount + 1 # found a non-air block.
					if currentBlockCount > lastBlockCount:  # new candidate for the surface height! Lock it in.
						surfaceLayer = iterY
						lastBlockCount = currentBlockCount

					if highestBlockLayer == 0: # we haven't seen a non-air block yet
						highestBlockLayer = iterY # ... and now we have seen our first, therefore highest, non-air block
						# print 'Highest block layer found at %s' % (highestBlockLayer)
				iterZ = iterZ +1
		iterY = iterY - 1
				
	# Coming out of step 1 the surface of the land has been located and is in "surfaceLayer". The highest block has been identified and is in "highestBlockLayer".

	amountToRaiseTheChunk = height - highestBlockLayer

	print '%s: Surface at %s, Highest block at %s, Amount to raise the land is %s' % (method, surfaceLayer, highestBlockLayer, amountToRaiseTheChunk)

	# Step 2 - shift the region of interest upwards! Take everything in a sort of conical section below the surface.
	
	typeOfSubsurface = randint(0,5)  # randomly upheave different shapes from the land
	
	RANDMULTIPLIER = randint(1,8)
	
	
	
	for iterX in xrange(0, width):
		angleX = ANGLESTEPSIZEX*iterX
		minMaxZ = (int)(sin(angleX)*centreDepth)
		radiusMax = ( sqrt(centreWidth * centreWidth + minMaxZ * minMaxZ))	
		ANGLE = pi/2/radiusMax
		ANGLE2 = ANGLE/8*RANDMULTIPLIER
		iterZ = -minMaxZ
		while iterZ < minMaxZ:  # This method is slightly better than rotation mapping for speed and leaving no holes due to rounding
			deltaX = centreWidth - iterX
			localRadius = sqrt(deltaX*deltaX + iterZ*iterZ)
			
			if typeOfSubsurface == 0:
				depthToCopy = localRadius /  radiusMax * surfaceLayer  # Magic math for the subsurface column at this x,z point
			elif typeOfSubsurface == 1:
				depthToCopy = localRadius /  radiusMax * surfaceLayer - randint(0,2)  # Magic math for the subsurface column at this x,z point
			elif typeOfSubsurface == 2:
				depthToCopy = sin(localRadius * ANGLE) * surfaceLayer
			elif typeOfSubsurface == 3:
				depthToCopy = (localRadius * localRadius)
				if depthToCopy > surfaceLayer:
					depthToCopy = surfaceLayer
				depthToCopy = depthToCopy - randint(0,(surfaceLayer/3))
			else:
				depthToCopy = sin(localRadius * ANGLE2) * surfaceLayer
						
			depthToCopyTo = (int)( depthToCopy ) # Depending on where we are on the disc of land, the depth under the surface to be copied varies
			if depthToCopyTo < 0:
				depthToCopyTo = 0
			elif depthToCopyTo > surfaceLayer:
				depthToCopyTo = surfaceLayer
				
			# print 'depthToCopyTo is %s' % (depthToCopyTo)
			iterY = highestBlockLayer
			while iterY > depthToCopyTo: # for each vertical column of blocks, shift up by amountToRaiseTheChunk.
				setBlock(level, (myBox[iterX, iterY, iterZ+centreDepth,0],myBox[iterX, iterY, iterZ+centreDepth,1]), box.minx+iterX, box.miny+iterY + amountToRaiseTheChunk, box.minz+centreDepth+iterZ) # copy
				setBlock(level, AIR, box.minx+iterX, box.miny+iterY, box.minz+centreDepth+iterZ) # ... then clear

				iterY = iterY - 1
			iterZ = iterZ +1


	print '%s: Ended at %s' % (method, time.ctime())


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''

	Flyland(level, box, options)		
	
	level.markDirtyBox(box)