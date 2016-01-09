title: Android中线程、进程与组件的关系
date: 2015-04-08 08:35:03
tags:
- Android
- 进程
- 线程
- 组件
- 调度

---

## I. 安全

#### 基本保障

每个应用 - Linux 用户ID

权限: 应用本身与用户可见

<!--more-->

#### 不同应用程序共享数据(基于这套机制)

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

#### Dalvik虚拟机功能(都是使用Linux底层的功能)

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

#### 进程重要性级别

1. 前台进程: 正在使用的进程
2. 可见进程: 屏幕上有显示，当不是正在使用
3. 服务进程: 运行Service的进程(只要**前台进程**和**可见进程**有足够内存，系统就不会回收)
4. 后台进程: 运行着不可见Activity(并回调过`onStop()`(一般按了Back或Home键至少会执行到`onStop()`)的进程(**前三种**优先级进程需要内存，会回收)
5. 空进程: 未运行任何程序组件

> **优点:**  下次启动该应用程序时会更快速（因为资源可能没有被回收）
> **缺点:**  可能资源被回收，而启动时资源不够，需要等待系统回收其他资源

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
