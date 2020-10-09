title: 翻墙的VPS选择与SS快速搭建与优化[本文将删除]
date: 2018-02-28 11:06:03
updated: 2018-02-28
permalink: 2016/11/30/vps-ss-will-be-removed
categories:
- 网络
tags:
- 翻墙
- Shadowsocks
- VPS
- Kcptun

---

{% note info %}从十九大召开到现在，陆陆续续有看到身边的朋友反馈说是不是现在翻墙完全不work了，根据我的观察发现，其实只是GW加大了力度，特别是针对日本、美国的出口，十九大期间我换了多条线路最后还是稳定的翻墙并且保持到现在，这个笔录希望能够对诸位有所帮助。{% endnote %}

<!-- more -->

### 最终的情况

- 我使用[Vultr][vultr_url]的情况: 通过这个教程，最终的结果是各类墙外页面都能够秒开，pornhub、youtube等各类视频网站基本都可以看最高质量视频(1080P或者4K、甚至8K)。
- 费用方面: 一个月`$3.5`([Vultr][vultr_url]支持支付宝)，按小时付费，并且随时可以关停。
- 节点切换方面: 1小时内完成节点切换，如果需要的话，不过我用了几年下来，基本上没有特殊情况一年都不用切换一次。
- 关于延时方面: 延时其实只是其中一个很小的纬度，我用的延时就是`200ms`左右，但是我的情况是通过下面教程的Kcptun后(我的Kcptun的配置可以通过[这篇文章](https://blog.dreamtobe.cn/r7800-ss-kcptun/)拿到)就是能够达到上面提到的情况


### I. VPS的选择

#### 1. 前言

在十九大之前，我是采用[portal.shadowsocks.la](https://portal.shadowsocks.la)中够买的VPN，其VPS的香港与日本的线路是采用阿里云，延时极低全部直连在平时速度是极快的，但是十九大之后便变得十分不可靠，而后我自己在通过[Vultr][vultr_url]够买VPS开始自行搭建自己的SS，刚开始也并非一帆风顺。

![](/img/ss-and-vps-6.png)

最早在[Vultr][vultr_url]够买的是其在日本的VPS，刚开始是很快的，后来发现GW对其逐渐加大力度以至于后来经常出现不稳定的情况，由于[Vultr][vultr_url]是按照小时计费的，并且每小时的费用极低，于是我再创建了新加坡的VPS，通过其提供的Snapshot快速恢复了日本VPS的环境，最终新加坡线路也同日本线路一样的情况，而后我切换到美国的VPS发现情况类似。

#### 2. 最终的选择

最后我选择了[Vultr][vultr_url]在阿姆斯特丹的线路(费用: 每月`$3.5`，每小时`$0.005`)，从十九大期间一直使用到现在非常可靠稳定，速度方面youtube的访问常常都是1080P，因此VPS的选择推荐[Vultr][vultr_url]中的荷兰阿姆斯特丹的VPS。

![](/img/ss-and-vps-1.png)
![](/img/ss-and-vps-8.png)
![](/img/ss-and-vps-3.png)

其速度测试，可自行到[这里](https://www.vultr.com/faq/#downloadspeedtests)进行验证，我直接用它的阿姆斯特丹的服务器ping我上海腾讯云的服务器大约在200多毫秒:

![](/img/ss-and-vps-7.png)

### II. SS的搭建

Shadowsocks这块，推荐直接使用Teddysun的这个[一键安装脚本](https://teddysun.com/342.html)版本(如果是teddysun的这个网站挂了，可以直接拷贝[这个sh脚本](https://gist.dreamtobe.cn/Jacksgong/a7a01aacbdf1ca8b80df53fbd5df4630)，下载后执行即可)，真正做到简单省事，非常可靠。

![](/img/ss-and-vps-4.png)

#### 需要注意

唯一需要注意的可能是有人在[issue](https://github.com/shadowsocks/shadowsocks-windows/issues/1243)中提到的:

![](/img/ss-and-vps-5.png)

不过我在杭州与上海的电信线路上实际测试的结果是`aes-256-gcm`加密算法依然可靠有效，并没有出现所谓的问题。

### III. Kcptun

**Kcptun是可选的，可用可不用**。其用于加速翻墙的速度，但是需要服务端与客户端双端的支持，大概原理是使用KCP + UDP通过牺牲部分带宽来提高带宽利用率，一般来说优化效果会比较明显，特别在弱网环境。

对于服务端而言推荐使用该[一键安装脚本](https://blog.kuoruan.com/110.html)(如果这个网站挂了可以手动clone[这个github项目](https://github.com/kuoruan/shell-scripts)然后执行`kcptun/kcptun.sh`即可)，十分可靠，客户端的话[手机版的SS](https://github.com/shadowsocks/shadowsocks-android/releases)通过kcptun插件有支持，[mac版](https://github.com/shadowsocks/ShadowsocksX-NG/releases)有支持，路由器的openwrt一般也会有集成。

相关加速的其他选择还有`锐速`与[finalspeed](https://github.com/d1sm/finalspeed)。

### IV. BBR

**BBR也是可选的，可用可不用**。其是采用更激进的拥塞算法，优化了在复杂网络环境下TCP协议的吞吐量，关于BBR的详情可以参看: [这篇文章](https://blog.dreamtobe.cn/tcp-window/)与[这篇文章](https://blog.dreamtobe.cn/network_basic/)

这块也是推荐采用该[一键安装脚本](https://teddysun.com/489.html)，实测BBR对SS影响还是挺明显的。

### V. V2Ray

如果你不想使用SS + Kcptun，有另外一款更加稳定的选择方案，那就是V2Ray，针对V2Ray的搭建可以参看[这篇文章](https://blog.dreamtobe.cn/r7800-openwrt-v2ray_to_delete/)的《上V2ray》的部分。

### VI. 其他


最后如果有Ubuntu服务端维护相关的问题，欢迎转到[这篇文章](https://blog.dreamtobe.cn/maintain-website-server/)。如果有任何问题欢迎评论讨论。

[vultr_special]: https://www.vultr.com/?ref=7604654
[vultr_url]: https://www.vultr.com/?ref=7210853
