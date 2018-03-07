# This filter is for creating structures
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_
import time # for timing

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from numpy import *
from pymclevel import TAG_String # @Texelelf
from pymclevel import TileEntity # @Texelelf
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, MCMaterials
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
from mcplatform import *
from os import listdir
from os.path import isfile, join
import glob
# import from @Texelelf
from copy import deepcopy
import bresenham # @Codewarrior0
from random import *
from random import Random # @Codewarrior0

# GLOBAL
CHUNKSIZE = 16

inputs = (
		("Noodlor", "label"),
		("Inspired by the work of", "label"),
		("/u/MCNoodlor", "label"),
		("Seed:", 0),
		("Operation",(
			"Turret",
			"Wall X Axis",
			"Wall Z Axis",
			"Castle")
		),
		("Edge Material",alphaMaterials.StoneBricks),
		("Wall Material",alphaMaterials.Sandstone),
		("Floor Material",alphaMaterials.WoodPlanks),
		("Support Material",alphaMaterials.StoneStairs),
		("Slab Material",alphaMaterials.StoneSlab),
		("Glass Material",alphaMaterials.GlassPane),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	# Local variables
	method = "Perform"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start
	
	if options["Operation"] == "Turret":
		turret(level,box,options)
	elif options["Operation"] == "Wall X Axis":
		wallX(level,box,options)
	elif options["Operation"] == "Wall Z Axis":
		wallZ(level,box,options)
	else:
		noodlor(level, box, options)

	FuncEnd(level,box,options,method) # Log end	

def windows(level, matEdge, matGlass, (matSupportID,matSupportData), (x1,y1,z1), (x2,y2,z2)):
	height = y2-y1
	width = x2-x1
	depth = z2-z1

	AIR = (0,0)
	
	offset = 0
	while int((x2+x1)/2)+offset < x2-2 or int((z2+z1)/2)+offset < z2-2:
		if int((x2+x1)/2)+offset < x2-2:
			edgeRegion(level, matEdge, (int((x2+x1)/2-1)+offset,int((y2+y1)/2)+1,z1),(int((x2+x1)/2+1)+offset,int((y2+y1)/2)+5,z1))
			fillRegion(level, matGlass, (int((x2+x1)/2)+offset,int((y2+y1)/2)+2,z1),(int((x2+x1)/2)+offset,int((y2+y1)/2)+4,z1))
			edgeRegion(level, matEdge, (int((x2+x1)/2-1)+offset,int((y2+y1)/2)+1,z2),(int((x2+x1)/2+1)+offset,int((y2+y1)/2)+5,z2))
			fillRegion(level, matGlass, (int((x2+x1)/2)+offset,int((y2+y1)/2)+2,z2),(int((x2+x1)/2)+offset,int((y2+y1)/2)+4,z2))
			edgeRegion(level, matEdge, (int((x2+x1)/2-1)-offset,int((y2+y1)/2)+1,z1),(int((x2+x1)/2+1)-offset,int((y2+y1)/2)+5,z1))
			fillRegion(level, matGlass, (int((x2+x1)/2)-offset,int((y2+y1)/2)+2,z1),(int((x2+x1)/2)-offset,int((y2+y1)/2)+4,z1))
			edgeRegion(level, matEdge, (int((x2+x1)/2-1)-offset,int((y2+y1)/2)+1,z2),(int((x2+x1)/2+1)-offset,int((y2+y1)/2)+5,z2))
			fillRegion(level, matGlass, (int((x2+x1)/2)-offset,int((y2+y1)/2)+2,z2),(int((x2+x1)/2)-offset,int((y2+y1)/2)+4,z2))
		if int((z2+z1)/2)+offset < z2-2:
			edgeRegion(level, matEdge, (x1,int((y2+y1)/2)+1,int((z2+z1)/2-1)+offset),(x1,int((y2+y1)/2)+5,int((z2+z1)/2+1)+offset))
			fillRegion(level, matGlass, (x1,int((y2+y1)/2)+2,int((z2+z1)/2)+offset),(x1,int((y2+y1)/2)+4,int((z2+z1)/2)+offset))
			edgeRegion(level, matEdge, (x2,int((y2+y1)/2)+1,int((z2+z1)/2-1)+offset),(x2,int((y2+y1)/2)+5,int((z2+z1)/2+1)+offset))
			fillRegion(level, matGlass, (x2,int((y2+y1)/2)+2,int((z2+z1)/2)+offset),(x2,int((y2+y1)/2)+4,int((z2+z1)/2)+offset))
			edgeRegion(level, matEdge, (x1,int((y2+y1)/2)+1,int((z2+z1)/2-1)-offset),(x1,int((y2+y1)/2)+5,int((z2+z1)/2+1)-offset))
			fillRegion(level, matGlass, (x1,int((y2+y1)/2)+2,int((z2+z1)/2)-offset),(x1,int((y2+y1)/2)+4,int((z2+z1)/2)-offset))
			edgeRegion(level, matEdge, (x2,int((y2+y1)/2)+1,int((z2+z1)/2-1)-offset),(x2,int((y2+y1)/2)+5,int((z2+z1)/2+1)-offset))
			fillRegion(level, matGlass, (x2,int((y2+y1)/2)+2,int((z2+z1)/2)-offset),(x2,int((y2+y1)/2)+4,int((z2+z1)/2)-offset))
		offset = offset + 3
		

	if height >= 16: # If there is room, add archways.
		if depth >= 13: # If there is room
			fillRegion(level, AIR, (x1,y1,int((z2+z1)/2-3)),(x1,y1+6,int((z2+z1)/2+3)))
			edgeRegion(level, matEdge, (x1,y1,int((z2+z1)/2-3)),(x1,y1+6,int((z2+z1)/2+3)))
			setBlock(level, (matSupportID,6),x1,y1+5,int((z2+z1)/2+2))
			setBlock(level, (matSupportID,7),x1,y1+5,int((z2+z1)/2-2))
			fillRegion(level, AIR, (x2,y1,int((z2+z1)/2-3)),(x2,y1+6,int((z2+z1)/2+3)))
			edgeRegion(level, matEdge, (x2,y1,int((z2+z1)/2-3)),(x2,y1+6,int((z2+z1)/2+3)))
			setBlock(level, (matSupportID,6),x2,y1+5,int((z2+z1)/2+2))
			setBlock(level, (matSupportID,7),x2,y1+5,int((z2+z1)/2-2))

		if width >= 13: # If there is room
			fillRegion(level, AIR, (int((x2+x1)/2-3),y1,z1),(int((x2+x1)/2+3),y1+6,z1))
			edgeRegion(level, matEdge, (int((x2+x1)/2-3),y1,z1),(int((x2+x1)/2+3),y1+6,z1))
			setBlock(level, (matSupportID,4),int((x2+x1)/2+2),y1+5,z1)
			setBlock(level, (matSupportID,5),int((x2+x1)/2-2),y1+5,z1)
			fillRegion(level, AIR, (int((x2+x1)/2-3),y1,z2),(int((x2+x1)/2+3),y1+6,z2))
			edgeRegion(level, matEdge, (int((x2+x1)/2-3),y1,z2),(int((x2+x1)/2+3),y1+6,z2))
			setBlock(level, (matSupportID,4),int((x2+x1)/2+2),y1+5,z2)
			setBlock(level, (matSupportID,5),int((x2+x1)/2-2),y1+5,z2)
	
	
def room(level,matEdge,matWall,matFloor,(matSupportID,matSupportData),matSlab,matGlass,(x1,y1,z1),(x2,y2,z2),dir):
	AIR = (0,0)
	fillRegion(level, matFloor, (x1,y1,z1),(x2,y1,z2)) 	# Floor
	fillRegion(level, matWall, (x1,y1,z1),(x1,y2,z2)) 	# Walls
	fillRegion(level, matWall, (x2,y1,z1),(x2,y2,z2)) 	# Walls
	fillRegion(level, matWall, (x1,y1,z1),(x2,y2,z1)) 	# Walls
	fillRegion(level, matWall, (x1,y1,z2),(x2,y2,z2)) 	# Walls
	windows(level, matEdge, matGlass, (matSupportID,matSupportData), (x1,y1,z1),(x2,y2,z2)) # Windows
	edgeRegion(level, matEdge, (x1,y1,z1),(x2,y2,z2))
	edgeRegion(level, matEdge, (x1-1,y1,z1-1),(x2+1,y1,z2+1) ) #Base Flange
	fillRegion(level, matEdge, (x1,y2,z1),(x2,y2,z2)) # Roof of tower
	fillRegionSkip(level, (matSupportID,5), (x2+1,y2,z1),(x2+1,y2,z2),2) # Stone stairs upright west
	fillRegionSkip(level, (matSupportID,4), (x1-1,y2,z1),(x1-1,y2,z2),2) # Stone stairs upright east
	fillRegionSkip(level, (matSupportID,6), (x1,y2,z1-1),(x2,y2,z1-1),2) # Stone stairs upright south
	fillRegionSkip(level, (matSupportID,7), (x1,y2,z2+1),(x2,y2,z2+1),2) # Stone stairs upright north
	fillRegion(level, matFloor, (x1-1,y2+1,z1-1),(x2+1,y2+1,z2+1)) 	# Roof
	edgeRegion(level, matEdge, (x1-1,y2+1,z1-1),(x2+1,y2+1,z2+1))	# Roof edge
	edgeRegion(level, matEdge, (x1-1,y2+2,z1-1),(x2+1,y2+2,z2+1)) 	# Crenelations
	edgeRegion(level, matSlab, (x1-1,y2+3,z1-1),(x2+1,y2+3,z2+1)) 	# Crenelations
	count = 0
	(sslabID,t) = matSlab
	for z in xrange(z1-1,z2+1):
		count = count +1
		if (count == 3 or count == ((z2+1)-(z1-1)-1)) or (count > 3 and count < ((z2+1)-(z1-1)-1) and (count-3)%4 == 0):
			setBlock(level,AIR,x1-1,y2+3,z) # Air
			setBlock(level,(sslabID,5),x1-1,y2+2,z) # Stone brick slab
			setBlock(level,AIR,x2+1,y2+3,z) # Air
			setBlock(level,(sslabID,5),x2+1,y2+2,z) # Stone brick slab
	count = 0
	for x in xrange(x1-1,x2+1):
		count = count +1
		if (count == 3 or count == ((x2+1)-(x1-1)-1)) or (count > 3 and count < ((x2+1)-(x1-1)-1) and (count-3)%4 == 0):
			setBlock(level,AIR,x,y2+3,z1-1) # Air
			setBlock(level,(sslabID,5),x,y2+2,z1-1) # Stone brick slab
			setBlock(level,AIR,x,y2+3,z2+1) # Air
			setBlock(level,(sslabID,5),x,y2+2,z2+1) # Stone brick slab

def turret(level,box,options):
	matEdge = getBlockFromOptions(options, "Edge Material")
	matWall = getBlockFromOptions(options, "Wall Material") 
	matFloor = getBlockFromOptions(options, "Floor Material")
	matSupport = getBlockFromOptions(options, "Support Material")
	matSlab = getBlockFromOptions(options, "Slab Material")
	matGlass = getBlockFromOptions(options, "Glass Material")
	
	room(level,matEdge,matWall,matFloor,matSupport,matSlab,matGlass,(box.minx+1,box.miny,box.minz+1),(box.maxx-2,box.maxy-4,box.maxz-2))
	
def wallX(level,box,options):
	matEdge = getBlockFromOptions(options, "Edge Material")
	matWall = getBlockFromOptions(options, "Wall Material") 
	matFloor = getBlockFromOptions(options, "Floor Material")
	matSupport = getBlockFromOptions(options, "Support Material")
	matSlab = getBlockFromOptions(options, "Slab Material")
	matGlass = getBlockFromOptions(options, "Glass Material")
	w = box.maxz-box.minz
	w1 = int(w/4)
	room(level,matEdge,matWall,matFloor,matSupport,matSlab,matGlass,(box.minx+1,box.miny,box.minz+w1),(box.maxx-2,box.maxy-4,box.maxz-w1-1))

def wallZ(level,box,options):
	matEdge = getBlockFromOptions(options, "Edge Material")
	matWall = getBlockFromOptions(options, "Wall Material") 
	matFloor = getBlockFromOptions(options, "Floor Material")
	matSupport = getBlockFromOptions(options, "Support Material")
	matSlab = getBlockFromOptions(options, "Slab Material")
	matGlass = getBlockFromOptions(options, "Glass Material")
	w = box.maxx-box.minx
	w1 = int(w/4)
	room(level,matEdge,matWall,matFloor,matSupport,matSlab,matGlass,(box.minx+w1,box.miny,box.minz+1),(box.maxx-w1-1,box.maxy-4,box.maxz-w1-2))

	
def noodlor(level, box, options):
	method = "noodlor"
	(method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method) # Log start

	CUBEWIDTH = 17
	CUBEMID = CUBEWIDTH-(int(CUBEWIDTH)/2)
	# Make a blocky array in the selection box
	cwidth = int(width/CUBEWIDTH)
	cdepth = int(depth/CUBEWIDTH)
	cheight = int(height/CUBEWIDTH)
	print cwidth,cdepth,cheight
	
	# Mechanism to repeat a build by number
	rand = Random(options["Seed:"])
	if options["Seed:"] == 0:
		rand = Random()
	
	# Materials
	EDGEMAT = 1
	WALLMAT = 2
	FLOORMAT = 3
	
	# Enumerations
	VOID = 0
	TOWER = 1
	
	map = zeros((cwidth,cheight,cdepth))
	
	ang=pi/2/cheight
	
	# Create a random structure
	iy = cheight-1 # Start one layer below top to allow crenelations to be added later
	#for iy in xrange(0,cheight):
	while iy > 0:
		iy = iy -1
		for iz in xrange(0,cdepth):
			for ix in xrange(0,cwidth):
				# FUTURE - I may only want to create a component at odd grid axis
				
				# if there is something above, something should be below...
				# Future - consider arches
				distx = abs(int(cwidth/2)-ix)
				distz = abs(int(cdepth/2)-iz)
				dist = int(sqrt(distx**2+distz**2))
				if ix%2 == 1 and iz%2 == 1 and rand.randint(1,100) < cos(iy*ang)*20*dist/((distx+distz)/2): # Prefer low structures
					map[ix,iy,iz] = TOWER # Something is here
				
				if iy < cheight-1: # bounds checking - don't step outside the array
					if map[ix,iy+1,iz] > 0:
						map[ix,iy,iz] = TOWER # Tower section
	
	# Now we have a plan... render it
	
	# Placeholder
	for iy in xrange(0,cheight-1):
		for iz in xrange(0,cdepth):
			for ix in xrange(0,cwidth):
				if map[ix,iy,iz] == TOWER:
					print (ix,iy,iz)
					(x1,y1,z1) = (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH)
					(x2,y2,z2) = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy+1)*CUBEWIDTH-1,box.minz+(iz+1)*CUBEWIDTH-1)
					dy = iy*2
					x1d = x1+dy
					x2d = x2-dy
					z1d = z1+dy
					z2d = z2-dy
					if z2d-z1d >= 7:
						room(level,(x1d,y1,z1d),(x2d,y2,z2d))
