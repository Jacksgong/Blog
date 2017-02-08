title: LeakCanary使用总结
date: 2015-05-18 08:35:03
permalink: 2015/05/18/LeakCanary使用总结
tags:
- LeakCanary
- 内存泄漏
- 使用
- Android
- 优化

---

## I. 使用

`build.gradle`中配置:

```
dependencies {
   debugCompile 'com.squareup.leakcanary:leakcanary-android:1.3'
   releaseCompile 'com.squareup.leakcanary:leakcanary-android-no-op:1.3'
 }
```

`Application` class中配置:

```
public class ExampleApplication extends Application {

  @Override public void onCreate() {
    super.onCreate();
    LeakCanary.install(this);
  }
}
```

## II. 初始化与原理

### 根据`build.gradle`配置:

debug包走：`com.squareup.leakcanary:leakcanary-android:1.3`
release包走: `com.squareup.leakcanary:leakcanary-android-no-op:1.3`

### 分别解析

#### release

release包，`LeakCanary.install(this)`就是返回了一个`RefWatcher#DISABLED`，而`RefWatcher#DISABLE`中返回的都是空方法。

<!--more-->

#### debug包

```
public static RefWatcher install(Application application,
      Class<? extends AbstractAnalysisResultService> listenerServiceClass) {
      // listenerServiceClass = DisplayLeakService.class
    if (isInAnalyzerProcess(application)) {
      return RefWatcher.DISABLED;
    }
    enableDisplayLeakActivity(application);
    HeapDump.Listener heapDumpListener =
        new ServiceHeapDumpListener(application, listenerServiceClass);
    RefWatcher refWatcher = androidWatcher(heapDumpListener);
    ActivityRefWatcher.installOnIcsPlus(application, refWatcher);
    return refWatcher;
  }
```

1. 如果是`HeapAnalyzerService`的进程（非app主的进程），返回一个DISABLED。否则创建一个Android默认配置的RefWatcher
2. 创建一个`Application#ActivityLifecycleCallbacks`，并且注册到当前`Application`上（由于该Api是在api 14才有的，因此低版本没有注册），主要是为了，在所有的`Activity#onDestroy`执行的最后通过调用`RefWatcher#watch(Object)`来检测`Activity`是否出现了泄漏。

#### `RefWatcher#watch(Object o)`基本原理


1. 先促发一次GC
2. 如果`o`依然存在，dump heap到本地
3. dump完成后启动`HeapAnalyzerService`服务(如果不存在)（单独进程）
4. 在`HeapAnalyzerService`中读取本地dump下来的文件，使用`HAHA`库进行分析。
5. 如果检测到内存泄漏，将结果返回给`DisplayLeakService`服务，并且显示通知

## III. 定位检测情况

### 推荐log关键字

```
leak | hprof | analysis
```

### 下面是几个案例

```
adb logcat | grep -e "leak" -e "hprof" -e "analysis"
```

![](/img/leakcanary-1.png)

![](/img/leakcanary-2.png)

![](/img/leakcanary-3.png)


## IV. 注意点

1. release千万不要带上(带no-op包)，由于GC耗时，因此会带来：安装包增加、应用onDestory由于gc带来耗时、由于新建的分析进程带来内存开销，由于大量的计算分析，带来的CPU资源的占用。
2. Android api 14以下的`LeakCanary#install(Application):RefWatcher`是不会自动注册对`Activity`的检测的，需要自己实现`BaseActivity`并且在`Activity#onDestroy`的地方主动调用`RefWatcher#watch(Object)`进行检测
3. 检测是比较慢的，其中涉及i/o，涉及大量的计算分析，通常在20s~1分钟左右，根当前cpu资源占用情况有关。

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
