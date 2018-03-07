# This filter is for making blocky musical thingies.
# abrightmoore@yahoo.com.au
# http://brightmoore.net

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

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
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy

# For Reference (see @Texelelf and @CodeWarrior0 examples)
# 	schematic = level.extractSchematic(BoundingBox((box.minx, box.miny, box.minz), (width, height, depth))) # Mirror the blocks - in memory working read only copy
# 	level.copyBlocksFrom(schematic, BoundingBox((0,0,0),(width,height,depth)), (box.minx, box.miny, box.minz ))
#	setBlock(schematic, (BLOCKID, BLOCKDATA), (int)(centreWidth+xx), (int)(centreHeight+yy), (int)(centreDepth+zz))

# YOUR CODE GOES HERE \/ \/ \/ \/ \/ \/ \/ \/ \/

inputs = (
		("ORCHESTRA", "label"),
		("Notes per bar", 16),
		("Rest", 0.5),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	Orchestra(level, box, options)
	level.markDirtyBox(box)

def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def createCommandBlockData(x, y, z, theCommand):
	e = TileEntity.Create("Control")
	e["Command"] = TAG_String(theCommand)
	TileEntity.setpos(e, (x, y, z))
	return e
	
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(x, y, z, block)
	level.setBlockDataAt(x, y, z, data)
	
def Orchestra(level, box, options):
	method = "ORCHESTRA"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = getBoxSize(box)
	centreWidth = width / 2
	centreHeight = height / 2
	centreDepth = depth / 2
	AIR = (0,0)
	COMMANDBLOCK = (137,0)
	CHUNKSIZE = 16
	RESTBLOCK = (1,0)
	TRIGGERBLOCK = (2,0)

	SOUNDS = [
		"note.harp",
		"note.bass",
		"note.bd",
		"note.pling",
		"note.snare"
		"note.bassattack",
		"note.hat",


	]

	BARSIZE = options["Notes per bar"]
	REST = options["Rest"]

	for iterbands in xrange(0,randint(1,10)):
		pallette = getRandomTonePallette()
		if randint(0,2) == 1:
			pallette = getBalancedTonePallette(randint(0,5)) # Gap between notes

		print pallette
	
		BANDSIZE = randint(1,len(SOUNDS)-1)

		spawnerX = box.minx+1 + iterbands *4
		spawnerY = box.miny
		spawnerZ = box.minz
		chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
		setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
		chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
									spawnerY, 
									spawnerZ, 
									"fill ~ ~ ~1 ~ ~64 ~1 minecraft:redstone_block 0 replace minecraft:grass"
								))		
		chunk.dirty = True

		INSTRUMENTidx = 0
		for iterInstruments in xrange(0, BANDSIZE):
			INSTRUMENTidx = (INSTRUMENTidx +1) % len(SOUNDS)
			INSTRUMENT = SOUNDS[INSTRUMENTidx]
			
			spawnerX = box.minx+1 + iterbands *4
			spawnerY = box.miny + 5*iterInstruments # vertical offset each instrument
			spawnerZ = box.minz+1

			RESTCHANCE = randint(0,5)
			for iterSteps in xrange(0,BARSIZE):
				print 'Step %s of %s' % (iterSteps,BARSIZE)

				if randint(0,10) >= 5+RESTCHANCE:
					setBlock(level, RESTBLOCK, spawnerX, spawnerY, spawnerZ)
				else:
					chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
					setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
					chunk.TileEntities.append( 	createCommandBlockData(spawnerX,spawnerY,spawnerZ,"execute @a ~ ~ ~ playsound "+INSTRUMENT+" @p ~ ~ ~ 1 "+str(pallette[randint(0,len(pallette)-1)])+" 1"))
					chunk.dirty = True

				spawnerX = spawnerX-1
				spawnerY = spawnerY+1

				chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
				setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)

				if iterSteps != BARSIZE-1:
					theCommand = "summon FallingSand ~1 ~"+str(REST)+" ~1 {Block:minecraft:redstone_block,Time:1}"
				else:
					theCommand = "summon FallingSand ~1 ~"+str(REST)+" ~"+str(-(BARSIZE-1))+" {Block:minecraft:redstone_block,Time:1}"
				
				chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
											spawnerY, 
											spawnerZ, 
											theCommand
										))		
				chunk.dirty = True
				
				if iterSteps == 0: # place a trigger placeholder. In game do a fill replace to start
					setBlock(level, TRIGGERBLOCK, spawnerX+1, spawnerY, spawnerZ)

				spawnerX = spawnerX+2

				chunk = level.getChunk(spawnerX/CHUNKSIZE, spawnerZ/CHUNKSIZE)
				setBlock(level, COMMANDBLOCK, spawnerX, spawnerY, spawnerZ)
				theCommand = "setblock ~-1 ~ ~ minecraft:air"
				chunk.TileEntities.append( 	createCommandBlockData(spawnerX, 
											spawnerY, 
											spawnerZ, 
											theCommand
										))				
					
				spawnerX = spawnerX-1
				spawnerY = spawnerY-1
				spawnerZ = spawnerZ+1

	print '%s: Ended at %s' % (method, time.ctime())


		

def getRandomTonePallette():
	colours = "0.5 0.53 0.56 0.6 0.63 0.67 0.7 0.75 0.8 0.85 0.9 0.95 1.0 1.05 1.1 1.2 1.25 1.32 1.4 1.5 1.6 1.7 1.8 1.9 2.0".split() # I like this sequence
	coloursList = map(float, colours)
	coloursListLen = len(coloursList)
	baseIndex = randint(0,coloursListLen)
	pallette = zeros(randint(2,8))
	gap = randint(0,coloursListLen-1)
	for iterC in xrange(0,len(pallette)):
		pallette[iterC] = (float)(coloursList[(baseIndex+iterC*gap)%coloursListLen])
	return pallette

def getBalancedTonePallette(gap):
	colours = "0.5 0.53 0.56 0.6 0.63 0.67 0.7 0.75 0.8 0.85 0.9 0.95 1.0 1.05 1.1 1.2 1.25 1.32 1.4 1.5 1.6 1.7 1.8 1.9 2.0".split() # I like this sequence
	coloursList = map(float, colours)
	coloursListLen = len(coloursList)
	baseIndex = randint(0,coloursListLen)
	pallette = zeros(randint(2,8))
	for iterC in xrange(0,len(pallette)):
		pallette[iterC] = (float)(coloursList[(baseIndex+iterC*gap)%coloursListLen])
	return pallette					
					
#/playsound note.harp @p 1067 5 750 1 1.44 1
#/summon FallingSand ~1 ~1 ~1 {Block:minecraft:redstone_block,Time:1}