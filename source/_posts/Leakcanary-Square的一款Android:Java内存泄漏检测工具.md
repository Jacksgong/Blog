title: Leakcanary Square的一款Android/Java内存泄漏检测工具
date: 2015-05-12 08:35:03
updated: 2015-05-12 08:35:03
permalink: 2015/05/12/Leakcanary-Square的一款Android/:Java内存泄漏检测工具
categories:
- Android内存
tags:
- Square
- 内存泄漏
- Android
- 优化

---

> git地址: [square/leakcanary](https://github.com/square/leakcanary)

# git readme:

**中文翻译[@Jacksgong](https://github.com/Jacksgong/leakcanary)**

> 一款Android与Java的内存检测库

> "A small leak will sink a gret ship." - Benjamin Franklin

<!--more-->

![](https://raw.githubusercontent.com/Jacksgong/leakcanary/master/assets/screenshot.png)

## I. 开始

`build.gradle` 中的配置:

```
dependencies {
   debugCompile 'com.squareup.leakcanary:leakcanary-android:1.3'
   releaseCompile 'com.squareup.leakcanary:leakcanary-android-no-op:1.3'
 }
```

`Application` class 中的配置:

```
public class ExampleApplication extends Application {

  @Override public void onCreate() {
    super.onCreate();
    LeakCanary.install(this);
  }
}
```

**这样就可以了!** 在debug包中activity内存泄漏将会被监听到，并且将会自动显示一个通知(show a notification)。


## II. 为什么要使用LeakCanary?

好问题! 我们已经在 [博客文章](http://squ.re/leakcanary)中回答了这个问题。

## III. 应该怎么使用它呢？

使用`RefWatcher`来监听引用是否已经被GC:

```
RefWatcher refWatcher = {...};

// We expect schrodingerCat to be gone soon (or not), let's watch it.
// 我们预测shcrodingerCat很快会销毁(也许不会)，这里监听了它.
refWatcher.watch(schrodingerCat);
```
`LeakCanary.install()`会返回预设的`RefWatcher`，并且安装了一个`ActivityRefWatcher`来监听activity调用了`Activity.onDestroy()`以后的泄漏。

```
public class ExampleApplication extends Application {

  public static RefWatcher getRefWatcher(Context context) {
    ExampleApplication application = (ExampleApplication) context.getApplicationContext();
    return application.refWatcher;
  }

  private RefWatcher refWatcher;

  @Override public void onCreate() {
    super.onCreate();
    refWatcher = LeakCanary.install(this);
  }
}
```
你也可以使用`RefWatcher`来监听fragment的泄漏:

```
public abstract class BaseFragment extends Fragment {

  @Override public void onDestroy() {
    super.onDestroy();
    RefWatcher refWatcher = ExampleApplication.getRefWatcher(getActivity());
    refWatcher.watch(this);
  }
}
```

## IV. LeakCanary是如何工作的呢?

1. `RefWatcher.watch()`创建了一个[`KeyedWeakReference`](https://github.com/square/leakcanary/blob/master/library/leakcanary-watcher/src/main/java/com/squareup/leakcanary/KeyedWeakReference.java)到了监控的对象。
2. 之后，在后台线程，它检查引用是否已经被释放，如果没有它将促发一次GC。
3. 如果引用依然没有被释放，它会导出heap到存储在app文件系统的`a.hprof`文件。
4. `HeapAnalyzerService`在单独的一个进程被启动，并且`HeapAnalyzer`使用[`HAHA`](https://github.com/square/haha)来解析heap。
5. `HeapAnalyzer`由于采用了单独的reference key，在heap dump中找到了`KeyedWeakReference`并且定位到泄漏的引用。
6. `HeapAnalyzer`通过计算出到GC根部最短路径的强引用来决定是否这里是泄漏了，并且建立导致泄漏的引用关系链。
7. 结果将传回在app进程的`DisplayLeakService`，并且显示泄漏通知。

## V. 我应该如何拷贝leak trace呢？

可以在Logcat中看到leak trace:

```
In com.example.leakcanary:1.0:1 com.example.leakcanary.MainActivity has leaked:
* GC ROOT thread java.lang.Thread.<Java Local> (named 'AsyncTask #1')
* references com.example.leakcanary.MainActivity$3.this$0 (anonymous class extends android.os.AsyncTask)
* leaks com.example.leakcanary.MainActivity instance

* Reference Key: e71f3bf5-d786-4145-8539-584afaecad1d
* Device: Genymotion generic Google Nexus 6 - 5.1.0 - API 22 - 1440x2560 vbox86p
* Android Version: 5.1 API: 22
```

也可以从**action bar menu**分享leak trace与heap dump文件。

## VI. 应该如何解决内存泄漏呢?

一旦拥有了leak trace，就可以分析出哪个路径中的引用不应该存在，然后分析出引用依然存在的原因。通常情况是注册的监听没有反注册，或者是`close()`方法没有调用，或者是一个未知的类((通常也是没有句柄的对象，就纯new出来执行了某方法)hold住了外部类的引用。如果你分析不出你代码中的问题，别放弃，可以在[Stack Overflow question](http://stackoverflow.com/questions/tagged/leakcanary)(使用`leakcanary` 标签)中创建相关问题。

## VII. 我的泄漏是因为执行Android SDK导致的！

随着时间的推移，已经有一些已知的由于Android SDK的执行导致的内存泄漏得到了作为生厂商AOSP的修复。当发生这样的内存泄漏的时候，其实我们作为应用开发者能做的很少。对于这样的问题，LeakCanary已经有内建了一个忽略已知Android SDK泄漏的列表: [`AndroidExcludedRefs.java`](https://github.com/square/leakcanary/blob/master/library/leakcanary-android/src/main/java/com/squareup/leakcanary/AndroidExcludedRefs.java)。如果你发现了新的，请提供leak trace、reference key、设备版本与Android版来[创建问题](https://github.com/square/leakcanary/issues/new)，当然如果能够提供一个heap dump的文件连接更好。

这对于**新发布的Android**来说是特别重要的，你有机会能够帮助尽早发现新的内存泄漏，使整个Android社区受益。

开发版本的快照: [Sonatype's `snapshots` repository](https://oss.sonatype.org/content/repositories/snapshots/)。

## VIII. 超出leak trace范围

通常leak trace是不够的，还需要通过[MAT](http://eclipse.org/mat/)或者[YourKit](https://www.yourkit.com/)来深挖heap dump，下面是你如何通过heap dump来找出泄漏:

1. 找到`com.squareup.leakcanary.KeyedWeakReference`所有的实例。
2. 对于每个实例，查看它的`key`成员变量。
3. 找到包含与LeakCanary报出的reference key相同`key`成员变量的`KeyedWeakReference`。
4. 那么这个`KeyedWeakReference`中的`reference`成员变量，就是你泄漏了的对象。
5. 到此为止，剩余的工作就是，开始查找到GC Roots最短路径(不包含弱引用)。

## IX. 定制

### 图标与标注(Icon and Label)

`DisplayLeakActivity`默认是使用默认的图标与标注，当然你可以通过在你的app中提供`R.drawable.__leak_canary_icon`与`R.string.__leak_canary_display_activity_label`来定制这个:

```
res/
  drawable-hdpi/
    __leak_canary_icon.png
  drawable-mdpi/
    __leak_canary_icon.png
  drawable-xhdpi/
    __leak_canary_icon.png
  drawable-xxhdpi/
    __leak_canary_icon.png
  drawable-xxxhdpi/
    __leak_canary_icon.png
```

```
<?xml version="1.0" encoding="utf-8"?>
<resources>
  <string name="__leak_canary_display_activity_label">MyLeaks</string>
</resources>
```

### 存储leak traces

`DisplayLeakActivity`最多在app目录中存储7个heap dumps与leak traces 文件。你可以通过在你的app中提供`R.integer.__leak_canary_max_stored_leaks`来定制这个:

```
<?xml version="1.0" encoding="utf-8"?>
<resources>
  <integer name="__leak_canary_max_stored_leaks">20</integer>
</resources>
```

### 上传到服务器

可以通过修改默认的行为来上传leak trace与heap dump到指定的服务器。

创建一个你自己的`AbstractAnalysisResultService`。最简单的方法是在debug的app中继承`DefaultAnalysisResultService`:

```
public class LeakUploadService extends DefaultAnalysisResultService {
  @Override protected void afterDefaultHandling(HeapDump heapDump, AnalysisResult result, String leakInfo) {
    if (!result.leakFound || result.excludedLeak) {
      return;
    }
    myServer.uploadLeakBlocking(heapDump.heapDumpFile, leakInfo);
  }
}
```

要确认发布的Application类使用无效的`RefWatcher`:

```
public class ExampleApplication extends Application {

  public static RefWatcher getRefWatcher(Context context) {
    ExampleApplication application = (ExampleApplication) context.getApplicationContext();
    return application.refWatcher;
  }

  private RefWatcher refWatcher;

  @Override public void onCreate() {
    super.onCreate();
    refWatcher = installLeakCanary();
  }

  protected RefWatcher installLeakCanary() {
    return RefWatcher.DISABLED;
  }
}
```

在你debug的Application类中创建一个自定义的`RefWatcher`:

```
public class DebugExampleApplication extends ExampleApplication {
  protected RefWatcher installLeakCanary() {
    return LeakCanary.install(app, LeakUploadService.class);
  }
}
```

不要忘了在debug的manifest里面注册service:

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    >
  <application android:name="com.example.DebugExampleApplication">
    <service android:name="com.example.LeakUploadService" />
  </application>
</manifest>
```

你也可以上传leak traces到Slack或者HipChat，[这里是一个例子](https://gist.github.com/pyricau/06c2c486d24f5f85f7f0)

![](https://raw.githubusercontent.com/Jacksgong/leakcanary/master/assets/icon_512.png)

**LeakCanary** 名称是为了表达[canary in a coal mine](http://en.wiktionary.org/wiki/canary_in_a_coal_mine)，因为LeakCanary是通过提供危险预警，检测风险的哨兵，维护者[@edenman](https://github.com/edenman)提的建议!

## X. License

```
Copyright 2015 Square, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---
