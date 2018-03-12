# This filter is a hack of @Sethbling's Player Statue filter. 
# It takes a (small) PNG from a web site and renders it vertically as blocks using @Sethbling's material mapping
# This hack @abrightmoore http://brightmoore.net
# Hacks marked up. All other code by @Sethbling, as below:

# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from httplib import HTTPConnection
import png

# displayName = "PNG to Blocks" # hack

inputs = (
	("Host", ("string", "value=i.imgur.com:80")), # hack
	("Path", ("string","value=/zzFmHnk.png")), # hack
	("Horizontal", True),
)

materials = [
	(1,   0,  125, 125, 125),
	(3,   0,  134,  96,  67),
	(5,   0,  156, 127,  78),
	(5,   1,  103,  77,  46),
	(5,   2,  195, 179, 123),
	(5,   3,  154, 110,  77),
	(22,  0,   29,  71, 165),
	(24,  0,  229, 221, 168),
	(25,  0,  100,  67,  50),
	(35,  0,  221, 221, 221),
	(35,  1,  219, 125,  62),
	(35,  2,  179,  80, 188),
	(35,  3,  107, 138, 201),
	(35,  4,  177, 166,  39),
	(35,  5,   65, 174,  56),
	(35,  6,  208, 132, 153),
	(35,  7,   64,  64,  64),
	(35,  8,  154, 161, 161),
	(35,  9,   46, 110, 137),
	(35, 10,  126,  61, 181),
	(35, 11,   46,  56, 141),
	(35, 12,   79,  50,  31),
	(35, 13,   53,  70,  27),
	(35, 14,  150,  52,  48),
	(35, 15,   25,  22,  22),
	(41,  0,  249, 236,  78),
	(42,  0,  219, 219, 219),
	(45,  0,  146,  99,  86),
	(49,  0,   20,  18,  29),
	(57,  0,   97, 219, 213),
	(80,  0,  239, 251, 251),
	(82,  0,  158, 164, 176),
	(87,  0,  111,  54,  52),
	(88,  0,   84,  64,  51),
	(98,  0,  122, 122, 122),
	(103, 0,  141, 145,  36),
	(112, 0,   44,  22,  46),
	(121, 0,  221, 223, 165),
	(133, 0,   81, 217, 117),
	#(152, 0,  171,  27,   9), # 1.5
	#(155, 0,  236, 233, 226), # 1.5
]

def getPixel(pixels, x, y):
	idx = x*4
	return (pixels[y][idx], pixels[y][idx+1], pixels[y][idx+2], pixels[y][idx+3])
	
def transparent((r, g, b, a)):
	return a < 128
	
def closestMaterial((r, g, b, a)):
	closest = 255*255*3
	best = (35, 0)
	for (mat, dat, mr, mg, mb) in materials:
		(dr, dg, db) = (r-mr, g-mg, b-mb)
		dist = dr*dr+dg*dg+db*db
		if dist < closest:
			closest = dist
			best = (mat, dat)
	
	return best

def perform(level, box, options):
	host = options["Host"] # hack
	conn = HTTPConnection(host, timeout=10000) # hack
	path = options["Path"] # hack
	horizontal = options["Horizontal"] # hack
	print "Retrieving " + path + " from " + host # hack
	conn.request("GET", path)
	response = conn.getresponse()
	print response.status, response.reason
		
	data = response.read()
	conn.close()
	
	reader = png.Reader(bytes=data)
	(width, height, pixels, metadata) = reader.asRGBA8()
	pixels = list(pixels)
	
	for x in xrange(0, width): # hack
		y = height # hack
		while y > 0: # hack
			colour = getPixel(pixels, width-x-1, height-y) # hack
			if not transparent(colour):
				(mat, dat) = closestMaterial(colour)
				if horizontal == True:
					level.setBlockAt(box.minx + x, box.miny, box.minz+y, mat) # hack
					level.setBlockDataAt(box.minx + x, box.miny, box.minz+y, dat) # hack
				else:
					level.setBlockAt(box.minx + x, box.miny+y, box.minz, mat) # hack
					level.setBlockDataAt(box.minx + x, box.miny+y, box.minz, dat) # hack
			y = y - 1 # hack
			
