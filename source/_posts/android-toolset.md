title: Android开发周边
date: 2017-03-16 02:23:03
categories:
- 工程师技能
tags:
- Android
- gradle
- Programing

---


{% note info %} 本文主要提到Android开发中的一些周边，不过做好Android开发，更需要在性能稳定性方面(如[单元测试](/2016/05/15/android_test/)、[开发流程](/large-project-develop/)、[内存泄露的监控](/2015/05/18/LeakCanary使用总结/)、关键页面进出时帧数的监控、[应用线程数变化的监控](https://github.com/Jacksgong/ThreadDebugger)、网络层优化、甚至是[基于Android不同虚拟机规范更好的编程习惯对性能的影响](/2015/10/26/android_optimize/))、安全方面(如如何更有效的反签名重新打包(如考虑关键ndk LoadLibrary中校验)、[nimbledroid扫描系统](https://nimbledroid.com/)、[腾讯金刚审计系统]( http://jaq.alibaba.com/)、[阿里聚安全检测]( http://jaq.alibaba.com/)等)，亦或是监控统计算法(如区间分段)、有损体验(如离线模式)等方面进行投入。{% endnote %}

<!-- more -->

## I. 开发工具

#### 1. 快速运行github项目

开源库: [cesarferreira/dryrun](https://github.com/cesarferreira/dryrun)

通过`dryrun`可以简单的通过一个github中的地址，就直接将项目运行到手机上。

#### 2. 检索引用

开源库: [cesarferreira/alfi](https://github.com/cesarferreira/alfi)

可以快速检索需要引用库的`jcenter`与`maven central`的引用代码。

#### 3. 快速反编译

开源库: [skylot/jadx](https://github.com/skylot/jadx)

很便捷的反编译工具，可对dex文件直接反编译打开: `jadx-gui classes.dex`。

#### 4. 图片压缩

除了在CI系统上保持对资源变化的持续监控(对大多数的Android应用而言，资源往往是Apk大小的主要根源之一)，别忘了对已有资源进行无损压缩(当然，如果是相对简单的图片尽可能使用矢量图(xml、vector drawable)方式，使得只要带上一个矢量图，而不需要带上多张不同dpi的图片来减少大小):

- Google刚开源的号称能够减少JPEG 35%文件大小的开源库: [google/guetzli](https://github.com/google/guetzli)
- 高效且给力的png无损压缩工具开源库: [nukesaq88/Pngyu](https://github.com/nukesaq88/Pngyu)
- 支持绝大多数图片类型多功能压缩神器ImageOptim: https://imageoptim.com/


## II. gradle小技巧

- 通过`--offline`，离线编译，免去检测的网络耗时
- 通过`gradle --stop`，停止所有的gradle编译，包括IDE中的
- 需要配置分离api、impl包可以参考开源库: [Jacksgong/gralde-sample](https://github.com/Jacksgong/gralde-sample)

#### 引用关系

可以通过 `./gradlew dependencies`来查看最终的依赖关系。

如针对项目中的`app module`进行查看其引用关系: `./gradlew :app:dependencies`。

<img src="/img/android-toolset-1.png" width="300px">

**需要特别注意**

都是对相通库同类型的引用，如都是`testCompile`，或都是`compile`，那么Gradle会自动选择最高版本的:

```groovy
compile'cn.dreamtobe.filedownloader:filedownloader-okhttp3-connection:1.0.0'
compile 'com.squareup.okhttp3:okhttp:3.6.0'
compile 'com.liulishuo.filedownloader:library:1.4.1'
```

![](/img/android-toolset-2.png)

对相同库不同类型的引用时，此时会发生冲突:

```groovy
compile'cn.dreamtobe.filedownloader:filedownloader-okhttp3-connection:1.0.0'
compile 'com.squareup.okhttp3:okhttp:3.6.0'
testCompile 'com.liulishuo.filedownloader:library:1.4.1'
```

![](/img/android-toolset-3.png)

这个时候我们就要根据需要exclude掉冲突的版本，如我们只需要引用`okhttp 3.6.0`版本与`filedownloader 1.4.1`:

```groovy
compile('cn.dreamtobe.filedownloader:filedownloader-okhttp3-connection:1.0.0') {
    exclude group: 'cn.dreamtobe.filedownloader', module: 'library'
    exclude module: 'okhttp'
}
compile 'com.squareup.okhttp3:okhttp:3.6.0'
compile 'com.liulishuo.filedownloader:library:1.4.1'

testCompile 'com.liulishuo.filedownloader:library:1.4.1'
testCompile 'com.squareup.okhttp3:okhttp:3.6.0'
```

## III. 编程工具

#### 1. 耗时日志

**hugo**

开源库: [JakeWharton/hugo](https://github.com/JakeWharton/hugo)

轻松给方法添加耗时日志:

```java
@DebugLog
public String getName(String first, String last) {/* ... */}
```

输出日志:

```java
V/Example: --> getName(first="Jake", last="Wharton")
V/Example: <-- getName [16ms] = "Jake Wharton"
```

**Pury**

开源库: [NikitaKozlov/Pury](https://github.com/NikitaKozlov/Pury)

统计事件之间的耗时:

```
App Start --> 0ms
  Splash Screen --> 5ms
    Splash Load Data --> 37ms
    Splash Load Data <-- 1042ms, execution = 1005ms
  Splash Screen <-- 1042ms, execution = 1037ms
  Main Activity Launch --> 1043ms
    onCreate() --> 1077ms
    onCreate() <-- 1100ms, execution = 23ms
    onStart() --> 1101ms
    onStart() <-- 1131ms, execution = 30ms
  Main Activity Launch <-- 1182ms, execution = 139ms
App Start <-- 1182ms
```


#### 2. 日志着色

开源库: [JakeWharton/pidcat](https://github.com/JakeWharton/pidcat)

![](/img/android-toolset-4.png)

#### 3. 数据库网络监控

#####  3.1 Stetho - Facebook

基于Chrome DevTools十分实用便捷的数据库网络监控工具，官网: http://facebook.github.io/stetho/

官网的教程已经非常简洁明了，如查看数据库:

**首先引入基础库**

```groovy
// Gradle dependency on Stetho
dependencies {
  compile 'com.facebook.stetho:stetho:1.4.2'
}
```

**在`Application`中初始化它**

```java
public class MyApplication extends Application {
  public void onCreate() {
    super.onCreate();
    Stetho.initializeWithDefaults(this);
  }
}
```

**然后手机连接电脑，Chrome浏览器的地址栏输入`chrome://inspect`**


![][chrome-inspect]
<p style="text-align: center;"> 看到已经连接上的手机，并且看到初始化过Stetho应用的包名，点击`inspect`</p>

![][stetho-db]
<p style="text-align: center;"> 然后通过`Resources`就可以查看到数据库信息了</p>

##### 3.2 Mitmproxy

在终端中抓包HTTP/HTTPS，官网: http://docs.mitmproxy.org/en/latest/mitmproxy.html

需要注意的是HTTPS需要在手机端安装对应的证书，HTTP直接可以抓取。如果你和我一样是VI-MODE的死忠粉，那么用起来就会非常爽且高效。并且你可以通过[ustwo/mastermind](https://github.com/ustwo/mastermind)来模拟相关请求的返回，来解决联调时，前后端互等的效率问题。

这块官网的教程也十分的详尽。比如监听并抓包8889端口过来的所有HTTP请求:

下面的案例运行在OS X下

**安装**

建议直接通过Homebrew直接进行安装: `brew install mitmproxy`

**配置**

安装完成后，在用户目录下会有相关的配置目录`.mitmproxy`，打开`~/.mitmproxy/common.conf`添加监听端口为`8889`:

```
port = 8889
```

**抓包**

- 将手机与MacBook连接同一Wiki使其在同一个局域网内，然后在手机设置代理到MacBook的IP，端口为`8889`
- MacBook上，在Terminal中输入mitmproxy，此时就开始抓包所有`8889`端口代理进来的HTTP请求了

![][mitmproxy]

##### 3.3 其他

- 常见的[Charles](https://www.charlesproxy.com/download/)(收费的)，通过窗口呈现，交互非常友好，很赞的抓包软件，并且你可以通过它的`Throttle Settings`来模拟不同的网络环境
- 抓包TCP协议层的[TCPDUMP](http://www.tcpdump.org/tcpdump_man.html)，如果你需要调优网络（如检测建连、挥手、期间的各类ACK、超时重连等TCP层细节）可以考虑使用这个。如需要监听所有来往`10.15.71.165`IP的TCP: `sudo tcpdump host 10.15.71.165`

#### 4. 项目License配置

基于Android Studio的Copyright功能

**第一步. 在Copyright Profiles中添加license**

![](/img/android-toolset-5.png)

**第二步. 在Copyright中配置项目默认的license**

![](/img/android-toolset-6.png)

至此，默认创建的文件就顶部就会申明license，并且可以对文件一件添加license
![](/img/android-toolset-7.png)

当然如果需要特殊配置针对不同语言文件license格式等配置，可以在Formatting下面进一步配置。

#### 5. 查看依赖库方法数

Methods Count: http://www.methodscount.com

![](/img/android-toolset-8.png)

#### 6. UI生成器

> 如果是Material这类简单的图片，推荐使用`.svg`这样的矢量图来代替栅格化图片，以此不用考虑DPI的适配，因此只需要带一份图片，来减少包大小
> 并且在Support Library的`23.2`版本或更高版本我们可以在`ImageView`中使用`app:srcCompat`而非`android:src`使用svg来对下兼容

- [Icon/styles genrator](http://romannurik.github.io/AndroidAssetStudio/)
- [Material design icons](https://materialdesignicons.com/)
- [Color Tool](https://material.io/color): 根据选择的颜色，快速呈现效果以达到创建颜色组合、预览效果、检测不同背景下文字的可辨度。
- [Material icons](https://material.io/icons/): 这里有大量的material的Icon，并且可以直接下载`VectorDrawable`支持的SVG格式
- [Device Metrics](https://material.io/devices/): 各类设备的尺寸以及Density、DPI

除了上面几个，也可以使用Android Studio自带的:

![](/img/android-toolset-9.png)

#### 7. 包大小跟踪与对比

**包大小跟踪**

开源库: [googlesamples/apk-patch-size-estimator](https://github.com/googlesamples/apk-patch-size-estimator)

谷歌官方提供的Google Play差分包大小，也可以做简单的文件大小变更大小对比，可以集成到CI中持续跟踪包大小变化，也可以简单的对比两个包的大小:

```
New APK size on disk: 18,271,850 bytes [17.4MB]

Estimated download size for new installs:
   Full new APK (gzipped) size: 16,339,603 bytes [15.6MB]

Estimated download size for updates from the old APK, using Bsdiff:
   Bsdiff patch (gzipped) size: 2,989,691 bytes [2.85MB]

Estimated download size for updates from the old APK,
 using File-by-File:
   File-by-File patch (gzipped) size: 1,912,751 bytes [1.82MB]
```

**可视化包大小内容比较**

Android Studio Compare Apk files: https://developer.android.com/studio/build/apk-analyzer.html#compare_apk_files

通过Android Studio Compare Apk files工具进行对比

![](/img/android-toolset-10.png)

---

[本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/android-toolset.md)

---

本文已经发布到JackBlog公众号: [Android开发周边 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483721&idx=1&sn=070ac8ab054274818831a5756170b642)


---

- [Mastering the Terminal side of Android development](https://medium.com/@cesarmcferreira/mastering-the-terminal-side-of-android-development-e7520466c521#.3rz28xfsv)
- [Tracking app update sizes](https://medium.com/google-developers/tracking-app-update-sizes-1a1f57634f7b#.w1txjnwhl)
- [Resolving Conflicts in android gradle dependencies](https://blog.mindorks.com/avoiding-conflicts-in-android-gradle-dependencies-28e4200ca235#.oabd56w24)
- [WHY YOU SHOLD CARE ABOUT COPYRIGHT](http://jeroenmols.com/blog/2016/08/03/copyright/)
- [Color Tool - Material Design](https://material.io/guidelines/style/color.html#)
- [How we reduced our Android app size by 65%](https://medium.com/pregbuddy-engineering/how-we-reduced-our-android-app-size-by-65-54b17ae9a3c6)

---

  [chrome-inspect]: /img/android-toolset-chrome-inspect.png
  [stetho-db]: /img/android-toolset-stetho-db.png
  [mitmproxy]: /img/android-toolset-mitmproxy.png
