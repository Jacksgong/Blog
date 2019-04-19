title: TLS握手、中断恢复与证书中心的原因
date: 2019-04-19 17:48:03
updated: 2019-04-19
categories:
- 网络
tags:
- TLS
- DH
- RSA
- 数字证书

---

{% note info %} 我们在以前的多篇文章中都有提到各类网络协议的特征(如[常见网络协议优化与演进](https://blog.dreamtobe.cn/network_basic/))，但是对于网络安全相关这块却很零碎，我本地整理了挺多文章但是我给文章定的框架过大，导致完全无法结束，今天就把其中两个常见的问题抽出来整理成文，希望对大家有所帮助。{% endnote %}

<!-- more -->

## I. TLS 握手

### 常见的RSA算法

![](/img/tls-cert-1.jpg)

在双方都拿到随机数A、B、C后，将会使用这三个随机数生成一个对话密钥，然后使用该对话密钥进行对称加密通信，这种方式我们可以看到，安全性取决于随机数C的加密，前面的几个都是明文传的，这里就取决于服务器的公私钥机制(默认是RSA算法)

### DH算法

![](/img/tls-cert-2.jpg)

Diffie-Hellman算法，Premaster secret不需要传递，双方只需要交换各自参数，就可以算出这个随机数

## II. TLS 中断恢复(Session 恢复）

对话中断，如何避免重新握手

### session ID

- 每一次对话都有一个编号(session ID)
- 重连时如果服务端有客户端给出的这个编号就重新使用已有对话密钥

![](/img/tls-cert-3.jpg)

- 优点: 所有浏览器都支持
- 缺点: session ID通常只保留在一台服务器

### session ticket

- 客户端发送服务器上一次对话中发过来的session ticket(服务端加密的(内容包括密钥、加密方法))
- 服务端如果能够解密发送过来的session ticket，就可以复用对话密钥了

![](/img/tls-cert-4.jpg)

- 优点: 不局限于单台服务器
- 缺点: 只有如Firefox与Chrome部分浏览器支持

## III. 非对称加密常见问题

### 常规使用

![](/img/tls-cert-5.jpg)

### 确保发送者可信

这里我们有可能遇到的问题是，如上面的TLS，我们无法确定发送者是否就是我们的服务端，因此这里引入了证书中心，由于证书中心是第三方可信机构，公钥不再直接明文发送，而是通过证书中心的私钥进行加密后与相关信息一起生成数字证书再发送给客户端，客户端此时逐个使用第三方可信机构的公钥进行解密，如果成功解密，则说明该公钥是可信的，可使用。

![](/img/tls-cert-6.jpg)

因此这里有一点，是我们通常往如Letsencrypt申请证书时，实际上就是将我们服务端生成的公钥给到Letsencrypt，Letsencrypt使用其私钥以及我们给过去的信息生成一个数字证书给我们。

---

- [图解SSL/TLS协议](http://www.ruanyifeng.com/blog/2014/09/illustration-ssl.html)
- [数字签名是什么？](http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html)
