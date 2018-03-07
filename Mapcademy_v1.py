
import string
from pymclevel import *

inputs = (
	("Mapcademy","label"),
	("Mode", ("Mob Cells",
			  "Mob Cells 2")
	),
	("Mob Cell Schematic", ("string", "value=C:\\Users\\Adrian\\Documents\\MCEdit\\Filters\\MapcademyMobCell_v1.schematic")),
	("@TheWorldFoundry","label")
	)


def perform(level,box,options):
	MobCells(level,box,options)

def MobCells(level,box,options):
#	entityNames1 = "minecraft:area_effect_cloud, minecraft:armor_stand, minecraft:arrow, minecraft:bat, minecraft:blaze, minecraft:boat, minecraft:cave_spider, minecraft:chest_minecart, minecraft:chicken, minecraft:commandblock_minecart, minecraft:cow, minecraft:creeper, minecraft:donkey, minecraft:dragon_fireball, minecraft:egg, minecraft:elder_guardian, minecraft:ender_crystal, minecraft:ender_dragon, minecraft:ender_pearl, minecraft:enderman, minecraft:endermite, minecraft:evocation_fangs, minecraft:evocation_illager, minecraft:eye_of_ender_signal, minecraft:falling_block, minecraft:fireball, minecraft:fireworks_rocket, minecraft:furnace_minecart, minecraft:ghast, minecraft:giant, minecraft:guardian, minecraft:hopper_minecart, minecraft:horse, minecraft:husk, minecraft:illusion_illager, minecraft:item, minecraft:item_frame, minecraft:leash_knot, minecraft:lightning_bolt, minecraft:llama, minecraft:llama_spit, minecraft:magma_cube, minecraft:minecart, minecraft:mooshroom, minecraft:mule, minecraft:ocelot, minecraft:painting, minecraft:parrot, minecraft:pig, minecraft:polar_bear, minecraft:potion, minecraft:rabbit, minecraft:sheep, minecraft:shulker, minecraft:shulker_bullet, minecraft:silverfish, minecraft:skeleton, minecraft:skeleton_horse, minecraft:slime, minecraft:small_fireball, minecraft:snowball, minecraft:snowman, minecraft:spawner_minecart, minecraft:spectral_arrow, minecraft:spider, minecraft:squid, minecraft:stray, minecraft:tnt, minecraft:tnt_minecart, minecraft:vex, minecraft:villager, minecraft:villager_golem, minecraft:vindication_illager, minecraft:witch, minecraft:wither, minecraft:wither_skeleton, minecraft:wither_skull, minecraft:wolf, minecraft:xp_bottle, minecraft:xp_orb, minecraft:zombie, minecraft:zombie_horse, minecraft:zombie_pigman, minecraft:zombie_villager"

	entityNamesFarmAnimals = "minecraft:wolf, minecraft:horse, minecraft:donkey, minecraft:mule, minecraft:cow, minecraft:mooshroom, minecraft:llama, minecraft:sheep, minecraft:pig, minecraft:chicken"

	entityNamesBeasts = "minecraft:polar_bear, minecraft:ocelot, minecraft:rabbit, minecraft:parrot, minecraft:bat"
	
	entityNamesMobs = "minecraft:shulker, minecraft:spider, minecraft:cave_spider, minecraft:blaze, minecraft:creeper, minecraft:magma_cube, minecraft:slime, minecraft:enderman, minecraft:endermite, minecraft:silverfish, minecraft:elder_guardian, minecraft:guardian, minecraft:lightning_bolt"
	
	entityNamesMobHumanoid = "minecraft:wither_skeleton, minecraft:skeleton, minecraft:zombie_pigman, minecraft:witch, minecraft:zombie, minecraft:zombie_villager, minecraft:vindication_illager, minecraft:husk, minecraft:illusion_illager, minecraft:stray, minecraft:evocation_illager, minecraft:evocation_fangs, minecraft:vex, minecraft:snowman, minecraft:villager, minecraft:villager_golem"

	entityNamesMobMounts = "minecraft:zombie_horse, minecraft:skeleton_horse"
	
	entityLists = [entityNamesMobs, entityNamesMobHumanoid, entityNamesMobMounts, entityNamesFarmAnimals, entityNamesBeasts]
	
	yOffset = 0
	for entityNames in entityLists:
		entityNameList = string.split(entityNames,", ")
		
		schema = MCSchematic(filename=options["Mob Cell Schematic"])
		
		schemCount = 0
		for entityName in entityNameList:
			print "Processing "+entityName
			entityTypes = string.split(entityName,":")
			entityType = entityTypes[len(entityTypes)-1]
			print entityType
			
			# Find and replace the nbt on the sign
			for t in schema.TileEntities:
				if t["id"].value.startswith("minecraft:sign"):
					t["Text1"] = TAG_String("")
					t["Text2"] = TAG_String("{\"text\":\""+entityType+"\"}")
					t["Text3"] = TAG_String("")
					t["Text4"] = TAG_String("")
			
			# Find and replace the nbt on the command blocks
				elif t["id"].value.startswith("minecraft:command"):
					if t["Command"].value.startswith("kill"):
						t["Command"] = TAG_String("kill @e[r=3,type="+entityName+"]")
					elif t["Command"].value.startswith("summon"):
						t["Command"] = TAG_String("summon "+entityName+" ~ ~-1 ~-2")
			
			# Copy the modified schematic over
			level.copyBlocksFrom(schema, BoundingBox((0,0,0),(schema.Width,schema.Height,schema.Length)),(box.minx,box.miny+yOffset*schema.Height,box.minz+schema.Length*schemCount))
			
			
			schemCount += 1
		yOffset += 1
		
		
		
		