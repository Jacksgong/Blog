title: TP-Link WR841N-V7 路由器刷机 OpenWrt
date: 2015-09-05 02:08:03
updated: 2015-09-05 02:08:03
permalink: 2015/09/05/TP-Link-WR841N-V7-OpenWrt-ShadowSocks-404/
categories:
- OpenWrt
tags:
- 硬件
- 路由器
- 翻墙
- shadowsocks
- OpenWrt

---

> 由于家里，有 ipad、iphone、小米手机、小米盒子...，一直一来我都是用 shadowsocks 协助翻墙，Android 配起来还快，iphone 和 ipad 很是苦恼，没有越狱就只能在 Shadowsocks 自带 app 上玩玩，小米盒子就更不用想了，因此就琢磨着给路由器直接翻墙。

刚开始是家里刚好有一台 TP-Link WR720N，根据网上的教程很快的就刷好了，配了 wireless，network，眼看可以了，但是开始整挂载，luci，shadowsocks 时，才发现可是蛋疼的是只有 4M 内存，做起事来畏首畏尾，各种提示没有空间，...咋办，淘宝了下，直接入手了一台别人搞好的（包括硬件与软件）TP-Link WR841n v7，但是考虑到路由器的安全问题，还是打算把里面的软的全部重新刷过，重新配。

<!--more-->

## 简单说明

### I. 刷入了 Bootloader

> 根据此 [AR/QCA/MT7620 Breed, ，功能强大的多线程 Bootloader](http://www.right.com.cn/forum/thread-161906-1-1.html)，可以配合[不死 uBoot](http://www.right.com.cn/forum/thread-136444-1-1.html)这里的配置表看看对应的机型对应要下载对应的硬件配置。

1. 按住复位键再插电源，等所有网囗指示灯一闪一闪后松开复位按钮，然后在浏览器中输入 192.168.1.1 进入控制台刷机页面
2. 根据路由器机器背面的说明，录入 MAC 地址与 PIN。
3. 完成。

### II. 刷入固件

原本我选用的是: [AR 系列 OPENWRT 固件--带是像鬼 qos,qosv4,下载,vpn,翻 wall 等](http://www.right.com.cn/forum/thread-139399-1-1.html)，后来发现比较大，带的东西比较多，大神做的东西果断是给力啊，但是就是界面无法接受了点，后来就选用了设置页面好看，固件小够用的[OpenWrt ar71xx 系列 for BB r46516 4M](http://www.right.com.cn/forum/thread-114913-1-1.html)，我选的是 8M 那个。

1. 按住复位键再插电源，等所有网囗指示灯一闪一闪后松开复位按钮，然后在浏览器中输入 192.168.1.1 进入控制台刷机页面
2. 点击固件升级、上传下载来的固件(\*.bin)的固件。
3. 刷成功后，等路由器的设置的灯不再闪了，就说明重新开机成功了。

### III. 其他小坑

好吧，由于我的是**特别的**电信路由器，我这边还必须需要配置下 lan 口为静态 ip，并且配置`ipaddr`为非 192.168.1.1 的 ip 段，否则取不到 wan 口的地址，上不了网，好吧，我给配了，192.168.2.1，至此，可以正常上网工作了。

### III. ShadowSocks 配置

原本我是打算参照[这个](http://hong.im/2014/03/16/configure-an-openwrt-based-router-to-use-shadowsocks-and-redirect-foreign-traffic/)教程搞 shadowsocks 的，但是猛然在执行一半时候发现，这个固件既然已经安装了`shadowsocks-libev-spec`，显然是已经支持了，我再看了下设置页面的扩展，果然有。于是乎，嘿嘿。。

唯一需要注意的地方是: 配置文件`config.json`的格式是:

```
{
    "server":"[服务器IP地址]",
    "server_port":[服务器端口],
    "local_port":[本地端口,稍后iptables会用到],
    "password":"[密码]",
    "timeout":600,
    "method":"[加密方式]"
}
```

> 大功告成!

---

- [TP-Link WR720N 刷入 OpenWrt 之一：刷入](http://seak.me/archives/125)
- [wifi client mode with static ip](https://forum.openwrt.org/viewtopic.php?id=29667)
- [OpenWrt and WPA wireless setup](http://developwithguru.com/openwrt-and-wpa-wireless-setup/)
- [openwrt 刷机包](http://downloads.openwrt.org/snapshots/trunk/ar71xx/generic/)
- [指定 DNS 服务器](http://www.right.com.cn/forum/thread-46811-1-1.html)
- [OpenWrt Download](http://downloads.openwrt.org.cn/)
- [DNS errot](https://forum.openwrt.org/viewtopic.php?id=16929)
- [WR84n v7 改造](http://www.right.com.cn/forum/forum.php?mod=viewthread&tid=170441&highlight=wr841n)
- [不死 uBoot](http://www.right.com.cn/forum/thread-136444-1-1.html)
- [AR/QCA/MT7620 Breed, ，功能强大的多线程 Bootloader](http://www.right.com.cn/forum/thread-161906-1-1.html)
- [AR 系列 OPENWRT 固件--带是像鬼 qos,qosv4,下载,vpn,翻 wall 等](http://www.right.com.cn/forum/thread-139399-1-1.html)
- [OpenWrt ar71xx 系列 for BB r46516 4M](http://www.right.com.cn/forum/thread-114913-1-1.html)
- [OpenWrt 智能、自动、透明翻墙](https://github.com/softwaredownload/openwrt-fanqiang)

---
