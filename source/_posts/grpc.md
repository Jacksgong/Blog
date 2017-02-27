title: gRPC
date: 2017-02-16 22:38:03
categories:
- 网络
tags:
- gRPC
- Thrift
- HTTP/2
- Proto3

---

> 2015年2月由Google公司牵头，2016年8月对外正式发布的基于HTTP/2以及使用Proto3作为IDL与传输数据格式的通用的开源RPC架构。

<!-- more -->

> And Square, which has been working with Google on gRPC since the very early days, is connecting polyglot microservices within its infrastructure. - [gRPC: a true internet-scale RPC framework is now 1.0 and ready for production deployments](https://cloudplatform.googleblog.com/2016/08/gRPC-a-true-Internet-scale-RPC-framework-is-now-1-and-ready-for-production-deployments.html)

## I. 特点

- 低延迟、高拓展、高性能
- 目前Google、Square等贡献代码
- 已经在Google云服务、Netflix、CoreOS、Vendasta、Cockroachdb等上使用
- 基于HTTP/2协议标准设计(双向流、头部压缩、多复用请求、二进制以帧为单位传输等)，节省带宽，降低TCP连接次数、节省CPU使用、电池寿命，便于负载均衡、认证、日志监控
- 使用ProtocolBuffer3(也可以使用proto2)作为IDL(Interface Definition Language)来定义服务以及数据的格式，使用简单快速接入
- 支持双向通信(Bidirectional Streaming): 可以通过单个gRPC建立的一个stream，使得客户端与服务端可以相互发送消息(有序)
- 支持同步与异步的RPC
- 目前支持: C（核心库)、C++、Ruby、NodeJS、Python、PHP、C#、Objective-C(IOS)、Java(后端服务/Android)、go
- 处理了所有的复杂的：严格的约定、数据序列化、有效的网络通信、安全校验、访问控制、分布式等

