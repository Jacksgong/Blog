title: MessageHandler
date: 2016-01-16 17:36:03
permalink: 2016/01/16/message_handler
categories:
- 开源项目
tags:
- Handler
- Message
- Thread safe
- recycle
- project

---

> 已开源 [Jacksgong/MessageHandler](https://github.com/Jacksgong/MessageHandler)

- [版本迭代日志](https://github.com/Jacksgong/MessageHandler/blob/master/CHANGELOG.md)
- [中文说明文档](https://github.com/Jacksgong/MessageHandler/blob/master/README-zh.md)
- [问题讨论区](https://github.com/Jacksgong/MessageHandler/issues)

<!-- more -->

---

这个组件是一个简单小巧的Handler转发，主要是为了对外提供绑定目标Handler对象的所有消息的`暂停`、`恢复`、`废弃`、`取消所有队列中的消息`，用于整个完全解耦消息队列的全局性有效管理。

---

> 随着RxJava的普及，逐渐有一些文章出来，提出了EventPool/Handler这些抛事件的架构已死或不建议使用的说法，而无非就是不易于调试，不够灵活。

> 个人觉得确实很多事务用RxJava可以解决。但是就解耦，全局的大架构，还是这类抛事件的更易于阅读代码更加干净，甚至更易于全局性控制。
如Picasso，业务非常的复杂，因此内部使用了Handler抛事件的方式来促使事务流的运作。


## 简述所解决问题

系统提供的Handler用于解决跨线程抛消息，复杂的事务流固然方便，但是缺少全局性的控制，如暂停，恢复等，故有了这个基于`android.os.Handler`进行上层封装转发实现全局控制功能的组件。

## Demo

![][demo_gif]

[license_2_svg]: https://img.shields.io/hexpm/l/plug.svg
[bintray_svg]: https://api.bintray.com/packages/jacksgong/maven/MessageHandler/images/download.svg
[bintray_url]: https://bintray.com/jacksgong/maven/MessageHandler/_latestVersion
[demo_gif]: https://github.com/Jacksgong/MessageHandler/raw/master/art/demo.gif
