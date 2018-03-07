# This filter creates a boulder.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials


inputs = (
	  ("BOULDER", "label"),
	  ("Material:", alphaMaterials.Cobblestone),
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
	Boulder(level, box, options)		
	level.markDirtyBox(box)
	
def Boulder(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "BOULDER"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	material = (options["Material:"].ID, options["Material:"].blockData)
	AIRBLOCK = 0
	AIR = (AIRBLOCK,0)
	destY = 127
	destX = 0
	destZ = 0
	# END CONSTANTS

	boulder = zeros( (width, height, depth) )

	# choose three points on the edges of the box - defines a plane. Mark the blocks to delete from this corner

	numIterations = randint(1,4)

	for iters in xrange(0, numIterations):
		# Corners
		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	


		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[iterX][height-1-iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, width)
		depthP = randint(1, depth)
		heightP = randint(1, height)
		for iterX in xrange(0, widthP):
			heightHere = heightP - (iterX*heightP/widthP)
			depthHere = depthP - (iterX*depthP/widthP)
			# carve out the triangle described by these dimensions
			for iterY in xrange(0, (int)(heightHere)):
				depthRightHere = depthHere - (iterY*depthHere/heightHere)
				for iterZ in xrange(0, (int)(depthRightHere)):
					boulder[width-1-iterX][height-1-iterY][depth-1-iterZ] = 1 # denotes an air block	

		# long vertical edges
		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[width-1-iterX][iterY][iterZ] = 1 # denotes an air block	

		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		widthP = randint(1, centreWidth)
		depthP = randint(1, centreDepth)
		for iterY in xrange(0, height):
			for iterX in xrange(0, widthP):
				depthHere = depthP - (iterX*depthP/widthP)
				for iterZ in xrange(0, (int)(depthHere)):
					boulder[width-1-iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		# long horizontal edges
		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][iterY][depth-1-iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		depthP = randint(1, centreDepth)
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depthP):
				heightHere = heightP - (iterZ*heightP/depthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][depth-1-iterZ] = 1 # denotes an air block	


		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[iterX][height-1-iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[width-1-iterX][iterY][iterZ] = 1 # denotes an air block	

		heightP = randint(1, centreHeight)
		widthP = randint(1, centreWidth)
		for iterZ in xrange(0, depth):
			for iterX in xrange(0, widthP):
				heightHere = heightP - (iterX*heightP/widthP)
				for iterY in xrange(0, (int)(heightHere)):
					boulder[width-1-iterX][height-1-iterY][iterZ] = 1 # denotes an air block	
	
	
	for iterX in xrange(0, width):
		for iterY in xrange(0, height):
			for iterZ in xrange(0, depth):
				if boulder[iterX][iterY][iterZ] == 0:
					setBlock(level, material, box.minx+iterX, box.miny+iterY, box.minz+iterZ)
	
					
	print '%s: Ended at %s' % (method, time.ctime())