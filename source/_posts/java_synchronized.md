title: Java Synchronised机制
date: 2015-11-13 21:14:03
updated: 2015-11-13 21:14:03
permalink: 2015/11/13/java_synchronized
wechatmptitle: Java Synchronized机制与常见的多线程抢占
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483673&idx=1&sn=cc20b1149e9ffed649dd00d8737e6a08
categories:
- Android机制
tags:
- Android
- JDK
- Java
- Synchronized
- 同步
- 偏向锁
- 轻量级锁
- 重量级锁
- 自旋

---

> Java中锁的控制可以参看这篇文章: [Java多线程抢占](http://blog.dreamtobe.cn/2015/03/25/Java多线程抢占/)。

## I. 原末

#### 矛盾1:

**A**: 重量级锁中的阻塞(挂起线程/恢复线程): 需要转入内核态中完成，有很大的性能影响。

**B**: 锁大多数情况都是在很短的时间执行完成。

**解决方案**: 引入轻量锁(通过自旋来完成锁竞争)。

<!-- more -->

#### 矛盾2:

**A**: 轻量级锁中的自旋: 占用CPU时间，增加CPU的消耗(因此在多核处理器上优势更明显)。

**B**: 如果某锁始终是被长期占用，导致自旋如果没有把握好，白白浪费CPU资源。

**解决方案**: JDK5中引入默认自旋次数为10(用户可以通过`-XX:PreBlockSpin`进行修改)， JDK6中更是引入了自适应自旋（简单来说如果自旋成功概率高，就会允许等待更长的时间（如100次自旋），如果失败率很高，那很有可能就不做自旋，直接升级为重量级锁，实际场景中，HotSpot认为最佳时间应该是一个线程上下文切换的时间，而是否自旋以及自旋次数更是与对CPUs的负载、CPUs是否处于节电模式等息息相关的)。

#### 矛盾3:

**A**: 无论是轻量级锁还是重量级锁: 在进入与退出时都要通过CAS修改对象头中的`Mark Word`来进行加锁与释放锁。

**B**: 在一些情况下总是同一线程多次获得锁，此时第二次再重新做CAS修改对象头中的`Mark Word`这样的操作，有些多余。

**解决方案**: JDK6引入偏向锁(首次需要通过CAS修改对象头中的`Mark Word`，之后该线程再进入只需要比较对象头中的`Mark Word`的Thread ID是否与当前的一致，如果一致说明已经取得锁，就不用再CAS了)。

#### 矛盾4:

**A**: 项目中代码块中可能绝大情况下都是多线程访问。

**B**: 每次都是先偏向锁然后过渡到轻量锁，而偏向锁能用到的又很少。

**解决方案**: 可以使用`-XX:-UseBiasedLocking=false`禁用偏向锁。

#### 矛盾5:

**A**: 代码中JDK原生或其他的工具方法中带有大量的加锁。

**B**: 实际过程中，很有可能很多加锁是无效的(如局部变量作为锁，由于每次都是新对象新锁，所以没有意义)。

**解决方法**: 引入锁削除(虚拟机即时编译器(JIT)运行时，依据逃逸分析的数据检测到不可能存在竞争的锁，就自动将该锁消除)。

#### 矛盾6:

**A**: 为了让锁颗粒度更小，或者原生方法中带有锁，很有可能在一个频繁执行(如循环)中对同一对象加锁。

**B**: 由于在频繁的执行中，反复的加锁和解锁，这种频繁的锁竞争带来很大的性能损耗。

**解决方法**: 引入锁膨胀(会自动将锁的范围拓展到操作序列(如循环)外, 可以理解为将一些反复的锁合为一个锁放在它们外部)。


## II. 基本原理

JVM会为每个对象分配一个`monitor`，而同时只能有一个线程可以获得该对象`monitor`的所有权。在线程进入时通过`monitorenter`尝试取得对象`monitor`所有权，退出时通过`monitorexit`释放对象`monitor`所有权。

> `monitorenter`与`monitorexit`在编译后对称插入代码。

- `monitorenter`: 被插入到同步代码块之前。
- `monitorexit`: 被插到同步代码块之后或异常处。


#### 1. 相关数据存在哪里?

对象头。

##### 对象头结构:
> 数组会多1字宽(32位: 4字节)来存储数组长度

长度 | 内容 | 说明
-|-|-
1字宽 | Mark Word | 存储对象的hashCode或锁信息等
1字宽 | Class Metadata Address | 存储对象类型数据的指针
1字宽 | Array length | 数组长度(如果是数组对象)

而对象的锁，一般只和`Mark Word`有关。

#### 2. 各个锁的关系以及升级情况?

> 锁升级是单向的: 无锁 -> 偏向锁 -> 轻量级锁 -> 重量级锁

![](/img/java_synchronized.png)

## III. 多线程下数据同步

> 这类锁/关键字主要是为了维护数据在高并发情况下的一致性/稳定性。

### 1. 数据库中的锁

#### 共享锁(Share Lock)

> 又称为读锁

多个线程可并发的获得某个数据的共享锁锁，并行读取数据。在数据存在共享锁期间，不能修改数据，不能加排他锁。

> 如MySQL中，在查询语句最后加上`LOCK IN SHARE MODE`。

#### 排他锁(eXclusive Lock)

> 又称为写锁

同能只能有一个线程可以获得某个数据的排他锁。在线程获取排他锁后，该线程可对数据读写，但是其他线程不能对该数据添加任何锁。

### 2. `volatile`

> 如果一个共享变量被声明成`volatile`，java线程内存模型将会确保所有线程看到这个变量的值是一致的。

- **基本策略**: 写操作时，会有`Lock`前缀指定，处理器会立马将修改直接写回系统内存，并且其他处理器会将该值在其上的高速缓存标为无效。
- **可能带来的性能消耗**: 写操作实时写回内存，锁总线/锁内存。
- **优势**: 一些场景上相比`synchronized`，执行成本更低(不会引起线程上下文切换以及调度)，使用更方便。

---

- [Java的多线程机制系列：(三）synchronized的同步原理](http://www.cnblogs.com/mengheng/p/3491304.html)
- [再说 lock-free 编程](http://www.cnblogs.com/lucifer1982/archive/2009/04/08/1431992.html)
- [聊聊并发（一）——深入分析Volatile的实现原理](http://www.infoq.com/cn/articles/ftf-java-volatile)
- [聊聊并发（二）——Java SE1.6中的Synchronized](http://www.infoq.com/cn/articles/java-se-16-synchronized)
- [深入JVM锁机制1-synchronized](http://blog.csdn.net/chen77716/article/details/6618779)
- [虚拟机中的锁优化简介（适应性自旋/锁粗化/锁削除/轻量级锁/偏向锁）](http://icyfenix.iteye.com/blog/1018932)
- [Java偏向锁实现原理(Biased Locking)](http://my.oschina.net/u/140462/blog/490897)
- [JVM内部细节之二：偏向锁（Biased Locking）](http://www.cnblogs.com/javaminer/p/3892288.html)
- [java锁优化](http://luojinping.com/2015/07/09/java锁优化/)
- [Java锁Synchronized之偏向锁](http://blog.sina.com.cn/s/blog_c038e9930102v2hs.html)
- [MySQL中的共享锁与排他锁](http://www.hollischuang.com/archives/923)

---
