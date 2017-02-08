title: Android AIDL 通信与回调
date: 2013-12-14 08:35:03
permalink: 2013/12/14/Android-AIDL-通信与回调
tags:
- AIDL
- 通信
- Android

---

> 测试源码已经更新到GitHub: AIDL_COMMUNICATE-CALLBACK 感兴趣的同学的下载看看。

### 本项目主要在于学习Android中通过AIDL完成进程间通信与回调。
    项目组成：AIDL_SERVICE_LIB[库项目]、AIDL_CLIENT。

<!--more-->

### 那么主要的需要实现的功能通过几个AIDL文件就可以获知:

### IAIDLService.aidl:
    package cn.dreamtobe.aidl.service;
    import cn.dreamtobe.aidl.service.Book;
    import cn.dreamtobe.aidl.service.IServiceCallback;
    interface IAIDLService{
    int getCount();
    Book getBook();
    boolean startTestTask();
    void stopTestTask();
    void registerCallback(IServiceCallback paramIServiceCallback);
    void unregisterCallback(IServiceCallback paramIServiceCallback);
    }

### IServiceCallback.aidl:
    package cn.dreamtobe.aidl.service;
    import cn.dreamtobe.aidl.service.Book;
    interface IServiceCallback {
    void handlerCommEvent(int msgId, int param);
  	void callbackBookEvent(int cmd, in Book book);
    }

###     
 最终目的是需要跨进程，AIDLService通过回调通知AIDLClient处理并传递有关值，并且AIDLClient可以通过AIDLService中定义好的AIDL有关方法，进行通知或取值。

![image](https://github.com/Jacksgong/AIDL_COMMUNICATE-CALLBACK/raw/master/aidl_readme/raw/com_task.png)
![image](https://github.com/Jacksgong/AIDL_COMMUNICATE-CALLBACK/raw/master/aidl_readme/raw/bind_succeed.png)
![image](https://github.com/Jacksgong/AIDL_COMMUNICATE-CALLBACK/raw/master/aidl_readme/raw/unbind.png)
![image](https://github.com/Jacksgong/AIDL_COMMUNICATE-CALLBACK/raw/master/aidl_readme/raw/unbind_request.png)

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
