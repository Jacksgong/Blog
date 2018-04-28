title: QUIC协议
date: 2017-04-21 18:11:03
wechatmpurl: https://mp.weixin.qq.com/s/hzwsHiwi55JZkOpKZaw8pA
wechatmptitle: TCP窗口
updated: 2018-04-28
categories:
- 网络
tags:
- quic
- udp

---

{% note info %} 这块资料是在2017年年初整理的，当时在支付宝网络组忙于各类学习很多整理后的没有发布出来，前几天参加InfoQ，听了一场QUIC相关的分享，故重新拾起进行整理。{% endnote %}

<!-- more -->

> 基于UDP搭建起来的稳定的快速的协议(内置TLS与相关TCP的活)
> 目前Youtube，Google，Google Photos等都已经在使用QUIC
> 社区: https://groups.google.com/a/chromium.org/forum/#!forum/proto-quic
> 实验教程: https://www.chromium.org/quic/playing-with-quic

## I. 起因

一般的稳定网络传输都是通过TCP，但是在网络基建本身就已经越来越完善的情况下，TCP设计本身的问题便暴露了出来，特别是在弱网环境下，让我们不得不考虑一些新的可能性。

### 1. TCP协议连接建立的成本较高

需要三次握手(如果需要提高数据交互的安全性，还需要增加传输层安全协议(TLS)，就需要更多握手)，(TCP慢启动机制)

![](/img/quic-1.png) ![](/img/quic-2.png)

### 2. TCP快速打开(TCF)由于存在漏洞，未被广泛使用

由于它未考虑安全原因而存在漏洞，所以未被广泛使用。

> TFO是对TCP连接的一种简化握手手续的拓展，提高两端的打开速度。通过SYN包中的`TFO cookie`来验证之前连接过的客户端，如果验证通过，在三次握手最终的ACK包收到之前就开始发送数据。

### 3. UDP不可靠

由于UDP协议只负责发数据，并没有进行确保验证，因此不可靠。

### 4. SPDY基于TCP还有很多消耗

虽然SPDY也采用了多路复用，并且对请求头进行压缩等各类优化，但是由于其基于TCP因此还存在以下问题:

1. 由于TCP所带来的各类消耗（如建连握手等）
2. 由于TCP是实现在操作系统内核中，因此难以普及与控制
3. 相比多个HTTP连接包含多个阻塞窗口 ，TCP的单个阻塞窗口也使得SPDY无法发挥。
TCP连接中一个丢包会阻塞那个连接上所有的多路复用的SPDY流
4. 多个并行的HTTP连接中单个丢包只会阻塞1个连接
5. 基于UDP，QUIC可以支持无序的递交，因此通常单个丢包最多只会影响1个流。并且我们希望权衡QUIC中单独的阻塞窗口来更好的适配一批多路复用的连接

## II. 什么是QUIC

> - QUIC(Quick UDP Internet Connections)，发音同`quick`
> - QUIC是Google设计的实验性的传输层网络协议
> - 开源
> - Chrome中默认打开(2013年8月20日开始成为Chromium的一部分)

QUIC协议十分类似`TCP+TLS+HTTP/2`的实现，不同的是:

1. 很大程度减少了建连所需时间
2. 提高了拥塞控制
3. 多路复用，并且单个丢包最多只会影响1个流
4. 前向错误修正
5. 连接迁移

### 1. 目的

- 尽可能的接近独立的TCP连接的同时，降低大量的延时。
- 更好的SPDY多路复用与连接管理支持

### 2. 建连

> 0-RTT(send hello，and then send ata request without waiting)

相比于TCP+TLS需要1-3次往返，QUIC的在发送数据前握手无需往返。

1. 首次客户端连接服务端的时候，客户端必须执行一次往返来获得完成握手需要的数据。

在1到2个数据包[^1](取决于连接的服务器是新的还是已知的)内完成连接的创建(包括TLS)

![](/img/quic-3.png)

大多数的工作: 当建立一个新的连接时减少round trip

1. 握手步骤
2. 加密配置
3. 初始化数据请求


QUIC协议内置TLS栈(数据加密)，并且包含部分HTTP/2的实现:

![](/img/quic-4.png)

为什么基于UDP: UDP现在用于视屏与游戏，因此几乎所有的中间件都能支持

实现: 阻塞控制;断线重传

## III. 现有QUIC选型

### 1. 对于后端而言

- `go-quic`: 代码不活跃
- `google-quic`: demo级别(不支持proxy，玩具级别)
- `caddy+quic`: **首选**, 活跃，微博的QUIC后端就是基于此

### 2. 客户端选择

无疑是Google开源的[chromium-net](https://github.com/hanpfei/chromium-net)

## IV. 现在QUIC大环境对QUIC

### 存在问题

- 小地方，路由封杀UDP 443端口
- UDP包过多，由于QS限定，会被服务商误认为是攻击，UDP包被丢弃
- 无论是路由器还是防火墙目前对QUIC都做好准备
- 现在在[IETF](https://datatracker.ietf.org/wg/quic/about/)上QUIC依然还是草稿，并且存在Google QUIC与IETF QUIC两类不稳定的协定

### 临时解决方案

- 通过使用类似`kcptun`或者是`udp2raw-tunnel`之类的工具，将UDP包封装为TCP包以避过网络中间件对UDP包的处理
- 在始终没有响应的情况下（被丢包），降级为TCP+TLS

---

- [Google QUIC协议：从TCP到UDP的Web平台](http://www.infoq.com/cn/articles/quic-google-protocol-web-platform-from-tcp-to-udp)
- [TCP快速打开](https://zh.wikipedia.org/zh/TCP%E5%BF%AB%E9%80%9F%E6%89%93%E5%BC%80)
- [Next generation multiplexed transport over UDP (PDF)](https://www.nanog.org/sites/default/files/meetings/NANOG64/1051/20150603_Rogan_Quic_Next_Generation_v1.pdf)
- [Web Performance and the Impact of SPDY, HTTP/2 & QUIC - Part 5](http://www.apmdigest.com/web-performance-spdy-http2-quic-7)
- [QUIC Geek FAQ](https://docs.google.com/document/d/1lmL9EF6qKrk7gbazY8bIdvq3Pno2Xj_l_YShP40GLQE/edit#heading=h.h3jsxme7rovm)
- [Google Wants To Speed Up The Web With Its QUIC Protocol](https://techcrunch.com/2015/04/18/google-wants-to-speed-up-the-web-with-its-quic-protocol/)

[^1]: QUIC建立连接数据包个数(1到2个)取决于连接的服务器是新的还是已知的
