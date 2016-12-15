#!/usr/bin/env python
# -*- coding:utf-8 -*-

#./autobuild.py -p youproject.xcodeproj -t youproject -o ~/Desktop/youproject.ipa
#./autobuild.py -w youproject.xcworkspace -s youproject -o ~/Desktop/youproject.ipa

from optparse import OptionParser
import subprocess

# 需要改动的地方 (根据自己的项目信息改动改动)
PROJECT_NAME = "Name" 			    	#项目名称
VERSION = "1.0.0"  						#打包版本号 会根据不同的版本创建文件夹（与项目本身的版本号无关）
TAGREAT_NAME = "%s" %(PROJECT_NAME) 	#就是对应的target

CONFIGURATION = "Release" 				#Release 环境  Debug 环境
PROFILE = "Dev" 						#配置文件分为四种 AdHoc  Dev  AppStore Ent 分别对应四种配置文件
OUTPUT = "./Packge/%s" %(CONFIGURATION) #打包导出ipa文件路径（请确保 “%s” 之前的文件夹正确并存在）

WORKSPACE = "%s.xcworkspace" %(PROJECT_NAME)
PROJECT = "%s.xcodeproj" %(PROJECT_NAME)
SDK = "iphoneos"
#注意：如果在项目中用到 pod 请启用此行！！！！！！
PROJECT = None

#蒲公英上传
OPEN_PYUPLOAD = False  	#是否开启蒲公英上传功能  True  False
USER_KEY = "****************"
API_KEY = "****************"

#fir.im 上传
OPEN_FIR_UPLOAD = False  	#是否开启fir.im上传功能  True  False

#AppStore上传
OPEN_APPSTORE_UPLOAD = False  #是否开启AppStore上传上传功能  True  False
USER_NAME = "****************"
USER_PASSWORD = "****************"

#启动打印函数
def printStart():
	print "*****************************************************************"
	print "*****************************************************************"
	print "                       开始打包                             "
	print "  项目名称：%s" %(PROJECT_NAME)
	print "  Target：%s" %(TAGREAT_NAME)
	print "  版 本 号：%s" %(VERSION)
	print "  编译环境：%s" %(CONFIGURATION)
	print "  证书配置：%s" %(PROFILE)
	print "  是否上传蒲公英：%s" %(OPEN_PYUPLOAD)
	print "  是否上传FIR.IM：%s" %(OPEN_FIR_UPLOAD)
	print "  是否上传AppStore：%s\n" %(OPEN_APPSTORE_UPLOAD)
	print "*****************************************************************"
	print "*****************************************************************"

#结束打印函数
def printEnd():
	print "*****************************************************************"
	print "*****************************************************************"
	print "                       结束打包                             "
	print "  项目名称：%s" %(PROJECT_NAME)
	print "  Target：%s" %(TAGREAT_NAME)
	print "  版 本 号：%s" %(VERSION)
	print "  编译环境：%s" %(CONFIGURATION)
	print "  证书配置：%s" %(PROFILE)
	print "  是否上传蒲公英：%s" %(OPEN_PYUPLOAD)
	print "  是否上传FIR.IM：%s" %(OPEN_FIR_UPLOAD)
	print "  是否上传AppStore：%s\n" %(OPEN_APPSTORE_UPLOAD)
	print "*****************************************************************"
	print "*****************************************************************"

#清除 build 目录
def cleanBuildDir(buildDir):
	cleanCmd = "rm -r %s" %(buildDir)
	process = subprocess.Popen(cleanCmd, shell = True)
	process.wait()

#创建路径
def createDir(ipaDir):
	createCmd = "mkdir %s" %(ipaDir)
	process = subprocess.Popen(createCmd, shell = True)
	process.wait()

def uploadPgy(ipaPath):
	print "\n***************开始上传到蒲公英*********************\n"
	uploadCmd = 'curl -F \"file=@%s\" -F \"uKey=%s\" -F \"_api_key=%s\" https://www.pgyer.com/apiv1/app/upload' %(ipaPath, USER_KEY, API_KEY)
	process = subprocess.Popen(uploadCmd, shell = True)
	process.wait()
	print "\n\n***************上传结束 Code=0 为上传成功*********************\n"

def uploadFir(ipaPath):
	print "\n***************开始上传到FIR.IM*********************\n"
	uploadCmd = 'fir p %s' %(ipaPath)
	process = subprocess.Popen(uploadCmd, shell = True)
	process.wait()
	print "\n\n***************上传结束 Published succeed 为上传成功*********************\n"
	

def uploadAppStore(ipaPath):

	altool = "/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool"

	print "\n***************开始上传到AppStore*********************\n"
	uploadCmd = '%s --upload-app -f %s -t ios -u %s -p %s' %(altool, ipaPath, USER_NAME, USER_PASSWORD)
	process = subprocess.Popen(uploadCmd, shell = True)
	process.wait()
	print "\n\n***************上传结束 No errors uploading 为上传成功*********************\n"
	print "***************上传成功后，稍等片刻才能在 iTunes Connect 上更新*********************\n"



#打包
def xcbuild():
	#配置打包命令
	if PROJECT is None and WORKSPACE is None:
		pass
	elif PROJECT is not None:
		buildCmd = 'xcodebuild archive -project %s -scheme %s -sdk %s -configuration %s  ONLY_ACTIVE_ARCH=NO -archivePath ./build/%s.xcarchive' %(PROJECT, TAGREAT_NAME, SDK, CONFIGURATION,PROJECT_NAME)
		pass
	elif WORKSPACE is not None:
		buildCmd = 'xcodebuild archive -workspace %s -scheme %s -sdk %s -configuration %s  ONLY_ACTIVE_ARCH=NO -archivePath ./build/%s.xcarchive' %(WORKSPACE, TAGREAT_NAME, SDK, CONFIGURATION, PROJECT_NAME)
		pass
	
	printStart()

	#开始执行打包命令
	process = subprocess.Popen(buildCmd, shell = True)
	process.wait()

	#创建目录
	createDir(OUTPUT)
	createDir(OUTPUT+"/"+VERSION)

	#执行签名验证导出命令
	signCmd = 'xcodebuild -exportArchive -archivePath ./build/%s.xcarchive -exportPath %s/%s/%s_%s_%s -exportOptionsPlist ./AutoBuild/plist/%s.plist' %(PROJECT_NAME, OUTPUT, VERSION,PROJECT_NAME,VERSION,CONFIGURATION,PROFILE)
	process = subprocess.Popen(signCmd, shell = True)
	process.wait()

	printEnd()

	ipaPath = "%s/%s/%s_%s_%s/%s.ipa" %(OUTPUT, VERSION,PROJECT_NAME,VERSION,CONFIGURATION,TAGREAT_NAME)

	#蒲公英上传
	if OPEN_PYUPLOAD == True:
		uploadPgy(ipaPath)

	#FIR.IM上传
	if OPEN_FIR_UPLOAD == True:
		uploadFir(ipaPath)

	#AppStore上传
	if OPEN_APPSTORE_UPLOAD == True:
		uploadAppStore(ipaPath)

	#清理build目录
	cleanBuildDir("./build")


def main():

	xcbuild()

if __name__ == '__main__':
	main()
