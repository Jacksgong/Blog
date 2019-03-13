title: 通过Xposed隐藏MIUI Launcher图标
date: 2019-03-14 00:07:03
updated: 2019-03-14
categories:
- Fun
tags:
- xposed
- miui

---

{% note info %} 最近总看一些看雪的东西，顺便反编译了下MiuiHome，然后隐藏了下桌面的应用，虽然是很小的场景吧，但是想想记录下，说不定对其他人有帮助呢。{% endnote %}

<!-- more -->

## 前言

开始之前呢，首先我是基于MIUI10，并且手机已经完成Root以及Xposed框架的安装了。这块就不多说了，由于我的其中一台测试机是红米Note4X，因此就是基于红米Note4X。这块的大概流程我稍微的提下:

1. 解锁BL，这个就不多说了，唯一的坑点是，MIUI的解锁程序只有Windows的
2. 解锁后，进入BL... `adb reboot bootloader`
3. 下载红米Note4X的TWRP: [这里下载](https://dl.twrp.me/mido/twrp-3.2.3-1-mido.img.html)
4. 在BL状态下，通过`fastboot flash recovery twrp-3.2.3-1-mido.img`输入TWPR，然后通过`fastboot boot twrp-3.2.3-1-mido.img`进入TWRP的Recovery，这里顺便提一句，如果你遇到类似 `FAILED (remote: 'dtb not found')` 那么很有可能是下载的TWRP存在问题
5. 在[这里](http://www.supersu.com/download)下载最新版本的SuperSu的Zip包，然后通过`adb push SuperSu.zip /sdcard/Download/`传入手机后，通过TWRP刷入，刷入后重启手机，此时已经完成Root
6. 最后下载XDA论坛提供的[这个xposedinstaller_3.1.5.apk](https://forum.xda-developers.com/showthread.php?t=3034811)，安装后给到Root权限，便可快速完成Xposed框架安装

这里顺便说下，以前有写过有关[Android Root](https://blog.dreamtobe.cn/android-root/)的浅文，感兴趣的同学也可以关注下。

## I. 反编译MiuiHome

首先小米的桌面是MiuiHome，其在`/system/priv-app/MiuiHome`目录下:

![](/img/xposed-miui-launcher-1.png)

需要注意的是，相关的code是在已经优化后的odex文件，so，dump出来，我们通过以下工具进行逆向成源码:

首先在[这里](https://bitbucket.org/JesusFreke/smali/downloads/)下载最新版本的`baksmali-x.x.x.jar`以及`smali-x.x.x.jar`。

我们通过以下指令将`MiuiHome.odex`解成`smali`:

```
java -jar baksmali-x.x.x.jar d MiuiHome.odex -o MiuiHome
```

然后我们通过以下指令将`MiuiHome`这个包含一堆`smali`的目录合并为`dex`:

```
java -jar smali-x.x.x.jar ass MiuiHome/ -o classes.dex
```

接下来就愉快了，我相信大家应该都是直接用`apktool d classes.dex`解好后，然后用`JD-GUI`打开后，然后将源码全部保存下来最后通过Studio打开来分析，各有所好吧，我个人感觉`jadx`解的更好些。

## II. 分析源码

Okay, 现在已经有源码了，肿么分析呢，全局搜下: `Log`看看这些明文的日志内容吧。

![](/img/xposed-miui-launcher-2.png)

诶... 好辣眼睛，怎么这个开发日志都没有去掉，，好吧，，可能是桌面似乎也搞不出太多幺蛾子？废话不多说，看来可以直接通过`adb logcat`看看运行时的日志输出吧，既然有现成的。

![](/img/xposed-miui-launcher-3.png)

捕捉到一条日志，可以看看这个`Launcher`做啥的，顺便在这个类上面搜索下`addApp`之类的看看:

![](/img/xposed-miui-launcher-4.png)

果然有惊喜，看来就看这个`addToAppsList`线索往下找引用关系应该很快会有思路的，不过话说回来，这代码肿么都没有混淆呢？？？？好吧不管了。继续..

顺着这条线路一直找`Launcher#bindItem`调用，然后`LauncherModel#bindItem`中调用了`Launcher#bindItem`，我们要找到的是最终哪里找到这些应用，然后给添加进来的，继续看这条线索。

`LauncherModel#loadShortcut`中调用，但是依然不是遍历调用，继续看! 居然看到 `AllAppsList#addApp`调用，看来这个`AllAppsList`肯定没跑了，我们反过来搜索对`AllAppsList`引用的。

我们发现`LauncherModel#mAllAppsList`，ok，看来都是在这里处理，看看哪里有对这个对象添加数据。发现在`LauncherModel#loadAndBindMissingIcons`有做`mAllAppsList.updatePackage`，刚好这里是个遍历。看看数据源。

这里的数据源来自`updatedPackages`，再追溯这个的赋值会发现来自`mInstalledComponents`，OK，我们看看`mInstalledComponents`的数据来源。

很快就搜索到在`LauncherModel#loadAndBindWorkspace`中通过遍历`PortableUtils.launcherApps_getActivityList(this.mContext, null, null);`的`installedApps`得到的，八九不离十了。

![](/img/xposed-miui-launcher-5.png)

我们hook下看看这个的输出结果。不用多说了，就是这个。。

## III. 编写代码进行Hook

这块就比较简单了，可以直接参看我之前写过的一篇短文: [5分钟发布一个Xposed Module](https://blog.dreamtobe.cn/xposed_module/)

不过代码相关的咱们还是稍微提下，我稍微抽象了下，请原谅我没有用驼峰，自己玩嘛，我觉得这也挺可读:

```
class MiuiHome {
    companion object {
        val packageName = "com.miui.home"

        val className_PortableUtils = "com.miui.launcher.utils.PortableUtils"
        val methodName_launcherApps_getActivityList = "launcherApps_getActivityList"
    }

}

object Launcher {
    private const val TAG = "Launcher"
    private val hideList = arrayListOf("com.xiaomi.wallet")

    fun hideIcons(lpparam: XC_LoadPackage.LoadPackageParam) {
        if (lpparam.packageName == MiuiHome.packageName) {
            ALog.d(TAG, "init for hide icon ${lpparam.packageName} ${lpparam.appInfo} ${BuildConfig.BUILD_TIME}")

            findAndHookMethod(MiuiHome.className_PortableUtils,
                lpparam.classLoader,
                MiuiHome.methodName_launcherApps_getActivityList,
                "android.content.Context",
                "java.lang.String",
                "android.os.UserHandle",
                object : XC_MethodHook() {
                    override fun afterHookedMethod(param: MethodHookParam) {
                        val list = (param.result as ArrayList<*>)
                        val toHideList = ArrayList<Any>()
                        list.forEach { info ->
                            val componentName = info!!::class.java.getDeclaredField("componentName").get(info)
                            val packageName =
                                componentName::class.java.getMethod("getPackageName").invoke(componentName) as String
                            if (hideList.contains(packageName)) {
                                toHideList.add(info)
                                ALog.d(TAG, "find $packageName so hide it!")
                            } else {
                                ALog.d(TAG, "permitted show: $packageName")
                            }
                        }

                        for (it in toHideList) {
                            list.remove(it)
                        }
                    }
                })
        }
    }
}
```

最后水一下，Xposed调试确实不是很友好，软启动有时候不会生效，也没有花时间看具体原因，就加了包的编译时间在日志，如果不是最新的就手动重启设备。后面有时间还是要看看原因，拥抱社区吧。
