title: Newifi Y1 刷Openwrt 自配Shadowsocks高稳定翻墙
date: 2016-04-24 00:22:03
tags:
- 翻墙
- OpenWrt
- ShadowSocks
- Newifi

---

> 之前我用的是 TP-LINK WR720N v3，也[刷了OpenWrt进行翻墙](http://blog.dreamtobe.cn/2015/09/06/wr720n-v3-openwrt-shadowsocks/)，上段时间同事一直给我推荐 Lenovo的 Newifi，各项硬件都不错，于是就入手了，网上查了下，简单的刷了个基于Openwrt的Pandorabox，结果发现相同的节点，看YouTuBe连720p都卡成了翔，还不如我之前WR720N来得稳定，严重影响工作效率，于是就倒腾起来，决定还是刷官网的OpenWrt。刷完官网的OpenWrt以及配置以后，速度飕飕的，又回到了YouTuBe流畅1080p的时代，而且各方面感觉相比之前使用TP-LINK WR720N v3，会来的更快些。

<!-- more -->

![](/img/newifi-1.png)

---

## I. 刷入官网OpenWrt

> Newifi Y1 OpenWrt 官方Wiki: https://wiki.openwrt.org/toh/lenovo/lenovo_y1_v1

1. 下载Newifi Y1 系统镜像 ： http://downloads.openwrt.org/chaos_calmer/15.05/ramips/mt7620/openwrt-15.05-ramips-mt7620-Lenovo-y1-squashfs-sysupgrade.bin
2. 拔掉路由去电源。
3. 将路由器连接电脑，并且电脑端新建一个连接，设置IP `192.168.1.1` 以及掩码 `255.255.255.0`，网关 `192.168.1.1`。
4. 长按复位键的同时连接电源，看到路由器上面有两个LED等在闪说明进入了刷机模式。
5. 选择下载的镜像刷入。

## II. 基本配置

#### 1. 安装5G网络

安装一个包就可以了，登录终端以后执行以下命令:

```
opkg update && opkg -y install kmod-mt76
```

#### 2. 镜像源配置

> 留意是: `chaos_calmer`，并且是 `ramips` 架构。

可选择源:

- https://openwrt.mirrors.ustc.edu.cn/chaos_calmer/15.05/ramips/mt7620/
- http://ba.mirror.garr.it/mirrors/openwrt/chaos_calmer/15.05/ramips/mt7620/
- http://downloads.openwrt.org/chaos_calmer/15.05/ramips/mt7620/

## III. 安装ChinaDNS、Shadowsocks与相关组件包

> 由于不同于以前用的WR720N的情况，mt7620的官方源中并没有相关组件包，因此都需要自己下载配置。
> 自行下载的可以下载下来通过`scp`传到路由器，然后再执行`opkg install 本地ipk文件路径`进行安装。

首先一些基本的组件包官方源是有的直接安装:

```
opkg update
opkg install libpolarssl
opkg install resolveip
```

#### 1. 安装ChinaDNS以及其luci

> https://github.com/aa65535/openwrt-chinadns

- ChinaDNS(我当时选用`1.3.2-d3e75dd`(当时最新版本)): https://sourceforge.net/projects/openwrt-dist/files/chinadns/
- ChinaDNS-luci(我当时选用`1.4.0-1_all`(当时最新版本): https://sourceforge.net/projects/openwrt-dist/files/luci-app/chinadns/

#### 2. 安装Shadowsocks以及其luci

> https://github.com/shadowsocks/openwrt-shadowsocks

- 下载安装openssl: http://jaist.dl.sourceforge.net/project/openwrt-dist/depends-libs/ramips/libopenssl_1.0.1i-1_ramips_24kec.ipk
- 到[这里](https://sourceforge.net/projects/openwrt-dist/files/shadowsocks-libev/):
选用最新版本的目录进入(但是我选择的是`2.4.6-98cf545`)，然后进入`ramips`目录，下载并安装 `shadowsocks-libdev-spec_xxxx_ramips`(针对 OpenWrt 的优化版本)。
- shadowsocks-luci (选用最新版本下载安装(我当时选用的是1.4.0)): https://sourceforge.net/projects/openwrt-dist/files/luci-app/shadowsocks-spec/

## IV. 配置

基本的配置与 [TP-LINK WR720N v3刷OpenWrt完美翻墙](http://blog.dreamtobe.cn/2015/09/06/wr720n-v3-openwrt-shadowsocks/)中的(`VI. 配置shadowsocks和chinadns`)一致，配置完以后，**再进行以下最后的配置即可**。

#### 1.手动在Global Setting中选中Server

> 在 Shadowsocks 配置中 需要手动在Global Setting 中选中其中一个Server，方可运行。

![](/img/newifi-2.png)

#### 2. 手动指定过滤的IP列表

> 在 Shadowsocks 配置中 需要手动在 Access Control->Interfaces-WAN 中手动选择 Bypassed IP List。

![](/img/newifi-3.png)


---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
