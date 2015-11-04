title: DexGuard、Proguard、Multi-dex
date: 2015-11-04 19:26:03
tags:
- Android
- Build
- Proguard
- Gradle
- DexGuard
- Multi-Dex

---

> Proguard与DexGuard是同一团队开发的

## I. 区别表

Proguard | DexGuard | 备注
-|-|-
免费 | 收费 | [DexGuard GuardSquare](https://www.guardsquare.com/dexguard)
一般代码混淆 | 代码混淆力度更大 + 资源混淆 + so加壳等
不需要multi-dex | 自带multi-dex扫描

<!-- more -->

#### 资源混淆?
首先， 所有static final的都会直接预编译，代码中都是资源ID，资源混淆只和 **resources.arsc** (资源ID、string、路径映射等)、**资源路径**、**资源文件名** 有关。

#### 资源混淆可能的坑?:

Resources#getIdentifier估计废了，记得白名单。

#### Proguard也想要资源混淆?:

试试这个: [AndResGuard](https://github.com/shwenzhang/AndResGuard)

#### 为啥国内很少用DexGuard?有坑?

- 付费
- 国内文档少，而且配置起来会比Proguard复杂一些，细节多些。
- 由于需要做非常重度的混淆，因此由自带multi-dex，更多细节问题
- 第三方库用该混淆可能会有难以预料的坑，特别是国内的，基本上保证Proguard没有问题给出文档，Dexguard基本都没有测试过(比如以前使用这个木有关注到umeng既然有些资源采用反射取，官方也没有给明，完全是盲人摸象等)

## II. Multi-dex

#### 为啥有这梗

> 可以先参看: [ART、Dalvik](http://blog.dreamtobe.cn/2015/11/01/android_art_dalvik/)

用Dalvik虚拟机的Android手机，在安装app的时候，会有一个优化dex的过程，使用dexopt将dex优化的更加高效于运行存储为odex，但是dexopt把每个类的方法id检索的链表长度使用的short（为了效率？木有考虑到？），无论如何，就导致了如果一个dex中的方法数超过了65535就跪了，so...

> 以下针对Gradle multi-dex说明

#### 配置

Gradle:

```
...
android {

    ...
    defaultConfig {
        ...
        // Enabling multidex support.
        multiDexEnabled true
    }
    ...
}
dependencies {
  compile 'com.android.support:multidex:1.0.0'
}
```

AndroidManifest.xml:

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.android.multidex.myapplication">
    <application
        ...
        android:name="android.support.multidex.MultiDexApplication">
        ...
    </application>
</manifest>
```

#### 优化

##### 问题1:
由于multidex配置需要编译系统复杂的处理引用关系来判断哪些需要在主dex，哪些需要在次dex，因此势必会增加日常编译的耗时

##### 解决方法:
可以创建两个variations用于gradle编译，定义在`productFlavors`，一个定义最低sdk到21(由于ART不再需要运行时加载，并且其在安装时翻译的时候，会处理classes(..N).dex，因此build直接每个module一个dex不用merge不用分主次dex，每次只需要重新计算修改过的modules的dex，省去很多很多时间)，一个为发布需要的最低sdk。自己调试的时候，结合选用Debug的Type，在Build Variants中选用`devDebug`即可。

```
android {
    productFlavors {
        // Define separate dev and prod product flavors.
        dev {
            // dev utilizes minSDKVersion = 21 to allow the Android gradle plugin
            // to pre-dex each module and produce an APK that can be tested on
            // Android Lollipop without time consuming dex merging processes.
            minSdkVersion 21
        }
        prod {
            // The actual minSdkVersion for the application.
            minSdkVersion 14
        }
    }
          ...
}
```

##### 问题2:

由于Dalvik运行时加载dex，如果dex多而且大，在启动应用的时候加载其余dex的时可能会出现ANR，甚至在Android 4.0(API 14)以前的机器无法运行。

##### 解决方法:

Gradle配置

```
android {
    buildTypes{
        release {
            minifyEnabled true // 混淆时删除无用代码
            shrinkResources true // 删除混淆是标注的无用资源(res/)
            ...
        }
    ...
    }
}
```

以上两个参数，有效删除无用代码与无用资源，减小包大小。如果需要支持4.0以前的机器，做好测试工作。如果是4.0以上的机器，可以考虑再AndroidManifest中配置`largeHeap=true`，一般来说java heap可以扩容到50%以上，具体看不同机器的配置(`/system/build.prop`)。

---

- [[Android] Proguard And DexGuard](http://blog.csdn.net/arui319/article/details/18360147)
- [Building Apps with Over 65K Methods](https://developer.android.com/intl/ko/tools/building/multidex.html)
- [How to disable Dexguard?](http://stackoverflow.com/questions/27508560/how-to-disable-dexguard)
- [“minifyEnabled” vs “shrinkResources” - what's the difference? and how to get the saved space?](http://stackoverflow.com/questions/30800804/minifyenabled-vs-shrinkresources-whats-the-difference-and-how-to-get-the)
- [Gradle Plugin User Guide](http://tools.android.com/tech-docs/new-build-system/user-guide)
- [PROGUARD FOR ANDROID](https://lab.getbase.com/proguard-for-android/)
