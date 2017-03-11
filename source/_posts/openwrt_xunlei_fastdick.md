title: OpenWrt通过迅雷快鸟提速
date: 2016-05-29 14:30:03
permalink: 2016/05/29/openwrt_xunlei_fastdick
categories:
- OpenWrt
tags:
- OpenWrt
- 迅雷快鸟
- Fastdick
- 宽带提速

---

> 这次提速是在Newifi Y1上([Newifi Y1 刷Openwrt 自配Shadowsocks高稳定翻墙](http://blog.dreamtobe.cn/2016/04/24/newifi_openwrt/))，不过只要是Openwrt都可以参考这个教程，整个提速的是基于[fffonion/Xunlei-Fastdick](https://github.com/fffonion/Xunlei-Fastdick)，十分的给力，我这边的宽带下行原本是30M，成功提速到50M。

<!-- more -->

---

## 最终结果图:

> 电信宽带测速网址: http://sh.189.cn/support/netreport/

![](/img/openwrt_xunlei-fastdick-1.png)

首先对于是否支持快鸟提速可以参考下迅雷官方给出的支持地图: http://k.xunlei.com/notice.html

---

## I. 准备

#### 1. 准备一个快鸟帐号

可以到淘宝买快鸟帐号或者直接到[迅雷会员官网](http://vip.xunlei.com/vip_service/introduce/)购买。

#### 2. 执行文件准备

直接clone [fffonion/Xunlei-Fastdick](https://github.com/fffonion/Xunlei-Fastdick) 项目。

#### 3. 准备环境

准备一个已经有python运行环境的地方(当然也可以直接在openwrt上面操作(`opkg install python`))。


## II. 生成运行ipk

#### 1. 配置帐号

在clone下来的fffonion/Xunlei-Fastdick项目目录(或与`swjsq.py`文件同目录就行)下创建文件`swjsq.account.txt`，输入帐号与密码格式如: `ahaha,123456`（英文逗号），并保存。

#### 2. 执行脚本

执行 `python ./swjsq.py &`，出现如下图 `Upgrade done: Down xxx, Up xxx`，表明提速成功，此时本地会生成`swjsq_0.0.1_all.ipk`文件。

![](/img/openwrt_xunlei-fastdick-2.png)

## III. 安装

#### 1. 安装ipk

在OpenWrt的`swjsq_0.0.1_all.ipk`所在目录执行 `opkg install swjsq_0.0.1_all.ipk`，进行安装。

#### 2. 配置开机启动

在OpenWrt的`/etc/hotplug.d/iface/`目录下，创建文件`99-xunlei`，并添加以下脚本:

```
#!/bin/sh
[ "$ACTION" = ifup ] || exit 0
[ "$INTERFACE" = wan ] || exit 0
killall -9 swjsq
(/bin/swjsq &)
```

#### 3. 重启完成

重启路由器，此时到OpenWrt的LUCI界面，在Status->Processes会看到有一个`swjsq`的进程在运行，说明已经成功运行。

![](/img/openwrt_xunlei-fastdick-3.png)

## IV. 升级

这块记得Watching [fffonion/Xunlei-Fastdick](https://github.com/fffonion/Xunlei-Fastdick) 项目，有更新的时候当然是要重新生成ipk，重新卸载安装即可。

---

本文已经发布到JackBlog公众号，可请直接访问: [OpenWrt通过迅雷快鸟提速 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483654&idx=1&sn=151940b17d4f1bd03076988027a35831)

---

- [加速你的带宽—迅雷快鸟OPENWRT插件](http://www.openwrt.org.cn/bbs/thread-19695-1-1.html)

---
