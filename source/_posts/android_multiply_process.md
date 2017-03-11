title: Android Binder IPC机制
date: 2015-11-25 23:54:03
permalink: 2015/11/25/android_multiply_process
categories:
- Android机制
tags:
- Android
- 多进程
- Binder
- ServiceManager

---

> IPC方式之一。
> 由OpenBinder演化而来。
> 类似于COM和CORBA分布式组件架构。

<!-- more -->

## I. 出现原因:

- C/S通信模式（除Binder外只有socket支持CS）。
- 有更好的传输性能(1.管道和消息队列，基于存储转发，至少需要两次拷贝; 2.内存共享没有拷贝但是控制机制复杂(多进程pid校验以及多种机制协作))。
- 安全性更好。

#### 1. CS通信方式

> Binder采用Client-Server(文中简称CS)方式。

linux支持通信方式: 消息队列/共享内存/信号量/socket，其中只有socket支持CS。


#### 2. 传输性能

IPC | 特征 | 拷贝次数 | 特点
:-: | :-: | :-: | :-
共享内存 | 控制复杂 | 0 | 极少用
Binder | 简单通用安全|  1 | Android中常用，性能高
Socket/管道/消息队列 | A中缓冲区 --(存储)--> 内核缓冲区 --(转发)--> B中缓冲区 | 2 | socket作为通用接口，传输效率低，开销大，一般用于跨网络的IPC/进程间低速IPC

#### 3. 安全

> 基于Android本身为每个应用分配了独立的UID，使用UID&PID作为进程身份标志

- 传统IPC依赖上层协议确保传入UID，十分危险，Binder支持实名(自身在内核中添加，安全可靠)也支持匿名。
- 传统IPC访问接入点(管道名/system V键值/socket ip地址/文件名)是开放的，无法建立私有通道。

#### 4. 面向对象，敏捷开发

Binder有意模糊了进程边界。在默认的IPC过程中，调用方进程中所在调用接口的线程会被block住等待接口的处理返回，仿佛就在同一个进程中调用接口方法。

## II. 特征

- 不同的应用之间可以通过Binder进行IPC(调用Stub中的相关方法)，只需要在对应的Stub中，复写`onTransact`方法，根据调用者的uid来做权限认证，返回`true`，让其调用成功，否则调用失败。
- 几乎所有系统服务都是通过Binder进行通信: `Telephone`、`Vibrator`、`Wifi`、`Battery`、`Notification`等。
- 几乎所有系统架构都是基于Binder进行通信: `Intent`、`Content Provider`、`Messager`、ActivityManagerServer中处理的各种生命周期(`onStart()`、`onResume()`...)。

### III. 原理

Binder相比一般的IPC而言，只需要一次内存拷贝即可实现数据传递，而这一特性与Binder的实现原理密不可分。


> 同一个物理页面，一方映射到进程虚拟地址空间，一方面映射到内核虚拟地址空间，这样通过指向同一个物理页面的方式，进程和内核之间就可以减少一次内存拷贝。

