title: TCP 窗口
date: 2018-01-30 18:11:03
wechatmpurl: https://mp.weixin.qq.com/s/hzwsHiwi55JZkOpKZaw8pA
wechatmptitle: TCP窗口
updated: 2018-01-31
categories:
- 网络
tags:
- tcp
- cwnd
- rwnd
- 拥塞算法

---

{% note info %} 这块的整理归根于FileDownloader开源库中，发现一个问题，在发起一个HTTP请求后，不主动读取输入流的情况下，抓包发现，莫名的下载了一小部分内容，而后发现，这块的资源是由于底层TCP在窗口中缓存的，而为什么需要存在这个窗口呢，这个就需要追溯本源了。{% endnote %}

<!-- more -->

### I. 抓包

我们用Wireshark抓包发现，在发起一个`Range: 0-`的请求后，只要不断开连接，底层就会自动的不断的自动下载内容，直到一定的大小后停止，如下图:

![][4]

其中我们可以发现，首先是三次握手:

- 第一次`SYN`: 我们告知服务端，我们的接收窗口(`Win`)为65535Bytes(64K)，最大报文段大小(`MSS`)为1460Bytes,窗口缩放因子(`WS`)为256
- 第二次`SYN,ACK`: 服务端告知我们，服务端的接收窗口(`Win`)为14480Bytes，最大报文段大小(`MSS`)为1456Bytes，窗口缩放因子(`WS`)为256
- 第三次`ACK`: 我们告知服务器，由于双方都有相同的窗口缩放因子256，因此我们的接收窗口根据当前处理能力修改为87808Bytes(`343*256`)

之后服务端根据我们的接收窗口大小，以及服务端的拥塞窗口大小决定其发送窗口大小，并根据协定的`MSS`一次发送多个报文段给我们TCP的接收窗口缓存，后面我们的TCP根据处理能力不断调整接收窗口大小持续接收数据，也就是说这块虽然我们应用层没有主动的不断读取输入流，但是TCP的接收窗口已经在不断缓存数据了。

### II. 基本概念

#### 什么是MTU(Maximum Transmit Unit)

由于以太网传输的限制，每个以太网网数据帧的大小都是落在在区间`[64Bytes,1518Bytes]`中的，不在区间内的一般会被视为错误的数据帧，以太网转发设备直接丢弃。而根据以太网每帧的数据构成，除去固定的部分，留给上层协议的只有`Data`域的1500Bytes，我们将它称为MTU。

**以太网(Ethernet II)每帧的数据构成:** 目的Mac地址(`DMAC`)+源Mac地址(`SMAC`)+类型(`Type`)+数据(`Data`)+校验(`CRC`) = 6Bytes(48bit)`DMAC` + 6Bytes(48bit)`SMAC` + 2Bytes(16bit)`Type` + 1500Bytes`Data` + 4Bytes(24bit)`CRC`

#### MTU照成什么影响

由于一个帧放不下，如IP协议，就会对数据包进行分片处理，这就导致了原本一次可以搞定的，被分为多次，降低传输性能，不过我们可以通过在数据包包头加上`DF(DonotFragment)`标签来强制不被分片处理。

- UDP协议不用关心数据的到达的有序以及正确，因此对分片无特殊要求
- TCP协议相反，因此TCP协议本身的最大报文段大小`MSS`也受MTU影响，通常`MSS`是: `MTU` - 20Bytes(`IP Header`) - 20Bytes(`TCP Header`)

不过好在绝大多数的网络链路都是1500Bytes的MTU或者更大

#### 什么是MSS(Maximum Segment Size)

TCP的最大报文段大小，只包含`TCP Payload`(不包含`TCP Header`与`TCP Option`)的TCP每次能够传输的最大数据分段的大小，可以用来限制每次发送的字节数。通常大小为1460Bytes(1500Bytes`MTU` - 20Bytes(`IP Header`) - 20Bytes(`TCP Header`))

MSS是在TCP建连时确定的，通讯双方会根据双方提供的MSS值，取最小的MSS作为该次连接数据传输的MSS

#### 什么是WS(Window Scaling)

![][6]

如上图由于表示Window Size的字段只有16位，因此按照协议，能表示的最大窗口大小是`2^16-1=65535Bytes`(64Kb)，因此TCP的选项字段中包含了窗口扩大因子(`WS`)分别用`option-kind`、`option-length`、`option-data`来表示，这个参数可带可不带，只有在双方都支持的情况下，才会生效。如双方的`WS`都是256，而后我们ACK `Window size value`是5，那么此时就可以表示我们的接收窗口是1280Bytes(`5*256=1280`)。

### III. 为什么需要窗口

- **解决问题:** TCP是以报文段(若干字节)为单位，每一个报文段需要一次ACK确认收到，但是其带来的问题很明显，频繁的发送确认等待导致用于确认与等待的时间太长。
- **解决方案:** 引入窗口后，发送端只要在窗口内，便不用每次都等待ACK才发送下一个报文段，可以在发送窗口内一次连续发送几个报文段而无需等待ACK

