title: Android中线程、进程与组件的关系
date: 2015-04-08 08:35:03
updated: 2015-04-08 08:35:03
permalink: 2015/04/08/android_thread_process_components
categories:
- Android机制
tags:
- Android
- 进程
- 线程
- 组件
- 调度

---

## I. 安全

### 基本保障

每个应用 - Linux 用户ID

权限: 应用本身与用户可见

<!--more-->

### 不同应用程序共享数据(基于这套机制)

1. `AndroidManifest`中给`manifest`标签中定义相同的`android:sharedUserId`属性
2. 以相同的签名加密

**[效果]**: 运行在相同的进程中，互相共享资源

## II. Dalvik、进程、应用程序关系

```
Linux进程
    |
Dalvik虚拟机
    |
应用程序
```

### Dalvik虚拟机功能(都是使用Linux底层的功能)

1. 组件生命周期
2. 堆栈管理
3. 线程管理
4. 安全
5. 异常管理
6. GC
7. ....

## III. 线程、进程与Android系统组件的关系

### 系统资源回收机制

#### 退出应用程序

应用程序所使用的资源(进程、虚拟机、线程等)**还存在**内存中

#### 应用程序资源回收时机

1. 系统内存不足时
2. 根据**进程中**运行的组件**类别**、组件的**状态** => 判断重要性，排序优先级

### 进程重要性级别

> 当A进程依赖(绑定)B进程的时候，那么系统会判定: B进程的进程重要性级别 至少会等于 A进程的重要性级别

#### 1. 前台进程:

> 正在使用的进程，满足以下任意一个条件的进程

- 持有一个用户正在交互的`Activity`(`Activity#onResume()`方法已经被调用)
- 持有一个`Service`绑定了用户正在交互的`Activity`
- 持有一个`Service`正在运行在前台模式下(通过`Service#startForeground()`开始前台模式)
- 持有一个`Service`正在执行它任意的生命周期回调(`onCreate()`、`onStart()`、`onDestroy()`)
- 持有一个`BroadcastReceiver`正在执行它的`onReceive()`方法

#### 2. 可见进程:

> 屏幕上有显示，当不是正在使用，满足以下任意一个条件的进程

- 持有一个`Activity`不在前台(`Activity#onPause()`已经被调用)，但是用户依然能够看到。(如另外一个程序启动了一个Dialog，此时上一个应用的`Activity`用户还能被用户看到，因此上一个应用就是可见进程)
- 持有一个`Service`绑定了一个可见`Activity`。


#### 3. 服务进程:

> 运行Service的进程(只要**前台进程**和**可见进程**有足够内存，系统就不会回收)

不属于`前台进程`，以及`可见进程`的，持有一个正在运行的`Service`的进程。

#### 4. 后台进程:

运行着不可见Activity(回调过`onStop()`(一般按了Back或Home键至少会执行到`onStop()`)的进程, 会存储在一个LRU队列中，在前三种优先级进程需要内存时，就会对最近最少使用的进程进行回收。

> 由于服务进程的优先级高于后台进程，因此很多后台事件可以优先考虑放到服务中处理，避免被回收。

#### 5. 空进程:

未运行任何程序组件的进程，通常这种进程缓存，只是为了加速下次组件启动时不用重复启动进程。

---

- [Processes and Threads](https://developer.android.com/guide/components/processes-and-threads.html)

---
