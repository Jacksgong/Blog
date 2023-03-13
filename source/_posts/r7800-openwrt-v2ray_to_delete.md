title: 网件R7800 OpenWrt使用V2Ray+mKcp+透明代理完美翻墙
date: 2018-11-17 11:51:03
updated: 2023-02-11
categories:
- 网络
tags:
- R7800
- 网件
- v2ray
- 透明代理

---

{% note info %} 本文主要介绍了基于R7800这个基于arm架构处理器的搭建openwrt以及对V2ray的安装，并适配mkcp与透明代理，其中的v2ray搭建相关理论上所有的openwrt都能够通用。{% endnote %}

<!-- more -->

首先在路由器的选择上，网件R7800是整套高通解决方案，相比于R8000、华硕AC88U等，在散热稳定性等方面有着很大的优势，为了省事以及一步到位，趁着双十一我直接入手了R7800。下面我们就开始对R7800开始手术，最终的目标是高可定制，基于kcp协议的稳定翻墙。


顺便提一下，这货还真的大，简直可以盖住我整个MBP的键盘。

![](https://blog.dreamtobe.cn/img/r7800-openwrt-3.jpeg)


这边R7800至少目前为止没有梅林等解决方案，但是其还有各类[其他选择](https://www.dropbox.com/sh/ew0gap0crn30wyk/AADQLCBF5All8wc8RXmxisqAa?dl=0)，今天我们就刷入[OpenWrt](https://openwrt.org/toh/netgear/r7800)，我们可以在[论坛上](https://forum.openwrt.org/t/netgear-r7800-exploration-ipq8065-qca9984/285)看到hnyman为其确实下了很多心血。

## I. 刷Openwrt

首先先下载[r7800-openwrt-18.06.4](http://downloads.openwrt.org/releases/18.06.4/targets/ipq806x/generic/openwrt-18.06.4-ipq806x-netgear_r7800-squashfs-factory.img)，下载完后我们通过以下步骤让路由器进入刷机模式并准备好刷机:

- 关闭路由器电源
- 按住复位键并接入电源，此时你会看到电源LED灯变成橙色等闪烁，接着会变为白色灯闪烁，此时可以放开复位键，路由器这时已经是进入了刷机模式
- 此时电脑通过网线连线路由器，并将IP设置为手动并修改为`192.168.1.20`，掩码改为`255.255.255.0`，网关改为`192.168.1.1`
- 最后进入放置刚刚下载好的img的目录

刷入openwrt:

通过`tftp`进行刷入，如果你是Mac OS，可以通过`brew install tftp`安装`tftp`，如果是windows可以自行在网络上下载`tftp`工具。然后如图进行刷入:

![](https://blog.dreamtobe.cn/img/r7800-openwrt-1.png)

通常几秒钟便完成刷机，此时路由器会自动重启并且进入openwrt。

此时记得将网络改回DHCP，便可以通过浏览器访问`192.168.1.1`进入Openwrt的luci页面了。

![](https://blog.dreamtobe.cn/img/r7800-openwrt-4.png)

此时通过`System->Administration`进入管理员密码设置，设置好密码以及SSH后便完成了第一步。

## II. 修改LAN IP

由于我这边的光猫也是路由，并且分配的是`192.168.1.x`网段，为了避免冲突，在将其接入R7800 WAN口之前，我这边将LAN IP修改为`99.1`，先SSH进入，然后输入:

```
uci set network.lan.ipaddr=192.168.99.1
uci commit
service network restart
```

修改好后，就可以将光猫出来的网线接入到WAN口，接入互联网了。配置WiFi之类的比较简单这里就不说了(需要留意下802.11ac才是传统意义的5G WiFi，配置的时候可以直接选择AP到WAN)。

## III. 添加HOST

这里我们可以修改host随意用一个不常用但是好记的域名访问，如果你觉得不需要可以跳过这步:

SSH进入路由器，然后修改`/etc/hosts`文件，添加:

```
192.168.99.1 r.cc
```

保存然后重启`network`服务:

```
service network restart
```

## IV. LUCI中文界面配置

直接通过SSH安装opkg包(也可以在luci界面中通过System->Software中搜索`uci-i18n-base-zh-cn`安装):

```
opkg update
opkg install luci-i18n-base-zh-cn
```

搞定后默认会切换到中文:

![](/img/r7800-openwrt-6.png)

## V. 配置系统运行日志

安装`rsyslog`:

```
opkg install rsyslog
/etc/init.d/rsyslog enable
/etc/init.d/rsyslog start
```

安装后，所有的运行日志都可以直接在`/var/log/messages`中查看了。

## VI. 上V2Ray

### 1. V2Ray在VPS端搭建与配置

> 当然如果你嫌麻烦也可以考虑直接通过这个[一元机场](https://xn--4gq62f52gdss.com/#/register?code=WM2k9oLY)，一个月1元钱500G流量，快速完成搭建使用，建议可以买一个备用
> 如果有Netflix/DisneyPlus的诉求，建议可以花15元买一个[Xrelay机场](https://isseys.net/#/register?code=BjU5h6ev)，这个机场主要是价格/性能最符合预期，我使用里面一个月20元一个月的188G套餐（最便宜有15元一个月108G的套餐），可以作为媒体通道，其他通道走[一元机场](https://xn--4gq62f52gdss.com/#/register?code=WM2k9oLY)或者是接下来的自建的v2ray。

要通过V2Ray进行翻墙，首先我们需要先有一台已经配置好V2Ray的墙外的VPS，对于VPS的选择与搭建可以参看[这篇文章](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)，下面我们就假定你已经通过[该篇文章](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)配置好了VPS，配置好后，你是一个Ubuntu，ok, 我们先开始搭建VPS端:

由于针对Ubuntu，[官方文档](https://www.v2ray.com/chapter_00/install.html)中已经有提供脚本安装，我们就直接通过该脚本进行安装即可:

```
bash <(curl -L -s https://install.direct/go.sh)
```

安装好后，我们对其进行配置，下面的配置`/etc/v2ray/config.json`文件，该文件如果不存在直接创建即可，如果存在将其内容完全替换为下面的内容，这里我们假设你使用的端口是`29001`，以及用于识别的UUID: `xxx-xxx-xxx-xx-xxx`(你可以通过[这里](https://www.uuidgenerator.net/)在线生成自己的UUID并替换):

```
{
  "log" : {
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log",
    "loglevel": "warning"
  },
  "inbound": {
    "port": 29001,
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "xxx-xxx-xxx-xx-xxx",
          "level": 1,
          "alterId": 64
        }
      ],
      "detour":{
        "to":"dynamicPort"
      }
    },
    "streamSettings":{
      "network":"kcp"
    }
  },
  "inboundDetour":[
    {
      "protocol": "vmess",
      "port": "10000-20000",
      "tag": "dynamicPort",
      "settings": {
        "default": {
          "level": 1,
          "alterId": 32
        }
      },
      "allocate": {
        "strategy": "random",
        "concurrency": 2,
        "refresh": 3
      },
      "streamSettings": {
        "network": "kcp"
      }
    }
  ],
  "outbound": {
    "protocol": "freedom",
    "settings": {}
  },
  "outboundDetour": [
    {
      "protocol": "blackhole",
      "settings": {},
      "tag": "blocked"
    }
  ],
 "transport":{
      "kcpSettings":{
         "mtu":1350,
         "tti":50,
         "uplinkCapacity":100,
         "downlinkCapacity":200,
         "congestion":true,
         "readBufferSize":2,
         "writeBufferSize":2,
         "header":{
            "type":"wechat-video"
         }
      }
   }
}
```

配置好后，可以通过`/usr/bin/v2ray/v2ray -test -config /etc/v2ray/config.json` 来检测下配置文件的格式是否存在问题。

我们假设你使用的是`29001`端口，并且已经通过[这篇文章](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)设置好了通过`ufw`管理防火墙，因此这边需要允许该端口的访问:

```
ufw allow 29001
```

此时重启`v2ray`服务便完成服务端配置:

```
service v2ray restart
```

### 2. V2Ray在路由器安装配置

下面假设你已经根据教程将LAN IP修改为了`192.168.99.1`，并且已经设置好了SSH，以及你的电脑已经有了SCP的工具。

首先由于R7800是高通ARM架构的CPU，这边我们先在[这里的Release列表](https://github.com/v2ray/v2ray-core/releases)下载arm架构的V2Ray，比如写这篇文章的时候最新版本是v4.5.0，这里我们就直接下载[这个v2ray-linux-arm.zip版本](https://github.com/v2ray/v2ray-core/releases/download/v4.5.0/v2ray-linux-arm.zip)

如果需要验证，下载好后可以通过对比[dgst](https://github.com/v2ray/v2ray-core/releases/download/v4.5.0/v2ray-linux-arm.zip.dgst)中描述的各类信息进行比对。

然后解压缩到`v2ray-linux-arm`文件夹，紧接着我们通过`SCP`将其传到路由器的`/root/v2ray`的目录下:

```
scp -r v2ray-linux-arm root@192.168.99.1:/root/v2ray
```

然后ssh进入路由器，然后按照常规的目录结构咱们来放置以及配置好`V2Ray`:

```
cd /root/v2ray
chmod +x v2ray v2ctl
mkdir /usr/bin/v2ray
mv v2ray v2ctl geoip.dat geosite.dat /usr/bin/v2ray/
```

除此之外`/root/v2ray`下面的其他文件其实我们都没有用到，可以直接删除。紧接着我们创建`/etc/v2ray/config.json`文件，并且将以下内容填入，这里我们假设你的VPS的IP是`x.x.x.x`，以及你的端口是`29001`、以及刚刚在VPS上你填写的UUID是`xxx-xxx-xxx-xx-xxx`:

```
{
  "log": {
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log",
    "loglevel": "warning"
  },
  "outbound": {
    "protocol": "vmess",
    "settings": {
      "vnext": [
        {
          "address": "x.x.x.x",
          "port": 29001,
          "users": [
            {
              "id": "xxx-xxx-xxx-xx-xxx",
              "level": 1,
              "alterId": 64
            }
          ]
        }
      ]
    },
    "streamSettings": {
      "network": "kcp"
    },
    "mux": {
      "enabled": true
    }
  },
  "outboundDetour": [
    {
      "protocol": "freedom",
      "settings": {},
      "tag": "direct"
    }
  ],
  "inbound": {
    "protocol": "dokodemo-door",
    "port": 5353,
    "settings": {
      "address": "119.29.29.29",
      "port": 53,
      "network": "udp",
      "timeout": 0,
      "followRedirect": false
    }
  },
  "inboundDetour": [
    {
      "domainOverride": [
        "http",
        "tls"
      ],
      "protocol": "dokodemo-door",
      "port": 1060,
      "settings": {
        "network": "tcp",
        "timeout": 30,
        "followRedirect": true
      }
    },
    {
      "protocol": "socks",
      "port": 8080,
      "settings": {
        "auth": "noauth",
        "udp": false,
        "ip": "127.0.0.1"
      }
    }
  ],
  "dns": {
    "servers": [
      "119.29.29.29",
      "localhost",
      "8.8.8.8",
      "8.8.4.4"
    ]
  },
  "routing": {
    "strategy": "rules",
    "settings": {
      "domainStrategy": "IPIfNonMatch",
      "rules": [
        {
          "type": "field",
          "domain": [
            "geosite:cn"
          ],
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "domain": [
            "google",
            "facebook",
            "youtube",
            "twitter",
            "instagram",
            "gmail",
            "domain:twimg.com",
            "domain:t.co"
          ],
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "ip": [
            "8.8.8.8/32",
            "8.8.4.4/32",
            "91.108.56.0/22",
            "91.108.4.0/22",
            "109.239.140.0/24",
            "149.154.164.0/22",
            "91.108.56.0/23",
            "67.198.55.0/24",
            "149.154.168.0/22",
            "149.154.172.0/22"
          ],
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "port": "1-52",
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "port": "54-79",
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "port": "81-442",
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "port": "444-3999",
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "port": "4001-65535",
          "outboundTag": "direct"
        },
        {
          "domain": [
            "vultr.com"
          ],
          "type": "field",
          "outboundTag": "direct"
        },
        {
          "type": "chinasites",
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "ip": [
            "0.0.0.0/8",
            "10.0.0.0/8",
            "100.64.0.0/10",
            "127.0.0.0/8",
            "169.254.0.0/16",
            "172.16.0.0/12",
            "192.0.0.0/24",
            "192.0.2.0/24",
            "192.168.0.0/16",
            "198.18.0.0/15",
            "198.51.100.0/24",
            "203.0.113.0/24",
            "::1/128",
            "fc00::/7",
            "fe80::/10"
          ],
          "outboundTag": "direct"
        },
        {
          "type": "chinaip",
          "outboundTag": "direct"
        }
      ]
    }
  },
  "transport": {
    "tcpSettings": {
      "connectionReuse": true
    },
    "kcpSettings": {
      "mtu": 1350,
      "tti": 50,
      "uplinkCapacity": 100,
      "downlinkCapacity": 200,
      "congestion": true,
      "readBufferSize": 2,
      "writeBufferSize": 2,
      "header": {
        "type": "wechat-video"
      }
    }
  }
}
```

配置好后依然可以通过`/usr/bin/v2ray/v2ray -test -config /etc/v2ray/config.json`这个来检查配置文件是否有效，注意将其中的VPS IP修改为你的VPS IP，UUID、端口改为你之前在VPS配置好的。

紧接着我们需要生效`v2ray`服务:

添加文件`/etc/init.d/v2ray`，并填写入以下内容:

```
#!/bin/sh /etc/rc.common
#
# Copyright (C) 2017 Ian Li <OpenSource@ianli.xyz>
#
# This is free software, licensed under the GNU General Public License v3.
# See /LICENSE for more information.
#

START=90

USE_PROCD=1

start_service() {
        mkdir /var/log/v2ray > /dev/null 2>&1
        procd_open_instance
        procd_set_param respawn
        procd_set_param command /usr/bin/v2ray/v2ray -config /etc/v2ray/config.json
        procd_set_param file /etc/v2ray/config.json
        procd_set_param stdout 1
        procd_set_param stderr 1
        procd_set_param pidfile /var/run/v2ray.pid
        procd_close_instance
}
```

填写好后设置其可执行的权限:

```
chmod +x /etc/init.d/v2ray
```

然后我们为其激活开机启动:
```
/etc/init.d/v2ray enable
```

自此你可以通过以下指令先将v2ray服务启动了:

```
service v2ray start
```

启动后你就可以通过`ps | grep v2ray`看到该服务在运行了:

![](https://blog.dreamtobe.cn/img/r7800-openwrt-2.png)

到这里你依然不能翻墙，除非你的电脑代理到路由器的对应`1060`的端口上，我们不废话，其实我们刚刚在路由器的`config.json`上已经配置了透明代理，只不过路由器的防火墙还没有做转发，现在我们开始配置这个转发，来完成透明代理:

配置`/etc/firewall.user`文件，在其中追加以下内容，需要特别注意将`x.x.x.x`改为你的VPS的IP:

```
iptables -t nat -N V2RAY
iptables -t nat -A V2RAY -d x.x.x.x -j RETURN
iptables -t nat -A V2RAY -d 0.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 10.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 127.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 169.254.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 172.16.0.0/12 -j RETURN
iptables -t nat -A V2RAY -d 192.168.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 224.0.0.0/4 -j RETURN
iptables -t nat -A V2RAY -d 240.0.0.0/4 -j RETURN
iptables -t nat -A V2RAY -p tcp -j REDIRECT --to-ports 1060
iptables -t nat -A PREROUTING -p tcp -j V2RAY
```

配置好保存后，这边我们重启防火墙服务:

```
service firewall restart
```

重启完成后你已经可以通过V2Ray翻墙了。

## VII. DNS污染问题处理

最后我们可以稍微优化下DNS解析，防止DNS污染的问题:

先安装`dnsmasq`，默认情况下是已经安装了的:

```
opkg install dnsmasq
```

然后通过[这里](https://coding.net/u/jacksgong/p/dns-accelerate/git/archive/master)下载`dnsmasq.d.zip`文件，然后进行解压缩，解压缩后，将该`dnsmasq.d`文件夹放入`/etc/`中，完成后，对`/etc/dnsmasq.conf`进行配置(这里我们假设你的网关地址是`192.168.99.1`):

```
listen-address=127.0.0.1
listen-address=192.168.99.1
cache-size=102400
conf-dir=/etc/dnsmasq.d
```

最后通过重启`dnsmasq`让其生效

```
service dnsmasq restart
```

自此已经完全全部配置，Have Fun!

## VIII. 最后

这边Youtube能够跑到1440P基本流畅不卡顿，跑下来平均速度在24.5Mbps(快的时候可以到30Mbps，慢的时候在18Mbps，80%的情况通常在22.5Mbps左右)，R7800的CPU基本上被吃到10%左右，算是符合预期吧，如果你的VPS选择也是参考[这篇文章](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)应该整体下来和我差不多:

![](https://blog.dreamtobe.cn/img/r7800-openwrt-5.png)

进一步优化:

由于V2Ray有各类方式可以进行伪装，这边不再需要像[这篇文章](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)中选用阿姆斯特丹，这边虽然阿姆斯特丹掉包率极低，但是由于[参考这边](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)中选用的VPS的日本东京VPS从中国电信过去是直连的，因此这边改用V2Ray后我这边便直接通过将旧的VPS打Snapshots然后恢复到新开的东京的VPS(每小时$0.007，具体如何购买可以直接参考[这篇文章](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)，改选东京即可):

![](/img/r7800-openwrt-v2ray-7.png)

并且这边针对性的对mKCP进行了优化(注意服务端与客户端两边咱们的配置文件`config.json`中都需要调整):

```
"kcpSettings": {
  "mtu": 1350,
  "tti": 50,
  "uplinkCapacity": 100,
  "downlinkCapacity": 200,
  "congestion": true,
  "readBufferSize": 2,
  "writeBufferSize": 2,
  "header": {
    "type": "wechat-video"
  }
}
```

> P.S. 如果`header`使用`wechat-video`伪装，王者荣耀等通过udp协议匹配后会直接连接失败，因此这边我们采用`utp`伪装为BT下载数据，`dtls`相关存在问题的具体原因还没有深究。

使用[这篇文章](https://blog.dreamtobe.cn/2016/11/30/vps-ss-will-be-removed/)的VPS换为东京后，并且如上做mKcp调整后，最终测速下来稳定在70Mbps左右:


![](/img/r7800-openwrt-v2ray-8.png)

---

- [V2ray网友自发编写教程](https://toutyrater.github.io/)
- [官方文档](https://www.v2ray.com/)
- [openwrt部署issue](https://github.com/v2ray/v2ray-core/issues/483#issuecomment-318895872)
- [网关服务器上设置V2Ray+dnsmasq透明代理](https://dakai.github.io/2017/11/27/v2ray.html)
- [一键脚本搭建V2Ray V2Ray配置与优化](http://kuaibao.qq.com/s/20180524G1Z2L600?refer=spider)
- [低丢包网络可以考虑关闭 FEC](https://github.com/xtaci/kcptun/issues/358)
- [init.d配置](https://odwiki.archive.openwrt.org/inbox/procd-init-scripts)
- [Openwrt设置开机启动](https://www.jianshu.com/p/20881a8b6e02)
- [OpenWrt下如何修改默认ip地址](https://blog.csdn.net/caoshunxin01/article/details/79355478)
- [OpenWrt的DNS相关设置](https://www.right.com.cn/forum/thread-194080-1-1.html)
- [openwrt 之 DNS配置文件修改](https://blog.csdn.net/zjqlovell/article/details/78598959)
- [测速](https://fast.com)
- [V2Ray各类模板配置](https://github.com/KiriKira/vTemplate)
