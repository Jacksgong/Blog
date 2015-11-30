title: Android GC
date: 2015-11-30 09:00:03
tags:
- GC
- Concurrent GC
- Activity Heap
- Zygote Heap
- Mark-Sweep

---

> Dalvik虚拟机Gc与ART运行时GC采用同一套机制

## Heap分布

Heap名 | 分布 | 内容
:-: | :-: | :-: |
Activity Heap | 第一个应用程序fork前，未使用的部分 | 第一个应用fork开始后，无论是Zygote进程，还是应用进程，分配的对象
Zygote Heap | 第一个应用程序fork前，已经使用的部分 | Zygote进程在启动过程中加载的类、资源、对象


<!-- more -->

## 资源回收:

#### Dalvik虚拟机中的堆:

> 匿名共享内存

不直接管理，封装成mspace交给C库来管理

#### Heap Bitmap

描述对象有没有被引用的数据结构

### Mark-Sweep算法

#### 1. Mark阶段

从对象的根集开始标记**被引用**的对象

##### 一般算法

> Stop The World

除垃圾收集线程之外，其他线程都停止，否则可能导致不能正确标记每一个对象

##### 并行垃圾收集算法

> Concurrent GC
> 有条件地允许程序的其他线程执行

分为两个阶段:

1. 只负责标记根集对象(GC开始的瞬间给，被全局变量、栈变量和寄存器等引用的对象): **Stop The World**
2. 顺着已标记的根集对象找到其余的被引用的变量: **允许除垃圾收集线程以外的线程运行**，但是需要由Card Table(一字节CLEAN/DIRTY)记录**在该过程中被修改的对象**(非垃圾收集堆对象 对 垃圾收集堆对象 的引用 -> 由于 Dalvik虚拟机进行部分垃圾收集时，只收集Activie堆上分配的对象 -> Zygote堆上分配的对象 在 部分垃圾收集执行过程中 对 在 Active堆上分配的对象的引用)

#### 2. Sweep阶段

回收没有被标记的对象占用的内存


---

- [Dalvik虚拟机垃圾收集机制简要介绍和学习计划](http://blog.csdn.net/luoshengyang/article/details/41338251)
