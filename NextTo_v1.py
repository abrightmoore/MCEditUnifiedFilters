import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, floor
from random import *
from os import listdir
from os.path import isfile, join
import glob
from mcplatform import *
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, TileEntity, alphaMaterials, MCSchematic, MCLevel, BoundingBox
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0

# from AJBHelper import *

inputs = (
		("Nexto", "label"),
		("Find:", alphaMaterials.BlockofQuartz),
		("Replace:", alphaMaterials.BlockofQuartz),
		("Material:", alphaMaterials.BlockofQuartz),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(originalLevel, originalBox, options):
	matFind = getBlockFromOptions(options, "Find:")
	matRep = getBlockFromOptions(options, "Replace:")
	mat = getBlockFromOptions(options, "Material:")

	SUCCESS = True
	level = originalLevel.extractSchematic(originalBox) # Working set
	box = BoundingBox((0,0,0),(originalBox.width,originalBox.height,originalBox.length))


	nexto(originalLevel,originalBox,level,box,matFind,matRep,mat)
	
	if SUCCESS == True: # Copy from work area back into the world
		b=range(4096)
		b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
		originalLevel.copyBlocksFrom(level, box, (originalBox.minx, originalBox.miny, originalBox.minz ),b)
		originalLevel.markDirtyBox(originalBox)



def nexto(oLevel,oBox,level,box,matFind,matRep,mat):
	op = "Nexto"
	checkIntersect = True
	for y in xrange(oBox.miny,oBox.maxy):
		if y%10 == 0:
			print str(time.ctime())+" Running "+op+" "+str(y)
		for z in xrange(oBox.minz,oBox.maxz):
			for x in xrange(oBox.minx,oBox.maxx):
				block = getBlock(oLevel,x,y,z)
				if block == matRep:
					collision = False
					if checkIntersect == True:
						for ddx in xrange(-1,1):
							for ddz in xrange(-1,1):
								for ddy in xrange(-1,1):
									px = x+ddx
									py = y+ddy
									pz = z+ddz
									if px >= oBox.minx and px < oBox.maxx and py >= oBox.miny and py < oBox.maxy and pz >= oBox.minz and pz < oBox.maxz and not (ddx == 0 and ddy == 0 and ddz == 0):
										block = getBlock(oLevel,px,py,pz)
										if block == matFind:
											collision = True
					if collision == True:
						setBlock(level,mat,x-oBox.minx,y-oBox.miny,z-oBox.minz)
						
						
	
def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)
	
	
def getBlock(level,x,y,z):
	return (level.blockAt(int(x),int(y),int(z)), level.blockDataAt(int(x),int(y),int(z)))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)