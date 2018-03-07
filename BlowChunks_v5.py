# Purge empty chunks - for Qwerty
# Based on @Texelelf's code samples

inputs = (
	  ("BLOW CHUNKS", "label"),
	  ("Minimum number of blocks:", 0),
	  ("Purge Unpopulated Chunks?", True),
	  ("Suppress Relighting?", True),
	  ("Requested by Qwertyuiopthepie", "label"),
	  ("abrightmoore@yahoo.com.au", "label"),
	  ("http://brightmoore.net", "label"),
)

def perform(level, box, options):
	''' Feedback to abrightmoore@yahoo.com.au '''
	BlowChunks(level, box, options)		
	
def BlowChunks(level, box, options):
	UNPOPURGE = options["Purge Unpopulated Chunks?"]
	SUPPRESS = options["Suppress Relighting?"]
	BLOCKTHRESHOLD = options["Minimum number of blocks:"]

	for (chunk, slices, point) in level.getChunkSlices(box):
		countTileEntities = len(chunk.TileEntities)
		# countTileTicks = len(chunk.TileTicks)
		countEntities = len(chunk.Entities)
		# countSections = len(chunk.Sections)
		countBlocks = 0
		for theBlocks in chunk.Blocks:
			if countBlocks > BLOCKTHRESHOLD:
				break; # Stop counting... we're done
			for theSubBlocks in theBlocks:
				for theBlock in theSubBlocks:
					if theBlock != 0:
						countBlocks = countBlocks + 1
	
		(cx, cz) = chunk.chunkPosition		
		print "Chunk cx = %s, cz = %s: TileEntities = %s, Entities = %s, Blocks = %s, Populated = %s" % (cx, cz, countTileEntities, countEntities, countBlocks, chunk.TerrainPopulated)
		if SUPPRESS == True:
			chunk.needsLighting = 0 # v3 - suppress lighting updates. Courtesy @Texelelf and @CodeWarrior
		
		theWorld = chunk.world
		
		if (countEntities == 0 and countTileEntities == 0 and countBlocks < BLOCKTHRESHOLD) or (chunk.TerrainPopulated == 0 and UNPOPURGE == True):
			# Purge the chunk
			print "Purge chunk cx = %s, cz = %s" % (cx, cz)
			theWorld.deleteChunk(cx, cz)
			theWorld._allChunks.discard((cx, cz))
