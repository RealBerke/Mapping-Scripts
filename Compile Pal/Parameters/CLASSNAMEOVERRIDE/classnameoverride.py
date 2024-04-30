strName = "Classname Override"
strAuthor = "Berke"
iVersion = 1

strKeyValueName = "classnameoverride"

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

			iAffectedEntities = 0

			for Entity in BSP.ENTITIES:
				if strKeyValueName in Entity:
					iAffectedEntities += 1

					Entity["classname"] = Entity["classname"] + "\"\n" + "\"classname\" \"" + Entity[strKeyValueName]

					del Entity[strKeyValueName]

			if iAffectedEntities:
				BSP.save()

				print("Overridden classname of " + str(iAffectedEntities) + " entit" + ("y" if iAffectedEntities == 1 else "ies") + ".")

			else:
				print("Couldn't find any entities to override the classname of.")

			print("Finished!")

		else:
			print("Specified path isn't pointing to a BSP file.")

	else:
		print("Path to the map file has to be supplied as an argument.")

if __name__ == "__main__":
	Main()