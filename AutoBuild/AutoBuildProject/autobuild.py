#!/usr/bin/env python
# -*- coding:utf-8 -*-

#./autobuild.py -p youproject.xcodeproj -t youproject -o ~/Desktop/youproject.ipa
#./autobuild.py -w youproject.xcworkspace -s youproject -o ~/Desktop/youproject.ipa

from optparse import OptionParser
import subprocess

# 需要改动的地方 (根据自己的项目信息改动改动)
PROJECT_NAME = "AutoBuildProject"  #项目名称
VERSION = "1.0.0"  #打包版本号 会根据不同的版本创建文件夹（与项目本身的版本号无关）

CONFIGURATION = "Release"  #Release 环境  Debug 环境
# CONFIGURATION = "Debug"   

TAGREAT_NAME = "%s" %(PROJECT_NAME) #scheme 就是对应的target
TAGREAT_NAME = "AutoBuildProject2"

PROFILE = "AdHoc" #配置文件分为三种 AdHoc  Dev  AppStore 分别对应三总配置文件

OUTPUT = "./Packge/%s" %(CONFIGURATION)  #打包导出ipa文件路径（请确保 “%s” 之前的文件夹正确并存在）


WORKSPACE = "%s.xcworkspace" %(PROJECT_NAME)
PROJECT = "%s.xcodeproj" %(PROJECT_NAME)

#如果在项目中没有用到 pod 请注释掉此行
# PROJECT = None


#蒲公英上传
OPEN_PYUPLOAD = False  #是否开启蒲公英上传功能  True  False
USER_KEY = "******************"
API_KEY = "******************"

SDK = "iphoneos"

#启动打印函数
def printStart():
    print "*****************************************************************"
    print "*****************************************************************"
    print "**                        开始打包                             **"
    print "*****************************************************************"
    print "*****************************************************************"

#结束打印函数
def printEnd():
    print "*****************************************************************"
    print "*****************************************************************"
    print "**                        结束打包                             **"
    print "*****************************************************************"
    print "*****************************************************************"

#清除 build 目录
def cleanBuildDir(buildDir):
    cleanCmd = "rm -r %s" %(buildDir)
    process = subprocess.Popen(cleanCmd, shell = True)
    process.wait()
    print "***************cleaned buildDir*********************\n %s \n*******************************************" %(buildDir)

#创建路径
def createDir(ipaDir):
    createCmd = "mkdir %s" %(ipaDir)
    process = subprocess.Popen(createCmd, shell = True)
    process.wait()
    print "***************create Dir*********************\n %s \n*******************************************" %(ipaDir)

def uploadPgy(ipaPath):
    print "\n***************开始上传到蒲公英*********************\n"
    uploadCmd = 'curl -F \"file=@%s\" -F \"uKey=%s\" -F \"_api_key=%s\" https://www.pgyer.com/apiv1/app/upload' %(ipaPath, USER_KEY, API_KEY)
    process = subprocess.Popen(uploadCmd, shell = True)
    process.wait()
    print "\n\n***************上传结束 Code=0 为上传成功*********************\n"


#打包project
def buildProject(project, scheme, output):

    buildCmd = 'xcodebuild archive -project %s -scheme %s -sdk %s -configuration %s  ONLY_ACTIVE_ARCH=NO -archivePath ./build/%s.xcarchive' %(project, scheme, SDK, CONFIGURATION,PROJECT_NAME)
    process = subprocess.Popen(buildCmd, shell = True)
    process.wait()
    print "*************************buildProject*******************************\n %s \n********************************************************" %(buildCmd)

    createDir(OUTPUT)
    createDir(OUTPUT+"/"+VERSION)

    signCmd = 'xcodebuild -exportArchive -archivePath ./build/%s.xcarchive -exportPath %s/%s/%s_%s_%s -exportOptionsPlist ./AutoBuild/plist/%s.plist' %(PROJECT_NAME, output, VERSION,PROJECT_NAME,VERSION,CONFIGURATION,PROFILE)
    process = subprocess.Popen(signCmd, shell = True)
    process.wait()
    print "*************************signCmd*******************************\n %s \n********************************************************" %(signCmd)
    
    ipaPath = "%s/%s/%s_%s_%s/%s.ipa" %(output, VERSION,PROJECT_NAME,VERSION,CONFIGURATION,TAGREAT_NAME)

    if OPEN_PYUPLOAD == True:
        uploadPgy(ipaPath)
    
    cleanBuildDir("./build")

#打包workspace
def buildWorkspace(workspace, scheme, output):

    buildCmd = 'xcodebuild archive -workspace %s -scheme %s -sdk %s -configuration %s  ONLY_ACTIVE_ARCH=NO -archivePath ./build/%s.xcarchive' %(workspace, scheme, SDK, CONFIGURATION, PROJECT_NAME)
    process = subprocess.Popen(buildCmd, shell = True)
    process.wait()
    print "*************************buildWorkspace*******************************\n %s \n********************************************************" %(buildCmd)

    createDir(OUTPUT)
    createDir(OUTPUT+"/"+VERSION)

    signCmd = 'xcodebuild -exportArchive -archivePath ./build/%s.xcarchive -exportPath %s/%s/%s_%s_%s -exportOptionsPlist ./AutoBuild/plist/%s.plist' %(PROJECT_NAME, output, VERSION,PROJECT_NAME,VERSION,CONFIGURATION,PROFILE)
    process = subprocess.Popen(signCmd, shell = True)
    process.wait()
    print "*************************signCmd*******************************\n %s \n********************************************************" %(signCmd)

    ipaPath = "%s/%s/%s_%s_%s/%s.ipa" %(output, VERSION,PROJECT_NAME,VERSION,CONFIGURATION,TAGREAT_NAME)

    if OPEN_PYUPLOAD == True:
        uploadPgy(ipaPath)

    cleanBuildDir("./build")

#打包
def xcbuild(options):
    project = options.project
    workspace = options.workspace
    scheme = options.scheme
    output = options.output

    printStart()

    if project is None and workspace is None:
        pass
    elif project is not None:
        buildProject(project, scheme, output)
    elif workspace is not None:
        buildWorkspace(workspace, scheme, output)

    printEnd()


def main():



    parser = OptionParser()
    parser.add_option("-w", "--workspace", default=WORKSPACE, help="Build the workspace test.xcworkspace.")
    parser.add_option("-p", "--project", default=PROJECT, help="Build the project test.xcodeproj.")
    parser.add_option("-s", "--scheme", default=TAGREAT_NAME, help="Build the scheme specified by schemename. Required if building a workspace.")
    parser.add_option("-o", "--output", default=OUTPUT, help="specify output filename")

    (options, args) = parser.parse_args()

    print "options: %s, args: %s" % (options, args)

    xcbuild(options)

if __name__ == '__main__':
    main()
