title: Facebook 网络
date: 2017-04-20 18:11:03
wechatmpurl: https://mp.weixin.qq.com/s/hzwsHiwi55JZkOpKZaw8pA
wechatmptitle: TCP窗口
updated: 2018-04-28
categories:
- 网络
tags:
- 302
- proxygen
- fbthrift
- quic

---

{% note info %} 这块资料是在2017年年初整理的，但是在支付宝网络组忙于各类学习很多整理后的没有发布出来，现在先整理到博客上，后续会持续完善。{% endnote %}

<!-- more -->

## I. 提升cache利用率，减少302检验性请求

> [This browser tweak saved 60% of requests to Facebook
](https://code.facebook.com/posts/557147474482256/this-browser-tweak-saved-60-of-requests-to-facebook/)

### 1. 遇到问题

- 很多静态资源(如js、logo等)在不同的页面中都会用到，而我们进入每个页面都重复拉取这些数据，非常的浪费资源。

### 2. 业界方案

> 为每个请求带上以下参数来复用资源

- expiration time: 通过`Cache-Control`的请求头来告诉流量器响应资源可以复用的时间
- validator: 当expiration time过了以后，可以通过`Last-Modified`或`Etag`来告知浏览器还可以复用

但是这个方案依然存在一个问题，如果将expiration time设置为1h，那么每1h都要检测一遍，在一些资源下是浪费的，也考虑到这个时间是难以抉择。

### 3. Facebook解决方案

- expiration time: 全部设置为1年
- 资源的请求链接，采用概念性的链接: 源请求链接后带上资源的md5，这样一旦资源有变化该链接就会发生变化，对应映射关系用数据库维护。
- 联系浏览器商，调整重复校验的策略: 浏览器厂商有些时候甚至会忽略请求头中的时间，而做重复的检验，如 chrom认为post请求通常是提交表单是会有资源变化的，所以他们会触发校验性请求（后facebook说服他们没有必要做这样独特的约定），如最终与firefox约定`cache-control`中带上`immutable`关键字，点击刷新按钮就不再重复校验(如: `cache-control: max-age=3600, immutable`)。

如: logo.png的md5是abc123，那么该资源的URL: http://www.facebook.com/rsrc.php/abc123.png

## II. Proxygen

> - Facebook的HTTP网络栈，支持HTTP/1.1、SPDY/3、SPDY/3.1、HTTP/2高性能的使用C++14开发的自定义HTTP网络栈

> - 目前只开源的抽象出来的服务端部分，后续是有开源客户端API部分的

2011年启动，2012年支持SPDY/2，2013年支持SPDY/3，2014年支持了SPDY/3.1，依赖: [fbthrift](https://code.facebook.com/projects/1410559149202582/fbthrift/)、[folly](https://code.facebook.com/projects/527543867323997/folly/)

## III. 建连

使用TLS(1.2)，具体实现使用带OpenSSL的Folly。Facebook的TLS连接仅额外增加了一轮往返(1-RTT):

- 距离用户最新的边缘位置终止TLS连接
- 复用HTTP2连接
- 复用会话
- TLS抢跑(False start)
- 推断式连接启动
- 现代化的Cipher套件

### 0-RTT往返

印度等新兴市场(弱网): 600ms(75%)才能建立TLS连接

考虑到重构代价，采用逐步进行的实验。基于TLS 1.3的0-RTT进行优化。
最终: 使用改动后的QUIC的加密协议构建基于TCP的实验性0-RTT，并贡献给了TLS1.3
2016年实验与部署，连接延迟降低41%，处理请求总时间降低2%
经验: API设计、安全属性、部署

### QUIC协议改动

QUIC加密:

- 从未与服务通信过: 通过1-RTT发送Inchoate Client Hello(CHLO)，下载Server Config(SCFG)
- 初始密钥(0-RTT密钥): 通过SCFG中的Diffie-Hellman共享派生0-RTT密钥发送初始数据给服务器
- 向前安全密钥(1-RTT密钥): 1-RTT完成后，服务器发出新的暂存Diffie-Hellman共享，客户端由此派生1-RTT密钥，并用此加密传输

1. 一旦攻击者"重播"相同的CHLO，服务端就会用相同的密钥加密不同的SHLO返回给攻击者，导致AEAD加密算法失效，因此Facebook引入另一种明文方式的nonce机制。。当然也提给google，google也根据不同的场景区分CHLO来解决了该漏洞
2. 一旦SCFG在有效期内被攻击者截取，它就能模拟服务器来响应客户端，因此Facebook限制了SCFG的有效时间长度，(QUIC中如果要替换客户端已缓存的SCFG，就必须在客户端用原有SCFG请求时，拒绝其请求，这样就会导致这些请求数据被丢弃)，Facebook采用服务端中备份"上一个SCFG"、"当前SCFG"、"下一个SCFG"，当客户端采用"上一个SCFG"请求时，让客户端完成连接，通过加密的SHLO为客户端提供"当前SCFG"，以防止被拒绝。


#### 重播缓存

对每一个时间窗口内发送的0-RTT Client Hello进行缓存，进而拒绝重复的消息

解决问题:

虽然缩短0-RTT数据有效期的时间窗口，降低了攻击者无止境的重播0-RTT请求。
但是，在时间窗口内，依然可能有多次重播请求，并且攻击者可以根据统计学分析回应的时间。

拓展:

将重播的次数限制为客户端的重试次数，以满足客户大劫案自动被拒绝的0-RTT请求一1-RTT数据的方式重新发送

情况:

- 0-RTT协议中没有全面启动
- TLS 1.3时，会开始部署

---

- Group: https://groups.google.com/forum/#!forum/facebook-proxygen
- Post: https://code.facebook.com/posts/1503205539947302
- facebook/proxygen - github: https://github.com/facebook/proxygen

---

- [Building Zero protocol for fast, secure mobile connections](https://code.facebook.com/posts/608854979307125/building-zero-protocol-for-fast-secure-mobile-connections/)
