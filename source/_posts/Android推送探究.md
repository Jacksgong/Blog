title: Android推送探究
date: 2013-07-12 08:35:03
permalink: 2013/07/12/Android推送探究
categories:
- Android机制
tags:
- 推送
- Android
- 探究


---

> 最近刚好公司需要用到推送，就做了一些分析并且成功的调通了几个通用的项目。
首先说下Android的推送，不像Ios的已经有了很好的C2DM的机制，虽然谷歌也提供这种机制的推送，不过介于国内…

<!--more-->
下面对一些主流的几个方案进行分析，这里参考网络上的一些分析:

## 方案1、使用GCM服务（Google Cloud Messaging）

> 简介：Google推出的云消息服务，即第二代的C2DM。

- 优点：Google提供的服务、原生、简单，无需实现和部署服务端。
- 缺点：Android版本限制（必须大于2.2版本），该服务在国内不够稳定、需要用户绑定Google帐号，受限于Google。

## 方案2、使用XMPP协议（Openfire + Spark + Smack）

> 简介：基于XML协议的通讯协议，前身是Jabber，目前已由IETF国际标准化组织完成了标准化工作。

- 优点：协议成熟、强大、可扩展性强、目前主要应用于许多聊天系统中，且已有开源的Java版的开发实例androidpn。
- 缺点：协议较复杂、冗余（基于XML）、费流量、费电，部署硬件成本高。

## 方案3、使用MQTT协议（更多信息见：http://mqtt.org/）

> 简介：轻量级的、基于代理的“发布/订阅”模式的消息传输协议。

- 优点：协议简洁、小巧、可扩展性强、省流量、省电，目前已经应用到企业领域（参考：http://mqtt.org/software），且已有C++版的服务端组件rsmb。
- 缺点：不够成熟、实现较复杂、服务端组件rsmb不开源，部署硬件成本较高。

## 方案4、使用HTTP轮循方式

> 简介：定时向HTTP服务端接口（Web Service API）获取最新消息。

- 优点：实现简单、可控性强，部署硬件成本低。
- 缺点：实时性差。

---

> 通过网络上的一些评论，与个人的测试，都是主推MQTT，辅推XMPP的。

下面就MQTT的调配做下记录以备以后使用。

### 1. 首先下载需要的文件：
http://pan.baidu.com/share/link?shareid=3690050211&uk=859141184

### 2. 下载以后，可以看到三个文件夹：

AndroidPushNotificationsDemo(Android端)、rsmb(服务端工具)、send_mqtt(服务端)

#### Android端需要注意的是：

1. 导入以后记得勾选有关包
2.PushService.java中配置MQTT_HOST为可解析的对应的服务端地址（要能ping的通的）（比如我这边用send_mqtt.dreamtobe.cn)

#### 服务端需要注意的是：

1. 修改send_mqtt/etc下的config.php中的MQTT_SERVER_HOST为对应的服务器ip.
2. 对应自己服务器系统。打开rsmb中的broker(比如centos 32，请运行./linux_ia32/broker即可）

## 我这边已经调配好一个：

http://send_mqtt.dreamtobe.cn

大家可以设置这边下载的开源代码，并且设置对应的MQTT_HOST为send_mqtt.dreamtobe.cn进行测试
如上已经配置好。

> 下面配置一款基于XMPP协议的开源项目AndroidPn（我这边只针对Tomcat）:

### 1. 先下载对应需要准备的文件：

http://pan.baidu.com/share/link?shareid=3761244206&uk=859141184

### 2. 下载以后解压，有两个文件夹：
androidpn-client(客户端)、Androidpn-tomcat(服务端)

#### 客户端需要注意：

1. 修改raw中androidpn.properties的xmppHost为服务器的ip.
服务端注意:
2. 导入myeclipse后，打开resources中的jdbc.properties 设置对应mysql的用户名密码（jdbcUsername、jdbcPassword)。
3. 设置jdbc.properties中的数据库名(下面test部分)：
jdbc:mysql://127.0.0.1:3306/test?useUnicode=true&characterEncoding=utf-8&zeroDateTimeBehavior=convertToNull
4. 创建数据库(假设上面数据库名填写test):
`create database test;`
5. 完成配置

---
