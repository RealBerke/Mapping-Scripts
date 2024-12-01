strName = "Set Model Support"
strAuthor = "Berke"
iVersion = 1

strFileExtension = "bsp"
strInternalPropDataPath = "scripts/"
strInternalPropDataFileName = "propdata.txt"
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

	if iArgumentAmount > 1:
		strMapPath = strArguments[1]

		from os.path import isfile

		if isfile(strMapPath):
			if strMapPath.endswith("." + strFileExtension):
				if iArgumentAmount > 2:
					strGameFolder = strArguments[2]

					from os.path import isdir

					if isdir(strGameFolder):
						if iArgumentAmount > 3:
							strBSPZipPath = strArguments[3]

							if isfile(strBSPZipPath):
								if iArgumentAmount > 4:
									strPropDataPath = strArguments[4]

									if isfile(strPropDataPath):
										iFileType = 1

										if strPropDataPath.endswith(".vpk"):
											iFileType = 0

											bIsValid = True

											strInternalFullPropDataPath = strInternalPropDataPath + strInternalPropDataFileName

											import vpk

											try:
												vpk.open(strPropDataPath)

											except:
												bIsValid = False

												print("Could not open the \"VPK\" file.")

											if bIsValid:
												VPK = vpk.open(strPropDataPath)

												bIsValid = True

												try:
													VPK.get_file(strInternalFullPropDataPath)

												except:
													bIsValid = False

													print("Could not find the \"" + strInternalPropDataFileName + "\" inside the \"VPK\" file.")

												if bIsValid:
													iFileType = 2

										if iFileType:
											print("Modifying the \"" + strMapPath + "\" file.")

											from bsp_tool import load_bsp

											BSP = load_bsp(strMapPath)

											iFoundInputs = 0

											lModels = list()

											iCacheAmount = iCacheStartIndex + len(BSP.MODELS)

											for dEntity in BSP.ENTITIES:
												for strKeyValue in dEntity:
													Value = dEntity[strKeyValue]

													if isinstance(Value, list):
														for iOutputIndex, strOutput in enumerate(Value):
															lResults = ModifyOutput(strOutput, lModels, iCacheAmount)

															bFoundInput = lResults[0]

															if bFoundInput:
																iFoundInputs += bFoundInput

																dEntity[strKeyValue][iOutputIndex] = lResults[1]

																strModel = lResults[2]

																if strModel not in lModels:
																	lModels.append(strModel)

													else:
														lResults = ModifyOutput(Value, lModels, iCacheAmount)

														bFoundInput = lResults[0]

														if bFoundInput:
															iFoundInputs += bFoundInput

															dEntity[strKeyValue] = lResults[1]

															strModel = lResults[2]

															if strModel not in lModels:
																lModels.append(strModel)

											if iFoundInputs:
												print("Modified " + str(iFoundInputs) + " \"" + strInputName + "\" input" + GetPluralitySuffix(iFoundInputs) + ".")

												BSP.save()

												lPackList = list()

												strFixedGameFolder = strGameFolder.replace("\\", "/")

												for strModel in lModels:
													strModelPath = strFixedGameFolder + "/" + strModel

													if isfile(strModelPath):
														lPackList.append(strModelPath)

												iPackListLength = len(lPackList)

												if iPackListLength:
													if iPackListLength == 1:
														print("Pack this model:")

													else:
														print("Pack these models:")

													for strPack in lPackList:
														print(strPack)

												if iFileType == 1:
													fPropData = open(strPropDataPath)

												else:
													from io import StringIO

													fPropData = StringIO(vpk.open(strPropDataPath).get_file(strInternalFullPropDataPath).read().decode("utf-8"))

												import vdf
												from vdf import VDFDict

												dPropData = vdf.load(fPropData)

												if iFileType == 1:
													fPropData.close()

												if len(dPropData):
													for strFirstKey in list(dPropData):
														if strFirstKey == "PropData.txt" or strFirstKey == "0":
															dPropDataFirst = dPropData[strFirstKey]

															if len(dPropDataFirst):
																if strFirstKey != "0":
																	dPropData["0"] = dPropDataFirst

																for strSecondKey in list(dPropDataFirst):
																	if strSecondKey == strPropDataSection:
																		dPropDataSecond = dPropDataFirst[strSecondKey]

																		for strThirdKey in list(dPropDataSecond):
																			dPropDataThird = dPropDataSecond[strThirdKey]

																			for strForthKey in list(dPropDataThird):
																				if not strForthKey.islower() or "\\" in strForthKey:
																					del dPropDataThird[strForthKey]

																					strForthKey = strForthKey.lower().replace("\\", "/")

																					dPropDataThird[strForthKey] = 0

																	else:
																		del dPropData[strFirstKey][strSecondKey]

															else:
																dPropDataFirst[strPropDataSection] = VDFDict([("0", VDFDict())])

														if strFirstKey != "0":
															del dPropData[strFirstKey]

												else:
													dPropData["0"] = VDFDict([(strPropDataSection, VDFDict([("0", VDFDict())]))])

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

											else:
												print("Could not find any \"" + strInputName + "\" inputs.")

											print("Finished!")

									else:
										print("Forth argument is not pointing to a file.")

								else:
									print("Path to the \"" + strInternalPropDataFileName + "\" file has to be supplied as the forth argument. Can be a \"VPK\" file.")

							else:
								print("Third argument is not pointing to a file.")

						else:
							print("Path to the \"BSPZip\" file has to be supplied as the third argument. Can be a \"VPK\" file.")

					else:
						print("Second argument is not pointing to a folder.")

				else:
					print("Path to the game folder has to be supplied as the second argument.")

			else:
				print("First argument is not pointing to a \"" + upper(strFileExtension) + "\" file.")

		else:
			print("First argument is not pointing to a file.")

	else:
		print("Path to the map \"" + upper(strFileExtension) + "\" file has to be supplied as the first argument.")

def GetPluralitySuffix(iNumber):
	return "" if iNumber == 1 else "s"

def ModifyOutput(strOutput, lModels, iCacheAmount):
	strModel = ""

	bFoundInput = False

	if strOutput.count(strInputSeperator) == 4:
		lOutput = strOutput.split(strInputSeperator)

		try:
			float(lOutput[1])

		except:
			strThirdParameter = lOutput[2]

			try:
				float(strThirdParameter)

			except:
				if strThirdParameter.startswith("models/") and strThirdParameter.endswith(".mdl"):
					bIsValid = False

					try:
						float(lOutput[3])

						bIsValid = True

					except:
						False

					if bIsValid:
						strFifthParameter = lOutput[4]

						if strFifthParameter == "-1" or strFifthParameter.isdigit() and lOutput[1] == strInputName:
							bFoundInput = True

							strModel = lOutput[2]

							lOutput[1] = strWorkAroundInput

							iModelIndex = iCacheAmount

							if strModel in lModels:
								iModelIndex += lModels.index(strModel)

							else:
								iModelIndex += len(lModels)

							lOutput[2] = "modelindex " + str(iModelIndex)

							strOutput = ""

							for iOutputIndex in range(len(lOutput)):
								strOutput += lOutput[iOutputIndex] + ("" if iOutputIndex == 4 else strInputSeperator)

	return bFoundInput, strOutput, strModel

def PackFile(strPath, strInternalPath):
	from sys import argv

	strArguments = argv

	strMapPath = strArguments[1]

	import subprocess

	subprocess.run([strArguments[3], "-addfile", strMapPath, strInternalPath, strPath, strMapPath])

if __name__ == "__main__":
	Main()