推荐结合老罗在[浅谈Service Manager成为Android进程间通信（IPC）机制Binder守护进程之路](http://blog.csdn.net/luoshengyang/article/details/6621566) 提到的源码一起分析。

#### 1. Binder驱动程序

- **所在空间**: 内核空间。
- **基本功能**: 提供/dev/binder与用户空间交互。

> 这块也可以结合ActivityManagerService在Activity启动过程中绑定Binder的流程: [ActivityManagerService](http://blog.dreamtobe.cn/2015/11/26/activitymanagerservice/)

##### 设备文件

> `/dev/binder`

在Binder驱动程序模块初始化时创建的。

##### 主入口循环对象

> `bs:binder_state`

句柄为0

##### 文件描述符

> `bs->fd`

打开`/dev/binder`以后获得(对应Binder驱动程序的`binder_open`函数)。

- `O_RDWR/filp`: 类型(file)。
- `filp->private_data`: 类型(binder_proc), 会保存打开设备文件`/dev/binder`的进程的上下文信息。
- 结构`binder_procs`: 全局哈希表(驱动程序内部使用)。

##### 起始地址映射

> `bs->mapped`

把设备文件`/dev/binder`映射到进程空间的起始地址(对应Binder驱动程序的`binder_mmap`函数)。

> 这也是Binder只需要一次拷贝的核心机制: `vma:vm_area_struct`(给进程使用的虚拟地址)与`area:vm_struct`(给内核使用的虚拟地址): 映射了同一个物理页面。

- `filp->private_data->vima`: 类型(vm_area_struct), 映射进程使用的虚拟地址。
- `filp->private_data->buffer`: 类型(area->addr), 映射要映射的物理内存在内核空间的起始位置。
- `filp->private_data->buffer_size`: 类型(size_t), 要映射的物理内存在内核空间的长度。
- `area`: 类型(vm_struct), 给内核使用的虚拟地址。
- `vma`: 类型(vm_area_struct), 给进程使用的虚拟地址。


#### 2. Service Manager

- **所在空间**: 用户空间。
- **基本功能**: 辅助, Binder机制的守护进程用于管理Server、向Client提供查询Server远程接口。

##### 角色:

- Binder机制的守护进程。
- 特殊Server: 启动以后进入无穷循环充当Server，等待Client请求; 特殊之处: 句柄为0(Binder通信机制使用句柄代表远程接口)，其余Server的句柄值皆大于0(由Binder驱动程序自动分配)。

##### 功能:

> 需要和Server已经Client通信。
> PS: Server、Client、ServiceManager分别在不同进程。

- 管理开发者创建的各种Server。
- 向Client提供查询Server远程接口。

##### 启动执行步骤

1. 打开`/dev/binder`文件: `bs->fd = open("/dev/binder", O_RDWR);`
2. 建立128K内存映射: `bs->mapped = mmap(NULL, mapsize, PROT_READ, MAP_PRIVATE, bs->fd, 0);`
3. 通知Binder驱动程序它是守护进程: `binder_become_context_manager(bs);`
4. 进入循环等待请求的到来: `binder_loop(bs, svcmgr_handler);`(此处句柄`svcmgr_handler = BINDER_SERVICE_MANAGER = 0()`)

#### 3. Client与Server

> 对于应用开发者而言，直接接触的是这两Binder架构中的组件。

- **所在空间**: 用户空间。
- **基本功能**: 应用开发人员实现。

##### 通信过程中线程关系

> Client - Proxies (封装调用方法，将对象转为系统可读): 提交处理给Binder内核驱动并且block住 ||| Service - Stubs(Listens): 监听Binder内核驱动并且基于接收的回调反序列化为对象。

> 如果不想被block住，可以通过`IBinder.FLAG_ONEWAY`标记，将会立马完成返回空数据。

##### Client 与 Service通信

Client - `transact()`(block client thread by default) -> Service - `onTransact()`(这个方法在Binder线程执行执行，完成后，unblock client thread)。

> 执行`onTransact()`的Binder线程池最大活动线程数量: 16

![](https://sujaiantony.files.wordpress.com/2011/12/binder_commn.png)
(图片来自:[An Android 101](https://sujaiantony.wordpress.com/2011/12/28/an-android-101-an-overview-on-binder-framework/))


##### Service 与 Client通信

Service - `onTransact()` -> Client - transaction (transaction, 在binder thread)。

> The client will receive the transaction in the thread waiting for the first transaction to be finished rather than a binder thread.

---

本文已经发布到JackBlog公众号，可请直接访问: [Android Binder IPC机制 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483670&idx=1&sn=d9124d91d37fa1ecaf131238bda3fb94)

---

- [Android Binder设计与实现](http://blog.csdn.net/universus/article/details/6211589)
- [快速简单Demo](http://blog.csdn.net/singwhatiwanna/article/details/17041691)
- [浅谈Service Manager成为Android进程间通信（IPC）机制Binder守护进程之路](http://blog.csdn.net/luoshengyang/article/details/6621566)
- [Android进程间通信（IPC）机制Binder简要介绍和学习计划](http://blog.csdn.net/luoshengyang/article/details/6618363)
- [An Overview of Android Binder Framework](http://codetheory.in/an-overview-of-android-binder-framework/)
- [An Android 101 : An overview on Binder framework.](https://sujaiantony.wordpress.com/2011/12/28/an-android-101-an-overview-on-binder-framework/)

---
