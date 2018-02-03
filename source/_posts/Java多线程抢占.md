title: Java多线程抢占
date: 2015-03-25 08:35:03
updated: 2015-03-25 08:35:03
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483673&idx=1&sn=cc20b1149e9ffed649dd00d8737e6a08
wechatmptitle: Java Synchronized机制与常见的多线程抢占
permalink: 2015/03/25/Java多线程抢占
categories:
- 编程语言
tags:
- java
- 多线程
- Android
- 优化

---

## 前言 机制种类

- 抢占机制

	对于CPU而言多个线程处于就绪线程队列，但是只有一个线程在运行状态。

	为Java多线程机制。

- 分时机制

	顾名思义。

<!--more-->

> 多线程抢占中很多机制是与`synchronized`机制息息相关的。关于Java Synchronised机制可以参看这篇文章: http://blog.dreamtobe.cn/2015/11/13/java_synchronized/

## I. `interrupt`

- **方法来源**: `Thread`
- **作用范围**: `wait`/`sleep`/`join`
- **作用效果**: 立即抛出`InterruptedException`

## II. `wait`

> 基本原理是: 通过调整`Mark Word`中的标志位来释放对象的所有权，休眠当前线程并且进入等待池来实现。

- **方法来源**: `Object`
- **使用前提**: 由于其实现原理，因此必须在`synchronized`块下调用。
- **作用效果**: 释放锁（暂时将锁借给别的线程用），并进入等待池。

### 恢复:

![](/img/javathread-1.png)

**促发恢复:** 1. 调用`notify`；2. `wait(millisecond)` 给定时间；3. 通过`interrupt`打断等待状态，并抛出`InterruptedException`。
**恢复状态:** 进入锁池。
**真正恢复:** 从锁池中重新竞争对象锁，获得锁后回到中断现场(从`wait`后继续执行代码)。

## III. `sleep`

- **方法来源**: `Thread`
- **方法特点**: 不释放锁。
- **促发恢复**: 1. `sleep(millisecond)`给定时间；2. 通过`interrupt`打断睡眠状态，并抛出`InterruptedException`。

## IV. `join`

- **方法来源**: `Thread`
- **作用效果**: 调用线程停下来等待`join`方法所在线程。
- **促发恢复**: `join`方法所在线程结束（`run()`方法结束）

## V. `yield`

- **方法来源**: `Thread`
- **作用效果**: 停止当前线程，让同等优先级线程运行, 如果没有同等优先级的线程，`yield`将不会起作用。

## VI. suspend
可能导致死锁，因此弃用

## Android 中抢占机制需要注意的地方

> 需要注意的是: Android中如果某进程中只有某线程且被长期阻塞在等待池，并且进程所在组件优先级较低，可能会被系统回收。此时更应该考虑使用`AlarmManager`，它持有一个CPU唤醒锁，并且即便是组件或进程已经被回收也会被重新唤起，是不存在这个问题的。(因此如果要做轮询、Socket心跳之类的，推荐使用`AlarmManager`，这样才能保证时间间隔的稳定、可靠)。

---

- [Java线程中sleep()、wait()和notify()和notifyAll()、yield()、join()等方法的用法和区别](http://zheng12tian.iteye.com/blog/1233638)
- [Difference between wait() and sleep()](http://stackoverflow.com/questions/1036754/difference-between-wait-and-sleep)

---
