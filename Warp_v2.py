# This filter is for warping space
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import Random # @Codewarrior0
import inspect # @Texelelf
from PIL import Image
import png

# GLOBAL
CHUNKSIZE = 16
a = pi/180
AIR = (0,0)

# Filter pseudocode:
#

inputs = (
		("WARP", "label"),
		("Operation:", ( "Twist", "Mix", "GWave", "Double", "Halve", "Lattice" )),
		("Origin X:", 0),
		("Origin Y:", 0),
		("Origin Z:", 0),
		("Delete source?", True),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def Twist((x,y,z)):
	Q = []
	
	dist = sqrt(x**2+z**2)
	horizAngle = atan2(z,x)
	x1 = dist*cos(horizAngle+a*y)
	y1 = y
	z1 = dist*sin(horizAngle+a*y)
	
	Q.append((x1,y1,z1))
	return Q

def GWave((x,y,z)):
	Q = []
	
	distH = x**2+z**2
	dist = sqrt(y**2+distH)
	amplitude = 8*cos(dist*(3*a))
	dist = dist+amplitude
	horizAngle = atan2(z,x)
	vertAngle = atan2(y,sqrt(distH))
	x1 = dist*cos(horizAngle)*cos(vertAngle)
	y1 = dist*sin(vertAngle)
	z1 = dist*sin(horizAngle)*cos(vertAngle)
	
	Q.append((x1,y1,z1))
	return Q
	
def Mix((x,y,z)):
	Q = []
	
	dist = sqrt(x**2+z**2)
	horizAngle = atan2(z,x)
	b = randint(-abs(y),abs(y))
	x1 = dist*cos(horizAngle+a*b)
	y1 = y
	z1 = dist*sin(horizAngle+a*b)
	
	Q.append((x1,y1,z1))
	return Q

	
def Double((x,y,z)):
	Q = []
	
	x1 = 2 * x
	y1 = 2 * y
	z1 = 2 * z
	
	Q.append((x1,y1,z1))
	return Q

def Halve((x,y,z)):
	Q = []
	
	x1 = x/2
	y1 = y/2
	z1 = z/2
	
	Q.append((x1,y1,z1))
	return Q
	
def remap(p,func):
	possibles = globals().copy() # http://stackoverflow.com/questions/7936572/python-call-a-function-from-string-name
	possibles.update(locals())
	method = possibles.get(func)
	if not method:
		raise Exception("Method %s not implemented" % method_name)
	return method(p) # call the method and return a list of co-ordinates

def warp(level, box, options):
	method = "Warp"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	# for each point within the selection area, apply a transformation and re-map the source to the target location in cartesian space.
	# copy the starting object out
	func = str(options["Operation:"])
	if func == "Lattice":
		lattice(level, box, options)
		return

		
	OX = options["Origin X:"]
	OY = options["Origin Y:"]
	OZ = options["Origin Z:"]
	source = level.extractSchematic(box)
	delete = options["Delete source?"]
	if delete == True:
		level.fillBlocks(box,alphaMaterials.Air)
	
	print box.miny
	for yi in xrange(box.miny,box.maxy):
		y = yi+OY
		if yi%5 == 0:
			print yi
		for zi in xrange(box.minz,box.maxz):
			z = zi+OZ
			for xi in xrange(box.minx,box.maxx):
				x = xi+OX
				(b, d) = getBlock(source, xi-box.minx, yi-box.miny, zi-box.minz)
				if (b, d) != AIR:
					Q = remap((x,y,z),func)
					Q100 = remap((x+1,y,z),func)
					Q010 = remap((x,y+1,z),func)
					Q011 = remap((x,y+1,z+1),func)
					Q001 = remap((x,y,z+1),func)
					Q101 = remap((x+1,y,z+1),func)
					Q110 = remap((x+1,y+1,z),func)
					Q111 = remap((x+1,y+1,z+1),func)
					for p1 in Q:
						#print p1
						(p1x, p1y, p1z) = p1
						p1 = (p1x-OX,p1y-OY,p1z-OZ)
						for p2 in Q101:
							(p2x, p2y, p2z) = p2
							p2 = (p2x-OX,p2y-OY,p2z-OZ)
							for p3 in Q001:
								(p3x, p3y, p3z) = p1
								p3 = (p3x-OX,p3y-OY,p3z-OZ)							
								drawTriangle(level, p1, p2, p3, (b,d), (b,d))
							for p3 in Q100:
								(p3x, p3y, p3z) = p1
								p3 = (p3x-OX,p3y-OY,p3z-OZ)							
								drawTriangle(level, p1, p2, p3, (b,d), (b,d))
						for p2 in Q110:
							(p2x, p2y, p2z) = p2
							p2 = (p2x-OX,p2y-OY,p2z-OZ)
							for p3 in Q100:						
								(p3x, p3y, p3z) = p1
								p3 = (p3x-OX,p3y-OY,p3z-OZ)							
								drawTriangle(level, p1, p2, p3, (b,d), (b,d))
							for p3 in Q010:
								(p3x, p3y, p3z) = p1
								p3 = (p3x-OX,p3y-OY,p3z-OZ)							
								drawTriangle(level, p1, p2, p3, (b,d), (b,d))
						for p2 in Q011:
							(p2x, p2y, p2z) = p2
							p2 = (p2x-OX,p2y-OY,p2z-OZ)
							for p3 in Q010:						
								(p3x, p3y, p3z) = p1
								p3 = (p3x-OX,p3y-OY,p3z-OZ)							
								drawTriangle(level, p1, p2, p3, (b,d), (b,d))
							for p3 in Q001:
								(p3x, p3y, p3z) = p1
								p3 = (p3x-OX,p3y-OY,p3z-OZ)							
								drawTriangle(level, p1, p2, p3, (b,d), (b,d))
									
	FuncEnd(level,box,options,method)

def lattice(level, box, options):
	method = "Lattice"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)	
	chance = options["Origin X:"]
	size = randint(4,CHUNKSIZE)
	(edgeMaterialBlock, edgeMaterialData) = (options["Origin Y:"], options["Origin Z:"])
	for y in xrange(box.miny,box.maxy):
		for x in xrange(box.minx,box.maxx):
			for z in xrange(box.minz,box.maxz):
				# print (x,y,z,edgeMaterialBlock, edgeMaterialData)
				if (y == box.miny or y%size == 0 or y == box.maxy-1) and (x == box.minx or x%size == 0 or x == box.maxx-1) and (z == box.minz or z%size == 0 or z == box.maxz-1):
					if randint(0,100) < chance:
						drawLine(level, (edgeMaterialBlock, edgeMaterialData), (x,y,z), (x,y+size,z))
					if randint(0,100) < chance:
						drawLine(level, (edgeMaterialBlock, edgeMaterialData), (x,y,z), (x+size,y,z))
					if randint(0,100) < chance:
						drawLine(level, (edgeMaterialBlock, edgeMaterialData), (x,y,z), (x,y,z+size))
					if randint(0,100) < chance:
						drawLine(level, (edgeMaterialBlock, edgeMaterialData), (x,y,z), (x,y-size,z))
					if randint(0,100) < chance:
						drawLine(level, (edgeMaterialBlock, edgeMaterialData), (x,y,z), (x-size,y,z))
					if randint(0,100) < chance:
						drawLine(level, (edgeMaterialBlock, edgeMaterialData), (x,y,z), (x,y,z-size))


						
	FuncEnd(level,box,options,method)
	
