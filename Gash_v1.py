# This filter deforms the terrain in the selection box by creating a gash in the surface of the world
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *

inputs = (
	  ("GASH abrightmoore@yahoo.com.au http://brightmoore.net", "label"),
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

def Gash(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Gash"
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS


	if depth > width: # The gash runs the length of the selection box, whichever the orientation
	
		angleStart = randint(0,100)
		angleEnd = randint(100,200)
		angleStepSizeZ = (pi/50*(angleEnd-angleStart))/depth # describes the arc of the gash
		gashAngleStart = pi/50*angleStart
		gashStepSize = pi/depth # one full revolution
		
		for iterZ in xrange(0, depth):
			iterX = (int)(centreWidth*sin(gashAngleStart+angleStepSizeZ * iterZ))
			
			gashWidth = (int)(centreWidth*sin(gashStepSize*iterZ)/2)

			for iterY in xrange(0, height):			
				heightBand = 2 - (int)((iterY / (height / 2)))

				for sizeX in xrange(-gashWidth+heightBand,gashWidth-heightBand):
					posX = (float)(iterX+sizeX)

					gashWidthMultiplier = (float)(iterY/height)
										
					setBlock(level, 
						 AIR,
						 box.minx+centreWidth+(int)(posX),
						 box.miny+iterY,
						 box.minz+iterZ
						)				
		
	
	else:
		angleStart = randint(0,100)
		angleEnd = randint(100,200)
		angleStepSizeX = (pi/50*(angleEnd-angleStart))/width # describes the arc of the gash
		gashAngleStart = pi/50*angleStart
		gashStepSize = pi/width # one full revolution
		
		for iterX in xrange(0, width):
			iterZ = (int)(centreDepth*sin(gashAngleStart+angleStepSizeX * iterX))
			
			gashWidth = (int)(centreDepth*sin(gashStepSize*iterX)/2)

			for iterY in xrange(0, height):
				heightBand = 2 - (int)((iterY / (height / 2)))
				
				for sizeZ in xrange(-gashWidth+heightBand,gashWidth-heightBand):
					posZ = (float)(iterZ+sizeZ)
					
					setBlock(level, 
						 AIR,
						 box.minx+iterX,
						 box.miny+iterY,
						 box.minz+centreDepth+(int)(posZ)
						)					

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''

	Gash(level, box, options)		
	
	level.markDirtyBox(box)