
title: Android多进程
date: 2015-08-19 06:35:03
tags:
- Android
- 多进程

---
## I. Binder

> IPC方式之一

### 出现原因:

#### 1. CS通信方式

> Binder采用Client-Server方式

linux支持通信方式:消息队列/共享内存/信号量/socket，其中只有socket支持CS

<!--more-->

#### 2. 传输性能

IPC | 特征 | 拷贝次数 | 补充
:-: | :-: | :-: | :-
共享内存 | 控制复杂 | 0 | 极少用
Binder | 简单通用安全|  1 | Android常用啊，性能高
Socket/管道/消息队列 | A中缓冲区 --(存储)--> 内核缓冲区 --(转发)--> B中缓冲区 | 2 | socket作为通用接口，传输效率低，开销大，一般用于 跨网络的IPC/进程间低速IPC


#### 3. 安全

> 基于Android本身为每个应用分配了独立的UID，可以使用UID/PID作为进程身份标志

- 传统IPC依赖上层协议确保传入UID，十分危险，Binder支持实名(自身在内核中添加，安全可靠)也支持匿名。
- 传统IPC访问接入点(管道名/system V键值/socket ip地址/文件名)是开放的，无法建立私有通道。

#### 4. 面向对象，敏捷开发

> 通过Binder模糊了进程边界


我们可以将Binder理解为 通信管道的入口，Client 需要通信必须建立通信管道，并且获得通信管道入口。



---

1. [Android Binder设计与实现](http://blog.csdn.net/universus/article/details/6211589)
