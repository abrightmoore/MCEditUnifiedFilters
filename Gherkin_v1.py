# This filter draws a Gherkin building.
# Port and hack of WorldEdit custom script by /u/Hyta to MCEdit
# abrightmoore@yahoo.com.au / http://brightmoore.net

from math import sqrt, sin, cos, pi, ceil, floor
from random import *


# the size of the building
gherkinHeight = 82
gherkinTopFloor = 76
gherkinRadius = 17
staircaseRadius = 3.5
lampDensity = 4

# we will use these blocks
blockIron = (42,0)
blockGlass = (20,0)
blockGlowstone = (89,0)
blockObsidian = (49,0)
blockStone = (1,0)
blockWool = (35,0)

def setBlock(level, (block, data), x, y, z):
    level.setBlockAt(x, y, z, block)
    level.setBlockDataAt(x, y, z, data)


def perform(level, box, options):
	for y in range(gherkinHeight):
        	buildLayer(level, box, y)
        	buildWall(level, box, y)
        	buildSkeleton(level, box, y)
  	level.markDirtyBox(box)
  	
def getR(y):
	return 1.0 * gherkinRadius*((1.3*sin((0.45*y+55)/180*pi))-(3.6*sqrt(1/(gherkinHeight+15.5-y))))


def buildLayer(level, box, y):
        # the following function poorly approximates the shape of the Gherkin (don't ask)
        
        r = getR(y)
        
    
    	setBlock(level, (35,2), box.maxx, box.maxy, box.maxz)
    	
        # building the floors
        
        if (y%4 == 0) and (y <= gherkinTopFloor):
            for x in range((int)(-ceil(r)), (int)(ceil(r)+1)):
                for z in range((int)(-ceil(r)), (int)(ceil(r)+1)):
                    if (sqrt(x*x+z*z) < r) and (sqrt(x*x+z*z)) > staircaseRadius:
                        if (x%lampDensity == 0) and (z%lampDensity == 0) and (sqrt(x*x+z*z) < r-3):
                            setBlock(level, blockGlowstone, box.minx+x, box.miny+y, box.minz+z)
                        elif ((abs(x)<=1 or abs(z)<=1) or (sqrt(x*x+z*z)<r-2)):
                            setBlock(level, blockWool, box.minx+x, box.miny+y, box.minz+z)
                        else:
                            setBlock(level, blockStone, box.minx+x, box.miny+y, box.minz+z)

def buildWall(level, box, y):
    # building the walls
    angleTurn = -y
    r = getR(y)
    angle = 0
    
    while angle <= 360:
            a = angle+angleTurn
    	    if (y < gherkinTopFloor-9):
    	    	if (angle%60 < 20):
        		setBlock(level, blockObsidian, box.minx+(int)(r*sin(a*pi/180)), box.miny+y, box.minz+(int)(r*cos(a*pi/180)))
                else:
                	setBlock(level, blockGlass, box.minx+(int)(r*sin(a*pi/180)), box.miny+y, box.minz+(int)(r*cos(a*pi/180)))
                
            elif (y < gherkinTopFloor):
        	if ((angle%60 < 20) or ((floor(angle/20)+floor((360-angle-2*angleTurn)/20))%2 == 0)):
        	   	setBlock(level, blockObsidian, box.minx+(int)(r*sin(a*pi/180)), box.miny+y, box.minz+(int)(r*cos(a*pi/180)))
            	else:
            	    setBlock(level, blockGlass, box.minx+(int)(r*sin(a*pi/180)), box.miny+y, box.minz+(int)(r*cos(a*pi/180)))
       	    else: # the roof
 		setBlock(level, blockObsidian, box.minx+(int)(r*sin(a*pi/180)), box.miny+y, box.minz+(int)(r*cos(a*pi/180)))
            angle = angle + 1.8                
            
def buildSkeleton(level, box, y):
    # building the skeleton
    	angleTurn = -y
    	angle = 0
    	r = getR(y)
    
    	while angle < 360:
            if (random() + 0.4 + r/gherkinRadius > 1): # this condition is here to reduce the amount of iron on the roof
                a = angle+angleTurn
                setBlock(level, blockIron, box.minx+(int)(r*sin(a*pi/180)), box.miny+y, box.minz+(int)(r*cos(a*pi/180)))
                setBlock(level, blockIron, box.minx+(int)(r*sin(-a*pi/180)), box.miny+y, box.minz+(int)(r*cos(-a*pi/180)))
                
    		angle = angle + 20
    