### IV. 滑动窗口与拥塞窗口(cwnd)

- **滑动窗口(rwnd):** 用于流控的动态缩放可靠滑动的接收与发送窗口，防止发送端发送过快接收端被淹没
- **拥塞窗口(rwnd):** 在一个RTT内可以最多一次可发送的报文段数 --- 发送方的流量控制

### V. 滑动窗口

#### 1. 什么是发送窗口

![][5]

发送方任何时候其发送缓存内的数据都可以被分为4类:

1. 已发送，已收到ACK
2. 已发送，未收到ACK
3. 未发送，但允许发送
4. 未发送，但不允许发送

其中类型的`2`和`3`两部分一起，我们称为发送窗口。

#### 2. 发送窗口与滑动窗口

![][7]

对于发送方，发送窗口即为滑动窗口，如上图，原发送窗口从`32`到`51`，当收到`36`的ACK后，发送窗口滑动到`36`到`55`。

#### 3. 发送窗口大小怎么决定

拥塞窗口大小与接收端的滑动窗口大小共同决定了发送端的发送窗口大小，发送窗口每次都是取拥塞窗口大小与滑动窗口大小的最小值。

#### 4. 什么是接收窗口

接收缓存存在4类:

1. 已接收
2. 未接收，准备接收
3. 未接收，未准备接收

其中类型的`2`我们称为接收窗口。

#### 5. 发送窗口与接收窗口的关系

TCP是双工协议，会话双方都可以同时接收与发送数据，因此双方都同时维护一个发送窗口与接收窗口。

- 接收窗口大小取决于应用、系统、硬件等限制；
- 发送窗口大小取决于对方接收窗口的大小

#### 6. 窗口滑动协定

- 发送窗口只有在收到窗口内字节的ACK确认，才会滑动其左边界
- 接收窗口只有在窗口中所有的段都正确收到的情况下，才会滑动其左边界；当有字节未接收，但收到后面的字节的情况下，也会滑动，也不对后续字节确认，确保对方重传未接收字节

### VI. 哪些允许变化

- 最大报文段大小在握手中，就确定了
- 窗口缩放因子在握手中，就确定了
- 接收窗口大小在根据本地的处理能力与缓存剩余空间动态调整，通过ACK带给对方当前剩余的接收窗口大小

### VII. 窗口滑动协定

- 发送窗口只有在收到窗口内字节的ACK确认，才会滑动其左边界
- 接收窗口只有在窗口中所有的段都正确收到的情况下，才会滑动其左边界；当有字节未接收，但收到后面的字节的情况下，也会滑动，也不对后续字节确认，确保对方重传未接收字节

### VIII. 有滑动窗口了，为什么还要拥塞窗口

发送方与接收方之间存在多个路由器和速率较慢的链路时，一些中间路由器就必须缓存分组，并可能耗尽缓存，此时便会出现拥塞，这将严重降低了TCP连接的吞吐量，拥塞窗口就是为了防止过多的数据注入到网络中，中间路由无法消化的问题。

TCP的做法是引入`拥塞窗口(cwnd)`并策略性的调整其大小，如上文提到的`发送窗口大小`是取`滑动窗口大小`与`拥塞窗口大小`的最小值，这个正是用来缓解该问题，下面是拥塞窗口大小变化的策略:

#### 1. 慢开始、拥塞控制

![][1]

**其目的是:** 拥塞发生时循序减少主机发送到网络的报文数，使得这时路由器有足够的时间消化积压的报文。

- 当主机开发发送数据时，`拥塞窗口(cwnd)`被初始化为1个报文段，试探性的发送1个字节的报文
- 每收到一个ACK，拥塞窗口大小就指数的增加报文段数目(1,2,4,16...)
- 最终到达提前预设的`慢开始阀值(ssthresh)`，停止使用`慢开始`算法，改用`拥塞避免算法`
- `拥塞避免算法`是每经过一个RTT，拥塞窗口就增加一个报文段，即改为线性的增加报文段
- 最终会出现网络拥塞，比如丢包等情况，停止`拥塞避免算法`，将慢开始阀值设置为目前拥塞时拥塞窗口大小的一半，并重置拥塞窗口大小为1个报文段，开始新的一轮`慢开始`

#### 2. 快重传，快恢复

![][2]

**其目的是:** 减少因为拥塞导致的数据包丢失的重传时间，避免无用的数据到网络

**接收方:** 如果一个包丢失，后续的包继续发送针对该包的重传请求

**发送方:** 一旦收到三个一样的确认，判定为拥塞:

- 立即重传该包
- 开始执行`快恢复`算法
- `快恢复`是`慢开始阀值`设置为目前拥塞时拥塞窗口大小的一半；拥塞窗口大小设置为目前设置后的`慢开始阀值`的大小；执行`拥塞避免算法`


### IX. TCP窗口特殊情况

#### 1. Persistence timer

![][3]

