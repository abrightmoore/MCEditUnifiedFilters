# This filter flood fills from the selection box's centre block using that block's material.
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# v2 - GersinMC wants to move the fill start location around a bit. Also default to fill air.

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox

inputs = (
	  ("FILL3D", "label"),
	  ("Fill Material:", alphaMaterials.Stone),
	  ("Start from:", ("Box centre","Box bottom","Box top","Ignore 1x1 holes")),
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

def perform(originalLevel, originalBox, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform FILLter"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(originalLevel,originalBox,options,method) # Log start
	SUCCESS = False
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(width,height,depth))

	Fill3D(level, box, options)		

	
	SUCCESS = True
		
	# Conditionally copy back the working area into the world
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096); b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)

	FuncEnd(originalLevel,box,options,method) # Log end
	
def Fill3D(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "Fill3D"
	print '%s: Started at %s' % (method, time.ctime())
	material = (options["Fill Material:"].ID, options["Fill Material:"].blockData)
	startFrom = options["Start from:"]
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	ignore1x1 = False
	if options["Start from:"] == "Ignore 1x1 holes":
		ignore1x1 = True
	# END CONSTANTS

	matchBlock = (level.blockAt(box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth), level.blockDataAt(box.minx+centreWidth, box.miny+centreHeight, box.minz+centreDepth))
	Q = []
	if startFrom == "Box bottom":
		Q.append( (centreWidth, 0, centreDepth) )
	elif startFrom == "Box top":
		Q.append( (centreWidth, height-1, centreDepth) )
	else: # Box Centre or ignore 1x1 holes
		Q.append( (centreWidth, centreHeight, centreDepth) )

	while len(Q) > 0:
		(x, y, z) = Q.pop()
		if (ignore1x1 == False and (matchBlock == (level.blockAt(box.minx+x, box.miny+y, box.minz+z), level.blockDataAt(box.minx+x, box.miny+y, box.minz+z)))) or (ignore1x1 == True and ((matchBlock == (level.blockAt(box.minx+x, box.miny+y, box.minz+z), level.blockDataAt(box.minx+x, box.miny+y, box.minz+z))) and matchBlock == (level.blockAt(box.minx+x-1, box.miny+y, box.minz+z), level.blockDataAt(box.minx+x-1, box.miny+y, box.minz+z)) and matchBlock == (level.blockAt(box.minx+x+1, box.miny+y, box.minz+z), level.blockDataAt(box.minx+x+1, box.miny+y, box.minz+z)) and matchBlock == (level.blockAt(box.minx+x, box.miny+y-1, box.minz+z), level.blockDataAt(box.minx+x, box.miny+y-1, box.minz+z)) and matchBlock == (level.blockAt(box.minx+x, box.miny+y+1, box.minz+z), level.blockDataAt(box.minx+x, box.miny+y+1, box.minz+z)) and matchBlock == (level.blockAt(box.minx+x, box.miny+y, box.minz+z-1), level.blockDataAt(box.minx+x, box.miny+y, box.minz+z-1)) and matchBlock == (level.blockAt(box.minx+x, box.miny+y, box.minz+z+1), level.blockDataAt(box.minx+x, box.miny+y, box.minz+z+1)) )):
			setBlock(level, material, box.minx+x, box.miny+y, box.minz+z)
			if x-1 >= 0:
				Q.append( (x-1, y, z) )
			if x+1 < width:
				Q.append( (x+1, y, z) )
			if y-1 >= 0:
				Q.append( (x, y-1, z) )
			if y+1 < height:
				Q.append( (x, y+1, z) )
			if z-1 >= 0:
				Q.append( (x, y, z-1) )
			if z+1 < depth:
				Q.append( (x, y, z+1) )
		print '%s' % (len(Q))

	print '%s: Ended at %s' % (method, time.ctime())
	
############# METHOD HELPERS #############
	
def FuncStart(level, box, options, method):
	# abrightmoore -> shim to prepare a function.
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)	
	
	# other initialisation methods go here
	return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
	print '%s: Ended at %s' % (method, time.ctime())