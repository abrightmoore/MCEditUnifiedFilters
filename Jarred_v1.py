

# Start with a pattern within the selection area
# Run the filter and the pattern will be folded into a jar / vase
# Notes: 1. the centre of the patterns stays as-is as the flat base of the jar.
#        2. the lower portion of the jar is a concave curve defined by a radius that reaches the edge of the selection box
#        3. 

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	if makeJar(level, box, options) == True:
		level.markDirtyBox(box)

def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)

def analyse(level):
	''' Examine the object in the schematic for min, max non-empty co-ordinates so we can pack-them-in! '''
	
	# Find the bounding box for the object within this schematic. i.e. clip empty space
	method = "Analyse schematic contents for the object dimensions"
	print '%s: Started at %s' % (method, time.ctime())
	
	box = level.bounds
	(width, height, depth) = getBoxSize(level.bounds)

	#print 'ANALYSE %s %s %s' % (width, height, depth)

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

	#print 'ANALYSE RESULT %s %s %s %s %s %s' % (minX, minY, minZ, maxX, maxY, maxZ)
	#print '%s: Ended at %s' % (method, time.ctime())
	
	if found == False:
		return BoundingBox((0, 0, 0), (width, height, depth))	
	else:
		return BoundingBox((minX, 0, minZ), (maxX+1, maxY+1, maxZ+1))
	
def makeJar(level, box, options):
	# Track two positions. One is the source map, which are blocks in the selection area base that should be wrapped around
	# ... and the second is a target position which is the jar / gourd shape above the block selection area
	#
	method = "makeJar"
	print '%s: Started at %s' % (method, time.ctime())
	(width, height, depth) = (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)
	centreWidth = math.floor(width / 2)
	centreHeight = math.floor(height / 2)
	centreDepth = math.floor(depth / 2)
	AIR = 0
	ONEDEGREE = pi/360

	# Scan the selection to work out how much space is available for the jar
	patternBB = analyse(box) # a custom method I wrote to look at how large the non-air object is within the selection
	# .length, .width, .height
	tgtHeight = height - patternBB.height
	
	# For each part of the jar, draw the block at that position using the corresponding block from the original pattern.
	# At this point we know how big the source block pattern is, as well as how high the user has asked for the target 
	
	sourcePosX = 0
	sourcePosZ = 0
	sourcePosY = 0
	
	tgtPosTheta = 0 # longitude
	tgtPosPhi = 0 # latitude
	tgtPosDist = 0 # radius
	
	# Do the bottom "bowl" bit
	radiusBase = centreWidth
	ratio = 3 # Magic - move to options

	wallLength = 2*centreWidth*pi + 2*centreWidth*pi*2/3 + 2*centreWidth/4*pi + 2*centreWidth/4*pi # Number of blocks in the curve of the wall. Lots of magic numbers in here!
	# Now we know what the length of the wall is, we can think about mapping our pattern onto it and drawing out the jar

	# Start plotting:
	for phi in xrange(0,90): # for each line of latitude.
		# How many blocks are there around the jar?
		circumference =	ceiling(2*pi*(centreWidth*sin(phi*ONEDEGREE)))
		if circumference > 0:
			theta = 0
			stepSizeAngle = 2*pi/circumference # Each block in the circumference corresponds to an angle swept to reach it
			while theta < 360:
				setBlock(level, (1,0), box.minx + centreWidth + centreWidth*sin(phi*ONEDEGREE), box.miny + centreHeight*sin(phi*ONEDEGREE) ,box.minz + centreDepth + centreDepth*sin(phi*ONEDEGREE))
				theta = theta + stepSizeAngle
	
	
#	for iterY in xrange(0,height):
#		for iterZ in xrange(0,depth):
#			for iterX in xrange(0,width):
#				tempBlock = level.blockAt(box.minx + iterX, box.miny + iterY, box.minz + iterZ)
#				if tempBlock != AIR:
#					maxY = iterY
	
