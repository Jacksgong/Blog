title: ThreadDebugger And ThreadPool
date: 2016-09-01 16:43:03
updated: 2016-09-01 16:43:03
permalink: 2016/09/01/thread_debugger_and_thread_pool
categories:
- 开源项目
tags:
- ThreadDebugger
- ThreadPool
- Debugger
- Thread
- Project

---

> 已开源 [Jacksgong/ThreadDebugger](https://github.com/Jacksgong/ThreadDebugger)

- [中文迭代日志](https://github.com/Jacksgong/ThreadDebugger/blob/master/CHANGELOG_zh.md)
- [中文说明文档](https://github.com/Jacksgong/ThreadDebugger/blob/master/README_zh.md)
- [问题讨论区](https://github.com/Jacksgong/ThreadDebugger/issues)

<!-- more -->

---

### 简述所解决问题

#### 线程调试器

虽然我们知道已经有很多方法进行线程调试，如通过Android Studio Monitor 进行Allocation Tracking，在分析结果中会带有期间线程的一些信息；或者是通过Android Device Monitor进行Method Profiling，在分析结果中也会带有期间线程的一些信息。但是每次都需要进行启动关闭，并且每次结果分析都要几秒，几十秒甚至更久，显得不是很灵活。

ThreadDebugger是一个简单易用的线程调试器，可以帮助您随时查看应用中所有线程的使用情况，以及变化情况。

#### 线程池创建工具

该线程池创建工具，相比系统的Executors强制要求每次执行任务的时候都需要指定任务的名称，以便于更好的调试与监控，并且提供非常便捷的创建相关规则的线程池。
系统提供的DownloadManager由于是考虑系统层面所有应用公用，不够灵活。

### 特征

- 便捷
- 易用

### Demo

![](/img/thread_debugger_and_thread_pool.png)

---
