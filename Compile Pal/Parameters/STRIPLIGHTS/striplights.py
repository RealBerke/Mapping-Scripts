strName = "Strip Lights"
strAuthor = "Berke"
iVersion = 1

strLightClassnames = ("light_environment", "light_directional", "light", "light_spot")

def Main():
	print("\"" + strName +"\" by \"" + strAuthor + "\", version " + str(iVersion) + ".")

	import sys

	strArguments = sys.argv

	if len(strArguments) > 1:
		strArgument = strArguments[1]

		if strArgument.endswith(".bsp"):
			print("Modifying \"" + strArgument + "\".")

			import bsp_tool

			BSP = bsp_tool.load_bsp(strArgument)

			iAffectedEntities1 = 0

			iAffectedEntities2 = 0

			iAffectedEntities3 = 0

			strToggleLightNames = []

			iEntityIndex = 0

			Entites = BSP.ENTITIES

			while iEntityIndex < len(Entites):
				Entity = Entites[iEntityIndex]

				if Entity["classname"] in strLightClassnames:
					if "targetname" in Entity:
						strTargetname = Entity["targetname"]

						if strTargetname in strToggleLightNames:
							Entites.pop(iEntityIndex)

							iAffectedEntities1 += 1

						else:
							iKeyIndex = 0

							strAllowedKeyValues = ("classname", "targetname", "style")

							while iKeyIndex < len(Entity):
								strKey = list(Entity)[iKeyIndex]

								if strKey in strAllowedKeyValues:
									iKeyIndex += 1

								else:
									del Entity[strKey]

							iAffectedEntities2 += 1

							strToggleLightNames.append(strTargetname)

							iEntityIndex += 1

					else:
						Entites.pop(iEntityIndex)

						iAffectedEntities3 += 1

				else:
					iEntityIndex += 1

			if iAffectedEntities1 or iAffectedEntities2 or iAffectedEntities3:
				BSP.save()

				if iAffectedEntities2:
					print("Simplified " + str(iAffectedEntities2) + " toggle light" + ("" if iAffectedEntities2 == 1 else "s") + ".")

				if iAffectedEntities1:
					print("Deleted " + str(iAffectedEntities1) + " duplicate toggle light" + ("" if iAffectedEntities1 == 1 else "s") + ".")

				elif not iAffectedEntities2:
					print("Couldn't find any toggle light entities.")

				if iAffectedEntities3:
					print("Deleted " + str(iAffectedEntities3) + " static light" + ("" if iAffectedEntities3 == 1 else "s") + ".")

				else:
					print("Couldn't find any static light entities.")

			else:
				print("Couldn't find any light entities.")

			print("Finished!")

		else:
			print("Specified path isn't pointing to a BSP file.")

	else:
		print("Path to the map file has to be supplied as an argument.")

if __name__ == "__main__":
	Main()