
title: Android多进程
date: 2015-11-25 23:54:03
tags:
- Android
- 多进程
- Binder
- ServiceManager

---
## I. Binder

> IPC方式之一
> 由OpenBinder演化而来
> 类似于COM和CORBA分布式组件架构

<!-- more -->

### 出现原因:

#### 1. CS通信方式

> Binder采用Client-Server方式

linux支持通信方式:消息队列/共享内存/信号量/socket，其中只有socket支持CS


#### 2. 传输性能

IPC | 特征 | 拷贝次数 | 特点
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


## 注意

- 如果需要其他apk也可以调用AIDL来通信(调用Stub中的相关方法)，只需要在对应的Stub中，复写`onTransact`方法，根据调用者的uid来做权限认证，返回true，让其调用成功，否则调用失败。
- 几乎所有系统服务都是通过Binder进行通信: `Telephone`、`Vibrator`、`Wifi`、`Battery`、`Notification`等
- 几乎所有IPC架构都是基于Binder: `Intent`、`Content Provider`、`Messager`、ActivityManagerServer中处理的各种生命周期(`onStart()`、`onResume()`...)

### 通信过程中线程关系

> Client - Proxies (封装调用方法，将对象转为系统可读): 提交处理给Binder内核驱动并且block住 ||| Service - Stubs(Listens): 监听Binder内核驱动并且基于接收的回调反序列化为对象

> 如果不想被block住，可以通过`IBinder.FLAG_ONEWAY`标记，将会立马完成返回空数据

#### 1. Client 与 Service通信

Client - `transact()`(block client thread by default) -> Service - `onTransact()`(这个方法在Binder线程执行执行，完成后，unblock client thread)

执行`onTransact()`的Binder线程池最大活动线程数量: 16

![](https://sujaiantony.files.wordpress.com/2011/12/binder_commn.png)

图片来自: [An Android 101](https://sujaiantony.wordpress.com/2011/12/28/an-android-101-an-overview-on-binder-framework/)


#### 2. Service 与 Client通信

Service - `onTransact()` -> Client - transaction (transaction, 在binder thread)

> The client will receive the transaction in the thread waiting for the first transaction to be finished rather than a binder thread

#### 优点:

- C/S通信模式（除Binder外只有socket支持j）
- 有更好的传输性能(相比socket等，而管道和消息队列，基于存储转发，至少需要两次拷贝，而内存共享没有拷贝但是控制机制复杂(多进程pid校验以及多种机制协作))
- 安全性更好

### 高效的基本原理

#### 基本原理

相比一般的IPC而言，只需要一次内存拷贝即可实现数据传递

#### 根本原理

> 基于Service Manager与 Binder驱动程序
> 同一个物理页面，一方映射到进程虚拟地址空间，一方面映射到内核虚拟地址空间，这样，进程和内核之间就可以减少一次内存拷贝了，提到了进程间通信效率。


- 设备文件: /dev/binder，在Binder驱动程序模块初始化时创建的

- 主入口循环对象: `bs:binder_state`, 句柄0
`bs->fd`: 文件描述符: 打开/dev/binder以后获得(对应Bindr驱动程序的`binder_open`函数)
`bs->mapped`: 把设备文件/dev/binder映射到进程空间的起始地址(对应Binder驱动程序的`binder_mmap`函数)

##### Service Manager执行基本步骤

1. 打开/dev/binder文件: `bs->fd = open("/dev/binder", O_RDWR);`
2. 建立128K内存映射: `bs->mapped = mmap(NULL, mapsize, PROT_READ, MAP_PRIVATE, bs->fd, 0);`
3. 通知Binder驱动程序它是守护进程: `binder_become_context_manager(bs);`
4. 进入循环等待请求的到来: `binder_loop(bs, svcmgr_handler);`(此处句柄svcmgr_handler = BINDER_SERVICE_MANAGER = 0())

##### bs->fd赋值过程:

> 打开/dev/binder

以下两个变量存储**打开设备文件/dev/binder的进程**的上下文信息

- `filp->private_data`
- 全局哈希表`binder_proces`(驱动程序内部使用)

##### bs->mapped赋值过程:

> 内存映射
> `vma:vm_area_struct`(给进程使用的虚拟地址)与`area:vm_struct`(给内核使用的虚拟地址): 映射了同一个物理页面


- `flip->private_data->vima` 映射: 进程使用的虚拟地址
- `flip->private_data->buffer` 映射: 要映射的物理内存在内核空间的起始位置
- `flip->private_data->buffer_size` : 要映射的物理内存在内核空间的长度


##### 附录:

变量名 | 类型 | 备注
:-: | :-: | :- |
O_RDWR/flip | file | -
filp->private_data | binder_proc | 会保存 打开设备文件/dev/binder的进程 的上下文信息
flip->private_data->vima | vm_area_struct | 进程使用的虚拟地址
flip->private_data->buffer | area->addr | 要映射的物理内存在内核空间的起始位置
area | vm_struct | 给内核使用的虚拟地址
vma | vm_area_struct | 给进程使用的虚拟地址

### 架构

- Client
- Server
- Service Manager
- 驱动程序

#### 聊聊ServiceManager

##### 角色:

- Binder机制的守护进程
- 特殊Server: 启动以后进入无穷循环充当Server，等待Client请求; 特殊之处: 句柄为0(Binder通信机制使用句柄代表远程接口)，其余Server的句柄值皆大于0(由Binder驱动程序自动分配)

##### 功能:

> 需要和Server已经Client通信
> PS: Server、Client、ServiceManager分别在不同进程

- 管理开发者创建的各种Server
- 向Client提供查询Server远程接口


组件名 | 所在空间 | 基本功能
:-: | :-: | :-: |
Client | 用户空间 | 开发人员实现
Server | 用户空间 | 开发人员实现
Service Manager | 用户空间 | 辅助: Binder机制的守护进程用于管理Server、向Client提供查询Server远程接口
驱动程序 | 内核空间 | 提供/dev/binder与用户空间交互


---

- [Android Binder设计与实现](http://blog.csdn.net/universus/article/details/6211589)
- [快速简单Demo](http://blog.csdn.net/singwhatiwanna/article/details/17041691)
- [浅谈Service Manager成为Android进程间通信（IPC）机制Binder守护进程之路](http://blog.csdn.net/luoshengyang/article/details/6621566)
- [Android进程间通信（IPC）机制Binder简要介绍和学习计划](http://blog.csdn.net/luoshengyang/article/details/6618363)
- [An Overview of Android Binder Framework](http://codetheory.in/an-overview-of-android-binder-framework/)
- [An Android 101 : An overview on Binder framework.](https://sujaiantony.wordpress.com/2011/12/28/an-android-101-an-overview-on-binder-framework/)
