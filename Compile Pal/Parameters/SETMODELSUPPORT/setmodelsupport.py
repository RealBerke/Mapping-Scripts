strName = "Set Model Support"
strAuthor = "Berke"
iVersion = 1

strFileExtension = "bsp"
strInternalPropDataPath = "scripts/"
strInternalPropDataFileName = "propdata.txt"
strModelFolder = "models/"
strModelFileExtension = "mdl"
strPropDataSection = "BreakableModels"
strInputName = "SetModel"
strInputSeperator = ","
strWorkAroundInput = "AddOutput"
iCacheStartIndex = 1

def Main():
	print("\"" + strName +"\" by \"" + strAuthor + "\", version " + str(iVersion) + ".")

	from sys import argv

	strArguments = argv
	iArgumentAmount = len(strArguments)

	if iArgumentAmount == 1:
		print("Path to the map \"" + strFileExtension.upper() + "\" file has to be supplied as the first argument.")
		return;

	strMapPath = strArguments[1]

	from os.path import isfile

	if not isfile(strMapPath):
		print("First argument is not pointing to a file.")
		return

	if not strMapPath.endswith("." + strFileExtension):
		print("First argument is not pointing to a \"" + strFileExtension.upper() + "\" file.")
		return

	if iArgumentAmount == 2:
		print("Path to the game folder has to be supplied as the second argument.")
		return

	strGameFolder = strArguments[2]

	from os.path import isdir

	if not isdir(strGameFolder):
		print("Second argument is not pointing to a folder.")
		return

	if iArgumentAmount == 3:
		print("Path to the \"BSPZip\" file has to be supplied as the third argument.")
		return

	strBSPZipPath = strArguments[3]

	if not isfile(strBSPZipPath):
		print("Third argument is not pointing to a file.")
		return

	if not strBSPZipPath.endswith(".exe"):
		print("Third argument is not pointing to a \"EXE\" file.")
		return

	if iArgumentAmount == 4:
		print("Path to the \"" + strInternalPropDataFileName + "\" file has to be supplied as the forth argument. Can be a \"VPK\" file.")
		return

	strPropDataPath = strArguments[4]

	if not isfile(strPropDataPath):
		print("Forth argument is not pointing to a file.")
		return

	bIsVPK = strPropDataPath.endswith(".vpk")

	if not (strPropDataPath.endswith(".txt") or bIsVPK):
		print("Forth argument is not pointing to a \"TXT\" or \"VPK\" file.")
		return

	strInternalFullPropDataPath = strInternalPropDataPath + strInternalPropDataFileName

	if bIsVPK:
		import vpk

		try:
			vpk.open(strPropDataPath)
		except:
			print("Could not open the \"VPK\" file.")
			return

		VPK = vpk.open(strPropDataPath)

		try:
			VPK.get_file(strInternalFullPropDataPath)
		except:
			print("Could not find the \"" + strInternalPropDataFileName + "\" inside the \"VPK\" file.")
			return

	print("Modifying the \"" + strMapPath + "\" file.")

	from bsp_tool import load_bsp

	BSP = load_bsp(strMapPath)
	iFoundInputs = 0
	lModels = list()
	iCacheAmount = iCacheStartIndex + len(BSP.MODELS)

	for dEntity in BSP.ENTITIES:
		for strKeyValue in dEntity:
			Value = dEntity[strKeyValue]

			if not isinstance(Value, list):
				lResults = ModifyOutput(Value, lModels, iCacheAmount)

				if lResults[0]:
					iFoundInputs += 1
					dEntity[strKeyValue] = lResults[1]
					strModel = lResults[2]

					if strModel not in lModels:
						lModels.append(strModel)
			else:
				for iOutputIndex, strOutput in enumerate(Value):
					lResults = ModifyOutput(strOutput, lModels, iCacheAmount)

					if lResults[0]:
						iFoundInputs += 1
						dEntity[strKeyValue][iOutputIndex] = lResults[1]
						strModel = lResults[2]

						if strModel not in lModels:
							lModels.append(strModel)

	if not iFoundInputs:
		print("Could not find any \"" + strInputName + "\" inputs.")
	else:
		print("Modified " + str(iFoundInputs) + " \"" + strInputName + "\" input" + GetPluralitySuffix(iFoundInputs) + ".")

		BSP.save()

		lPacks = list()
		strFixedGameFolder = strGameFolder.replace("\\", "/")

		for strModel in lModels:
			strModelPath = strFixedGameFolder + "/" + strModel

			if isfile(strModelPath):
				lPacks.append(strModelPath)

		iPackLength = len(lPacks)

		if iPackLength:
			print("Pack th" + GetPluralitySuffix(iPackLength, "is", "ese") + ":")

			for strPack in lPacks:
				print(strPack)

		if bIsVPK:
			from io import StringIO

			fPropData = StringIO(vpk.open(strPropDataPath).get_file(strInternalFullPropDataPath).read().decode("utf-8"))
		else:
			fPropData = open(strPropDataPath)

		import vdf
		from vdf import VDFDict

		dPropData = vdf.load(fPropData)

		if not bIsVPK:
			fPropData.close()

		if not len(dPropData):
			dPropData["0"] = VDFDict([(strPropDataSection, VDFDict([("0", VDFDict())]))])
		else:
			for strFirstKey in list(dPropData):
				bIsFirstKeyNonZero = strFirstKey != "0"

				if strFirstKey != "PropData.txt" and bIsFirstKeyNonZero:
					del dPropData[strFirstKey]
				else:
					dPropDataFirst = dPropData[strFirstKey]

					if bIsFirstKeyNonZero:
						dPropData["0"] = dPropDataFirst

						del dPropData[strFirstKey]

						strFirstKey = "0"

					if not len(dPropDataFirst):
						dPropDataFirst[strPropDataSection] = VDFDict([("0", VDFDict())])
					else:
						for strSecondKey in list(dPropDataFirst):
							if strSecondKey != strPropDataSection:
								del dPropData[strFirstKey][strSecondKey]
							else:
								dPropDataSecond = dPropDataFirst[strSecondKey]

								for strThirdKey in list(dPropDataSecond):
									dPropDataThird = dPropDataSecond[strThirdKey]

									for strForthKey in list(dPropDataThird):
										if not strForthKey.islower() or "\\" in strForthKey:
											del dPropDataThird[strForthKey]

											strFixedForthKey = strForthKey.lower().replace("\\", "/")
											dPropDataThird[strFixedForthKey] = 0

		dSavedValues = dict(dPropData["0"][strPropDataSection])
		dPropData["0"][strPropDataSection] = VDFDict([("0", VDFDict())])

		for strModel in lModels:
			dPropData["0"][strPropDataSection]["0"][strModel] = 0

		for strKey, dValue in dSavedValues.items():
			dPropData["0"][strPropDataSection][strKey] = dValue

		strTemporaryPath = strBSPZipPath[0: strBSPZipPath.rfind("\\") + 1] + "Temp"
		fNewFile = open(strTemporaryPath, "w")

		fNewFile.write(vdf.dumps(dPropData, True))

		fNewFile.close()

		PackFile(strTemporaryPath, strInternalFullPropDataPath)

		import os

		os.remove(strTemporaryPath)

	print("Finished!")

