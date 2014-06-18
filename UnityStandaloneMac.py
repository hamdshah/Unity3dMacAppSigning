#!/usr/bin/pyhton

#created by: hamdullahshah@gmail.com

import os
import subprocess
import plistlib as PlistParser


appPath = "/Users/user/Desktop/MyApp.app"
entitlements = "/Users/user/Desktop/entitlements.plist"
signingProfileName = "3rd Party Mac Developer Application: Company, INC."
signingInstallerProfileName = ""

#outPut package name. or path to save default is current directory
AppPackageName = "myApp.pkg"


#Info.plist values
bundleStringinfoValue = "Kids Learning Program 1.1.0. (c) 2014 MyCompany Inc. All rights reserved."

bundleVersionStringValue = "1.1.0"

bundleVersionNumberValue = "1.1.0"

bundleIdentifierValue = "com.company.MyApp"

bundleNameValue = "MyApp"

ApplicationCategoryValue = "public.app-category.arcade-games"

ReadableCopyRightValue = "MyCompany  v1.0.0 (c) MyCompany, Inc."


def removeMetaFilesFromDirectiory(dirPath):
	fileslist = []
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			if file.endswith('.meta'):
				metaFilePath = root + '/' + file
				fileslist.append(metaFilePath)
				
	for filePath in fileslist:
		print 'deleting file: ', filePath
		os.remove(filePath)

def signPlugins():
	pluginsPath = appPath + '/Contents/Plugins'
	if os.path.exists(pluginsPath):
		for plugin in os.listdir(pluginsPath):
			p = pluginsPath + '/' + plugin
			removeMetaFilesFromDirectiory(p)
			executeCodeSign(p)



def UpdateInfoPlist():
	plistPath = appPath + "/Contents/Info.plist"

	allData = PlistParser.readPlist(plistPath)

	allData["CFBundleGetInfoString"] = bundleStringinfoValue

	allData["CFBundleShortVersionString"] = bundleVersionStringValue

	allData["CFBundleVersion"] = bundleVersionNumberValue

	allData["CFBundleIdentifier"] = bundleIdentifierValue

	allData["CFBundleName"] = bundleNameValue

	allData["LSApplicationCategoryType"] = ApplicationCategoryValue

	allData["NSHumanReadableCopyright"] = ReadableCopyRightValue

	PlistParser.writePlist(allData, plistPath)


def executeCodeSign(pathToTargetSign):
	codesignPlugin = subprocess.call(["codesign", "--deep", "-f", "-v", "-s", signingProfileName, "--entitlements", entitlements, pathToTargetSign])
	if codesignPlugin == 0:
		print '\nSigning Completed of ', pathToTargetSign
		return True
	else:
		print subprocess.CalledProcessError
		return False


def AppSigning():
	print "\n\n**********Signing App for Mac AppStore with \"", signingProfileName, "\" ************"
	codesignOutput = subprocess.call(["codesign", "--deep", "-f", "-v", "-s", signingProfileName, "--entitlements", entitlements, appPath])
	if codesignOutput == 0:
		print '\n\nSigning Completed'
		return True
	else:
		print subprocess.CalledProcessError
		return False

def PackageCreation():
	if len(signingInstallerProfileName) == 0:
		print '\n\nCreating Package without installer signing.'
		installerOutPut = subprocess.call(["productbuild", "--component", appPath, "/Applications", AppPackageName])
		if installerOutPut == 0:
			print '\n\nPackage Created'
		else:
			print subprocess.CalledProcessError
	else:
		print '\n\nCreating Package with ',signingInstallerProfileName, ' installer signing.'
		installerOutPut = subprocess.call(["productbuild", "--component", appPath, "/Applications", "--sign", signingInstallerProfileName, AppPackageName])
		if installerOutPut == 0:
			print '\n\nPackage Created'
		else:
			print subprocess.CalledProcessError

def  main():
	if os.path.exists(appPath) == False:
		print 'File Does Not Exist: ', appPath
		return
	
	if os.path.exists(entitlements) == False:
		print 'File Does Not Exist: ', entitlements
		return

	UpdateInfoPlist()

	signPlugins()

	isSigned = AppSigning()

	if isSigned:
		PackageCreation()
		
	print '\n\n**********End************'



if __name__ == "__main__":
    main()

