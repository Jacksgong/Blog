title: 网件R7800 Shadowsocks + ChinaDNS + KcpTun实现YouTuBe 4K流畅体验
date: 2018-11-25 16:44:03
updated: 2018-11-25
categories:
- 网络
tags:
- R7800
- 网件
- KcpTun
- Shadowsocks

---

{% note info %} 由于出口带宽的限制与拥塞，仅仅通过简单的V2ray+mKcp或者是SS+BBR实际上是很难达到YouTuBe 4K视频的流畅观影体验的，V2Ray+mKcp中由于对于kcp很难进一步定制，不像kcptun上层接口就支持灵活的定制，因此mKcp一直只能做到1080P流畅体验，切换到4K往往会比较卡顿，因此这边开始着手进行SS+Kcptun在R7800上的使用。{% endnote %}

<!-- more -->

## 前言

由于通过KcpTun相比于[前面我们配置的V2ray](https://blog.dreamtobe.cn/r7800-openwrt-v2ray/)来说没有复杂的混淆与动态端口，因此在一定情况下会相对轻量些，只需要不断怼流量，不过通过`fast.com`中测试下来的速度应该是不如V2ray方案(至少我这边测试下来的情况是的)，但是测试耗时却会快很多很多，但是由于KcpTun可以有很灵活的配置，这边可以通过不断堆流量让整个速度稳定在较高的水平，因此这边的实际体验是通过SS+KcpTun可以流畅体验YouTuBe 4K视频，不过在看4K视频时R7800的CPU会稳定在30%左右:

![](/img/r7800-ss-kcptun-3.png)

## I. 服务器端准备

这块请直接参看这篇文章: [翻墙的VPS选择与SS快速搭建与优化](https://blog.dreamtobe.cn/ss-and-vps/)

## II. 路由器配置Shadowsocks + ChinaDNS

首先建议可以先通过[这篇文章](https://blog.dreamtobe.cn/r7800-openwrt-v2ray/)中除V2ray部分的准备工作，然后我们再接下来操作。

### 1. 添加dist包


如果你不是r7800，你可以通过以下指令来确定自己的CPU架构, 然后做相应的调整:

```
opkg print-architecture|tail -n 1|awk '{print $2}'
```

首先添加 a65535 的 gpg key，只有这样，第三方的包才能通过签名验证:

```
wget http://openwrt-dist.sourceforge.net/packages/openwrt-dist.pub -O /tmp/openwrt-dist.pub
opkg-key add /tmp/openwrt-dist.pub
```

然后添加:

```
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/packages/base/arm_cortex-a15_neon-vfpv4
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/packages/luci
```

### 2. 生效ChinaDNS + Shadowsocks

#### 安装必要的包(这些包一共大约3M)

```
opkg update
opkg install curl bind-dig ChinaDNS luci-app-chinadns dns-forwarder luci-app-dns-forwarder shadowsocks-libev luci-app-shadowsocks
```

`ss-redir`支持 **UDP代理** 其依赖 `ip`与`iptables-mod-tproxy`软件包:

```
opkg find ip-full
opkg find *tproxy*
opkg install ip iptables-mod-tproxy
```

#### 配置

DNSmasq:

```
uci set dhcp.@dnsmasq[0].nohosts=1
uci set dhcp.@dnsmasq[0].noresolv=1
uci set dhcp.@dnsmasq[0].local=127.0.0.1#5353
uci changes
uci commit
```

关闭`Use DNS servers advertised by peer`来避免WAN接口被 **上层路由器** 指定DNS服务器:

```
uci set network.wan.peerdns=0
```

Shadowsock:

```
uci set shadowsocks.@servers[0].server=45.67.89.10
uci set shadowsocks.@servers[0].server_port=12345
uci set shadowsocks.@servers[0].password=SS_SRV_PASS
uci set shadowsocks.@servers[0].encrypt_method=chacha20-ietf-poly1305

uci set shadowsocks.@transparent_proxy[0].main_server=cfg0a4a8f

uci set shadowsocks.@access_control[0].lan_target=SS_SPEC_WAN_AC
uci set shadowsocks.@access_control[0].wan_bp_list=/etc/chinadns_chnroute.txt
uci changes
uci commit
```

这边要注意的是其中的`cfg0a4a8f`是别名，这边如果存在问题可以通过luci上进行手动调整。


Dns-Forwarder:

```
uci set dns-forwarder.@dns-forwarder[0].enable=1
uci set dns-forwarder.@dns-forwarder[0].listen_addr='0.0.0.0'
uci set dns-forwarder.@dns-forwarder[0].listen_port='5300'
uci set dns-forwarder.@dns-forwarder[0].dns_servers='8.8.8.8'
uci changes
uci commit
```

ChinaDNS:

```
uci set chinadns.@chinadns[0].enable=1
uci set chinadns.@chinadns[0].server='223.5.5.5,127.0.0.1:5300'
uci changes
uci commit
```

#### 启动与验证

Shadowsocks:

```
/etc/init.d/shadowsocks enable
/etc/init.d/shadowsocks start
pgrep -lf ss
netstat -lntpu|grep ss
```

Dns-Forwarder:

```
/etc/init.d/dns-forwarder enable
/etc/init.d/dns-forwarder start
pgrep -lf dns-forwarder
netstat -lntpu|grep dns-forwarder
```

ChinaDNS:

```
/etc/init.d/chinadns enable
/etc/init.d/chinadns start
pgrep -lf chinadns
netstat -lntpu|grep chinadns
```

测试下DNS:

```
dig +short dropbox.com @223.5.5.5
dig +short dropbox.com @127.0.0.1 -p 5353
dig +short dropbox.com @127.0.0.1 -p 5300
dig +short dropbox.com
```

![](/img/r7800-ss-kcptun-1.png)

重启dnsmasq进行生效:

```
/etc/init.d/dnsmasq restart
```

自此已经可以翻墙，接下来我们通过KcpTun进行加速。

## III. 配置KcpTun以及生效到SS上

Kcptun相对比较简单，主要通过Kcptun的执行指令+kcptun在luci上工具带的服务进行配置:

### 1. 添加KcpTun指令

首先我们知道R7800的CPU的架构是armv7的，因此这边直接在[Release页面](https://github.com/xtaci/kcptun/releases)上直接下载对应CPU架构的包,比如这边我们R7800就直接下载`kcptun-linux-arm-xxx.tar.gz`到，我们解压后，只需要用其中的`client_linux_arm7`。

我们将`client_linux_arm7`放到路由器的`/usr/bin`并重命名为`kcptun`，然后执行下面的命令让其拥有执行权限:

```
chmod +x /usr/bin/kcptun
```

### 2. 安装KcpTun LUCI


从[这里](https://github.com/kuoruan/luci-app-kcptun/releases)下载`luci-app-kcptun_1.4.5-1_all.ipk`与`luci-i18n-kcptun-zh-cn_1.4.5-1_all.ipk`，然后通过以下指令进行安装:

```
opkg install luci-app-kcptun_*.ipk
opkg install luci-i18n-kcptun-zh-cn_*.ipk
```

### 3. 开启KcpTun

安装好后，通过`服务`->`Kcptun服务`中设置`客户端文件`为`/usr/bin/kcptun`并且在`服务端管理`中添加一个KcpTun的设置(这些你应该在[这里](https://blog.dreamtobe.cn/ss-and-vps/)VPS上已经配置好了)，添加好后，在`设置`中配置`服务端地址`为刚刚配置好的，然后点击保存并运行。

![](/img/r7800-ss-kcptun-2.png)

确定下客户端状态是否是显示`运行中`，如果不是，可以`ssh`登录上路由器后，通过`service kcptun start`进行启动即可。

需要注意的是，在`Kcptun - 编辑服务端`时其中的`本地端口`随意设置一个，比如这里我们设置为`17600`，还有`本地监听地址`这边直接设置为`0.0.0.0`即可。

开启后可以通过以下指令进行验证:

```
netstat -lntpu|grep kcptun
```

### 4. 配置Shadowsocks，让其走KcpTun

我们假设上面我们设置的`本地端口`为`17600`，我们通过Luci界面，或者是`ssh`登录上去通过以下指令修改让Shadowsocks走Kcptun:

```
uci set shadowsocks.@servers[0].server=127.0.0.1
uci set shadowsocks.@servers[0].server_port=17600
uci changes
uci commit
```

至此Shadowsocks就已经走了KcpTun。

### 5. 其他

由于Shadowsocks依赖Kcptun，这边我们需要将Shadowsocks启动顺序延后，编辑`/etc/init.d/shadowsocks`将原本的`START=90`修改为`START=99`。

---

- [ChinaDNS + Shadowsocks](https://lvii.gitbooks.io/outman/content/ss.openwrt.html)
- [Shadowsocks + GfwList 实现 OpenWRT / LEDE 路由器自动翻墙](https://cokebar.info/archives/962)
- [Openwrt配置Shadowsocks](http://notes.guoliangwu.com/2017/04/02/OpenWrt-ShadowSocks-Config/)
- [OpenWrt 路由器安装 KCPTun 客户端](https://cyhour.com/479/)