title: 网络常见API、协议与工具
date: 2017-02-12 11:54:03
tags:
- Socket
- HTTP2.0
- HTTP
- HTTPS
- SPDY
- tcpdump

---


## I. 优化入口

- 带宽: 目前的网络基建越来越好，因此带宽的已经不再是瓶颈
- 延迟: 1. 策略性阻塞(如一般的浏览器内核只允许6个连接，更多的请求会被阻塞); 2. DNS查询阻塞(目前多数通过本地DNS缓存(存在有效时间间隔)); 3. 建连: TCP与SSL都需要在握手以后以后才开始传输数据; 4. 维连接: 读写超时如何快速有效恢复
- 冗余数据: 通常的一般的Http请求，每次请求header基本上没什么变化；
- 负载均衡: 收益较小的长连接，带来服务端没必要的性能开销
- 预准备: DNS-Prefetch、Preconnect、Prefetch、Flush HTML early、PreRender

<!-- more -->

## II. 常见网络协议与API

### 1. Socket

- 标准的Socket API最早是在Unix中定义的，Windows Scokets有其变种版本。
- TCP/IP、IPX/SPX、Appletalk 等协议都是使用Socket Api的

### 2. TCP

![image_1b8j1od7f11rspea7gi1stssbq9.png-104.2kB][1]

- ACK在三次握手与四次挥手中对受到的SYN和FIN做一个确认
- 是SYN还是FIN等，是在TCP的请求头中体现
- MSS是每一个TCP报文中数据字段最长长度(不包含TCP头部分大小)

![image_1b8j21mft14qk1djgsom1ad58kfp.png-175.3kB][2]


### 3. HTTP

#### `HTTP1.1` vs `HTTP1.0`

- **更灵活缓存处理:** 引入Etag(Entity tag)等目前常用的缓存相关策略
- **优化带宽使用:** 引入`range`头域，支持206(Partial Content)，用于数据断点续传。
- **错误机制更完善:** 引入24个错误状态码，如409(Conflict)请求资源与当前状态冲突； 410(Gone)资源在服务器上被永久删除
- **Host头处理:** 请求头中必须带上`host`，否则会报400 Bad Request，为了支持一台服务器上有多台虚拟主机，因此通常一个IP对应了多个域名。
- **长连接:** 默认`Connection: keep-alive`，以复用已建连通道，不像`http1.0`每个请求都需要重新创建

### 4. HTTPS

1994年由**网景**提出，并应用在网景导航者浏览器中。
最新的HTTPS在2000年5月公布的`RFC 2818`正式确定

- 早期HTTPS与SSL一起使用，后SSL逐渐演变为现在的TLS
- HTTP是运行在TCP上，SSL/TLS运行也是在TCP上，HTTPS运行在SSL/TLS上
- 由于需要SSL握手，可能会比HTTP慢，但是如果使用SPDY，HTTPS的速度甚至比HTTP快(SPDY 与 HTTP/2极大提高速度)
- 请求端口443
- 可以通过SNI(Server Name Indication)以达到一个IP部署多个证书
- 尽可能降低TLS新建的⽐率
- 杜绝运行商拦截

![image_1b8ji5se91a1kvn431umcc2vk9.png-44.3kB][3]

### 5. SPDY

> 读音speedy

是谷歌开发为了加快网页加载速度的网络协议。

- 采用多路复用(multiplexing)，多个请求stream共享一个tcp连接: 降低延时、提高带宽利用率
- 请求优先级: 允许给每个请求设置优先级，使得重要的请求得到优先响应
- 基于HTTPS的加密传输: 提高数据安全可靠性
- 允许`客户端/服务端`压缩`请求头/响应头`：当多个请求重复发送类似请求头时会得到压缩
- 允许同时发送多个请求，而非通过当个连接：减少服务端与客户端来回的耗时，并且避免了低优先级请求阻塞住高优先级请求
- 允许服务端主动的推送资源(js、css)给客户端，当知道客户端将会需要时，而不同客户端请求: 以此利用起空闲带宽
- SPDY兼容性: http://caniuse.com/#feat=spdy

#### 层级:

![image_1b8jj8l511lag13eslpm1al918krm.png-23.8kB][4]

### 6. HTTP2.0

> HTTP2.0基于SPDY设计

#### HTTP2.0 vs SPDY

- SPDY强制使用HTTPS，HTTP2.0支持明文HTTP传输
- HTTP2.0消息头压缩算法采用[HPACK](http://http2.github.io/http2-spec/compression.html)，SPDY采用[DEFLATE](http://zh.wikipedia.org/wiki/DEFLATE)
- HTTP2.0传输采用二进制而非HTTP的文本: 文本形式众多很难权衡健壮、性能与复杂度，二进制弥补了这个缺陷
- 都采用了多路复用，都允许服务端主动推送资源
![image_1b8jku3ol1rbveu4es1tp8rk61j.png-125kB][5]


## III. 工具

### 1. tcpdump

> [Linux抓包工具tcpdump详解 - 五、举例](http://www.ha97.com/4550.html)

需要监听所有来往`10.15.71.165`ip的TCP: `sudo tcpdump host 10.15.71.165`

---

- [从tcp原理角度理解Broken pipe和Connection Reset by Peer的区别](http://lovestblog.cn/blog/2014/05/20/tcp-broken-pipe/)
- [淘宝HTTPS探索](http://velocity.oreilly.com.cn/2015/ppts/lizhenyu.pdf)
- [HTTP,HTTP2.0,SPDY,HTTPS你应该知道的一些事](http://www.alloyteam.com/2016/07/httphttp2-0spdyhttps-reading-this-is-enough/)

---

> © 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---

  [1]: /img/network_basic-1.png
  [2]: /img/network_basic-2.png
  [3]: /img/network_basic-3.png
  [4]: /img/network_basic-4.png
  [5]: /img/network_basic-5.png
