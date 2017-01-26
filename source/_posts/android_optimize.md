title: Android优化
date: 2015-10-26 00:26:03
permalink: 2015/10/26/android_optimize
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

- 如果是需要全量数据的，考虑使用[Protobuffers](https://developers.google.com/protocol-buffers/?hl=zh-cn) (序列化反序列化性能高于json)，并且考虑使用[nano protocol buffer](https://android.googlesource.com/platform/external/protobuf/+/master/java/README.txt)。
- 如果传输回来的数据不需要全量读取，考虑使用[Flatbuffers](https://github.com/google/flatbuffers) (序列化反序列化几乎不耗时，耗时是在读取对象时(就这一部分如果需要优化，可以参看[Flatbuffer Use Optimize](http://blog.dreamtobe.cn/2015/01/05/Flatbuffer-Use-Optimize/)

#### 2. 输入流
> 使用具有缓存策略的输入流

原 | 建议替换为
-|-
`InputStream` | `BufferedInputStream`
`Reader` | `BufferedReader`

## II. 基础相关

#### 1. 数据结构
> 如果已知大概需要多大，就直接给初始大小，减少扩容时额外开销。

- `ArrayList`: 里面就一数组，内存小，有序取值快，扩容效率低
- `LinkedList`: 里面就一双向链表，内存大，随机插入删除快，扩容效率高。
- `HashSet`: 里面就一个`HashMap`，用key对外存储，目的就是不允许重复元素。
- `ConcurrentHashMap`: 线程安全，采用细分锁，锁颗粒更小，并发性能更优
- `Collections.synchronizedMap`: 线程安全，采用当前对象作为锁，颗粒较大，并发性能较差。
- `SparseArray`、`SparseBooleanArray`、`SparseIntArray`:  针对Key为`Int`、`Boolean`进行了优化，采用二分法查找，简单数组存储。相比`HashMap`而言，`HashMap`每添加一个数据，大约会需要申请额外的32字节的数据，因此`Sparsexxx`在内存方面的开销会小很多。

#### 2. 编码习惯

- 尽量简化，不要做不需要的操作。
- 尽量避免分配内存(创建对象): 1) 如果一个方法返回一个`String`，并且这个方法的返回值始终都是被用来`append`到一个`StringBuffer`上，就改为传入`StringBuffer`直接`append`上去，避免创建一个短生命周期的临时对象；2) 如果使用的字符串是截取自某一个字符串，就直接从那个字符串上面`substring`，不要拷贝一份，因为通过`substring`虽然创建了新的`String`对象，但是共享了里面的`char`数组中的`char`对象，减少了这块对象的创建；量使用多个一维数组，其性能高于多维数组；`int`数组性能远大于`Integer`数组性能；
- 如果你确定不需要访问类成员，让方法`static`，这样调用时可以提升15%~20%的速度，因为不需要切换对象状态。
- 如果某个参数是常量，别忘了使用`static final`，这样可以让`Class`首次初始化时，不需要调用`<clinit>`来创建`static`方法，而是在编译时就直接将常量替换代码中使用的位置。
- Android开发中，类内尽量避免通过`get/set`访问成员变量，虽然这在语言的开发中是一个好的习惯，但是Android虚拟机中，对方法的调用开销远大于对变量的直接访问。在没有JIT的情况下，直接的变量访问比调用方法快3倍，在JIT下，直接的变量访问更是比调用方法快7倍!
- 当内部类需要访问外部类的私有`方法/变量`时，考虑将这些外部类的私有`方法/变量`改用包可见的方式。首先在编写代码的时候，通过内部类访问外部类的私有`方法/变量`是合法的，但是在编译的时候为了满足这个会将需要被内部类访问的私有`方法/变量`封装一层包可见的方法，实现让内部类访问这些私有的`方法/变量`，根据前面我们有提到说方法的调用开销大于变量的调用，因此这样使得性能变差，所以我们在编码的时候可以考虑直接将需要被内部类调用的外部类私有`方法/变量`，改为包可见。
- 尽量少使用`float`。在很多现代设备中，`double`的性能与`float`的性能几乎没有差别，但是从大小上面`double`是`float`的两倍的大小。
- 尽量考虑使用整型而非浮点数，在较好的Android设备中，浮点数比整型慢一倍。
- 尽量不要使用除法操作，有很多处理器有乘法器，但是没有除法器，也就是说在这些设备中需要将除法分解为其他的计算方式速度会比较慢。
- 尽量使用系统sdk中提供的方法，而非自己去实现。如`String.indexOf()`相关的API，Dalvik将会替换为内部方法；`System.arraycopy()`方法在Nexus One手机上，会比我们上层写的类似方法的执行速度快9倍。
- 谨慎编写native，性能不一定更好，Native并不是用于使得性能更好，而是用于有些已经存在的库是使用native语言实现的，我们需要引入Android，这时才使用。1) 需要多出开销在维持Java-native的通信；2) 在native中创建的资源由于在native heap上面，因此需要主动的释放；3) 需要对不同的处理器架构进行支持，存在明显的兼容性问题需要解决。
- 在没有JIT的设备中，面向接口编程的模式(如`Map map`)，相比直接访问对象类(如`HashMap map`)，会慢6%，但是在存在JIT的设备中，两者的速度差不多。但是内存占用方面面向接口变成会消耗更多内存，因此如果你的面向接口编程不是十分的必要的情况下可以考虑不用。
- 在没有JIT的设备中，访问本地化变量相对与成员变量会快20%，但是在存在JIT的设备中，两者速度差不多。

