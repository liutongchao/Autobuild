# Autobuild

###集成自动打包功能
#####1. 把开源文件 `Resource` 中的三个文件拉倒项目根目录中

![Resource](http://upload-images.jianshu.io/upload_images/1951020-44b8e54572494d6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![根目录文件](http://upload-images.jianshu.io/upload_images/1951020-6677b62676f3c30e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


 `autobuild.py` 为一个 Python 脚本，是实现自动打包的主要文件。
`AutoBuild` 文件夹存放着三种配置文件的plist。
`Packge` 为自动打包后 `ipa` 文件的输出路径，默认为这个可根据自己需要改动。

#####2. 用 Xcode 打开 `autobuild.py` 文件，修改里面的配置信息。

![修改配置信息](http://upload-images.jianshu.io/upload_images/1951020-a0a56799c0b4cb0e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`APPNAME`   就是你项目工程的名字
`VERSION`  打包版本号 会根据不同的版本创建文件夹（与项目本身的版本号无关）
`CONFIGURATION` Release 环境  Debug 环境
`SCHEME` scheme 就是对应的target（如果项目有多个target那么要指定target，如果只有一个target 则不用修改）
`PROFILE` 配置文件信息分为三种 AdHoc  Dev  AppStore 分别对应三种配置文件
`OUTPUT` 打包导出ipa文件路径（请确保 “%s” 之前的文件夹正确并存在）

######最后一个 `PROJECT = None` 如果你的工程是以 `.xcworkspace` 运行的，请启用此行!!!



#####3. 确保你的项目已经启用自动签名功能，并能够在真机上运行。
启动自动签名：TARGETS -> General 

![自动签名配置](http://upload-images.jianshu.io/upload_images/1951020-6acc880361cf1872.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####4. 运行脚本
打开终端，cd 到你的项目根目录下，然后把 `autobuild.py` 拖入终端里，再回车，神奇的事即将发生。

![把脚本文件拖进终端里](http://upload-images.jianshu.io/upload_images/1951020-3107cae9b4c7171b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####5. 运行结果

![最终打包结果](http://upload-images.jianshu.io/upload_images/1951020-bc90935fb363e8df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如图出现 `** EXPORT SUCCEEDED **` 即打包成功，赶紧去`Packge` 文件夹看看吧。
如果出现了错误，请检查一下配置信息有没有错误。

#详细信息请查看博客
###[http://www.jianshu.com/p/902c04429179](http://www.jianshu.com/p/902c04429179)
