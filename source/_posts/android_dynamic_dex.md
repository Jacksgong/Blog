title: Android 动态加载dex
date: 2015-12-07 00:48:03
updated: 2015-12-07 00:48:03
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483667&idx=1&sn=5e4cc3bd07e81efa41fbfce25f4a6bd3
wechatmptitle: Android动态加载dex
permalink: 2015/12/07/android_dynamic_dex/
categories:
- Android机制
tags:
- Android
- dex
- gradle
- ant
- ClassLoader
- 安全

---

> 首先如果仅仅是因为64K method的问题可以直接看这里[DexGuard、Proguard、Multi-dex](http://blog.dreamtobe.cn/2015/11/04/guard_multi_dex/)给出的解决方案。

> 本文主要讨论从编译层面，dex动态加载器选择层面以及安全层面讨论dex动态加载

<!-- more -->

---

## I. 类加载器

比较两个类是否相等: 前提是采用的是同样的加载器加载的，否则必不相等。

### 一般加载器类别

#### 虚拟机的角度

##### 1. 启动类加载器(Bootstrap ClassLoader)

使用C++语言实现，虚拟机自身的一部分。

##### 2. 其他的类加载器

使用Java语言实现，独立于JVM外部，全部继承自类`java.lang.ClassLoader`。

#### 开发人员角度

##### 1. 启动类加载器(Bootstrap ClassLoader)

- **层级**: native层实现。
- **负责加载**: `JAVA_HOME\lib`目录中能被JVM识别的类库加载到JVM内存中(名称不符合的类库不会被加载)(java的核心类，如 `java.lang`、`java.util`等，是java运行时环境所需类的一部分, 如果是Android，还会加载Android sdk层，如`TextUtils`, `TextView`等)。
- **使用关系**: 无法被Java程序直接引用。

##### 2. 扩展类加载器(Extersion ClassLoader)

- **负责加载**: `JAVA_HOME\lib\ext`目录中的类库(继承自java核心类的类)。
- **使用关系**: 可以被开发者直接使用。

##### 3. 应用程序类加载器(Application ClassLoader)

> 系统类加载器。

- **负责加载**: 用户类路径(Classpath)上所指定的类库。Android中大多数的应用中的类(从odex中加载出来的类: 如 MainActivity、自定义View、XXXApplication)。
- **使用关系**:  可以被开发者直接使用。
- **备注**: 一般是应用程序默认的类加载器。

### 特性

#### 什么是双亲委派模型?

一个类收到了类加载请求，会将请求先委派给父类加载，每层皆如此，因此所有的类加载是从上而下的，只有上层无法加载了才到下层加载。

参考`ClassLoader`中给出的解释:

```
Loads the class with the specified name, optionally linking it after loading. The following steps are performed:
1. Call findLoadedClass(java.lang.String) to determine if the requested class has already been loaded.
2. If the class has not yet been loaded: Invoke this method on the parent class loader.
3. If the class has still not been loaded: Call findClass(java.lang.String) to find the class.
```

#### 为什么要遵循双亲委派模型?

为了保证所加载的类的唯一性，保证相同的类只会被一个加载器所加载。也保证了一个类不会被多个加载器加载到JVM中，导致同一个类在JVM被不同的加载器加载多次。

#### Dalvik虚拟机的类加载器与其他Java虚拟机的不同?

一般的Java虚拟机，是自定义继承自`ClassLoader`的类加载器，然后通过`defineClass`方法从二进制流中加载Class，或者从Class文件中读取。而Dalvik虚拟机是阉割以及修改过的，无法从二进制流中加载，Dalvik只识别dex文件，因此我们能加载的只是dex文件或包含dex文件的`.jar`或`.apk`。

#### 其他梗

- 当java源码被编译为binary class时，编译器会插入一个静态常量`final static java.lang.Class class`，因为任意类我们都可以通过`.class`获得当前类的`java.lang.Class`。
- java中的静态对象是attach到对应的class上面的，也就是attach在该class的`ClassLoader`上面的，当`ClassLoader`被unload的时候，如果再次访问该静态对象，就是一个全新的静态对象在一个新的`ClassLoader`上了。
- 可以通过`Class.getClassLoader()`来获得该类的`ClassLoader`。

## II. Android 动态加载Dex的方式

![](/img/android_dynamic_dex.png)

### DexFile

Android中的这几种类加载器实际是依赖`DexFile`的，对于`DexFile`有以下两点:

1. 打开的DEX文件不会直接存储在`DexFile`对象中，而是存储在对于虚拟机只读的memory-mapped上。
2. 我们无法直接调用`DexFile.loadClass`进行对dex的加载，只能通过ClassLoader进行加载。

案例参考:

- `PathClassLoader`的使用案例推荐参考: [secondary-dex-gradle/.../secondarydex/plugin/](https://github.com/creativepsyco/secondary-dex-gradle/tree/master/app/src/main/java/com/github/creativepsyco/secondarydex/plugin)
- `DexClassLoader`的使用案例推荐参考: [Custom Class Loading in Dalvik](http://android-developers.blogspot.hk/2011/07/custom-class-loading-in-dalvik.html)，如果你有网络下载dex动态打补丁的需求的话。

## III. 编译层面实现打指定独立dex

### Ant

可以参考[这里](http://android-developers.blogspot.hk/2011/07/custom-class-loading-in-dalvik.html)后面的`Build Process`。

### Gradle

在编译层面将指定的module拆分出来打包成dex放入assets中，完全可以参考这个方案: [secondary-dex-gradle/app/build.gradle](https://github.com/creativepsyco/secondary-dex-gradle/blob/master/app/build.gradle)

> 如果不理解的可以看我fork的，我添加了中文注解: [Jacksgong/secondary-dex-gradle/app/build.gradle](https://github.com/Jacksgong/secondary-dex-gradle/blob/master/app/build.gradle)

## IV. 安全性讨论

### 动态加载Dex的安全性主要存在两方面:

1. 存储dex的文件暴露在其他应用可读写的目录下。
2. 加载外部dex的时候没有做好完整的安全性校验。


### 解决方案

1. 尽量将dex放到当前应用的私有目录下，保证只有当前应用uid可以读甚至写(一般就只有`Context.getFileDir()`/ `Context.getDir(String, MODE_PRIVATE)` / `Context.getCacheDir()`)，这方面目录相关知识可以参看: [Android中尽量不用Storage Permission](http://blog.dreamtobe.cn/2015/11/30/android_storage_permission/)
2. 对从服务端下载或者外部加载的dex，做校验（对文件进行哈希值校验等）。
3. 将dex文件加密，通过JNI将解密代码写在Native层，解密之后通过`defineClass`指定路径加载完成后，删除解密后文件。

---

- [Custom Class Loading in Dalvik](http://android-developers.blogspot.hk/2011/07/custom-class-loading-in-dalvik.html)
- [Custom Class Loading in Dalvik with Gradle (Android New Build System)](http://stackoverflow.com/questions/18174022/custom-class-loading-in-dalvik-with-gradle-android-new-build-system)
- [外部动态加载DEX安全风险浅析](http://jaq.alibaba.com/blog.htm?id=63)
- [creativepsyco/secondary-dex-gradle](https://github.com/creativepsyco/secondary-dex-gradle)
- [Android类动态加载技术](http://www.blogjava.net/zh-weir/archive/2011/10/29/362294.html)
- [JVM学习笔记（八）：类加载器以及双亲委派模型介绍](http://chenzhou123520.iteye.com/blog/1601319)
- [Java Class Loader](http://javapapers.com/core-java/java-class-loader/)

---
