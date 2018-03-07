# This filter provides an in game pointer in the sky to blocks of interest
# Requested by @Helen269 on the forums
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob


# MCSchematic access method @TexelElf
# Texelelf's guidance:
#	from pymclevel import MCSchematic, mclevel
#	deformation = pymclevel.MCSchematic((width, height, length), mats=self.editor.level.materials)
#	deformation.setBlockAt(x,y,z,blockID)
#	deformation.setBlockDataAt(x,y,z,blockData)
#	deformation.Blocks[::4] = 57
#	schematic_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir? or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
#	deformation.saveToFile(schematic_file)
# And from Codewarrior0's filterdemo.py:
#	level.copyBlocksFrom(temp, temp.bounds, box.origin)

# Global constants
METHOD = "MAP MARKER"

inputs = (
	  ("MAPMARKER", "label"),
          ("Choose the block to locate:", "blocktype"),
          ("What should I look for?", ("Match Block Type Only", "Match Block Data") ),
#	  ("Ignore block IDs:", ("string","value=0 6 7 8 9 10 11 12 13 27 28 30 31 32 37 38 39 40 50 51 52 55 59 63 64 65 66 68 69 70 71 72 78 83 93 94 96 104 105 106 115 116 118 119 127 131 132 140 141 142 143 145 147 148 149 150 151 154 157") ),
          ("Main Material:", alphaMaterials.Stone),
          ("Secondary Material:", alphaMaterials.Cobblestone),
          ("Highlight Material:", alphaMaterials.WoodPlanks),
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

def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), maxLength ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)

	if distance < maxLength or maxLength < 1:
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			scratchpad.setBlockAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockID)
			scratchpad.setBlockDataAt(x+iter*cos(theta)*cos(phi), y+iter*sin(phi), z+iter*sin(theta)*cos(phi), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	print 'ANALYSE %s %s %s' % (width, height, depth)

	minX = width
	minY = height
	minZ = depth
	maxX = 0
	maxY = 0
	maxZ = 0
	found = False
	
	for iterY in xrange(0, height):
		for iterX in xrange(0, width):
			for iterZ in xrange(0, depth):
				if level.blockAt(iterX, iterY, iterZ) != 0:
					#print 'ANALYSING %s %s %s' % (iterX, iterY, iterZ)
					if iterX > maxX:
						maxX = iterX
					if iterY > maxY:
						maxY = iterY
					if iterZ > maxZ:
						maxZ = iterZ
				
					if iterX < minX:
						minX = iterX
					if iterY < minY:
						minY = iterY
					if iterZ < minZ:
						minZ = iterZ
						
					found = True

	print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	print '%s: Ended at %s' % (method, time.ctime())
	
	if found == False:
		return BoundingBox((0, 0, 0), (width, height, depth))	
	else:
		return BoundingBox((minX, 0, minZ), (maxX+1, maxY+1, maxZ+1))
	

def findSurface(x, y, z, level, box, options):
	# Find a candidate surface
	iterY = 250
	miny = y
	foundy = y
	while iterY > miny:
		block = level.blockAt(x,iterY,z)
		if block != 0: # not AIR
			#if (block not in ignoreList):
			foundy = iterY
			iterY = miny # end search, block found was a legitimate candidate for the surface				
		iterY = iterY -1
	return foundy


def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	mapMarker(level, box, options)		
	level.markDirtyBox(box)

def mapMarker(level, box, options):
	# CONSTANTS
	print '%s: Started at %s' % (METHOD, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	# END CONSTANTS

	baseBlock = options["Choose the block to locate:"].ID
	baseBlockData = options["Choose the block to locate:"].blockData

	# Prefill a list of schematic file names which we will choose from later on
	#os.listdir("filters/MapMarkerSchematics/") 
	# EncounterSchematicFiles = [ f for f in listdir("filters/MapMarkerSchematics") if isfile(join(f)) ] # http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
	print 'Scanning available schematics...'
	EncounterSchematicFiles = glob.glob("filters/MapMarkerSchematics/*.schematic")
	for fileName in EncounterSchematicFiles:
		print fileName
		
	print 'Found %s files' % (len(EncounterSchematicFiles))

	# First pass - search down-up for the block of interest. On the first hit at x/z, place a marker and move on with the search

	modeMatchBlockData = False
	if options["What should I look for?"] == "Match Block Data":
		modeMatchBlockData = True

	found = 0
	
	counter = 0
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			y = box.miny
			while y < box.maxy:
				counter = counter +1
				if counter%10000 == 0:
					print '%s %s: Searching at x=%s y=%s z=%s' % (METHOD, time.ctime(), x, y, z)
			
				chosenSchematic = randint(0,len(EncounterSchematicFiles)) % len(EncounterSchematicFiles)
				
				
			
				if modeMatchBlockData == True:
					if level.blockAt(x,y,z) == baseBlock and level.blockDataAt(x,y,z) == baseBlockData:
						print 'I found your block %s at %s %s %s with data value %s' % (baseBlock, x, y, z, baseBlockData)
						y = findSurface(x, y, z, level, box, options)
						if randint(0,10) == 1:
							buildATower(x,y,z, level, box, options)
						else:
							placeASchematic(x,y,z, EncounterSchematicFiles[chosenSchematic], level, box, options)
						found = found +1
						y = box.maxy # end search at this x/z coord
						
						#z = box.maxz
						#x = box.maxx
						#y = box.maxy
					
				else:
					if level.blockAt(x,y,z) == baseBlock:
						print 'I found your block %s at %s %s %s' % (baseBlock, x, y, z)
						y = findSurface(x, y, z, level, box, options)
						if randint(0,10) == 1:
							buildATower(x,y,z, level, box, options)
						else:
							placeASchematic(x,y,z, EncounterSchematicFiles[chosenSchematic], level, box, options)
						found = found +1
						y = box.maxy # end search at this x/z coord

						#z = box.maxz
						#x = box.maxx
						#y = box.maxy

				y = y+1

	print '%s: %s. Found %s' % (METHOD, time.ctime(), found)
	print '%s: Ended at %s' % (METHOD, time.ctime())



	
	
def buildATower(x, y, z, level, box, options):
	method = "buildATower"
	HEIGHTOFWALLS = 10
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	#ignore = options["Ignore block IDs:"].split()
	#ignoreList = map(int, ignore)
	AIR=(0,0)

	print '%s: Started at %s. Position %s %s %s' % (method, time.ctime(), x, y, z)
	
	TURRETWIDTH = 8 + randint(0,12)
	TURRETHEIGHT = HEIGHTOFWALLS + randint(4,16)
	TURRETDIAMETER = (int)(pi * TURRETWIDTH)+1 # the number of blocks around the circumference that need to be drawn.
	TURRETRADIUS = (int)(TURRETWIDTH/2)
	TURRETANGLE = (float)(2*pi / TURRETDIAMETER)
	
	startX = (int)(x) # Centre of the turret
	startZ = (int)(z)				

	for turretCircumferenceIter in xrange (0,TURRETDIAMETER):
		wallX = (int)(TURRETRADIUS * cos(TURRETANGLE*turretCircumferenceIter))
		wallZ = (int)(TURRETRADIUS * sin(TURRETANGLE*turretCircumferenceIter))
		window = False

		for iterY in xrange(0, TURRETHEIGHT):
			if randint(0,100) <= 4:
				block = materialSecondary
			else:				
				block = materialMain

			if iterY%6 == 2 and randint(0,100) == 1:
				window = True
				block = AIR
			elif window == True:
				block = AIR
				window = False


			if iterY == 0:
				setBlockToGround(level, block,  
					(int)(startX+wallX),
					(int)(iterY+y),
					(int)(startZ+wallZ),
					y-8
				)
			setBlock(level, block,  
				(int)(startX+wallX),
				(int)(iterY+y),
				(int)(startZ+wallZ)
			)

	for iterY in xrange(0, TURRETHEIGHT): # Now place flooring
		if (iterY%6) == 0:
			# Drop in a floor
			for floorRadius in xrange(0, TURRETRADIUS):
				floorCircumference = (int)(2 * floorRadius * pi)+1
				floorAngle = 2*pi/floorCircumference
				for floorIter in xrange(0, floorCircumference):
					floorX = (int)(floorRadius * cos(floorAngle * floorIter))
					floorZ = (int)(floorRadius * sin(floorAngle * floorIter))
					block = materialHighlight
					setBlockIfEmpty(level, block,  
						(int)(floorX+startX),
						(int)(iterY+y),
						(int)(floorZ+startZ)
						)
	
	print '%s: Ended at %s' % (method, time.ctime())
	
def placeASchematic(x,y,z, theFileName, level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	method = "placeASchematic"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	scratchpad = level.extractSchematic(box)
	SHAPE = (200,200,200)
	# END CONSTANTS

	# print os.getcwd()
	cursorPosn = box.origin
	# import the corresponding MCSchematic to the supplied filename
	print 'Loading schematic from file - %s' % (theFileName)
	charSchematic = MCSchematic(shape=SHAPE,filename=theFileName)

	cursorPosn = (x, y, z)		
	bb = analyse(charSchematic)
	level.copyBlocksFrom(charSchematic, bb, cursorPosn)

	print '%s: Ended at %s' % (method, time.ctime())
	