##### 遍历优化

> 尽量使用`Iterable`而不是通过长度判断来进行遍历。

```
// 这种性能是最差的，JIT也无法对其优化。
public void zero() {
    int sum = 0;
    for (int i = 0; i < mArray.length; ++i) {
        sum += mArray[i].mSplat;
    }
}

// 相对zero()来说，这种写法会更快些，在存在JIT的情况下速度几乎和two()速度一样快。
public void one() {
    int sum = 0;
    // 1) 通过本地化变量，减少查询，在不存在JIT的手机下，优化较明显。
    Foo[] localArray = mArray;
    // 2) 获取队列长度，减少每次遍历访问变量的长度，有效优化。
    int len = localArray.length;

    for (int i = 0; i < len; ++i) {
        sum += localArray[i].mSplat;
    }
}

// 在无JIT的设备中，是最快的遍历方式，在存在JIT的设备中，与one()差不多快。
public void two() {
    int sum = 0;
    for (Foo a : mArray) {
        sum += a.mSplat;
    }
}
```


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
](http://blog.dreamtobe.cn/2015/03/17/360手机卫士-Android开发-InfoQ视频-总结/)，但是考虑到多进程的消耗，我们更需要关注多个组件复用同一进程。
> 在没有做任何操作的空进程而言，其大约需要额外暂用1.4MB的内存。

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

#### 1. 响应式编程

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

## VIII. 内存

> 根据设备可用内存的不同，每个设备给应用限定的Heap大小是有限的，当达到对应限定值还申请空间时，就会收到`OutOfMemoryError`的异常。

### 1. 内存管理

> Android根据不同的进程优先级，对不同进程进行回收来满足内存的供求，可以参照这篇文章: [Android中线程、进程与组件的关系](http://blog.dreamtobe.cn/2015/04/08/android_thread_process_components/)。
> 在后台进程的LRU队列中，除了LRU为主要的规则以外，系统也会根据杀死一个后台进程所获得的内存是否更多作为一定的参考依据，因此后台进程为了保活，尽量少的内存，尽可能的释放内存也是十分必要的。

- 尽可能的缩短`Service`的存活周期（可以考虑直接使用执行完任务直接关闭自己的`IntentService`），也就是说在Service没有任何任务的时候，尽可能的将其关闭，以减少系统资源的浪费。
- 可以通过系统服务`ActivityManager`中的`getMemoryClass()`获知当前设备允许每个应用大概可以有多少兆的内存使用(如果在`AndroidManifest`设置了`largeHeap=true`，使用`getLargeMemoryClass()`获知)，并且让应用中的内存始终低于这个值，避免OOM。
- 相对于静态常量而言，通常`Enum`枚举需要大于两倍的内存空间来存储相同的数据。
- Java中的每个`class`(或者匿名类)大约占用500字节。
- 每个对象实例大约开销12~16字节的内存。

#### `onTrimMemory()`回调处理

> 监听`onTrimMemory()`的回调，根据不同的内存等级，做相应的释放以此让系统资源更好的利用，以及自己的进程可以更好的保活。

##### 当应用还在前台

- `TRIM_MEMORY_RUNNING_MODERATE`: 当前应用还在运行不会被杀，但是设备可运行的内存较低，系统正在从后台进程的LRU列表中杀死进程其他进程。
- `TRIM_MEMORY_RUNNING_LOW`: 当前应用还在运行不会被杀，但是设备可运行内存很低了，会直接影响当前应用的性能，当前应用也需要考虑释放一些无用资源。
- `TRIM_MEMORY_RUNNING_CRITICAL`: 当前应用还在运行中，但是系统已经杀死了后台进程LRU队列中绝大多数的进程了，当前应用需要考虑释放所有不重要的资源，否则很可能系统就会开始清理服务进程，可见进程等。也就说，如果内存依然不足以支撑，当前应用的服务也很有可能会被清理掉。

##### `TRIM_MEMORY_UI_HIDDEN`

当回调回来的时候，说明应用的UI对用户不可见的，此时释放UI使用的一些资源。这个不同于`onStop()`，`onStop()`的回调，有可能仅仅是当前应用中进入了另外一个`Activity`。

##### 当应用处于后台

- `TRIM_MEMORY_BACKGROUND`: 系统已经处于低可用内存的情况，并且当前进程处于后台进程LRU队列队头附近，因此还是比较安全的，但是系统可能已经开始从LRU队列中清理进程了，此时当前应用需要释放部分资源，以保证尽量的保活。
- `TRIM_MEMORY_MODERATE`: 系统处于低可用内存的情况，并且当前进程处于后台进程LRU队列中间的位置，如果内存进一步紧缺，当前进程就有可能被清理掉，需要进一步释放资源。
- `TRIM_MEMORY_COMPLETE`: 系统处于低可用内存的情况，并且当前进程处于后天进程LRU队列队首的位置，如果内存进一步紧缺，下一个清理的就是当前进程，需要释放尽可能的资源来保活当前进程。在API14之前，`onLowMemory()`就相当于这个级别的回调。

### 2. 避免内存泄漏相关

- 无法解决的泄漏（如系统底层引起的)移至独立进程(如2.x机器存在webview的内存泄漏)
- 大图片资源/全屏图片资源，要不放在`assets`下，要不放在`nodpi`下，要不都带，否则缩放会带来额外耗时与内存问题
- 4.x在`AndroidManifest`中配置`largeHeap=true`，一般dvm heep最大值可增大50%以上。但是没有特殊明确的需要，尽可能的避免这样设置，因为这样一来很可能隐藏了消耗了完全没有必要的内存的问题。
- 在`Activity#onDestory`以后，遍历所有View，干掉所有View可能的引用(通常泄漏一个Activity，连带泄漏其上的View，然后就泄漏了大于全屏图片的内存)。
- 万金油: 静态化内部类，使用`WeakReference`引用外部类，防止内部类长期存在，泄漏了外部类的问题。


### 3. 图片

> Android 2.3.x或更低版本的设备，是将所有的Bitmap对象存储在native heap，因此我们很难通过工具去检测其内存大小，在Android 3.0或更高版本的设备，已经调整为存储到了每个应用自身的Dalvik heap中了。

- 全局统一`BitmapFactory#decode`出口，捕获此处decode oom，控制长宽（小于屏幕分辨率大小 ）
- 如果采用RGB_8888 oom了，尝试RGB_565(相比内存小一半以上(w*h*2(bytes)))
- 如果还考虑2.x机器的话，设置`BitmapFactory#options`的`InNativeAlloc`参数为true，此时decode的内存不会上报到dvm中，便不会oom。
- 建议采用[lingochamp/QiniuImageLoader](https://github.com/lingochamp/QiniuImageLoader)的方式，所有图片的操作都放到云端处理，本地默认使用Webp，并且获取的每个位置的图片，尽量通过精确的大小按需获取，避免内存没必要的消耗。


## IX. 线程

- 采用全局线程池管理体系，有效避免野线程。可参照 [ThreadDebugger-demo/DemoThreadPoolCentral.java](https://github.com/Jacksgong/ThreadDebugger/blob/master/demo/src/main/java/cn/dreamtobe/threaddebugger/demo/DemoThreadPoolCentral.java)
- 结合全局线程池管理体系，使用[ThreadDebugger](https://github.com/Jacksgong/ThreadDebugger)监控线程，避免线程泄漏的存在。

## X. 编译与发布

- 考虑采用DexGuard，或ProGuard结合相关资源混淆来提高安全与包大小，参考: [DexGuard、Proguard、Multi-dex](http://blog.dreamtobe.cn/2015/11/04/guard_multi_dex/)
- 结合Gradle、Gitlab-CI 与Slack(Incoming WebHooks)，快速实现，打相关git上打相关Tag，自动编相关包通知Slack。
- 结合Gitlab-CI与Slack(Incoming WebHooks)，快速实现，所有的push，Slack快速获知。
- 结合Gradle中Android提供的`productFlavors`参数，定义不同的variations，快速批量打渠道包
- 迭代过程中，包定期做多纬度扫描，如包大小、字节码大小变化、红线扫描、资源变化扫描、相同测试用例耗电量内存等等，更多的可以参考 [360手机卫士 Android开发 InfoQ视频 总结](http://blog.dreamtobe.cn/2015/03/17/360%E6%89%8B%E6%9C%BA%E5%8D%AB%E5%A3%AB-Android%E5%BC%80%E5%8F%91-InfoQ%E8%A7%86%E9%A2%91-%E6%80%BB%E7%BB%93/)
- 迭代过程中，对关键`Activity`以及`Application`对打开的耗时进行统计，观察其变化，避免因为迭代导致某些页面非预期的打开变慢。

## XI. 工具

- [TraceView](https://developer.android.com/studio/profile/traceview.html)可以有效的更重一段时间内哪个方法最耗时，但是需要注意的是目前TraceView在录制过中，会关闭JIT，因此也许有些JIT的优化在TraceView过程被忽略了。
- [Systrace](https://developer.android.com/studio/profile/systrace.html)可以有效的分析掉帧的原因。
- [HierarchyViewer](https://developer.android.com/studio/profile/optimize-ui.html)可以有效的分析View层级以及布局每个节点`measure`、`layout`、`draw`的耗时。

## XII. 其他

- `final`能用就用（高效: 编译器在调用`final`方法时，会转入内嵌机制）
- 懒预加载，如简单的`ListView`、`RecyclerView`等滑动列表控件，停留在当前页面的时候，可以考虑直接预加载下个页面所需图片
- 智能预加载，通过权重等方式结合业务层面，分析出哪些更有可能被用户浏览使用，然后再在某个可能的时刻进行预加载。如，进入朋友圈之前通过用户行为，智能预加载部分原图。
- 做好有损体验的准备，在一些无法避免的问题面前做好有损体验（如，非UI进程crash，可以自己解决就不要让用户感知，或者UI进程crash了，做好场景恢复）
- 做好各项有效监控：crash(注意还有JNI的)、anr(定期扫描文件)、掉帧(绘制监控、activity生命周期监控等)、异常状态监控(本地Log根据需要不同级别打Log并选择性上报监控)等
- 文件存储推荐放在`/sdcard/Android/data/[package name]/`里(在应用卸载时，会随即删除)(`Context#getExternalFilesDir()`)，而非`/sdcard/`根目录建文件夹（节操问题）
- 通过gradle的`shrinkResources`与`minifyEnabled`参数可以简单快速的在编包的时候自动删除无用资源
- 由于resources.arsc在api8以后，aapt中默认采用UTF-8编码，导致资源中大都是中文的resources.arsc相比采用UTF-16编码更大，此时，可以考虑aapt中指定使用UTF-16
- 谷歌建议，大于10M的大型应用考虑安装到SD卡上: [App Install Location](http://developer.android.com/intl/zh-cn/guide/topics/data/install-location.html)
- 当然运维也是一方面: [Optimize Your App](http://developer.android.com/intl/zh-cn/distribute/essentials/optimizing-your-app.html)
- 在已知并且不需要栈数据的情况下，就没有必要需要使用异常，或创建`Throwable`生成栈快照是一项耗时的工作。
- 需要十分明确发布环境以及测试环境，明确仅仅为了方便测试的代码以及工具在发布环境不会被带上。

---

- 最后一次更新时间: 2016-9-19，[本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/android_optimize.md)。

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
- [Performance Tips](https://developer.android.com/training/articles/perf-tips.html)
- [Managing Your App's Memory](https://developer.android.com/training/articles/memory.html#YourApp)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