#				if ix > 0 and ix < cwidth-1 and iz > 0 and iz < cdepth and iy == 0:
#					if map[ix-1,iy,iz] == TOWER
				
#	for iz in xrange(0,cdepth):
#		for ix in xrange(0,cwidth):
#			iy = cheight
#			while iy > 0:
#				iy = iy - 1
#				if map[ix,iy,iz] == TOWER:
#					p000 = (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH)
#					p111 = (box.minx+(ix+1)*CUBEWIDTH-1,box.miny+(iy)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH-1)
#
#					tower(level, box, CUBEWIDTH, iy, p000, p111)
#					
#					iy = 0 # exit
					



					
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy)*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix)*CUBEWIDTH,box.miny+(iy)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+(ix+1)*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+iz*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
#					fillRegion(level, (155,0), (box.minx+ix*CUBEWIDTH,box.miny+iy*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH),(box.minx+(ix+1)*CUBEWIDTH,box.miny+(iy+1)*CUBEWIDTH,box.minz+(iz+1)*CUBEWIDTH) )
	
	FuncEnd(level,box,options,method) # Log end	

def edgeRegion(level, material, (x1,y1,z1), (x2,y2,z2)):
	fillRegion(level, material, (x1,y1,z1), (x2,y1,z1))
	fillRegion(level, material, (x1,y1,z1), (x1,y2,z1))
	fillRegion(level, material, (x1,y1,z1), (x1,y1,z2))
	fillRegion(level, material, (x1,y2,z2), (x2,y2,z2))
	fillRegion(level, material, (x2,y1,z2), (x2,y2,z2))
	fillRegion(level, material, (x2,y2,z1), (x2,y2,z2))
	fillRegion(level, material, (x1,y2,z1), (x2,y2,z1))
	fillRegion(level, material, (x1,y2,z1), (x1,y2,z2))
	fillRegion(level, material, (x2,y1,z1), (x2,y2,z1))
	fillRegion(level, material, (x1,y1,z2), (x1,y2,z2))
	fillRegion(level, material, (x2,y1,z1), (x2,y1,z2))
	fillRegion(level, material, (x1,y1,z2), (x2,y1,z2))
	
