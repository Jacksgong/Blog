title: 将MacMini/Macbook改为家庭服务器
date: 2023-09-02 00:41:54
updated: 2024-11-10
categories:
- service
tags:
- fun
- nas
- macbook
- macmini

---

{% note info %} 如果家里有一台闲置的Mac Mini或者是Macbook，将其改为Nas也是不错的选择，本文介绍了一些基本的改Nas的方法。 {% endnote %}

<!-- more -->

## I. 前置设置

### 关闭休眠

![](/img/mac_to_nas_4b4e2319_0.png)

如果是 MacbookPro 需要通过以下指令来避免盖下盖子被休眠了：

```bash
sudo pmset -b sleep 0; sudo pmset -b disablesleep 1
```

如果你想重新恢复原有的休眠能力可以用:

```bash
sudo pmset -b sleep 5; sudo pmset -b disablesleep 0
```

### 关闭登录验证

![](/img/mac_to_nas_47116094_1.png)

### 停电后自动开机

该设置这个在Mac Mini上有，在Macbook上是没有的:

![](/img/mac_to_nas_4f31556b_2.png)

## II. 远程访问

### 远程桌面访问

![](/img/mac_to_nas_8a8b8c51_3.png)

![](/img/mac_to_nas_b278e4be_4.png)

此刻就可以将这台Mac放到任意的地方，如果是Macbook就可以盖上盖子，它已经变为一台服务器了。

在远程通过VNC客户端就可以通过`vnc://ip` 可以直接访问了，如果是Mac，自带的屏幕共享即可连接使用。

如果是Mac Mini由于服务器没有外接显示器，因此，默认VNC分辨率是比较低的，该问题问题可以通过安装一个叫`BetterDummy`的软件，然后Create一个高清屏(如下图的16:9(HD/4K/5K/6K))来解决:
![](/img/mac_to_nas_ff85c5a3_5.png)

创建后，根据大小，比如我就最后选择1600x900显示刚刚好，分辨率越高显示内容会越小，越清晰，最后记得设置开启自动启动。
![](/img/mac_to_nas_71898fd0_6.png)

### 远程终端访问

![](/img/mac_to_nas_b49407f7_7.png)

此时即可在远程通过ssh访问:

![](/img/mac_to_nas_cd0ec930_8.png)

（可选）设置仅仅支持public key的方式访问，禁止密码登录:

1. 在`~/.ssh/authorized_keys`添加好需要访问的终端的public key
2. 编辑`/etc/ssh/sshd_config`并在其中添加:

```sshd_config
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM no
```

3. 重启服务

```bash
sudo launchctl stop com.openssh.sshd
sudo launchctl start com.openssh.sshd
```

### 远程smb访问

![](/img/mac_to_nas_c8067a2b_9.png)

当然如果你是有设备需要通过SMBv1来连接，需要注意做兼容开启：创建或者编辑文件`/etc/nsmb.conf`，添加如下：

```bash
[default]
signing_required=no
streams=yes
protocol_vers_map=7
minauth=ntlmv2
```

这里的`protocol_vers_map`，表明了最低兼容SMBv1，虽然牺牲了部分性能，但是至少能用了。配置后，到共享里面重新打开关闭一次文件共享即可。


### 缓存服务器

![](/img/mac_to_nas_b55986f4_10.png)

## III. 常用服务

### Plex

