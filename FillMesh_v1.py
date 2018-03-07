# This filter fills in gaps in a selection box
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *

inputs = (
  ("Number of blocks", 3),
  ("Fill Material:", "blocktype"),
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

def Fill(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	FILLMATERIAL = (options["Fill Material:"].ID, options["Fill Material:"].blockData)
	NUMBLOCKS = options["Number of blocks"]
	method = "FillMesh"
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS


	# Pass 1 - identify holes
	# Initialise the connected array
	blocksSet = zeros((width,height,depth))
				
	# Do this twice. First pass is setup air masking
	for iterY in xrange(box.miny+1, box.maxy-1): # start from the bottom
		print '%s: Air finder %s of %s' % (method, iterY-box.miny, height-2)
		for iterX in xrange(box.minx+1, box.maxx-1):
			for iterZ in xrange(box.minz+1, box.maxz-1):
				# work out if a peer block is populated
				if level.blockAt(iterX, iterY, iterZ) == 0: # current block is air
					blocksSet[iterX-box.minx,iterY-box.miny,iterZ-box.minz] = 1 # block is air
					#print 'Found air at %s %s %s' % (iterX, iterY, iterZ)
				else:
					blocksSet[iterX-box.minx,iterY-box.miny,iterZ-box.minz] = 0 # block is not air
					#print 'Found block at %s %s %s' % (iterX, iterY, iterZ)

	holesSet = zeros((width,height,depth))
	# Count the number of non-air blocks around air blocks
	for iterY in xrange(box.miny+1, box.maxy-1): # start from the bottom
		print '%s: Hole finder check %s of %s' % (method, iterY-box.miny, height-2)
		for iterX in xrange(box.minx+1, box.maxx-1):
			for iterZ in xrange(box.minz+1, box.maxz-1):
				# work out if a peer block is populated
				if blocksSet[iterX-box.minx, iterY-box.miny, iterZ-box.minz] == 1: # current block is air. Could be a hole
					#print 'Handling air at %s %s %s' % (iterX, iterY, iterZ)
					blockcount = 0
					for iter in xrange(-1,2):
						if iterX > box.minx and iterX < box.maxx:
							if iter <> 0 and blocksSet[iterX+iter-box.minx, iterY-box.miny, iterZ-box.minz] == 0: # Count the not-air blocks
								blockcount = blockcount + 1
						if iterY > box.miny and iterY < box.maxy:
							if iter <> 0 and blocksSet[iterX-box.minx, iterY+iter-box.miny, iterZ-box.minz] == 0: # Count the not-air blocks
								blockcount = blockcount + 1
						if iterZ > box.minz and iterZ < box.maxz:
							if iter <> 0 and blocksSet[iterX-box.minx, iterY-box.miny, iterZ+iter-box.minz] == 0: # Count the not-air blocks
								blockcount = blockcount + 1
					holesSet[iterX-box.minx,iterY-box.miny,iterZ-box.minz] = blockcount
					print 'Hole at %s %s %s %s %s' % (iterX, iterY, iterZ, holesSet[iterX-box.minx,iterY-box.miny,iterZ-box.minz], blockcount)
				else:
					#print 'Handling block at %s %s %s' % (iterX, iterY, iterZ)
					holesSet[iterX-box.minx,iterY-box.miny,iterZ-box.minz] = 0 # block is not air


	# Populate!
	for iterY in xrange(box.miny+1, box.maxy-1): # start from the bottom
		print '%s: Pasting blocks in holes %s of %s' % (method, iterY-box.miny, height-2)
		for iterX in xrange(box.minx+1, box.maxx-1):
			for iterZ in xrange(box.minz+1, box.maxz-1):
				#print 'Handling holes at %s %s %s %s %s' % (iterX, iterY, iterZ, holes[iterX-box.minx,iterY-box.miny,iterZ-box.minz], NUMBLOCKS)
				if (int)(holesSet[iterX-box.minx,iterY-box.miny,iterZ-box.minz]) >= (int)(NUMBLOCKS):
					setBlock(level, FILLMATERIAL, iterX, iterY, iterZ)
					print 'Handling holes at %s %s %s %s %s' % (iterX, iterY, iterZ, holesSet[iterX-box.minx,iterY-box.miny,iterZ-box.minz], NUMBLOCKS)


def perform(level, box, options):
	''' This script is used to erode the contents of a selected box. Feedback to abrightmoore@yahoo.com.au '''

	Fill(level, box, options)		
	
	level.markDirtyBox(box)