def fillRegion(level, material, (x1,y1,z1), (x2,y2,z2)):
	if (x1,y1,z1) == (x2,y2,z2):
		setBlock(level, material, x1,y1,z1)
	elif (x1,y1) == (x2,y2):
		for z in xrange(z1,z2+1):
			setBlock(level, material, x1, y1, z)
	elif (z1,y1) == (z2,y2):
		for x in xrange(x1,x2+1):
			setBlock(level, material, x, y1, z1)
	elif (z1,x1) == (z2,x2):
		for y in xrange(y1,y2+1):
			setBlock(level, material, x1, y, z1)
	elif x1 == x2:
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				setBlock(level, material, x1, y, z)
	elif y1 == y2:
		for x in xrange(x1,x2+1):
			for z in xrange(z1,z2+1):
				setBlock(level, material, x, y1, z)
	elif z1 == z2:
		for x in xrange(x1,x2+1):
			for y in xrange(y1,y2+1):
				setBlock(level, material, x, y, z1)
	else: # 
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				for x in xrange(x1,x2+1):
					setBlock(level, material, x, y, z)

def fillRegionSkip(level, material, (x1,y1,z1), (x2,y2,z2), skip):
	if (x1,y1,z1) == (x2,y2,z2):
		setBlock(level, material, x1,y1,z1)
	elif (x1,y1) == (x2,y2):
		for z in xrange(z1,z2+1):
			if (z-z1+1)%skip != 0:
				setBlock(level, material, x1, y1, z)
	elif (z1,y1) == (z2,y2):
		for x in xrange(x1,x2+1):
			if (x-x1+1)%skip != 0:
				setBlock(level, material, x, y1, z1)
	elif (z1,x1) == (z2,x2):
		for y in xrange(y1,y2+1):
			if (y-y1+1)%skip != 0:
				setBlock(level, material, x1, y, z1)
	elif x1 == x2:
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				if (z-z1+1)%skip != 0 and (y-y1+1)%skip != 0:
					setBlock(level, material, x1, y, z)
	elif y1 == y2:
		for x in xrange(x1,x2+1):
			for z in xrange(z1,z2+1):
				if (z-z1+1)%skip != 0 and (x-x1+1)%skip != 0:
					setBlock(level, material, x, y1, z)
	elif z1 == z2:
		for x in xrange(x1,x2+1):
			for y in xrange(y1,y2+1):
				if (x-x1+1)%skip != 0 and (y-y1+1)%skip != 0:
					setBlock(level, material, x, y, z1)
	else: # 
		for y in xrange(y1,y2+1):
			for z in xrange(z1,z2+1):
				for x in xrange(x1,x2+1):
					if (z-z1+1)%skip != 0 and (y-y1+1)%skip != 0 and (x-x1+1)%skip != 0:
						setBlock(level, material, x, y, z)
					
