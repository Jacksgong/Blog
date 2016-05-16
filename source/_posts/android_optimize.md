title: Android优化
date: 2015-10-26 00:26:03
tags:
- Android
- 优化
- JVM
- 多进程
- 典范

---

## I. 网络相关

> 更多网络优化，可参考: [Android网络](http://blog.dreamtobe.cn/2015/03/28/Android网络学习笔记整理/)

- http头信息带Cache-Control域 确定缓存过期时间  防止重复请求
- 直接用IP直连，不用域名，策略性跟新本地IP列表。 -- DNS解析过程耗时在百毫秒左右，并且还有可能存在DNS劫持。
- 图片、JS、CSS等静态资源，采用CDN（当然如果是使用7牛之类的服务就已经给你搭建布置好了）
- 全局图片处理采用漏斗模型全局管控，所请求的图片大小最好依照业务大小提供/最大不超过屏幕分辨率需要，如果请求原图，也不要超过`GL10.GL_MAX_TEXTURE_SIZE`
- 全局缩略图直接采用webp，在尽可能不损失图片质量的前提下，图片大小与png比缩小30% ~ 70%
- 如果列表里的缩略图服务器处理好的小图，可以考虑直接在列表数据请求中，直接以base64在列表数据中直接带上图片（国内还比较少，海外有些这种做法，好像web端比较常见）
- 轮询或者socket心跳采用系统`AlarmManager`提供的闹钟服务来做，保证在系统休眠的时候cpu可以得到休眠，在需要唤醒时可以唤醒（持有cpu唤醒锁）
- 可以通过将零散的网路的请求打包进行一次操作，避免过多的无线信号引起电量消耗。

<!-- more -->


#### 1. 传输数据格式选择

- 如果是基本需要全量数据的，考虑使用[Protobuffers](https://developers.google.com/protocol-buffers/?hl=zh-cn) (序列化反序列化性能高于json)
- 如果传输回来的数据不需要全量读取，考虑使用[Flatbuffers](https://github.com/google/flatbuffers) (序列化反序列化几乎不耗时，耗时是在读取对象时(就这一部分如果需要优化，可以参看[Flatbuffer Use Optimize](http://blog.dreamtobe.cn/2015/01/05/Flatbuffer-Use-Optimize/)

#### 2. 输入流
> 使用具有缓存策略的输入流

原 | 建议替换为
-|-
`InputStream` | `BufferedInputStream`
`Reader` | `BufferedReader`


## II. 数据结构

> 如果已知大概需要多大，就直接给初始大小，减少扩容时额外开销。

### 1. List

#### `ArrayList`
里面就一数组，内存小，有序取值快，扩容效率低

#### `LinkedList`
里面就一双向链表，内存大，随机插入删除快，扩容效率高。

### 2. Hash

#### `HashSet`

里面就一个`HashMap`，用key对外存储，目的就是不允许重复元素。

#### `ConcurrentHashMap`

线程安全，采用细分锁，锁颗粒更小，并发性能更优

#### `Collections.synchronizedMap`

线程安全，采用当前对象作为锁，颗粒较大，并发性能较差。

### 3. Int作为Key的Map

> 针对该特性进行了优化，采用二分法查找，简单数组存储。

`SparseArray`、`SparseBooleanArray`、`SparseIntArray`。

## III. 数据库相关

> 建多索引的原则: 哪个字段可以最快的**减少查询**结果，就把该字段放在最前面

#### 无法使用索引的情况

- 操作符`BETWEEN`、`LIKE`、`OR`
- 表达式
- `CASE WHEN`

#### 不推荐

- 不要设计出索引是其他索引的前缀（没有意义）
- 更新时拒绝直接全量更新，要更新哪列就put哪列的数据
- 如果最频繁的是更新与插入，别建很多索引 （原本表就很小就也没必要建）
- 拒绝用大字符串创建索引
- 避免建太多索引，查询时可能就不会选择最好的来执行

#### 推荐

- 多使用整型索引，效率远高于字符串索引
- 搜索时使用SQL参数(`"?", parameter`)代替字符串拼接（底层有特殊优化与缓存）
- 查询需要多少就limit多少（如判断是否含有啥，就limit 1就行了嘛）
- 如果出现很宽的列(如blob类型)，考虑放在单独表中(在查询或者更新其他列数据时防止不必要的大数据i/o影响性能)


## IV. JNI抉择

> Android JVM相关知识，可参看: [ART、Dalvik](http://blog.dreamtobe.cn/2015/11/01/android_art_dalvik/)

> Android JNI、NDK相关知识，可参看: [NDK](http://blog.dreamtobe.cn/2015/11/08/ndk/)

> JNI不一定显得更快，有些会更慢。

> 特点: 不用在虚拟机的框子下写代码

- 可以调用更底层的高性能的代码库 -- Good
- 如果是Dalvik，将省去了由JIT编译期转为本地代码的这个步骤。 -- Good
- Java调用JNI的耗时较Java调用Java肯定更慢，虽然随着JDK版本的升级，差距已经越来越小(JDK1.6版本是5倍Java调用Java方法的耗时) -- Bad
- 内存不在Java Heap，没有OOM风险，有效减少gc。 -- Good

> 一些重要的参数之类，也可以考虑放在Native层，保证安全性。参考: [Android应用程序通用自动脱壳方法研究](http://blog.dreamtobe.cn/2015/07/17/wh_android_tk/)

## V. 多进程抉择

> 360 17个进程: [360手机卫士 Android开发 InfoQ视频 总结
](http://blog.dreamtobe.cn/2015/03/17/360手机卫士-Android开发-InfoQ视频-总结/)

- 充分独立，解耦部分
- 大内存(如临时展示大量图片的Activity)、无法解决的crash、内存泄漏等问题，考虑通过独立进程解决
- 独立于UI进程，需要在后台长期存活的服务(参看[Android中线程、进程与组件的关系](http://blog.dreamtobe.cn/2015/04/08/android_thread_process_components/))
- 非己方第三方库（无法保证稳定、性能等问题，并且独立组件），可考虑独立进程

> 最后，多进程存在的两个问题: 1. 由于进程间通讯或者首次调起进程的消耗等，带来的cpu、i/o等的资源竞争。2. 也许对于部分同事来说，会还有可读性问题吧，毕竟多了层IPC绕了点。

## VI. UI层面

> 相关深入优化，可参看[Android绘制布局相关](http://blog.dreamtobe.cn/2015/10/20/android-view/)

> 对于卡顿相关排查推荐参看: [Android性能优化案例研究(上)](http://www.importnew.com/3784.html)与[Android性能优化案例研究（下）](http://www.importnew.com/4065.html)

- 减少不必要的不透明背景相互覆盖，减少重绘，因为GPU不得不一遍又一遍的画这些图层
- 保证UI线程一次完整的绘制(measure、layout、draw)不超过16ms(60Hz)，否则就会出现掉帧，卡顿的现象
- 在UI线程中频繁的调度中，尽量少的对象创建，减少gc等。
- 分步加载（减少任务颗粒）、预加载、异步加载(区别出耗时任务，采用异步加载)


## VII. 库推荐

> 可以参考Falcon Pro作者的推荐: [Falcon Pro 3如何完成独立开发演讲分析](http://blog.dreamtobe.cn/2015/06/14/Falcon-Pro-3-如何完成独立开发演讲分析/)

#### 1. 代码编写习惯

[RxJava](https://github.com/ReactiveX/RxJava) (响应式编程，代码更加简洁，异步处理更快快捷、异常处理更加彻底、数据管道理念)

相关了解可以参看: [RxJava](http://blog.dreamtobe.cn/2015/04/29/RxJava学习整理/)

#### 2. 图片加载:
- 小型快捷: [Picasso](https://github.com/square/picasso) (接口干净、支持okhttp、功能强大、稳定、高效, 可以延读: [PhotoGallery、Volley、Picasso 比较](http://blog.dreamtobe.cn/2015/04/28/PhotoGallery%E3%80%81Volley%E3%80%81Picasso-%E6%AF%94%E8%BE%83/))
- 大项目考虑: [Fresco](http://fresco-cn.org) (2.5M，pipeline解决资源竞争、Native Heep解决OOM，的同时减少GC)

#### 3. 网络底层库:

[Okhttp](https://github.com/square/okhttp): 默认gzip、缓存、安全等

#### 4. 网络基层:

[Retrofit](https://github.com/square/retrofit): 非常好用的REST Client，结合RxJava简单API实现、类型安全，简单快捷

#### 5. 数据库层:

[Realm](https://realm.io): 效率极高(Falcon Pro 3的作者Joaquim用了该库以后，所有数据库操作都放到了UI线程)（基于TightDB，底层C++闭源，Java层开源，简单使用，性能远高于SQLite等）

#### 6. Crash上报:

[Fabric](https://fabric.io): 全面的信息(新版本还支持JNI Crash获取和上报)、稳定的数据、及时的通知、强大的反混淆(其实在混淆后有上传mapping)

#### 7. 内存泄漏自动化检测

[LeakCanary](https://github.com/square/leakcanary): 自动化泄漏检测与分析 ( 可以看看这个[LeakCanary使用总结](http://blog.dreamtobe.cn/2015/05/18/LeakCanary%E4%BD%BF%E7%94%A8%E6%80%BB%E7%BB%93/)与[Leakcanary Square的一款Android/Java内存泄漏检测工具](http://blog.dreamtobe.cn/2015/05/12/Leakcanary-Square%E7%9A%84%E4%B8%80%E6%AC%BEAndroid:Java%E5%86%85%E5%AD%98%E6%B3%84%E6%BC%8F%E6%A3%80%E6%B5%8B%E5%B7%A5%E5%85%B7/))

#### 8. 其他

 - 代码质量: [phabricator 的arc diff](http://phabricator.org) (尽量小颗粒度的arc diff 与update review)，其实也可以看看Google是如何做的: [笔记-谷歌是如何做代码审查的](http://blog.dreamtobe.cn/2015/03/23/%5B笔记%5D谷歌是如何做代码审查的/)，还有一点的TODO要写好deadline与master
 - 编包管理: [Gitlab CI](https://about.gitlab.com/gitlab-ci/) (结合Gitlab，功能够用，方便)


## VIII. 内存泄漏相关

- 无法解决的泄漏（如系统底层引起的)移至独立进程(如2.x机器存在webview的内存泄漏)
- 大图片资源/全屏图片资源，要不放在`assets`下，要不放在`nodpi`下，要不都带，否则缩放会带来额外耗时与内存问题
- 4.x在AndroidManifest中配置`largeHeap=true`，一般dvm heep最大值可增大50%以上。
- 在`Activity#onDestory`以后，遍历所有View，干掉所有View可能的引用(通常泄漏一个Activity，连带泄漏其上的View，然后就泄漏了大于全屏图片的内存)。
- 万金油: 静态化内部类，使用`WeakReference`引用外部类，防止内部类长期存在，泄漏了外部类的问题。


#### 图片Decode

- 全局统一`BitmapFactory#decode`出口，捕获此处decode oom，控制长宽（小于屏幕分辨率大小 ）
- 如果采用RGB_8888 oom了，尝试RGB_565(相比内存小一半以上(w*h*2(bytes)))
- 如果还考虑2.x机器的话，设置`BitmapFactory#options`的`InNativeAlloc`参数为true，此时decode的内存不会上报到dvm中，便不会oom。


## IX. 编译与发布

- 考虑采用DexGuard，或ProGuard结合相关资源混淆来提高安全与包大小，参考: [DexGuard、Proguard、Multi-dex](http://blog.dreamtobe.cn/2015/11/04/guard_multi_dex/)
- 结合Gradle、Gitlab-CI 与Slack(Incoming WebHooks)，快速实现，打相关git上打相关Tag，自动编相关包通知Slack。
- 结合Gitlab-CI与Slack(Incoming WebHooks)，快速实现，所有的push，Slack快速获知。
- 结合Gradle中Android提供的`productFlavors`参数，定义不同的variations，快速批量打渠道包

## X. 其他

- `final`能用就用（高效: 编译器在调用`final`方法时，会转入内嵌机制）
- 懒预加载，如简单的ListView、RecyclerView等滑动列表控件，停留在当前页面的时候，可以考虑直接预加载下个页面所需图片
- 智能预加载，通过权重等方式结合业务层面，分析出哪些更有可能被用户浏览使用，然后再在某个可能的时刻进行预加载。如，进入朋友圈之前通过用户行为，智能预加载部分原图。
- 做好有损体验的准备，在一些无法避免的问题面前做好有损体验（如，非UI进程crash，可以自己解决就不要让用户感知，或者UI进程crash了，做好场景恢复）
- 做好各项有效监控：crash(注意还有JNI的)、anr(定期扫描文件)、掉帧(绘制监控、activity生命周期监控等)、异常状态监控(本地Log根据需要不同级别打Log并选择性上报监控)等
- 文件存储推荐放在`/sdcard/Android/data/[package name]/`里(在应用卸载时，会随即删除)(`Context#getExternalFilesDir()`)，而非`/sdcard/`根目录建文件夹（节操问题）
- 通过gradle的`shrinkResources`与`minifyEnabled`参数可以简单快速的在编包的时候自动删除无用资源
- 由于resources.arsc在api8以后，aapt中默认采用UTF-8编码，导致资源中大都是中文的resources.arsc相比采用UTF-16编码更大，此时，可以考虑aapt中指定使用UTF-16
- 谷歌建议，大于10M的大型应用考虑安装到SD卡上: [App Install Location](http://developer.android.com/intl/zh-cn/guide/topics/data/install-location.html)
- 当然运维也是一方面: [Optimize Your App](http://developer.android.com/intl/zh-cn/distribute/essentials/optimizing-your-app.html)
- 在已知并且不需要栈数据的情况下，就没有必要需要使用异常，或创建`Throwable`生成栈快照是一项耗时的工作。

---

- [应用的核心质量](http://developer.android.com/intl/zh-cn/distribute/essentials/quality/core.html)
- [JNI调用性能测试及优化](http://wiki.jikexueyuan.com/project/jni-ndk-developer-guide/performance.html)
- [Java学习笔记：(30)谨慎地使用本地方法](http://www.programgo.com/article/39033077030/)
- [Android 4.4 引入的 ART 对比 Dalvik 性能提升大吗，后者会不会被取代，会不会产生兼容性问题？](http://www.zhihu.com/question/21942389)
- [性能优化之Java(Android)代码优化](http://www.trinea.cn/android/java-android-performance/)
- [移动端网络优化](http://www.trinea.cn/android/mobile-performance-optimization/)
- [性能优化之Java(Android)代码优化](http://www.trinea.cn/android/java-android-performance/)
- [JNI性能测试一—JNI调用C与Java调用java性能比较](http://blog.csdn.net/zgjxwl/article/details/6232577)
- [微信ANDROID客户端-会话速度提升70%的背后](https://mp.weixin.qq.com/s?__biz=MzAwNDY1ODY2OQ==&mid=207548094&idx=1&sn=1a277620bc28349368b68ed98fbefebe)
- [新的Andriod Gradle插件可自动移除无用资源](http://www.infoq.com/cn/news/2014/11/new-android-gradle)
- [Android安装包相关知识汇总](https://mp.weixin.qq.com/s?__biz=MzAwNDY1ODY2OQ==&mid=208008519&idx=1&sn=278b7793699a654b51588319b15b3013)
- [Android优化实践](http://gold.xitu.io/entry/55272f6be4b0da2c5deb7f36)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
