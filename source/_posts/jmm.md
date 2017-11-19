title: Java(JVM) 内存模型与内存管理
date: 2017-11-19 17:45:03
updated: 2017-11-19
categories:
- 编程语言
tags:
- JVM
- Java
- GC

---

{% note info %} 我们知道Java最大的特性之一就是其运行的虚拟机环境通过内存模型与管理拥有自动垃圾回收机制，今天我们就看看该模型与如果通过该模型实现垃圾回收机制的。{% endnote %}

<!-- more -->

#### 内存模型

![](/img/jmm-1.png)
<p style="text-align: center;">上图来自[Java (JVM) Memory Model](https://www.journaldev.com/2856/java-jvm-memory-model-memory-management-in-java)</p>

![](/img/jmm-2.png)

> 分为年轻代空间与老年代空间的最直接的原因是: 通常很多新对象一创建就被释放，而很多生命周期较长的对象创建后会不断的被保留。

如上图所示，Java内存模型包含三部分:

> 根据不同的虚拟机，Memory Pool有可能存在Java Heap，也可能存在Perm Gen中，用于存储不可变的对象，如String

- `Java Heap`: 包含年轻代与老年代两个内存空间，几乎所有的创建的对象都存储在这里
- `Perm Gen` : 包含永久代内存空间，用于存储运行时的类、常量、静态变量以及方法代码、ClassLoader
- `Java Stack` : 每个线程启动时，都会创建一个自己的Java Stack，用于存储运行堆栈，以及原始类型临时变量，以及线程中用到的对象的引用

#### 内存管理的各类GC

关于单个GC(通常分为三步: 1标记出需要被回收的对象、2回收被标记的对象空间、3将回收的所有对象空间移动为连续的内存块便于分配给新的对象)具体流程，可以参照: [Android GC](https://blog.dreamtobe.cn/2015/11/30/gc/)

![](/img/jmm-3.jpg)
<p style="text-align: center;">上图来自[Minor GC vs Major GC vs Full GC](https://www.javacodegeeks.com/2015/03/minor-gc-vs-major-gc-vs-full-gc.html)</p>

![](/img/jmm-4.png)

如上图所示，常见的GC包含三类GC:

##### `Minor GC`

清理年轻代内存空间中的短生命周期对象，在年轻代空间中的短生命周期的对象在被Minor GC一定轮数后，会被转入老年代空间，判断为长生命周期对象。这类GC由于绝大多数都是短生命周期的对象，因此通常处理是很快的，因此其`Stop the World`操作带来的影响很小。在Eden内存空间满时被促发。

##### `Major GC`

清理老年代内存空间，老年代空间中的对象都是相对长生命周期的对象，因此处理起来相对耗时。

##### `Full GC`

将清理年轻代、老年代、永久代所有内存空间的对象，这也是为什么静态对象可能被回收。

---

- [Java (JVM) Memory Model – Memory Management in Java](https://www.journaldev.com/2856/java-jvm-memory-model-memory-management-in-java)
- [Minor GC vs Major GC vs Full GC](https://www.javacodegeeks.com/2015/03/minor-gc-vs-major-gc-vs-full-gc.html)
