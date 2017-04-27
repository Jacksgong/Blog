title: 常见网络协议优化与演进
date: 2017-02-12 14:09:03
update: 2017-04-12 14:09:03
sticky: 1
categories:
- 网络
tags:
- Socket
- HTTP
- HTTPS
- SPDY
- HTTP/2
- QUIC
- BBR

---

{% note warning %}本文通过对比分析了截至目前为止各类常见网路协议与其特性。{% endnote %}

<!-- more -->

## I. 协议优化演进

#### 1. 带宽与拥塞

**现状**

目前的网络基建越来越好，因此带宽的已经不再是瓶颈， 但是由于相关协议(如TCP)的拥塞窗口(CWND, congestion window)控制算法，很多时候并没有将带宽有效的利用，因此更有效的利用带宽是一个优化方向，特别针对视频、游戏等领域。

**应对**

- **QUIC:** 基于UDP，QUIC可以支持无序的递交，因此通常单个丢包最多只会影响1个请求stream，并且QUIC中一定程度上拆分拥塞窗口来更好的适配多个多路复用的连接，来尽可能的利用带宽，目前已经在Youtube以及一些Google通用库(如字体库)上应用
- **HTTP:** 通过同时建立多个连接通道，由于每个通道有单独的拥塞窗口保证一个丢包最多只拥塞一个连接通道
- **BBR:** Google推出的全新的阻塞拥塞控制算法，从根本上解决该问题，通过交替测量带宽和激进的估算算法尽可能的占满带宽与降低延迟（此方式极大的提高了带宽利用率），目前已经在Youtube上应用

**存在该缺陷的协议**

- **TCP:** 由于采用"加性增，乘性减"的拥塞控制算法，错误的将网络中的错误丢包也认为是拥塞丢包，导致拥塞窗口被收敛的很小，带宽无法有效利用
- **SPDY:** 由于SPDY基于TCP，因此存在TCP相同的缺陷问题，并且虽然SPDY采用了多路复用，也做个各类优化，但是由于一个TCP连接只有一个拥塞窗口，因此一个请求stream丢包，就会导致整个通道被阻塞

#### 2. 握手的N-RTT的开销

**现状**

目前TCP与SSL/TLS(1.0,1.1,1.2)，每次建连需要TCP三次握手+安全握手需要: `4~5-RRT`，导致建连效率低下，Google、Facebook、Tencent(Wechat)等公司推出了各类优化策略。

**应对**

- **TLS1.3:** 安全握手提出了0-RTT草案
- **QUIC:** 通过实现自己的安全模块，整个握手过程(TCP + TLS)采用全新的0-RTT方案，并计划当完成时适配到TLS1.3中
- **Proxygen:** Facebook基于QUIC的0-RTT协议进行优化，保证安全握手最多只有1-RTT，并运用在TCP中 ，并将贡献各类优化成果给TLS1.3
- **mmtls:** Wechat基于TLS1.3草案中的0-RTT，进行优化推出自己的mmtls，其对于长连接保障安全握手1-RTT，对于短连接安全握手尽可能使用0-RTT

**存在该缺陷的协议**

- **SSL、TLS1.3之前版本:**  在TLS1.2中，需要2~1-RTT(全握手需要2-RTT)

#### 3. 冗余数据

**现状**

通常的一般的HTTP请求，每次请求header基本上没什么变化；在一些情况下多个页面使用相同静态资源(js、logo等)，却每次都重复下载。

**应对**

