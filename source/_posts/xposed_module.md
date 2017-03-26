title: 5分钟发布一个Xposed Module
date: 2017-03-26 18:36:03
categories:
- 工程师技能
tags:
- Xposed
- Xda

---


{% note info %} 本文以隐藏微信发现页面游戏中心的入口为例子，源码在这: https://github.com/Jacksgong/wechat-hunter {% endnote %}

<!-- more -->

## I. Xposed原理浅谈

> 在此之前建议通过这几篇文章简单的了解下Android简要的知识: [ART、Dalvik](https://blog.dreamtobe.cn/2015/11/01/android_art_dalvik/)、[Android GC](https://blog.dreamtobe.cn/2015/11/30/gc/)、[ActivityManagerService](https://blog.dreamtobe.cn/2015/11/26/activitymanagerservice/)

#### 常用方法

通常我们去修改其他应用的行为，要通过反编译，然后重新编译、重新签名才行。

#### Xposed做法

而Xposed是通过hook方法的方式来实现，由于Xposed修改了系统在启动时加载的Zygote进程相关的逻辑以及加载的资源(并且所有应用的启动都是从Zygote进程中拷贝出来的)，因此几乎可以架空一切安全，做所有事情，包括修改系统行为。

#### hook的大概原理

而hook方法是`XposedBridge`中的一个私有native方法`hookMethodNative`改变被hook方法的类型为native并且link方法实现到它自己的native方法中，并且对调用者透明，该native方法调用XposedBridge中的`handleHookedMethod`方法，将参数，`this`引用等传进来，之后在回调回去，这样我们就可以在方法执行前后做任何的事情了。

## I. 编写code

#### 创建空Android项目

首先创建一个空的Android项目

本文案例使用:

- compileSdkVersion: 25
- buildToolsVersion: 25.0.2
- minSdkVersion: 9
- targetSdkVersion: 25

#### 申明为Xposed module项目

在`AndroidManifest`中通过`meta-data`申明:

> - `xposeddescription`: 该模块的简要描述
> - `xposedminversion`: 最低依赖的xposed版本(这里主要看你要使用的xposed的功能在该版本之下是否已经支持)

```xml
<application android:label="WechatHunt">

    <meta-data
        android:name="xposedmodule"
        android:value="true" />
    <meta-data
        android:name="xposeddescription"
        android:value="The hunter for wechat" />
    <meta-data
        android:name="xposedminversion"
        android:value="30" />

</application>
```

### 编写自己的Xposed加载器相关

#### 1. 引入依赖

由于这些依赖库在安装了Xposed框架手机的Zygote进程上默认就已经有加载了，所以我们这边只需要保证当前写代码时候找得到依赖，并不需要打入apk包中，因此使用`provided`关键字即可，还有一个是为了我们在code中看得到Java-Doc，因此两个都引接口:

> 这里的[latest version]替换为目前最新版本，如这边文章编写的时候最新版本是82

```groovy
provided 'de.robv.android.xposed:api:[latest version]'
provided 'de.robv.android.xposed:api:[latest version]:sources'
```

#### 2. coding

- 实现`IXposedHookLoadPackage`来在应用被加载的时候生效hook方法。
- 实现好之后，创建assets目录，默认情况下是在`app/src/main/assets`
- 在assets目录中创建`xposed_init`文件
- 在`xposed_init`中申明加载器(完整的加载器路径)，如`cn.dreamtobe.xposed.wechathunt.WechatHunt`

## II. 实现隐藏游戏中心入口

下载微信，解压缩，反编译，搜索关键字:

> 反编译工具，可以参看[Android开发周边](https://blog.dreamtobe.cn/android-toolset/)中的快速反编译

![](/img/xposed-module-1.png)
![](/img/xposed-module-2.png)


找到混淆后的类名后，进行编写

```java
// 找到需要hook的类
final Class<?> pluginHelper = findClass("com.tencent.mm.ay.c", lpparam.classLoader);
// 以及需要hook的方法FZ(String)
findAndHookMethod(pluginHelper, "FZ", String.class, new XC_MethodHook() {
    // 对方法执行后进行hook
    @Override
    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
        super.afterHookedMethod(param);

        final String plugin = (String) param.args[0];
        if (plugin.equals("game")) {
            // 将返回值修改为false
            param.setResult(false);
        }
    }
});
```

## III. 发布到Xposed Module Repo

> 十分简单，没有什么需要注意的地方

1. 创建[xda developers](forum.xda-developers.com)帐号
2. 在[Xposed Module repo](http://repo.xposed.info/)中使用xda帐号登录
3. 惦记Upload new module进行上传即可

当然如果是混淆的话，即可要keep加载器，因为是在assets中申明的，如这个案例中:

```
-keep class cn.dreamtobe.xposed.wechathunt.WechatHunt{*;}
-keepnames class cn.dreamtobe.xposed.wechathunt.WechatHunt
```

---

还有任何问题欢迎评论讨论。

---

- [Development tutorial](https://github.com/rovo89/XposedBridge/wiki/Development-tutorial)
- [Replacing resources](https://github.com/rovo89/XposedBridge/wiki/Replacing-resources)
- [Xposed Module Repository](http://repo.xposed.info/)
- [Q How to Proguard / Ofuscate xposed module?](https://forum.xda-developers.com/android/help/how-to-proguard-ofuscate-xposed-module-t3153420)
- [Using the Xposed Framework API](https://github.com/rovo89/XposedBridge/wiki/Using-the-Xposed-Framework-API)

---