> gRPC can help make connecting, operating and debugging distributed systems as easy as making local function calls; the framework handles all the complexities normally associated with enforcing strict service contracts, data serialization, efficient network communication, authentications and access control, distributed tracing and so on - [gRPC: a true internet-scale RPC framework is now 1.0 and ready for production deployments](https://cloudplatform.googleblog.com/2016/08/gRPC-a-true-Internet-scale-RPC-framework-is-now-1-and-ready-for-production-deployments.html)


## II. 安全校验

- 支持SSL/TLS
- 支持通过实现gRPC提供的接口来实现自己的校验机制


## III. 支持的服务方法

1. 类似本地调用方法: 客户端发送一个请求然后收到一个响应
2. 客户端发送一个请求给服务器，并且不断从服务端返回的数据流中读取数据，直到没有数据
3. 客户端使用stream不断写入一系列的数据并发送给服务端，当客户端完成写入以后等待服务端读取以及服务端的响应
4. 客户端与服务端通过可读写的stream发送一系列的消息实现双向通信: 两个stream是相互独立的，因此两端可以同时或错开无序的发送与接收数据

## IV. 流程

#### 开发流程

1. 通过proto编写接口
2. 通过proto编译插件，生成客户端与服务端的代码
3. 服务端实现在proto中定义的接口, gRPC负责: 解码客户端的请求，执行服务端方法，编码服务端响应
4. 客户端会有一个本地对象(如stub)其中已经包含了实现，因此客户端只需要调用这些方法，封装请求参数，等待返回即可。


#### 通信流程

> - 客户端可以通过请求的metadata上面的deadline参数告知服务度客户端可以等待响应的时间(超过`DEADLINE_EXCEEDED`)
> - 服务端与客户端的结束状态可能是不同的，有可能一边是正确结束了，一边却是错误结束的(如客户端发现超时了，刚好服务端那边检测没有超过时间，然后成功了)
> - 异步的RPC方法调用允许客户端或服务端将其随时取消

##### 一般RPC调用通信

1. 客户端通调用方法访问服务端方法，在metadata上面带上要访问的方法名、deadline等
2. 服务端可以直接方法初始化metadata 或 等待并接收客户端发送请求数据
3. 服务端获执行相关操作生成响应数据、状态码，状态信息、结束的metadata等
4. 客户端收到响应，完成调用

##### 双向通信

> 利用gRPC做push通道: [Question about events or push notification](https://github.com/grpc/grpc/issues/8718)

1. 客户端通调用方法访问服务端方法，在metadata上面带上要访问的方法名、deadline等
2. 服务端可以直接方法初始化metadata 或 等待并接收客户端发送请求数据
3. 客户端与服务端可以无序的独立完成读写操作
4. 服务端与客户端可以开始相互的发送消息

具体双向通信流程

- **客户端到服务端:** 带上`Call Header`, 以及optional的`Initial-Metadata`, `0`或`Payload Messages`数据
- **服务端到客户端:** 带上optional的`Initial-Metadata`, 以及`0`或`Payload Messages`数据
- **结束:** 带上`Status`，以及optional的`Status-Metadata` (也称为`Trailing-Metadata`)

其中的数据结构

- gPRC的双向stream是直接映射HTTP/2的stream，其中的每个请求的id是对应stream的id
- `Call Header`与`Initial Metadata`使用HTTP/2的`headers`发送因此也采用HPACK压缩
- `Payload Messages`将映射为字节流，在发送端组装为HTTP/2帧，在接收端重新组装为数据
- `Status`与`Trailing-Metadata`是通过HTTP/2的trailing headers进行传输

## V. PING帧

- 在deadline之内如果发送PING没有收到响应，服务端就会于`CANCELLED`状态直接结束所有操作，如果是客户端就会以UNAVAILABLE状态结束
- 发送PING的频率取决于网络环境，也可以自由的进行调整

## VI. 案例

- [官方案例](https://github.com/grpc/grpc/tree/master/examples)
- [自动服务端负载均衡docker(使用nghttp2、registrator、consul)](https://github.com/amitripshtos/grpc-docker-lb)


## VII. 其他

### gRPC比较Thrift

- gRPC基于最新的HTTP2公有协议,(Thrift采用私有协议)，gRPC更好做维护、性能优化、缓存、集群
- gRPC采用proto3.x作为IDL，更易于配置
- gRPC采用proto3.x作为传输数据的数据结构，序列化，反序列化速度比thrift稍好
- gRPC目前社区逐渐活跃，
- gRPC是非常与Google内部类似已经使用许多年的版本，但Thrift虽然在2007年就release了，但是内部很多重要的迭代Facebook拒绝贡献到开源社区中
- Facebook到后面就都没有维护Thrift了，都丢给社区维护了，不过14年的时候自己建了一个使用C++写的fbThrift

### gRPC使用反向代理

#### Nginx

> [gRPC-PHP](https://github.com/grpc/grpc/tree/master/src/php#use-the-grpc-php-extension-with-nginxphp-fpm)是可以的，但是其余的(如[gRPC-Java目前暂时不行](https://github.com/grpc/grpc-java/issues/2559)，但是[正在实现](https://github.com/grpc/grpc.github.io/issues/230#issuecomment-244508727))

- [讨论迁移gRPC nginx - 2016.03](https://trac.nginx.org/nginx/ticket/923)
- [How can I use nginx 1.9.5 as reverse proxy with gRPC](https://groups.google.com/forum/#!searchin/grpc-io/nginx|sort:relevance/grpc-io/gpNnAprcCxc/5Mr0xwAaCgAJ): 解释为什么grpc-php已经适配，但是grpc-java没有
- [nginx reverse proxy -Unknown frame type 50](https://github.com/grpc/grpc/issues/4911) 最终原因是nginx没有支持http2导致

#### 其他方案

- [Go语言编写的gRPC的反向代理](https://github.com/mwitkow/grpc-proxy)
- [Envoy](https://github.com/lyft/envoy/tree/master/examples/grpc-bridge)
- 可以使用nghttpx来做gRPC的负载均衡，而非nginx: [gRPC with nghttp2](https://movinggauteng.co.za/blog/2016/08/03/grpc-with-nghttp2/)、[Load balancing gRPC servers](https://groups.google.com/forum/#!topic/grpc-io/Ye9bcx62mJk)、[nghttpx - HTTP/2 proxy - HOW-TO](https://nghttp2.org/documentation/nghttpx-howto.html)

---

- [gRPC reaches 1.0 - Square](https://medium.com/square-corner-blog/grpc-reaches-1-0-85728518393b#.xcevdgx5x)
- [grpc/grpc - 开源库](https://github.com/grpc/grpc)
- [gRPC - official website](http://www.grpc.io/)
- [grpc-ecosystem/polyglot - 可以与任意gRPC服务端通信的客户端(Square将这个整合在它的架构中)](https://github.com/grpc-ecosystem/polyglot)
- [gRPC相关的学习材料](https://jaigouk.com/grpc/)
- [gRPC不同语言的性能数据](https://performance-dot-grpc-testing.appspot.com/explore?dashboard=5712453606309888)
- [gRPC: a true internet-scale RPC framework is now 1.0 and ready for production deployments](https://cloudplatform.googleblog.com/2016/08/gRPC-a-true-Internet-scale-RPC-framework-is-now-1-and-ready-for-production-deployments.html)
- [Allow proxy_http_version 2.0](https://trac.nginx.org/nginx/ticket/923)
- [gRPC学习笔记](https://skyao.gitbooks.io/leaning-grpc/content/introduction/)
- [状态码、请求头描述、响应头描述](http://www.grpc.io/docs/guides/wire.html)
- [Is GRPC better than Thrift?](https://www.quora.com/Is-GRPC-better-than-Thrift)

---

> © 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