def makeBlob(level, x, y, z, ore, radius, replaceMaterial):
	# Make an irregular blob of ore centred at the position
	if radius == 1:
		if getBlock(level,x,y,z) == replaceMaterial:
			setBlock(level, ore, x,y,z)
	else:
		if randint(1,100) < 10: # Spherish
			r2 = radius*radius
			for dy in xrange(-radius,+radius):
				for dz in xrange(-radius,+radius):
					for dx in xrange(-radius,+radius):
						dist = dy**2+dz**2+dx**2
						if dist < r2 or (dist == r2 and randint(1,100) <= 40):
							if getBlock(level,dx+x,dy+y,dz+z) == replaceMaterial:
								setBlock(level, ore, dx+x,dy+y,dz+z)
		else: # brownian squiggle
			radius = radius**2 # Steps
			keepGoing = True
			P = []
			P.append((x,y,z))
			while keepGoing:
				(px,py,pz) = P[randint(0,len(P)-1)]
				dx = randint(-1,1)
				dy = randint(-1,1)
				dz = randint(-1,1)
				P.append((px+dx,py+dy,pz+dz))
				radius = radius-1
				if radius < 1:
					keepGoing = False
			for (px,py,pz) in P:
				if getBlock(level,px,py,pz) == replaceMaterial:
					setBlock(level, ore, px,py,pz)
			

	
	
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
			rx = 0
			createArmorStand(level, (int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), "ls", 1, 0, 1, 1, 1, 0, 0, 0, rx, 0,0,0,1,"","","","","","stone",2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			iter = iter+0.5 # slightly oversample because I lack faith.

def getBlockFromOptions(options, block):
	return (options[block].ID, options[block].blockData)