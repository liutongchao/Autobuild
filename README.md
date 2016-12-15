# Autobuild

###自动打包环境
Xcode 必须为 Xcode 8.0 以上 （因为8.0整合了证书配置，大大简化了配置文件的配置）

###集成自动打包功能
#####1. 把开源文件 `Resource` 中的三个文件拉到项目根目录中

![Resource](http://upload-images.jianshu.io/upload_images/1951020-44b8e54572494d6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![根目录文件](http://upload-images.jianshu.io/upload_images/1951020-6677b62676f3c30e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


 `autobuild.py` 为一个 Python 脚本，是实现自动打包的主要文件。
`AutoBuild` 文件夹存放着三种配置文件的plist。
`Packge` 为自动打包后 `ipa` 文件的输出路径，默认为这个可根据自己需要改动。

#####2. 用 Xcode 打开 `autobuild.py` 文件，修改里面的配置信息。

    # 需要改动的地方 (根据自己的项目信息改动改动)
    PROJECT_NAME = "Name" 			    	#项目名称
    VERSION = "1.0.0"  						#打包版本号 会根据不同的版本创 建文件夹（与项目本身的版本号无关）
    TAGREAT_NAME = "%s" %(PROJECT_NAME) 	#就是对应的target

    CONFIGURATION = "Release" 				#Release 环境  Debug 环境
    PROFILE = "Dev" 						#配置文件分为四种 AdHoc  Dev  AppStore  Ent 分别对应四种配置文件
    OUTPUT = "./Packge/%s" %(CONFIGURATION) #打包导出ipa文件路径（请确保 “%s” 之前的文件夹正确并存在）

    WORKSPACE = "%s.xcworkspace" %(PROJECT_NAME)
    PROJECT = "%s.xcodeproj" %(PROJECT_NAME)
    SDK = "iphoneos"
    #注意：如果在项目中用到 pod 请启用此行！！！！！！
    #PROJECT = None

    #蒲公英上传
    OPEN_PYUPLOAD = False  	#是否开启蒲公英上传功能  True  False
    USER_KEY = "********************"
    API_KEY = "********************"

    #fir.im 上传
    OPEN_FIR_UPLOAD = True  	#是否开启fir.im上传功能  True  False

    #AppStore上传
    OPEN_APPSTORE_UPLOAD = False  #是否开启AppStore上传上传功能  True  False
    USER_NAME = "***************"
    USER_PASSWORD = "***************"

`PROJECT_NAME `   就是你项目工程的名字
`VERSION`  打包版本号 会根据不同的版本创建文件夹（与项目本身的版本号无关）
`CONFIGURATION` Release 环境  Debug 环境
`TAGREAT_NAME `  就是target名（如果项目有多个target那么要指定target，如果只有一个target 则不用修改）
`PROFILE` 配置文件分为四种 AdHoc  Dev  AppStore Ent 分别对应四种配置文件
`OUTPUT` 打包导出ipa文件路径，比如想导出到桌面上就把“./Packge/” 替换成 “/Users/`用户名`/Desktop/”（请确保 “%s” 之前的文件夹正确并存在）
`PROJECT = None`   如果你的工程是以 `.xcworkspace` 运行的，请启用此行!!!
`OPEN_PYUPLOAD ` 蒲公英应用托管上传，默认为False，如果需要上传请设置为True，并填入蒲公英账号的 USER_KEY 和  API_KEY。
`OPEN_FIR_UPLOAD ` Fir.im上传，需要自己配置fir-cli,后面会有相关资料，如何配置fir-cli
`OPEN_APPSTORE_UPLOAD ` AppStore自动上传，默认为False，如果需要上传到AppStore，请设置为True，并填入开发者账号 和 密码。
> ######注意： `PROJECT = None` 如果你的工程是以 `.xcworkspace` 运行的，请启用此行!!!

#####3. 确保你的项目已经启用自动签名功能，并能够在真机上运行。
启动自动签名：TARGETS -> General 

![自动签名配置](http://upload-images.jianshu.io/upload_images/1951020-6acc880361cf1872.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####4. 运行脚本
运行脚本有两种方式（建议用第二种方式）
①. 打开终端，cd 到你的项目根目录下，然后把 `autobuild.py` 拖入终端里，再回车，神奇的事即将发生。

![把脚本文件拖进终端里](http://upload-images.jianshu.io/upload_images/1951020-3107cae9b4c7171b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


②. 把资源中名为 `Python Launcher` 的小应用拉到 `应用程序` 中，然后找到项目根目录中的 `autobuild.py` 文件。
右键 -> 打开方式 -> Python Launcher

![ Python Launcher](http://upload-images.jianshu.io/upload_images/1951020-40c9b9ba81fb526a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![右键 -> 打开方式 -> Python Launcher](http://upload-images.jianshu.io/upload_images/1951020-9abef0737df8114b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####5. 运行结果

![最终打包结果](http://upload-images.jianshu.io/upload_images/1951020-bc90935fb363e8df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如图出现 `** EXPORT SUCCEEDED **` 即打包成功，赶紧去`Packge` 文件夹看看吧。
如果出现了错误，请检查一下配置信息有没有错误。

###ipa上传
>目前支持三种上传方式，分别为：蒲公英、Fir.im、AppStore

######1.蒲公英上传
①需要先到蒲公英申请账号，拿到两个Key,`USER_KEY`  和 `API_KEY`
②打开上传开关，并填入上述两个key。

    OPEN_PYUPLOAD = True  	#是否开启蒲公英上传功能  True  False
    USER_KEY = "************"
    API_KEY = "************"

######2. Fir.im上传
①需要先到Fir.im申请账号，拿到 `API  Token`
②配置本地 fir-cli 环境
>参考配置资料：[https://github.com/FIRHQ/fir-cli](https://github.com/FIRHQ/fir-cli)
######请务必先配置好本地 fir-cli 环境，否则无法上传成功！！

③打开上传开关

     OPEN_FIR_UPLOAD = True  	#是否开启fir.im上传功能  True  False

######3. AppStore上传
①打开开关，填入开发者账号和密码。

    OPEN_APPSTORE_UPLOAD = True  #是否开启AppStore上传上传功能  True  False
    USER_NAME = "************"
    USER_PASSWORD = "************"

###集成问题向导
1. 请仔细检查脚本中的配置是否有误。
    特别是下面这一行，如果用了 Pod 请启用这一行

        PROJECT = None
2. 确保有`Xcode` 的自带工具 `Command Line Tools` ，如果没有请执行如下命令安装。

        xcode-select --install
3. 确保 `Xcode 8` 在应用程序里，而不是把 `Xcode 8` 装在其他地方。
4. 如使用AppStore上传功能，请确保手动上传AppStore不出现错误。
   若出现上传成功，但在 iTunes Connect 中显示包无效，一般是隐私权限问题，需在 info.plist 里添加权限。（相机、麦克风、照片等）
5. 如果上传蒲公英时失败，出现 `curl: (26) couldn't open file "~/Desktop` 错误，请替换路径“~/Desktop” 为 “/Users/`用户名`/Desktop/” 。

#详细信息请查看博客
###[http://www.jianshu.com/p/902c04429179](http://www.jianshu.com/p/902c04429179)
