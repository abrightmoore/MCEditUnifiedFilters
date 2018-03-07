# This filter creates cubes in Minecraft. I know.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("CUBIFY", "label"),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
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

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Cubify(level, box, options)		
	level.markDirtyBox(box)
	
def Cubify(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Cubify"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIRBLOCK = -1 #0
	AIR = (AIRBLOCK,0)
	DESTY = 128
	DESTX = 0
	DESTZ = 0
	# END CONSTANTS

	PanelWidth = (int)(width/4)
	PanelDepth = (int)(depth/3)
	
	#  5
	# 1234
	#  6
	
	
	# Panel 1
	print '%s: Panel 1 started at %s' % (method, time.ctime())
	for iterX in xrange(0,PanelWidth):
		for iterZ in xrange(PanelDepth,2*PanelDepth):
			for iterY in xrange(0, height):
				tempBlock = (level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ), level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ))
				if tempBlock != AIR:
					setBlock(level, 
						 tempBlock,
						 DESTX - PanelWidth/2 - iterY,
						 DESTY - PanelWidth/2 + iterX,
						 DESTZ - PanelDepth/2 + (iterZ-PanelDepth)
						)

	# Panel 2
	print '%s: Panel 2 started at %s' % (method, time.ctime())
	for iterX in xrange(PanelWidth, 2*PanelWidth):
		for iterZ in xrange(PanelDepth,2*PanelDepth):
			for iterY in xrange(0, height):
				tempBlock = (level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ), level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ))
				if tempBlock != AIR:
					setBlock(level, 
						 tempBlock,
						 DESTX - PanelWidth/2 + (iterX-PanelWidth),
						 DESTY + PanelWidth/2 + iterY,
						 DESTZ - PanelDepth/2 + (iterZ-PanelDepth)
						)



	# Panel 3
	print '%s: Panel 3 started at %s' % (method, time.ctime())
	for iterX in xrange(2*PanelWidth, 3*PanelWidth):
		for iterZ in xrange(PanelDepth,2*PanelDepth):
			for iterY in xrange(0, height):
				tempBlock = (level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ), level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ))
				if tempBlock != AIR:
					setBlock(level, 
						 tempBlock,
						 DESTX + PanelWidth/2 + iterY,
						 DESTY + PanelWidth/2 - (iterX-2*PanelWidth),
						 DESTZ - PanelDepth/2 + (iterZ-PanelDepth)
						)



	# Panel 4
	print '%s: Panel 4 started at %s' % (method, time.ctime())
	for iterX in xrange(3*PanelWidth, 4*PanelWidth):
		for iterZ in xrange(PanelDepth,2*PanelDepth):
			for iterY in xrange(0, height):
				tempBlock = (level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ), level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ))
				if tempBlock != AIR:
					setBlock(level, 
						 tempBlock,
						 DESTX + PanelWidth/2 - (iterX-3*PanelWidth),
						 DESTY - PanelWidth/2 - iterY,
						 DESTZ - PanelDepth/2 + (iterZ-PanelDepth)
						)


	# Panel 5
	print '%s: Panel 5 started at %s' % (method, time.ctime())
	for iterX in xrange(PanelWidth, 2*PanelWidth):
		for iterZ in xrange(0,PanelDepth):
			for iterY in xrange(0, height):
				tempBlock = (level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ), level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ))
				if tempBlock != AIR:
					setBlock(level, 
						 tempBlock,
						 DESTX - PanelWidth/2 + (iterX-PanelWidth),
						 DESTY + PanelWidth/2 - iterZ,
						 DESTZ + PanelDepth/2 + iterY
						)


	# Panel 6
	print '%s: Panel 6 started at %s' % (method, time.ctime())
	for iterX in xrange(PanelWidth, 2*PanelWidth):
		for iterZ in xrange(2*PanelDepth,3*PanelDepth):
			for iterY in xrange(0, height):
				tempBlock = (level.blockAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ), level.blockDataAt(box.minx+iterX,box.miny+iterY,box.minz+iterZ))
				if tempBlock != AIR:
					setBlock(level, 
						 tempBlock,
						 DESTX - PanelWidth/2 + (iterX-PanelWidth),
						 DESTY + PanelWidth/2 - (iterZ-2*PanelDepth),
						 DESTZ - PanelDepth/2 - iterY
						)


					
	print '%s: Ended at %s' % (method, time.ctime())