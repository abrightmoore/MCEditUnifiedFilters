# This filter draws a rainbow.
# Port of WorldEdit custom script by /u/Hyta
# abrightmoore@yahoo.com.au / http://brightmoore.net
 
from math import sqrt, sin, cos, pi


colours = [ 14, 1, 4, 5, 11, 3, 10 ]



def perform(level, box, options):

	radius = (box.maxx - box.minx) / 2
	fidelity = radius * 20 # arbitrary based on leaving no gaps.

	depth = (box.maxz - box.minz)
	bandwidth = radius / 16
	if bandwidth < 1:
		bandwidth = 1

	deg = pi/fidelity
	
	heightscale = 1.0 * (box.maxy - box.miny) / radius # squish the arc based on box height
	
	
	for z in range(0, depth):
		for t in range(0, fidelity):
			offset = 0
			for c in colours:
				for i in range(0, bandwidth):
					x = (radius-offset) * cos(t * deg)
					y = heightscale * (radius-offset) * sin(t * deg)
					setBlock(level, 35, c, (int)(box.minx + radius + x), (int)(box.miny + y), box.minz+z)
					offset = offset + 1
		
	level.markDirtyBox(box)


# SethBling's utility method

def setBlock(level, block, data, x, y, z):
	level.setBlockAt(x, y, z, block)
	level.setBlockDataAt(x, y, z, data)