def perform(level,box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	warp(level,box,options)
	level.markDirtyBox(box)
	FuncEnd(level,box,options,method) # Log end	
	
####################################### LIBS
	
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
	
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

def getBlock(level,x,y,z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt(int(x), int(y), int(z), block)
	level.setBlockDataAt(int(x), int(y), int(z), data)

def drawTriangleEdge(level, box, options, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge):
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )
	
# Ye Olde GFX Libraries
def drawLine(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	drawLineConstrained(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLine1(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1) ):
	for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)):
		setBlock(scratchpad,(blockID, blockData),px,py,pz)
	setBlock(scratchpad,(blockID, blockData),x1,y1,z1)
	
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
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
			iter = iter+0.5 # slightly oversample because I lack faith.

def drawLineConstrainedRandom(scratchpad, (blockID, blockData), (x,y,z), (x1,y1,z1), frequency ):
	dx = x1 - x
	dy = y1 - y
	dz = z1 - z

	distHoriz = dx*dx + dz*dz
	distance = sqrt(dy*dy + distHoriz)


	phi = atan2(dy, sqrt(distHoriz))
	theta = atan2(dz, dx)

	iter = 0
	while iter <= distance:
		if randint(0,99) < frequency:
			scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
			scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
		iter = iter+0.5 # slightly oversample because I lack faith.

def drawTriangle(level, (p1x, p1y, p1z), (p2x, p2y, p2z), (p3x, p3y, p3z), materialEdge, materialFill):
	if materialFill != (0,0):
		# for each step along the 'base' draw a line from the apex
		dx = p3x - p2x
		dy = p3y - p2y
		dz = p3z - p2z

		distHoriz = dx*dx + dz*dz
		distance = sqrt(dy*dy + distHoriz)
		
		phi = atan2(dy, sqrt(distHoriz))
		theta = atan2(dz, dx)

		iter = 0
		while iter <= distance:
			(px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
			
			iter = iter+0.5 # slightly oversample because I lack faith.
			drawLine(level, materialFill, (px, py, pz), (p1x, p1y, p1z) )
	
	
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
	drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
	drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )
