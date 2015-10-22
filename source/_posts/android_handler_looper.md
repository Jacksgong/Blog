title: Android Handler Looper机制整理
date: 2015-10-22 00:13:03
tags:
- Handler
- Looper
- Android
- 消息机制

---

## I. Handler Looper机制

> 整理了半天，还不如画张图来的清晰

<!-- more -->

#### 1. Handler创建所在线程

![](/img/android_handler_looper-1.png)

#### 2. Handler发消息所在线程

![](/img/android_handler_looper-2.png)


## II. 常见异常及原因

```
public Handler() {
    if (FIND_POTENTIAL_LEAKS) {
        final Class<? extends Handler> klass = getClass();
        if ((klass.isAnonymousClass() || klass.isMemberClass() || klass.isLocalClass()) &&
                (klass.getModifiers() & Modifier.STATIC) == 0) {
            Log.w(TAG, "The following Handler class should be static or leaks might occur: " +
                klass.getCanonicalName());
        }
    }
    mLooper = Looper.myLooper();
    if (mLooper == null) {
        throw new RuntimeException(
            "Can't create handler inside thread that has not called Looper.prepare()");
    }
    mQueue = mLooper.mQueue;
    mCallback = null;
}
```
### 1. 可能导致内存泄漏

> `The following Handler class should be static or leaks might occur: <classCanonicalName>`

#### 原因:

由于`Handler`有可能会被`Looper#mQueue#mMessages#target`引用，而很有可能由于消息还未到达处理的时刻，导致引用会被长期持有，如果`Handler`是一个非静态内部类，就会持有一个外部类实例的引用，进而导致外部类很有可能出现无法及时gc的问题。

#### 通用解决方法:

直接静态化内部类，这样内部类`Handler`就不再持有外部类实例的引用，再在`Handler`的构造函数中以弱引用(当所指实例不存在强引用与软引用后，GC时会自动回弱引用指向的实例)传入外部类供使用即可。

### 2. 所在线程没有调用`Looper.prepare()`

> `Can't create handler inside thread that has not called Looper.prepare()`

#### 原因:

`Looper.prepare()`实际上是创建一个`Looper`传入作为所在线程的局部变量(全局由`ThreadLocal`与`Thread#localValues`来保证，简单参考`ThreadLocal#get`、`ThreadLocal#set`即可理解)，而在真正`Looper#loop`的时候，是需要已所在线程的局部变量的`Looper`为载体取得所有要处理的消息以及处理的方式的。

因此创建`Handler`的同时是需要保证所在线程已经有了局部变量`Looper`的实例，才能保证`Handler`接下来真正运作。

#### 通常解决方法:

在创建`Handler`前，主动调用下`Looper.prepare()`

> ps: 每个线程的的`Looper#prepare`相对所在线程只能被调用一次，否则会报`"Only one Looper may be created per thread"`(参见`Looper#prepare`)
> ps: 之所以主线程直接创建`Handler`不会抛出类似异常，是因为在程序启动时，系统已经帮我们调用了`Looper#prepare`(参见`ActivityThread#main`)

---

- [Android异步消息处理机制完全解析，带你从源码的角度彻底理解](http://blog.csdn.net/guolin_blog/article/details/9991569)
- [Android消息机制不完全解析（上）](http://blog.csdn.net/a220315410/article/details/9857225)
- [Android消息机制不完全解析（下）](http://blog.csdn.net/a220315410/article/details/10444171)
