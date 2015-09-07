title: TP-LINK WR720N v3 刷OpenWrt 完美翻墙
date: 2015-09-06 23:20:03
tags:
- 翻墙
- OpenWrt
- ShadowSocks
- WR720N

---

> 之前买了一台改过硬件的TP-Link WR841N-V7路由器，并且成功刷机OpenWrt也完成了翻墙，WR841N-V7的更多详情可以看[这里](http://jacksgong.com/2015/09/05/TP-Link-WR841N-V7-OpenWrt-ShadowSocks/)，但是可能卖家焊接的有问题，导致老是听到滋滋滋高频率的赤耳声音，很不爽，因此无奈拿起之前的TL-WR720N V3，这台内存小，存储空间小的路由器，倒腾起来，没想到，踩了一天的坑，总算是完美翻墙。

---

本文不会再提到坑的过程，有些地方稍微点下，主要是步骤。

---

<!-- more -->

## I. 选用固件

- 没有刷过OpenWrt，选择这个: [openwrt-ar71xx-generic-tl-wr720n-v3-squashfs-factory.bin](http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/openwrt-ar71xx-generic-tl-wr720n-v3-squashfs-factory.bin)

- 已经刷过OpenWrt的选择这个: [openwrt-ar71xx-generic-tl-wr720n-v3-squashfs-sysupgrade.bin](http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/openwrt-ar71xx-generic-tl-wr720n-v3-squashfs-sysupgrade.bin)

## II. 刷入目标OpenWrt

#### 没有刷过OpenWrt的路由器

连接以后，登录路由器，在系统升级页面选择刷机包，选择不配置，确定升级，在升级过程不可断电。升级结束后，就刷好了。

#### 刷过OpenWrt的路由器

1. 通过`scp openwrt-ar71xx-generic-tl-wr720n-v3-squashfs-sysupgrade.bin root@192.168.2.1:/tmp`拷贝到路由器的`/tmp`目录
2. 进入openwrt以后`mtd write /tmp/openwrt-ar71xx-generic-tl-wr720n-v3-squashfs-sysupgrade.bin firmware`刷入。
3. 完成以后重启。`reboot`

## III. 修改默认源为国内源

> 替换为: http://mirrors.ustc.edu.cn/openwrt 这个源，速度飕飕的。
> 最后几行是根据[ShadowSocks安装](http://openwrt-dist.sourceforge.net/)该官方文档添加的源，方便后面shadowsocks安装。

#### 1). ssh连上openWrt
#### 2). 修改`/etc/opkg.conf`文件内容为:

```
dest root /
dest ram /tmip
lists_dir ext /var/opkg-lists
option overlay_root /overlay
src/gz barrier_breaker_base http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/14.07/ar71xx/generic/packages/base
src/gz barrier_breaker_luci http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/14.07/ar71xx/generic/packages/luci
src/gz barrier_breaker_packages http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/14.07/ar71xx/generic/packages/packages
src/gz barrier_breaker_routing http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/14.07/ar71xx/generic/packages/routing
src/gz barrier_breaker_telephony http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/14.07/ar71xx/generic/packages/telephony
src/gz barrier_breaker_management http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/14.07/ar71xx/generic/packages/management
src/gz barrier_breaker_oldpackages http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/14.07/ar71xx/generic/packages/oldpackages

#shadowsocks
src/gz openwrt_dist http://openwrt-dist.sourceforge.net/releases/ar71xx/packages
src/gz openwrt_dist_luci http://openwrt-dist.sourceforge.net/releases/luci/packages
```

## IV. 挂载u盘(参考[加菲猫的博客](http://coffeecat.info/?p=175)进行调整，优化)

#### 1). 安装包

```
opkg update
opkg install kmod-usb-ohci kmod-usb2 kmod-fs-ext4 kmod-usb-storage block-mount 	kmod-nls-base kmod-nls-cp437 kmod-ipt-nat-extra iptables-mod-nat-extra
```

ps: 安装过程中会提示: `kmod: failed to insert /lib/modules/…`的错误，不要管，回头重启就好了。

#### 2). 现在关闭路由器

运行 `df`，会发现rootfs只剩下40k左右。

#### 3). 准备

1. 格式化准备好的u盘为`ext4`，并插入路由器的usb口。
2. 将路由器模式开关调为3g，开启路由器。
3. 等到路由器灯不闪了，ssh登录路由器。

#### 4). 挂载操作

1. 运行`ls /dev/sda*`，如果显示`/dev/sda /dev/sda1 ...`，说明u盘已经认出来了。否则拔出来格式化下。
2. 接着运行

```
block detect > /etc/config/fstab
vim /etc/config/fstab
```

修改内容为(uuid不要改动)

```
config 'global'
        option  anon_swap       '0'
        option  anon_mount      '0'
        option  auto_swap       '1'
        option  auto_mount      '1'
        option  delay_root      '5'
        option  check_fs        '0'

config 'mount'
        option  target  '/overlay'
        option  uuid    '4a639f83-8137-f649-0f2c-79d66189a4ca'
        option  fstype  ext4
        option  options rw,sync
        option  enabled '1'
        option  enabled_fsck 0

config 'swap'
        option  device  '/dev/sda2'
        option  enabled '1'
```

接着把4M文件系统中的文件拷贝到u盘

> 这么做附带是，能够从u盘重启失败，把u盘拔出来，还是可以通过路由器4M闪存进入系统操作

```
mkdir /mnt/sda1
mount /dev/sda1 /mnt/sda1
mkdir -p /tmp/cproot
mount --bind / /tmp/cproot/
tar -C /tmp/cproot/ -cvf - . | tar -C /mnt/sda1 -xf -
umount /dev/sda1
umount /tmp/cproot
echo option force_space >> /etc/opkg.conf
```

重启路由器

#### 5). 挂载最后的配置

1. 通过网页输入路由器ip进入luci
2. 选择system->mount point，可以看到rootfs已经变为U盘的大小
3. 最后的swap那边，勾选enable
4. 在Mount points，找到/dev/sda1那行，点击删除
5. 在Mount points后面点击添加
6. 选择/dev/sda1，文件系统选择ext4，这时候会出来一个选项，设置为rootfs，选中它，再选中启用
7. 保存并应用

## V. 安装chinadns和shadowscks

> 参考 [ShadowSocks安装](http://openwrt-dist.sourceforge.net/)

#### 1). 安装ipset

```
opkg update
opkg install ipset
```

ps: 安装过程中如果提示`kmod:failed to insert /lib/modules/...`的错误不用管他。

好了以后，重启路由器。

#### 2). ssh登录路由器，安装软件

```
opkg update
opkg install libpolarssl
opkg install resolveip
opkg install luci-i18n-chinese
opkg install ChinaDNS
opkg install luci-app-chinadns
opkg install shadowsocks-libev-spec
opkg install luci-app-shadowsocks-spec
```

#### 3). 通过路由器ip登录 luci，可以将luci修改为中文

选用system -> system -> language 选择中文
重启路由器

## VI. 配置shadowsocks和chinadns

#### 1). 通过路由器ip访问luci

#### 2). 配置ChinaDNS

进入 服务->ChinaDNS 修改上游服务器为:

```
223.6.6.6,123.125.81.6,114.114.115.115,114.114.114.114,8.8.4.4,127.0.0.1:5151
```

#### 3). 配置Shadowsocks

1. 进入 服务->ShadowSocks 配置好全局配置，UDP转发 选择勾选。
2. UDP本地端口保证与ChinaDNS中 上游服务器 中设置的本地的端口一样: 5151。

#### 4). DHCP/DNS设置

> 4个是为了保证稳定性，否则经常会出现解析失败导致网页无法打开，

网络->DHCP/DNS设置->基本设置->DNS转发设置为:

> 这里确实是#号

```
127.0.0.1#5353
127.0.0.1#5353
127.0.0.1#5353
127.0.0.1#5353
```

基本设置->host和解析文件

1. 忽略解析文件 打勾
2. 忽略HOSTS文件 打勾

#### 5). 更新ChinaDNS过滤ip

> `/etc/chinadns_chnroute.txt` 替换为 服务->ChinaDNS中的 国内路由表 地址

```
opkg update
opkg install libcurl curl
curl 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | grep ipv4 | grep CN | awk -F\| '{ printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/chinadns_chnroute.txt
```

---

- [国内源](http://mirrors.ustc.edu.cn/openwrt/openwrt/barrier_breaker/)
- [720N 4M-8M固件，含NAS、3G、Printer，支持3070和8187网卡[20120914更新]](http://www.right.com.cn/forum/thread-91571-1-1.html)
- [wr720n原厂_4M_编程器_固件，要的拿走](http://www.right.com.cn/forum/forum.php?mod=viewthread&tid=102354&highlight=wr720n)
- [TP-LINK TL-WR720N V3 OpenWrt 固件下载](http://blog.nanpuyue.com/2012/011.html)
- [【U-Boot】U-Boot 刷机方法大全](http://www.right.com.cn/forum/thread-154561-1-1.html)
- [Flash 由4M改8M/16M, u-boot不锁死可刷写, openwrt源码的修改 ](http://blog.chinaunix.net/uid-27194309-id-3407524.html)
- [TP-Link wr720n Openwrt 科学上网改造，使用ChinaDNS + Shadowsocks 攻略](http://coffeecat.info/?p=175)
- [解决OpenWRT Opkg Update Bad Address 问题](https://lostman.org/openwrt-opkg-update-bad-address/)
- [ShadowSocks安装](http://openwrt-dist.sourceforge.net/)
- [Where to get packages](http://wiki.openwrt.org/doc/packages)
- [南浦月 TP-LINK TL-WR720N V3 OpenWrt 固件下载](http://blog.nanpuyue.com/2012/011.html)
