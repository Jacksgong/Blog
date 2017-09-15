title: OkHttp3 整体架构分析
date: 2017-09-15 20:31:03
updated: 2017-09-15
categories:
- 架构
tags:
- OkHttp3

---

{% note info %}除了[Okhttp3](https://github.com/square/okhttp)在网络应用层方面的各类优化，支持SPDY/HTTP2(关于SPDY与HTTP2的特性可以参考[这篇文章](https://blog.dreamtobe.cn/network_basic/))以及其健壮性以外，对于Okhttp3简单清新、灵活健壮、可测试性的架构也早有耳闻，今天我们通读源码，通过图形，将他们都梳理出来，看看其优在何处。{% endnote %}

<!-- more -->

## I. 主框架分析


我们都知道在OkHttp3中，其灵活性，很大程度上体现在，我们可以`intercept`其任意一个环节，而这个优势便是okhttp3整个请求响应架构体系的精髓所在:

- 在OkHttp3中，每一个请求任务都封装为一个`Call`，其实现为`RealCall`。
- 而所有的策略几乎都可以通过`OkHttpClient`传入
- 所有全局策略与数据，除了存储在允许上层访问的`OkHttpClient`实例以外，还有一部分是存储在只允许包可见的`Internal.instance`中（如连接池、路由黑名单等)
- OkHttp中用户可传入的`interceptor`分为两类，一类是全局`interceptor`，该类`interceptor`在请求开始之前最早被调用，另外一类为非网页请求的`networkInterceptor`，这类`interceptor`只有在非网页请求中会被调用，并且是在组装完成请求之后，真正发起请求之前被调用(这块具体可以参看`RealCall#getResponseWithInterceptorChain()`方法)
- 整个请求过程通过递归`RealInterceptorChain#proceed`来实现，在每个`interceptor`中调用递归到下一个`interceptor`来完成整个请求流程，并且在递归回到当前`interceptor`后完成响应处理
- 在异步请求中，我们通过`Callback`来获得简单清晰的请求回调(`onFailure`、`onResponse`)
- 但是在`OkHttpClient`中，我们可以传入`EventListener`的工厂方法，为每一个请求创建一个`EventListener`，来接收非常细的事件回调

![](/img/okhttp3-call-flowchart.png)

#### 连接池

我们知道在OkHttp3存在连接池，并且该连接池是通过与`StreamAllocation`的配合完成连接池的维护。

- 所有的请求连接都会通过`StreamAllocation`进行获得，并且结合`ConnectionPool`进行引用计数，来有效缓存连接
- 而在`StreamAllocation`中，通过`RouteSelector`来根据请求地址进行路由处理，期间就涉及到了`DNS解析`、`协议处理`、`代理选择`、`签名校验`等

默认连接池策略:

- 最多64个请求
- 同一个host最多5个请求
- 连接最长闲置5分钟
- 异步连接所在线程池名: `OkHttp Dispatcher`
- 常驻清理连接线程池: `OkHttp ConnectionPool`

![](/img/okhttp3-obtain-conneciton.png)
<p style="text-align: center;">获得连接</p>

![](/img/okhttp3-connecitonpool-maintain.png)
<p style="text-align: center;">连接池</p>

## II. 各类线程池分析

OkHttp中的对所有的任务采用`NamedRunnable`，与我开源的[ThreadDebugger](https://github.com/Jacksgong/ThreadDebugger)中通过架构层面约束，让每个执行单元给出对应的业务名称，以便于线程维护不谋而合。关于Android中`ThreadPoolExecutor`的机制，可以看我之前写的[这篇文章](https://blog.dreamtobe.cn/thread-pool/)。

#### 1. 异步请求线程池

该线程池名`OkHttp Dispatcher`，该线程用于执行异步的请求任务。

- 该线程池本身: 无任务上限，自动回收闲置60s的线程
- 但是`Dispatcher`中在进口进行把关控制，默认情况下保证在当前进程中`OkHttpClient`最多只有64个请求，池子中相同host的请求不超过5个
- 架构上通过两个双端队列(`readyAsyncCalls:Deque<AsyncCall>`与`runningAsyncCals:Dequeue<AsyncCall>`)分别用于维护等待中的任务与运行中的任务
- 在每一个异步任务后，都会检查一遍`readyAsyncCalls`，在满足条件下，将最先进入队列的任务丢入该线程池进行执行

![](/img/okhttp3-dispatcher-threadpool.png)

#### 2. 连接池清理线程池

该线程池名`OkHttp ConnectionPool`，该线程用于自动清理长时间闲置或泄漏的连接。

- 该线程本身: 无任务上限，自动回收闲置60s的线程
- 但是`ConnectionPool`中通过一个`cleanupRunning`的标记，控制当前仅有一个清理任务进入队列
- 清理任务，会不断清理，在所有需要清理的连接都清理完成后，会计算出最近一次需要清理的时间并阻塞，不断清理直到连接池中没有任何连接，方才结束
- 在每次有连接加入连接池时，如果当前没有清理任务运行，会加入一个清理任务到清理线程池中执行

![](/img/okhttp3-connectionpool-threadpool.png)

#### 3. 缓存整理线程池

该线程池名`OkHttp DiskLruCache`，该线程池用于整理本地请求结果的缓存。

- 该线程池本身: 最多1个运行中线程，其余任务会阻塞住等待，回收闲置60s的线程
- 由于可运行仅为一个线程，因此所有操作无需考虑线程安全问题
- 缓存的整理包含: 达到阀值大小的文件，删除最近最少使用的记录；在有关操作达到一定数量以后对记录进行重建

![](/img/okhttp3-disklrucache-threadpool.png)

#### 4. HTTP2异步事务线程池

该线程池名`OkHttp Http2Connection`，我们都知道HTTP2采用了多路复用(相关知识可以翻看[这篇](https://blog.dreamtobe.cn/network_basic/)文章)，因此需要维护连接有效性，本线程池就是用于维护相关的各类HTTP2事务

- 该线程池本身: 无任务上限，自动回收闲置60s的线程
- 每一个HTTP2连接都有这么一个线程池存在

![](/img/okhttp3-http2connection-threadpool.png)

---

回望[FileDownloader](https://github.com/lingochamp/FileDownloader)，有一个极大的痛点是，在最早其就引入了多进程，虽然在后期实现了单进程与多进程的切换，但是整套体系不得不为该多进程买单，极大的增加了相关的复杂度，以及无法轻量的同步回调。如果让我再写一个下载引擎，我也许也会考虑分拆各个模块，让核心代码保持充分的简单，也让每个模块足够单一。

---
