title: Looper探底
date: 2017-11-19 22:54:03
updated: 2017-11-19
categories:
- Android机制
tags:
- Looper
- I/O多路复用
- Epoll

---

{% note info %} 之前有整理过一篇[Android Handler Looper机制](https://blog.dreamtobe.cn/2016/03/11/android_handler_looper/)，不过细细想来，其实还是可以再探探底的。{% endnote %}

<!-- more -->

#### 为什么主线程的Looper，"死循环"取消息并不会引发ANR?

因为ANR是主线程中需要处理的各类用户输入，得不到及时响应才被触发。
因此即便`Looper`中只要在有消息需要响应的时候，及时被唤醒响应，便不会存在该问题。

#### Looper是怎么取消息的，采用什么策略?

这个其实在我的[这篇文章](https://blog.dreamtobe.cn/2016/03/11/android_handler_looper/)中有分析到，如下图:

![](/img/android_handler_looper-4.png)

其取消息是通过`MessageQueue#next()`获取的，其出队策略并非始终从队头出。

首先`MessageQueue`的消息在入队的时候，会根据消息所带参数`when`的所代表的时间(单位为毫秒)，进行入队并保持队列按照`when`进行升序排列；

而后出队是与是否存在`Barrier`消息有关:

- 如果存在`Barrier`，`Barrier`之前的任何消息，按照时间升序逐一出队；`Barrier`之后的消息，只有`isAsynchronous()`为`true`的消息才能够按照时间按升序逐一出队
- 如果不存在`Barrier`，任何消息，按照时间升序逐一出队

#### 什么是`Barrier`消息，在Android中有什么应用?

`Barrier`消息是`Message#target`的值为空的消息，通常对上层是隐藏的，我们可以看到`Handler`带有`async`的构造方法是`@hide`的，而`MessageQueue#postSyncBarrier`与`MessageQueue#removeBarrier`都是`@hide`的，而`Message#setAsynchronous`也是在API22之后才对外开放。


#### Looper中是怎样进行休眠的，何时被唤醒？

休眠过程:

```java
// MessageQueue.java
Message next() {
  ...
  for(;;) {
    ...
    nativePollOnce(ptr, nextPollTimeoutMillis)
    ...
  }
}
```

```C++
// android_os_MessageQueue.cpp
// https://android.googlesource.com/platform/frameworks/base/+/master/core/jni/android_os_MessageQueue.cpp
void NativeMessageQueue::pollOnce(JNIEnv* env, jobject pollObj, int timeoutMillis) {
    ...
    mLooper->pollOnce(timeoutMillis);
    ...
}
```

```C++
// Looper.h
// https://android.googlesource.com/platform/frameworks/native/+/jb-dev/include/utils/Looper.h
inline int pollOnce(int timeoutMillis) {
    return pollOnce(timeoutMillis, NULL, NULL, NULL);
}
```

```C++
// Looper.cpp
// https://android.googlesource.com/platform/frameworks/native/+/jb-dev/libs/utils/Looper.cpp

...
Looper::Looper(bool allowNonCallbacks) :
        mAllowNonCallbacks(allowNonCallbacks), mSendingMessage(false),
        mResponseIndex(0), mNextMessageUptime(LLONG_MAX) {
    int wakeFds[2];
    int result = pipe(wakeFds); // 创建管道
    ...
    mWakeReadPipeFd = wakeFds[0]; // 管道的读端文件描述符
    mWakeWritePipeFd = wakeFds[1]; // 管道的写端文件描述符
    ...
    // Allocate the epoll instance and register the wake pipe.
    mEpollFd = epoll_create(EPOLL_SIZE_HINT); // 创建epoll实例并获得其文件描述符
    ...
    result = epoll_ctl(mEpollFd, EPOLL_CTL_ADD, mWakeReadPipeFd, & eventItem); // 开始监控管道读端事件
    ...
}

...
int Looper::pollOnce(int timeoutMillis, int* outFd, int* outEvents, void** outData) {
    int result = 0;
    for (;;) {
        ...// 由于outFd，outEvents, outDAta
        result = pollInner(timeoutMillis);
    }
}

...
int Looper::pollInner(int timeoutMillis) {
    ...
    // 进入等待epoll的事件通知
    int eventCount = epoll_wait(mEpollFd, eventItems, EPOLL_MAX_EVENTS, timeoutMillis);
    ...
}
```

唤醒过程:

```java
// MessageQueue.java
boolean enqueueMessage(Message msg, long when) {
  ...
  if (needWake) {
    nativeWake(mPtr);
  }
}
```

```c++
// android_os_MessageQueue.cpp
// https://android.googlesource.com/platform/frameworks/base/+/master/core/jni/android_os_MessageQueue.cpp
void NativeMessageQueue::wake() {
    mLooper->wake();
}
```

```c++
// Looper.cpp
// https://android.googlesource.com/platform/frameworks/native/+/jb-dev/libs/utils/Looper.cpp

void Looper::wake() {
    ssize_t nWrite;
    do {
        nWrite = write(mWakeWritePipeFd, "W", 1); // 在管道写端写入一个新的字符'W'，让其可读
    } while (nWrite == -1 && errno == EINTR);
    if (nWrite != 1) {
        if (errno != EAGAIN) {
            ALOGW("Could not write wake signal, errno=%d", errno);
        }
    }
}

// 前面休眠最后到这个方法
int Looper::pollInner(int timeoutMillis) {
    ...
    // 等待epoll的事件通知，由于写入了新的内容，因此被唤醒并返回可读事件数目
    int eventCount = epoll_wait(mEpollFd, eventItems, EPOLL_MAX_EVENTS, timeoutMillis);
    ...
    for (int i = 0; i < eventCount; i++) {
        ...
        if (fd == mWakeReadPipeFd) { // 是管道的读端被唤醒
            if (epollEvents & EPOLLIN) { // 是可读事件
                awoken(); // 到这里是已经唤醒了，因此只是将管道中的数据读完，也就消费完可读事件
            } else {
                ALOGW("Ignoring unexpected epoll events 0x%x on wake read pipe.", epollEvents);
            }
        } else { // 不是管道的读端被唤醒
          ...
        }
    }
    ...
}

...
void Looper::awoken() {
    char buffer[16];
    ssize_t nRead;
    do {
        nRead = read(mWakeReadPipeFd, buffer, sizeof(buffer));
    } while ((nRead == -1 && errno == EINTR) || nRead == sizeof(buffer));
}

```

#### 什么是I/O多路复用?

也被称为"事件驱动"，如Looper中采用的`epoll`系统调用函数来使用该功能，休眠与唤醒当前Looper所在线程。

除了`epoll`外还有`select`、`poll`、`kqueue`等函数可以用来实现I/O多路复用，这里的"复用"指的是复用同一个线程，因为正常的I/O操作，是会阻塞住当前线程直到缓冲区中有数据，因此会霸占整个线程，而I/O多路复用则是通过同时监听多个描述符的读写就绪情况，配合非阻塞的socket使用时，每次都是系统通知描述符可读时，才去执行有效的`read`操作，让多个描述符的I/O操作都能够在一个线程内并发交替地顺序完成。


#### 存在Looper的线程都是常驻线程?

对的


---

更多疑惑，欢迎评论讨论。

---

- [I/O多路复用技术（multiplexing）是什么？](https://www.zhihu.com/question/28594409)
- [Looper中的睡眠等待与唤醒机制](http://shangjin615.iteye.com/blog/1778615)