- **SPDY:** 采用[DEFLATE](http://zh.wikipedia.org/wiki/DEFLATE)对请求头/响应头进行压缩
- **HTTP/2:** 采用[HPACK](http://http2.github.io/http2-spec/compression.html)算法对请求头/响应头进行压缩，并且通讯双方各自cache一份header fields表，避免了重复header的传输
- **QUIC:** 目前版本采用[HPACK](http://http2.github.io/http2-spec/compression.html)算法对请求头/响应头进行压缩
- **HTTP/1.1、HTTP/2:** 支持`Cache-Control`用于控制资源有效时间,支持`Last-Modified`来控制资源是否可复用
- **Facebook geek方案:**  将`expiration time`全部设置为1年，所有的资源请求链接，都采用概念性的连接(在请求链接后加上资源名的md5，再做mapping)(只要资源不变化链接就不变化)，保证已下载资源能被有效利用的同时，避免重复检测资源有效性
- **浏览器优化:** Facebook联系Chrome与Firefox，针对复用资源可复用检测频率进行调整(如firefox支持在`cache-control`中的`immutable`关键字表示资源不可变不用重复检测)

**存在该缺陷的协议**

- **HTTP/1:** 请求头未做压缩，不支持`Cache-Control`与`Last-Modified`因此存在冗余资源重复下载问题
- **HTTP/1.1:** 请求头未做压缩

#### 4. 预准备

- **Taobao:** DNS-Prefetch、Preconnect、Prefetch、Flush HTML early、PreRender
- **SPDY、HTTP/2、QUIC:**: 允许服务端主动推服务端认为客户端需要的静态资源

#### 5. 负载均衡、超时策略优化与其他

- **负载均衡:** 收益较小的长连接，带来服务端没必要的性能开销
- **超时策略:** 策略性的调整建连与维连时的超时重连的频率、时间、IP/端口，来应对弱网状况，何时快速放弃节约资源(无网状态)，何时找到可用资源快速恢复连接(被劫持、服务器某端口/IP故障、基站繁忙、连接信号弱、丢包率高)
- **策略性阻塞:** 根据网络情况、请求数目动态调整连接数来保证吞吐量与稳定性（如SPDY、HTTP/2、QUIC中的多路复用）
- **DNS:** 结合TTL有效管理本地DNS缓存的有效时间、以及缓存大小来减少DNS查询的阻塞，以及可以通过HTTPDNS优化DNS请求的线路以及来避免DNS被篡改等问题(如果使用okhttp3，可以指定DNS，并且可以为请求设定缓存大小与时间，可以很轻易的实现自己的HTTPDNS)

## II. 常见协议区分

#### 1. TCP

目前应用最广泛的可靠的、有序的、自带问题校验修复([error-checked](https://en.wikipedia.org/wiki/Error_detection_and_correction))、传输协议，通常情况下发送端与接收端通过TCP协议来保障数据的可靠到达，中间层通过IP协议来路由数据的传递。

<center>![][1]</center>

- **建连:** 通过三次握手，保障连接已可靠连接
- **超时重试:** 通过连接超时重试、读写超时重试机制，来保障连接的稳定性
- **拥塞控制:** 通过"加性增，乘性减"算法，来保障尽量少的报文传输尽量多的数据的同时，减少丢包重传的概率
- **校验和:** 通过对TCP/IP头进行"校验和"检查，来保障传输数据与地址信息的可靠
- **有序性:** 通过"序列号"来鉴别每个字节数据，保证接收端能够有序的重建传输数据，以及校验数据完整性
- **应答机制:** 每次接收端会发送Acks(Acknowledgements)给发送端告知数据以被接收
- **断连:** 通过四次挥手，保障连接已可靠断开

#### 2. HTTP

**`HTTP1.1` vs `HTTP1.0`**

- **更灵活缓存处理:** 引入Etag(Entity tag)等目前常用的缓存相关策略
- **优化带宽使用:** 引入`range`头域，支持206(Partial Content)，用于数据断点续传。
- **错误机制更完善:** 引入24个错误状态码，如409(Conflict)请求资源与当前状态冲突； 410(Gone)资源在服务器上被永久删除
- **Host头处理:** 请求头中必须带上`host`，否则会报400 Bad Request，为了支持一台服务器上有多台虚拟主机，因此通常一个IP对应了多个域名
- **长连接:** 默认`Connection: keep-alive`，以复用已建连通道，不像`http1.0`每个请求都需要重新创建

#### 3. HTTPS

1994年由 **网景** 提出，并应用在网景导航者浏览器中。最新的HTTPS协议在2000年5月公布的`RFC 2818`正式确定。

HTTPS协议是基于TLS(Transport Layer Security)/SSL(Secure Sockets Layer)对数据进行加密校验，保障了网络通信中的数据安全。

在当前大陆的网络环境而言，是有效避免运营商劫持的手段。

<center>![image_1b8ji5se91a1kvn431umcc2vk9.png-44.3kB][2]</center>

- **SSL与TLS:** 早期HTTPS是通过SSL对数据验证加密，后SSL逐渐演变为现在的TLS，所以大多数为了有效的支持加密，都同时支持了SSL与STL
- **TLS提高了SSL:** 虽然最早的TLS1.0与SSL3.0非常类似，但是TLS采用HMAC(keyed-Hashing for Message Authentication Code)算法对数据验证相比SSL的MAC(Message Authentication Code)算法会更难破解，并且在其他方面也有一些小的改进
- **请求端口:** 443

#### 4. SPDY

> 读音speedy

是谷歌开发为了加快网页加载速度的网络协议。

SPDY兼容性: http://caniuse.com/#feat=spdy

<center>![image_1b8jj8l511lag13eslpm1al918krm.png-23.8kB][3]</center>

- **采用多路复用(multiplexing):** 多个请求stream共享一个tcp连接， 降低延时、提高带宽利用率
- **请求优先级:** 允许给每个请求设置优先级，使得重要的请求得到优先响应
- **TLS/SSL的加密传输:** 强制要求使用TLS/SSL提高数据安全可靠性
- **压缩`请求头/响应头`:** 通过DEFLATE或gzip算法进行对`请求头/响应头`进行压缩
- **支持Server Push:** 允许服务端主动的推送资源(js、css)给客户端，当分析获知客户端将会需要时，以此利用起空闲带宽
- **支持Server Hints:** 允许服务端可以在客户端还没有发现将需要哪些资源的时候，主动通知客户端，以便于客户端实现准备好相关资源的缓存

#### 5. HTTP/2

> HTTP/2基于SPDY设计

<center>![image_1b90ik3e01di41tgr16hc12ks19uvp.png-129.5kB][4]</center>
<center>![image_1b8jku3ol1rbveu4es1tp8rk61j.png-125kB][5]</center>

**HTTP/2 vs SPDY**

- **SSL/TLS:** SPDY强制使用SSL/TLS，HTTP/2非强制(但是部分浏览器(如Chrome)不允许，所以目前如果使用HTTP/2最好都配置SSL/TLS)
- **消息头压缩算法:** HTTP/2消息头压缩算法采用[HPACK](http://http2.github.io/http2-spec/compression.html)，SPDY采用[DEFLATE](http://zh.wikipedia.org/wiki/DEFLATE)，一般情况下HPACK的压缩率会高于DEFLATE
- **传输格式:** HTTP/2传输采用二进制而非文本，因此HTTP/2中的基本单位是帧, 文本形式众多很难权衡健壮、性能与复杂度，二进制弥补了这个缺陷，并且是无序的帧，最终根据头帧重新组装
- **继承与优化:** HTTP/2继承并优化了SPDY的多路复用与Server Push

#### 6. QUIC

- 发音`quick`
- QUIC 参考了HTTP/2与SPDY
- Google在2013年10月第一次在IETF展示QUIC, 2016年7月启动工作群
- 可靠的，多路复用的基于UDP的网络协议，内置安全加密模块，低延迟、运行在用户空间、开源的新一代网络协议。Google计划在完成后将其服务于所有的Google服务。

<center>![][6]</center>
<center>![][7]</center>

- **减少建连延迟:** 从未访问过服务的情况下1-RTT，其他的可以立马开始传输数据(0-RTT)
- **拥塞控制:** 提升TCP Cubic拥塞控制
- **HOL阻塞:** 消除多路复用中的HOL阻塞(head-of-line blocking)
- **更少的帧消耗:** Quic数据包包含更少的帧，因此更多的数据包可以携带数据
- **提升丢包重试:** 丢包重试时使用新的序列号以及采用重新加密
- **安全加密:** 内置的加密模块(支持SNI，因此支持一个IP部署多个证书)，并且是默认打开的，相比TLS更高效的向前加密 - 完成以后，将计划适配到TLS 1.3中
- **端口:** 使用443端口来处理UDP协议数据 - [Port 80/443 UDP Traffic to Google?](https://community.spiceworks.com/topic/601177-port-80-443-udp-traffic-to-google)
- **其他:** 更好的FEC(Forward error correction)机制、与Connection migration机制

---

- [从tcp原理角度理解Broken pipe和Connection Reset by Peer的区别](http://lovestblog.cn/blog/2014/05/20/tcp-broken-pipe/)
- [淘宝HTTPS探索](http://velocity.oreilly.com.cn/2015/ppts/lizhenyu.pdf)
- [HTTP,HTTP/2,SPDY,HTTPS你应该知道的一些事](http://www.alloyteam.com/2016/07/httphttp2-0spdyhttps-reading-this-is-enough/)
- [QUIC Geek FAQ](https://docs.google.com/document/d/1lmL9EF6qKrk7gbazY8bIdvq3Pno2Xj_l_YShP40GLQE)
- [google/bbr](https://github.com/google/bbr)
- [滑动窗口和拥塞窗口简述](http://www.cnblogs.com/mydomain/archive/2013/04/18/3027668.html)
- [BBR算法原理 - 李博杰](https://www.zhihu.com/question/53559433)
- [QUIC - Next generation multiplexed transport over UDP](https://www.nanog.org/sites/default/files/meetings/NANOG64/1051/20150603_Rogan_Quic_Next_Generation_v1.pdf)
- [Building Zero protocol for fast, secure mobile connections](https://code.facebook.com/posts/608854979307125/building-zero-protocol-for-fast-secure-mobile-connections/)
- [基于TLS1.3的微信安全通信协议mmtls介绍](https://github.com/WeMobileDev/article/blob/master/%E5%9F%BA%E4%BA%8ETLS1.3%E7%9A%84%E5%BE%AE%E4%BF%A1%E5%AE%89%E5%85%A8%E9%80%9A%E4%BF%A1%E5%8D%8F%E8%AE%AEmmtls%E4%BB%8B%E7%BB%8D.md)
- [QUIC Wire Layout Specification](https://docs.google.com/document/d/1WJvyZflAO2pq77yOLbp9NsGjC1CHetAXV8I0fQe-B_U/edit)
- [SPDY - Wiki](https://en.wikipedia.org/wiki/SPDY)
- [This browser tweak saved 60% of requests to Facebook](https://code.facebook.com/posts/557147474482256/this-browser-tweak-saved-60-of-requests-to-facebook/)
- [HTTP2学习(四)—HTTP2的新特性](http://jiaolonghuang.github.io/2015/08/16/http2/)
- [Server Push and Server Hints](https://www.chromium.org/spdy/link-headers-and-server-hint)
- [What is TLS/SSL?](https://technet.microsoft.com/en-us/library/cc784450(v=ws.10).aspx)
- [QUIC - Google-peering](http://peering.google.com/#/learn-more/quic)
- [QUIC教材](https://www.chromium.org/quic)
- [QUIC视频介绍](https://www.youtube.com/watch?v=hQZ-0mXFmk8)

---

[本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/network_basic.md)

---

本文已经发布到JackBlog公众号: [常见网络协议与演进 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483713&idx=1&sn=a7a67d3a2258c738c725c37f7c37b210)

---

  [1]: /img/network_basic-1.png
  [2]: /img/network_basic-2.png
  [3]: /img/network_basic-3.png
  [4]: /img/network_basic-4.png
  [5]: /img/network_basic-5.png
  [6]: /img/network_basic-6.png
  [7]: /img/network_basic-7.png
