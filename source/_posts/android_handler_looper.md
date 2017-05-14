title: Android Handler Looper机制
date: 2016-03-11 14:36:03
updated: 2016-03-11 14:36:03
permalink: 2016/03/11/android_handler_looper
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483661&idx=1&sn=39c0e67abfb50042936f4af9ec985ed8
wechatmptitle: Android Handler
categories:
- Android机制
tags:
- Handler
- Looper
- Android
- 消息机制
- MessageQueue
- Barrier

---

## I. Handler Looper机制

> 整理了半天，还不如画张图来的清晰

<!-- more -->

#### 1. Handler创建所在线程(Looper所在线程)

![](/img/android_handler_looper-1.png)

#### 2. Handler发消息所在线程

![](/img/android_handler_looper-2.png)

### 3. Handler中Message回收机制

Message中回收用的池子:

> 池子大小50个Message

 `sPool:Message`(静态变量)、`next#message`、`sPoolSize:int`(静态变量)、`sPoolSync:Object`(静态常量)形成一个简单的线程安全的先进先出的单向链表作为Message复用的池子。每次`obtain`时，取链表头Message, 标记`flag`为0，返回;`recycle`时，放入链表头。


> 记录参数: `Message#flag`， 基于位运算用于记录`FLAG_IN_USE`与`FLAG_ASYNCHRONOUS` (是否使用中 与 是否是是异步消息)

由于对外可见的`recycle`在检测flag的时候有可能会抛crash，因此不得不跟踪flag的变化。

![](/img/android_handler_looper-3.png)

### 4. Handler提供功能

除了常用的`send*`、`post*`、`remove*`以外还有一个`runWithScissors`:

#### `runWithScissors`:

 若是调用线程与Handler的Looper所在线程非同一线程，将通过该方法可以简单的实现timeout，调用以后会block，直到传入的runnable结束或者是timeout，若是timeout，返回false，否则返回true。

#### `asynchronous`:

> @see `MessageQueue#postSyncBarrier`、`MessageQueue#removeSyncBarrier`
> 案例: View请求启动绘制生命周期: `ViewRootImpl#scheduleTraversals`

![](/img/android_handler_looper-4.png)

1. MessageQueue 从栈底到栈顶按`Message.when`降序排列(相同`Message.when`的先进栈的离栈顶更近)的后进先出的栈(`MessageQueue#enqueueMessage` `MessageQueue#next`)
2. `barrier`的Message与普通Message的差别是target(类型是Handler)为null，只能通过`MessageQueue#postSyncBarrier`创建 `barrier` Message
3. `barrier`的Message与普通Message以同样的规则进栈，但是却只能通过 `MessageQueue#removeSyncBarrier`出栈
4. 每个`barrier`使用独立的token(记录在`Message#arg1`)进行区分
5. 所有的同步消息(相对与异步消息而言，默认消息都是同步消息)如果`barrier`之后，都会被延后执行，直到调用`MessageQueue#removeSyncBarrier`通过其token将该barrier清除
6. 当`barrier`在栈顶时，栈中的异步消息照常出栈不受影响

 > Handler中的对应构造函数被隐藏，但是可以通过调用`Message#setAsynchronous`指定对应的Message为asynchronous的Message。
 >值得一提的是，部署barrier(`MessageQueue#postSyncBarrier`)与清除barrier(`MessageQueue#removeSyncBarrier`)的相关方法都是对外不可见的。

---

> ps: 关于Handler的外界有效全局控制，我开源了一个库，支持Handler的暂停、恢复等操作: [Jacksgong/MessageHandler](https://github.com/Jacksgong/MessageHandler)

---

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

---