Plex Server已经支持Silicon，直接到[官网](https://www.plex.tv/media-server-downloads/)，下载后打开即可。

![](/img/mac_to_nas_8fbdee35_11.png)

如果异常关机，有可能会引发Plex Server打开失败，现象就是一打开Menu Bar上面Plex的iCon出现立马消失，修复方法就是参考[官方教程](https://support.plex.tv/articles/202485658-restore-a-database-backed-up-via-scheduled-tasks/)重新恢复数据库，大概步骤:

![](/img/mac_to_nas_b67647ff_12.png)

1. 进入`/Users/[你的用户名]/Library/Application Support/Plex Media Server/Plug-in Support/Databases`
2. 将以下文件移动到任意其他目录用作备份

```
com.plexapp.plugins.library.db
com.plexapp.plugins.library.db-shm
com.plexapp.plugins.library.db-wal
com.plexapp.plugins.library.blobs.db
com.plexapp.plugins.library.blobs.db-shm
com.plexapp.plugins.library.blobs.db-wal
```

3. 然后在目录下选一个备份的重命名为`db`与`blobs.db`，这里案例我选了一个9.27自动备份的:

```bash
cp com.plexapp.plugins.library.db-2023-09-27 com.plexapp.plugins.library.db
cp com.plexapp.plugins.library.blobs.db-2023-09-27 com.plexapp.plugins.library.blobs.db
```

4. 重新打开Plex Server就修复了

### Nezha监控

参照[官方](https://nezha.wiki/guide/agent.html#%E5%9C%A8-macos-%E4%B8%AD%E5%AE%89%E8%A3%85-agent)教程，即可，唯一需要留意的是`1`代表正常启动，`0`代表没有启动，负数代表有错误。在启动时需要在设置里面点击仍然打开。

![](/img/mac_to_nas_762e59a0_13.png)


### Radarr

> 主要参考[该 Wiki](https://wiki.servarr.com/radarr/installation/macos)

1. 到Radarr[官网](https://github.com/Radarr/Radarr/releases/tag/v5.3.6.8612)下载最新版本

![](/img/mac_to_nas_475fa02b_14.png)

2. 解压缩拷贝到`/System/Applications`目录下

3. 执行脚本使用`Self-sign`:

```bash
codesign --force --deep -s - /Applications/Radarr.app && xattr -rd com.apple.quarantine /Applications/Radarr.app
```

最后打开该 App 即可。

![](/img/mac_to_nas_df5fa305_15.png)

### 其他小工具

- AutoMounter：自动挂载
- Hazel: 文件自动迁移

## IV. 路由

我们甚至可以让 Macmini 成为一台路由器，通过在虚拟机VMware Fusion上运行 OpenWrt来实现。

### 下载安装VMware Fusion

这个大家自行下载安装就行，比如我用的就是13.6.1这个版本（13.6 版本网上有很多注册码）

![](/img/mac_to_nas_f898cbe6_16.png)

### 准备好兼容的 OpenWrt 的VMDK文件

**方案一. K9 提供的 VMDK**

本案例以K9的[这个为案例](https://openwrt.ai/?target=armsr%2Farmv8&id=generic)，直接下载下图这个制作好的VMDK即可：

![](/img/mac_to_nas_215739e8_17.png)

比如我就下载的是上图中的`kwrt-09.26.2024-armsr-armv8-generic-ext4-combined.vmdk`这个版本。

**方案二. 官网提供的自行制作**

当然也可以参考[这个教程](https://openwrt.org/docs/guide-user/virtualization/fusion)，到[targets/armsr/arvm8/ 目录](https://downloads.openwrt.org/releases/)这个官方地址下载最新的`generic-ext4-combined.img.gz`

![](/img/mac_to_nas_ca9360b9_18.png)

下载后先得到`img`: 

```
gzcat openwrt-*ext4-combined.img.gz > openwrt.img
```

然后用再将其转化为`vmdk`（需要留意的是转化工具如果没有可以通过Homebrew安装: `brew install qemu`）：

```
qemu-img convert -O vmdk openwrt.img openwrt.vmdk
```

###  在VMware Fusion上跑起VMDK

先新建，创建自定义虚拟机：

![](/img/mac_to_nas_4c3caf6f_19.png)

操作系统选择`Linux`->`其他 Linux 5.x 内核 64 位 ARM`:

![](/img/mac_to_nas_1ab82776_20.png)

选择虚拟磁盘这里，选择`使用现有虚拟磁盘`->`选择虚拟磁盘`，然后选择刚刚制作好的`vmdk`文件

![](/img/mac_to_nas_59ee2f26_21.png)

然后继续，完成，存储虚拟机配置文件，保存在任意自己想要的目录，比如我将其保存为`kwrt.wmwarevm`:

![](/img/mac_to_nas_ad7dfa40_22.png)

接着虚拟机会自动启动，我们先手动关闭它，在`虚拟机`->`关机`

![](/img/mac_to_nas_36a5c277_23.png)

### 虚拟机配置


进入到设置页面后，可以先将CD/DVD与声卡移除了，移除方法都是点击进去以后在下面找到移除按钮移除即可:

![](/img/mac_to_nas_9364e50d_24.png)


这里我的案例是，我有两个网口，一个是我用usb给 MacMini 拓展的网口，这里将用桥接方式，后面进入到OpenWrt后会自动将它作为 lan 口，这里我们修改原本的`网络适配器`:

![](/img/mac_to_nas_af28ed7f_25.png)

然后另一个网口，就是 MacMini 自带的千兆以太网口，这里我们创建一个，然后用桥接方式，后面进入到OpenWrt后会自动将它作为 wan 口，这里我们添加一个`网络适配器`：

![](/img/mac_to_nas_90b48c43_26.png)

自此网络这块配置完成了，需要特别注意的是，由于是桥接，在MacMini上这两个网口有自己的 IP 地址，但是在 OpenWrt 里面这两个网口也有自己的 IP，两者是不影响的，中间是一层虚拟的物理桥接。

修改下处理器，我使用 `2`个内核与`2048`内存:

![](/img/mac_to_nas_be826056_27.png)

然后开机

### 配置并进入到 OpenWrt 管理页面

开机以后，我们手动设置下网络，让可以在外部局域网访问到OpenWrt的luci页面:

先编辑网络配置文件:

```
vim /etc/config/network
```

我们假设你家里的局域网网段是`10.0.0.x`，这里我们指定 `10.0.0.168`这里只需要确保这里的 IP 与你现在电脑在同一个局域网网段，并且这个 IP 没有和局域网中的其他 IP 冲突即可:

![](/img/mac_to_nas_6f9aa81c_28.png)


修改完后`:wq`退出，然后重启网络`/etc/init.d/network restart`

![](/img/mac_to_nas_427149c0_29.png)

重启后，此时你就已经可以在你当前电脑通过刚刚设定的IP访问到这台OpenWrt了:

![](/img/mac_to_nas_dcc6d8fe_30.png)

### 特别说明

我说下网络情况，我的情况是做`路由迁移`，也就是原本就有一个路由，另外 MacMini 

- MacMini 没有屏幕，我需要始终通过`屏幕共享`可以访问到 MacMini，无论局域网里面有没有路由器存在
- 网络中原本就有一个`路由器`，这个路由器的 Lan 口对外提供 DHCP 服务的 IP 是`10.0.0.1`

在这个情况下我做了几件事情：

1. 我手头的电脑固定了 IP 地址，确保无论局域网有没有路由，都在`10.0.0.x`网段，这里我将其固定为了`10.0.0.233`，网关固定为`10.0.0.1`
2. MacMini 那个被映射到 OpenWrt 为 Lan 口的那个网卡，我在MacMini 的系统设置上，我都固定IP地址，也是希望确保`10.0.0.x`网段，这里我将其固定为`10.0.0.68`，网关固定为`10.0.0.1`
3. MacMini 那个被映射到 OpenWrt 为 Lan 口的那个网卡，我在MacMini 上虚拟机的 OpenWrt 的设置上，将其固定 IP 为`10.0.0.168`，网关可以先不设定


这样以来无论要被迁移的路由器有没有关机，我手头电脑都能通过屏幕共享，访问到MacMini，以及OpenWrt的luci界面，方便配置使用。

现在我们做迁移，迁移期间，我有一个诉求，MacMini 虚拟机里面的 OpenWrt 与我旧的路由器的 OpenWrt 都需要开机状态，方便配置做一些参考（因为不同版本 OpenWrt 原因没办法直接备份与恢复），那么做了几件事情：

我先将旧的OpenWrt上的 Lan 口的 IP 改为非`10.0.0.1`，因为这个需要给到MacMini 虚拟机里的 OpenWrt 使用

![](/img/mac_to_nas_63e7f64e_31.png)

然后将旧的OpenWrt上的 Lan 口 DHCP 能力关闭了，这样以来局域网里面就只有虚拟机里的 OpenWrt 提供 DHCP 服务，就可以完成迁移：

![](/img/mac_to_nas_ca82992b_32.png)

其他大家有任何问题，欢迎探讨，这块已经非常清晰了，但是我遇到一个问题，我自己也没有任何办法，就是无法跑满千兆的外网：

以下是我家里正常的外网速度:

![](/img/mac_to_nas_657ffd2d_33.png)

但是在虚拟机里的 OpenWrt，速度都只能跑到 400Mb/s 左右，最高也只能到600Mb/s，根本跑不满，而且对于我家这台 MacMini M2 来说，通过监控看，CPU 最大占用只能到 25%（无论配置8核8G，给满配，还是 2 核 2G，都一样，所以我刚开始就是怀疑 OpenWrt 的原因，换了上面 K9 与官网两个版本都一样，我甚至怀疑是因为外接 RAID 硬盘读写速度原因，换到内部 SSD 也一样）

![](/img/mac_to_nas_bbc925bd_34.png)

---

- [Disable ssh password authentication on High Sierra - Ask Different](https://apple.stackexchange.com/questions/315881/disable-ssh-password-authentication-on-high-sierra)