title: ActivityManagerService
date: 2015-11-26 20:49:03
permalink: 2015/11/26/activitymanagerservice
categories:
- Android机制
tags:
- ActivityManagerService
- ActivityThread
- Zygote

---

> 负责为应用程序创建新进程，本身也是运行在独立进程，系统启动时创建

<!-- more -->

ServiceManager初始化，有一个循环等待Client组件发送的请求(参考[Android多进程](http://blog.dreamtobe.cn/2015/11/25/android_multiply_process/))，当时我们自己创建的Service的时候并没有循环等待Client，那是怎么做到通信的呢?

1. ServiceManager中特有句柄为0
2. ActivityManagerService在启动应用(ActivityThread.main)之前就已经建立好了这个循环

![](/img/ActivityManagerService.png)

---

- [本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/activitymanagerservice.md)。

---

本文已经发布到JackBlog公众号: [Activity管理服务、虚拟机与GC - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483725&idx=1&sn=1b416b52c51ed0486bd34d66fc5abb2f)

---

- [Android应用程序进程启动过程源码分析](http://blog.csdn.net/luoshengyang/article/details/6747696)

---
