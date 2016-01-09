title: ActivityManagerService
date: 2015-11-26 20:49:03
tags:
- ActivityManagerService
- ActivityThread
- Zygote

---

> 负责为应用程序创建新进程，本身也是运行在独立进程，系统启动时创建

<!-- more -->

ServiceManager初始化，有一个循环等待Client组件发送的请求(参考[Android多进程]http://blog.dreamtobe.cn/2015/11/25/android_multiply_process/)，当时我们自己创建的Service的时候并没有循环等待Client，那是怎么做到通信的呢?

1. ServiceManager中特有句柄为0
2. ActivityManagerService在启动应用(ActivityThread.main)之前就已经建立好了这个循环

![](/img/ActivityManagerService.png)

---

- [Android应用程序进程启动过程源码分析](http://blog.csdn.net/luoshengyang/article/details/6747696)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
