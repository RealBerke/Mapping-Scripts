strName = "Order Entities"
strAuthor = "Berke"
iVersion = 1

strKeyValueName = "entityorder"

def Main():
	print("\"" + strName +"\" by \"" + strAuthor + "\", version " + str(iVersion) + ".")

	import sys

	strArguments = sys.argv

	if len(strArguments) > 1:
		strArgument = strArguments[1]

		if strArgument.endswith(".vmf"):
			print("Modifying \"" + strArgument + "\".")

			import valvevmf

			VMF = valvevmf.Vmf(strArgument)

			iAffectedEntities = 0

			FilteredEntities = []

			iNodeIndex = 0

			Nodes = VMF.nodes

			while iNodeIndex < len(Nodes):
				bNoOrder = True

				Node = Nodes[iNodeIndex]

				for Property in Nodes[iNodeIndex].properties:
					if Property[0] == strKeyValueName:
						iAffectedEntities += 1

						bNoOrder = False

						FilteredEntities.append(Nodes.pop(iNodeIndex))

						break

				if bNoOrder:
					iNodeIndex += 1

			FilteredEntities.sort(key = SortEntityOrder)

			for FilteredEntity in FilteredEntities:
				Properties = FilteredEntity.properties

				for iPropertyIndex, Property in enumerate(Properties):
					if Property[0] == strKeyValueName:
						Properties.pop(iPropertyIndex)
						
						break;

				Nodes.append(FilteredEntity)

			if iAffectedEntities:
				VMF.save()

				print("Changed order of " + str(iAffectedEntities) + " entit" + ("y" if iAffectedEntities == 1 else "ies") + ".")

			else:
				print("Couldn't find any entities to change order of.")

			print("Finished!")

		else:
			print("Specified path isn't pointing to a VMF file.")

	else:
		print("Path to the map file has to be supplied as an argument.")

def SortEntityOrder(Value):
	for Property in Value.properties:
		if Property[0] == strKeyValueName:
			return Property[1]

if __name__ == "__main__":
	Main()