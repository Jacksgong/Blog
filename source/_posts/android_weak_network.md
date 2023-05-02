title: Android弱网通信探究
date: 2016-08-16 11:34:03
updated: 2017-02-10 11:34:03
permalink: 2016/08/16/android_weak_network/
categories:
- 网络
tags:
- Android
- 心跳
- TCP
- 弱网长连接

---

## I. 微信心跳机制

> 其中的有考虑到如何让手机更省电，因此有与Android的alarm对齐唤醒的处理(可以参见已经[开源的mars](https://github.com/Tencent/mars)的`smart_heartbeat.cc`)

<!-- more -->

![](/img/android-weak-network-1.png)

---

- [Android微信智能心跳方案](http://mp.weixin.qq.com/s?__biz=MzAwNDY1ODY2OQ==&mid=207243549&idx=1&sn=4ebe4beb8123f1b5ab58810ac8bc5994)
- [微信终端跨平台组件 mars 系列 - 我们如约而至](https://mp.weixin.qq.com/s?__biz=MzAwNDY1ODY2OQ==&mid=2649286451&idx=1&sn=9711761792fe800094efde219fda3cde)

---