防止丢包导致发送端停留在上次收到的接收窗口大小为0的情况:

- 接收端B: 我的缓存已满，接收窗口为0
- 发送端A: 停止发送数据, **并启动持续计时器(Persistence timer)**
- 接收端B: 消化完缓存，发送报文给发送端A，我的接收窗口大小为400，但是 **这个报文丢了**
- 发送端A: **计时器时间到，发送一个1字节的探测报文**
- 接收端B: 重新发送，接收窗口大小为400
- 发送端A: 继续发送数据

#### 2. 应用层每次单字节发送

单个发送字节，然后等待一个确认，再发送一个字节，这样为一个字节添加40个字节头的做法，无疑增加了网络中许多不必要的报文，该问题TCP层的解决方案:

**发送方采用`Nagle`算法:**

- 若应用层是逐个字节把数据送到TCP，那么TCP不会逐个的发送，而是先发送第一个数据字节，然后缓存剩余的
- 在收到第一个字节的ACK获知网络情况与对方的接收窗口大小后，把缓存的剩余字节组成合适的报文发送出去
- 到达的数据达到发送窗口大小的一半或者报文段的最大长度时，立即发送

**接收方的做法:**

等待本地有足够的缓存空间容纳一个报文段，或者等到本地的缓存空间有一半空闲的时候，再通知发送端发送数据。

### X. FileDownloader上该问题的解决

#### 策略一

如公众平台上李冬冬回复提到，改用`HEAD`方法的请求。

![][9]

根据[RFC2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html)中定义，HEAD请求服务端只会返回相同的`GET`请求的响应头，而不带回消息体，由于其特性，响应速度会比一般的`GET`请求更快，这显然是我们试探连接想要做的。
但是我们发现，实际过程中，有很多的请求的返回的状态码与`GET`请求并不一致，比如`GET`时返回的是`206`，但是`HEAD`时，返回的却是`200`，因此我们查找[RFC2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)文档，在Session 14中，看到了`Accept-Ranges`这个响应头字段: 如果是`Accept-Ranges: none`代表不支持，而`Accept-Ranges: bytes`代表支持，但是如果没有这个响应头字段却也不能说明不支持。

#### 策略二

正如issue上[jiangyanlily](https://github.com/jiangyanlily)，提到的，采用`0-0`的`Range`发起`GET`方法的请求。

![][8]


根据[RFC7233](https://tools.ietf.org/html/rfc7233#page-6)的协议，此时返回的只有第一个字节与最后一个字节，并且我们可以通过响应头的`Content-Range`来获取总大小，以及返回的状态码来获知是否支持断点续传的判定。

#### 综合考虑

实际测试下来在使用`0-0`的`Range`前提下，确实使用`HEAD`比使用`GET`少去了`1bytes`的body，实际上这个意义并不是特别大，不过就协议而言，确实`HEAD`方法请求更加合理:

![][10]

其实如果真的要一个依据，肯定是以RFC作为依据的，如果按照RFC的定义，目前看来策略一是最靠谱的，但是考虑到现实中策略一中返回状态码并无法完全说明是否支持`Range`的情况，我们这边会再配合响应头的`Accept-Ranges`进行判断；而在处理`HEAD`的请求出现问题的情况下，我们会结合策略二来处理，最终方案如下:

- 默认发起一个带有`If-Match`并且`Range`为`0-0`的`HEAD`请求
- 支持`Range`判定: 返回状态码是`206`或者响应头包含`Accept-Ranges: bytes`
- `Etag`过期判定: 对比响应头中的`Etag`与请求头中的`If-Math`
- 总大小获取: 先通过`Content-Range`获取，如若获取不到，再通过`Content-Length`进行获取

---

- [TCP的滑动窗口与拥塞窗口](http://blog.csdn.net/zhangdaisylove/article/details/47294315)
- [计算机网络【七】：可靠传输的实现 ](http://blog.chinaunix.net/uid-26275986-id-4109679.html)
- [TCP窗口控制、流控制、拥塞控制](http://blog.csdn.net/cloud323/article/details/77481711)
- [也谈一下TCP segment of a reassembled PDU](http://blog.csdn.net/hldjf/article/details/7450565)
- [TCP流量控制中的滑动窗口大小](https://www.zhihu.com/question/48454744)
- [TCP 滑动窗口（发送窗口和接收窗口）](https://my.oschina.net/xinxingegeya/blog/485650)
- [TCP协议的滑动窗口具体是怎样控制流量的？](https://www.zhihu.com/question/32255109)


  [1]: /img/tcp-window-1.png
  [2]: /img/tcp-window-2.png
  [3]: /img/tcp-window-3.png
  [4]: /img/tcp-window-4.png
  [5]: /img/tcp-window-5.jpg
  [6]: /img/tcp-window-6.jpg
  [7]: /img/tcp-window-7.jpg
  [8]: /img/tcp-window-8.png
  [9]: /img/tcp-window-9.png
  [10]: /img/tcp-window-10.png