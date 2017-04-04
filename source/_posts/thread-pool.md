title: ThreadPoolExecutor与ScheduledThreadPoolExecutor
date: 2017-04-04 01:22:03
categories:
- 编程语言
tags:
- ThreadPool
- ThreadPoolExecutor
- ScheduledThreadPoolExecutor

---

{% note info %}之前有开源过一个[Jacksgong/ThreadDebugger](https://github.com/Jacksgong/ThreadDebugger)的开源库，主要用于**监控线程变化**以及**封装的各类的线程池**。
很早就想将`ThreadPoolExecutor`与`ScheduledThreadPoolExecutor`的理解整理下，但是由于这块逻辑用文字表达起来相对不好理解，因此还是决定用图片来表达。 {% endnote %}

<!-- more -->

## ThreadPoolExecutor

![](/img/thread-pool-executor.png)

## ScheduledThreadPoolExecutor

![](/img/scheduled-thread-pool-executor.png)

#### 需要注意

- `scheduleAtFixedRate`: 无论运行任务用的多久，还是指定固定的时间执行，如任务在initDelay, initDelay + period, initDelay + period * 2会被执行
- `scheduleWithFixedDelay`: 指定固定的间隔执行，如每次都是在上次执行后间隔delay以后执行

---
