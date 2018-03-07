# This filter draws castles in your selection box.
# No fiddling, no fuss. Select area, select the filter, and run it.
#
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# 

from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from pymclevel import alphaMaterials

inputs = (
  
  ("Main Material:", alphaMaterials.Stone),
  ("Secondary Material:", alphaMaterials.Cobblestone),
  ("Highlight Material:", alphaMaterials.WoodPlanks),
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

def SymmetricCastle(level, box, options):
	# CONSTANTS AND GLOBAL VARIABLES
	materialMain = (options["Main Material:"].ID, options["Main Material:"].blockData)
	materialSecondary = (options["Secondary Material:"].ID, options["Secondary Material:"].blockData)
	materialHighlight = (options["Highlight Material:"].ID, options["Highlight Material:"].blockData)
	method = "CastleSymmetric"
	(width, height, depth) = getBoxSize(box)
	centreWidth = (int)(width / 2)
	centreHeight = (int)(height / 2)
	centreDepth = (int)(depth / 2)
	
	# First, what is the layout for this castle?
	NUMBEROFWALLS = randint(8,8 + (int)(width/8) ) # maximum number of wall sections is influenced by the width of the selection box.
	HEIGHTOFWALLS = (int)( height/5+randint(0,height/3) )
	NUMBEROFWALLSPERQUADRANT = (int)(NUMBEROFWALLS/4) # Optimisation - calculate once, draw four times
	if NUMBEROFWALLSPERQUADRANT == 0:
		NUMBEROFWALLSPERQUADRANT = 1
	DEPTHOFWALLS = randint(3, randint(4,10) ) 
	AIR = (0,0)
	
	# Do the wall. Travel around the circumference of the castle drawing the wall as we go.
	
	WALLANGLE = (float)(pi/2/NUMBEROFWALLSPERQUADRANT) # FIX: radians, not degrees.
	
	continueWalling = True
	while continueWalling == True:
		for wallInstanceNum in xrange(0, NUMBEROFWALLSPERQUADRANT):
			print '%s1: %s of %s' % (method, wallInstanceNum, NUMBEROFWALLSPERQUADRANT)
			# Work out the direction and distance. Calculate in Quadrant 1, apply in all quadrants
			
			STARTANGLE = wallInstanceNum * WALLANGLE
			ENDANGLE = (wallInstanceNum +1) * WALLANGLE

			isaGate = False
			if randint(0,100) < 10:
				isaGate = True

			for wallDepthIter in xrange(0,DEPTHOFWALLS):
				print '%s1a: Rendering wall layer %s of %s' % (method, wallDepthIter, DEPTHOFWALLS)
				
				startX = (int)((centreWidth - wallDepthIter) * cos(STARTANGLE))
				startZ = (int)((centreDepth - wallDepthIter) * sin(STARTANGLE))

				endX = (int)((centreWidth - wallDepthIter) * cos(ENDANGLE))
				endZ = (int)((centreDepth - wallDepthIter) * sin(ENDANGLE))

				dX = endX - startX
				dZ = endZ - startZ
				WALLDIRECTION = (float)(atan2( dZ, dX))

				WALLDISTANCE = (int)( sqrt( dX**2 + dZ**2) ) # This is the number of steps from start of the wall to finish. FIX: +, not *!
				WALLDISTANCE = WALLDISTANCE # adjust for turret.




				for wallIter in xrange(0,WALLDISTANCE+1): # Now, let's go for a walk, adding a layer of wall as we go! We are basically increasing the distance of the vector at each step

					# Calculate the next centre block location.
					offsetX = wallIter * cos(WALLDIRECTION)
					offsetZ = wallIter * sin(WALLDIRECTION)


					for y in xrange(0, HEIGHTOFWALLS-(int)(wallDepthIter/3)):
						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain

						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth+(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth+(startZ+offsetZ))
						)

						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain
						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth-(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth+(startZ+offsetZ))
						)

						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain
						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth-(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth-(startZ+offsetZ))
						)

						if randint(0,100) <= 4:
							block = materialSecondary
						else:				
							if wallDepthIter/3 > 0 and y == (HEIGHTOFWALLS-1-(int)(wallDepthIter/3)):
								block = materialHighlight
							else:
								block = materialMain
						if isaGate == True and (wallIter > (WALLDISTANCE/3 - 2)) and (wallIter < (WALLDISTANCE/2 +3)) and y < 10:
							block = AIR

						setBlock(level, block,  
							(int)(box.minx+centreWidth+(startX+offsetX)),
							(int)(box.miny+y),
							(int)(box.minz+centreDepth-(startZ+offsetZ))
						)
					
		continueWalling = False

	# Turrets

	for wallInstanceNum in xrange(0, NUMBEROFWALLS):	
		print '%s2: %s of %s' % (method, wallInstanceNum+1, NUMBEROFWALLS)
		if randint(0,4) < 3:
			# Lets place a turret.

			TURRETWIDTH = 10 + randint(0,11)*2
			TURRETHEIGHT = HEIGHTOFWALLS + randint(6,(int)(height/4))
			TURRETDIAMETER = (int)(pi * TURRETWIDTH)+1 # the number of blocks around the circumference that need to be drawn.
			TURRETRADIUS = (int)(TURRETWIDTH/2)
			TURRETANGLE = (float)(2*pi / TURRETDIAMETER)
			STARTANGLE = wallInstanceNum * WALLANGLE

			startX = (int)((centreWidth) * cos(STARTANGLE)) # Centre of the turret
			startZ = (int)((centreDepth) * sin(STARTANGLE))				

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
						block = AIR # AIR
						window = False


					setBlock(level, block,  
						(int)(box.minx+centreWidth+(startX+wallX)),
						(int)(box.miny+iterY),
						(int)(box.minz+centreDepth+(startZ+wallZ))
					)
				
			for iterY in xrange(0, TURRETHEIGHT): # Now place flooring
				if (iterY%6) == 0:
					# Drop in a floor
					print 'Placing a floor at %s on Turret # %s' % (iterY, wallInstanceNum)
					for floorRadius in xrange(0, TURRETRADIUS):
						floorCircumference = (int)(2 * floorRadius * pi)+1
						floorAngle = 2*pi/floorCircumference
						for floorIter in xrange(0, floorCircumference):
							floorX = (int)(floorRadius * cos(floorAngle * floorIter))
							floorZ = (int)(floorRadius * sin(floorAngle * floorIter))
							block = materialHighlight
							setBlockIfEmpty(level, block,  
								(int)(box.minx+centreWidth+(startX+floorX)),
								(int)(box.miny+iterY),
								(int)(box.minz+centreDepth+(startZ+floorZ))
								)

	# Now for a few towers in the courtyard

	NUMHALLS = randint(0, 8)

	for wallInstanceNum in xrange(0, NUMHALLS):	
		print '%s3: %s of %s' % (method, wallInstanceNum+1, NUMHALLS)
		# Lets place a turret.

		DISTANCEX = randint(0, (int)(centreWidth/2))
		DISTANCEZ = randint(0, (int)(centreDepth/2))

		TURRETWIDTH = 16 + randint(0,(int)((DISTANCEX+DISTANCEZ)/2))
		TURRETHEIGHT = randint(12,height)
		TURRETDIAMETER = (int)(pi * TURRETWIDTH)+1 # the number of blocks around the circumference that need to be drawn.
		TURRETRADIUS = (int)(TURRETWIDTH/2)
		TURRETANGLE = (float)(2*pi / TURRETDIAMETER)
		STARTANGLE = randint(0,360) * pi / 180

		startX = (int)(DISTANCEX * cos(STARTANGLE)) # Centre of the turret
		startZ = (int)(DISTANCEZ * sin(STARTANGLE))				

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
					block = AIR # AIR
				elif window == True:
					block = AIR # AIR
					window = False


				setBlock(level, block,  
					(int)(box.minx+centreWidth+(startX+wallX)),
					(int)(box.miny+iterY),
					(int)(box.minz+centreDepth+(startZ+wallZ))
				)

		for iterY in xrange(0, TURRETHEIGHT): # Now place flooring
			if (iterY%6) == 0:
				# Drop in a floor
				print 'Placing a floor at %s on Hall # %s' % (iterY, wallInstanceNum)
				for floorRadius in xrange(0, TURRETRADIUS):
					floorCircumference = (int)(2 * floorRadius * pi)+1
					floorAngle = 2*pi/floorCircumference
					for floorIter in xrange(0, floorCircumference):
						floorX = (int)(floorRadius * cos(floorAngle * floorIter))
						floorZ = (int)(floorRadius * sin(floorAngle * floorIter))
						block = materialHighlight
						setBlockIfEmpty(level, block,  
							(int)(box.minx+centreWidth+(startX+floorX)),
							(int)(box.miny+iterY),
							(int)(box.minz+centreDepth+(startZ+floorZ))
							)
								
	
def perform(level, box, options):
	''' This script is used to generate a Castle in Minecraft. Feedback to abrightmoore@yahoo.com.au '''
	# METHODS
	SymmetricCastle(level, box, options)	

	
	level.markDirtyBox(box)