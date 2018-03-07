# This filter draws clouds.
# 
# abrightmoore@yahoo.com.au / http://brightmoore.net

from math import sqrt, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians
from random import *


inputs = (
  ("Pick a block:", "blocktype"),
)

def setBlock(level, (block, data), x, y, z):
    level.setBlockAt(x, y, z, block)
    level.setBlockDataAt(x, y, z, data)

def getXYZ(radius, theta, phi):
	dx = (radius*cos(radians(phi))*cos(radians(theta)))
	dy = (radius*sin(radians(phi)))
	dz = (radius*cos(radians(phi))*sin(radians(theta)))	
	return (dx, dy, dz)

def drawSphere(level,block,r,x,y,z, fidelity):
	theta = 0
	while theta <= 360:
		phi = 0
		while phi <= 360:
			(dx, dy, dz) = getXYZ(r, theta, phi)
			setBlock(level, block, (int)(x+dx), (int)(y+dy), (int)(z+dz))
			phi = phi + fidelity
		theta = theta + fidelity

def perform(level, box, options):

	baseBlock = options["Pick a block:"].ID
	baseBlockData = options["Pick a block:"].blockData


	radius = randint(6,11)
	x = (box.maxx - box.minx) / 2
	y = (box.maxy - box.miny) / 2
	z = (box.maxz - box.minz) / 2
	
	nodes = randint(5,11)
	zone = 0
	for h in range(nodes):
		zone = zone + 1
		(ddx, ddy, ddz) = getXYZ(radius*2*zone,randint(0,360),0)
				
		j = randint(radius/3,radius*3)
		while j < 90:
			i = randint(radius/3,radius*3)	
			while i < 360:
		   		(dx, dy, dz) = getXYZ(randint(radius/3,radius*4), i, j)
		   		drawSphere(level, (baseBlock, baseBlockData), radius, box.minx+dx+x+ddx, box.miny+(dy/2)+y+ddy, box.minz+dz+z+ddz, 360/45)
		   		i = i + randint(radius/3,radius*3)
		   	j = j + randint(radius/3,radius*3)
    
    
  	level.markDirtyBox(box)