def GetPluralitySuffix(iNumber, strSingularSuffix = "", strPluralSuffix = "s"):
	return strSingularSuffix if iNumber == 1 else strPluralSuffix

def ModifyOutput(strOutput, lModels, iCacheAmount):
	if strOutput.count(strInputSeperator) != 4:
		return [False]

	lOutput = strOutput.split(strInputSeperator)

	if lOutput[1] != strInputName:
		return [False]

	strThirdParameter = lOutput[2]

	if not (strThirdParameter.startswith(strModelFolder) and strThirdParameter.endswith(strModelFileExtension)):
		return [False]

	try:
		float(lOutput[3])
	except:
		return [False]

	strFifthParameter = lOutput[4]

	if strFifthParameter != "-1" and not strFifthParameter.isdigit():
		return [False]

	lOutput[1] = strWorkAroundInput
	strModel = lOutput[2]
	iModelIndex = iCacheAmount

	if strModel in lModels:
		iModelIndex += lModels.index(strModel)

	else:
		iModelIndex += len(lModels)

	lOutput[2] = "modelindex " + str(iModelIndex)
	strOutput = ""

	for iOutputIndex in range(len(lOutput)):
		strOutput += lOutput[iOutputIndex] + ("" if iOutputIndex == 4 else strInputSeperator)

	return True, strOutput, strModel

def PackFile(strPath, strInternalPath):
	from sys import argv

	strArguments = argv
	strMapPath = strArguments[1]

	import subprocess

	subprocess.run([strArguments[3], "-addfile", strMapPath, strInternalPath, strPath, strMapPath])

if __name__ == "__main__":
	Main()