title: 将MacMini/Macbook改为家庭服务器
date: 2023-09-02 00:41:54
updated: 2024-11-11
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

我们甚至可以让 Macmini 成为一台路由器，通过在虚拟机UMT上运行 OpenWrt来实现。

### 下载安装UTM

> 之前我使用过VMware Fusion，发现其根本跑不满网速，但是UMT可以跑满，这很重要，详情可以参照我在[恩山发的帖子](https://www.right.com.cn/forum/forum.php?mod=viewthread&tid=8405649&page=1#pid20912133)

大家直接到[getutm.app](https://docs.getutm.app/installation/macos/) 下载他的最新版本即可


![](/img/mac_to_nas_60b7d375_16.png)


### 准备好兼容的 OpenWrt 的img文件

**方案一. K9 提供的 img**

本案例以K9的[这个为案例](https://openwrt.ai/?target=armsr%2Farmv8&id=generic)，主要是默认提供了一些基础的代理，配置过程有较好的容错，直接下载下图这个即可：

![](/img/mac_to_nas_560ca402_17.png)

**方案二. 官网提供的自行制作**

当然也可以参考[这个教程](https://openwrt.org/docs/guide-user/virtualization/fusion)，到[targets/armsr/arvm8/ 目录](https://downloads.openwrt.org/releases/)这个官方地址下载最新的`generic-ext4-combined.img.gz`

![](/img/mac_to_nas_ca9360b9_18.png)

下载后先得到`img`: 

```
gzcat openwrt-*ext4-combined.img.gz > openwrt.img
```

###  在UTM上跑起镜像

先新建，创建自定义虚拟机：

![](/img/mac_to_nas_cd85c6f5_19.png)

操作系统选择`其他`:

![](/img/mac_to_nas_fca65d18_20.png)

Boot Device这里，选择`无`:

![](/img/mac_to_nas_ae89a0bf_21.png)

然后这个内存与 CPU 你根据需求来就行，比如我家常年 50+设备需要接入路由，外加有比较多的服务需要，因此我设置了 2G 内存以及 2 个核心：

![](/img/mac_to_nas_1492cab2_22.png)

存储空间，默认就行，别管他，一会儿还得删除了：

![](/img/mac_to_nas_1f8362b9_23.png)

共享目录，默认就行，用不到:

![](/img/mac_to_nas_47bb4250_24.png)

勾选`打开虚拟机设置`，名称取一个你喜欢的，点击保存

![](/img/mac_to_nas_ffe7a7a8_25.png)

### 虚拟机配置

保存后，自动进入到设置页面，之后移除掉声音，用不到:

![](/img/mac_to_nas_7cdbf518_26.png)

然后删除掉 默认配置的驱动器，一会儿添加我们自己的：

![](/img/mac_to_nas_b67a1659_27.png)

添加我们自己的驱动器，在驱动器下面点击`新建`->`导入`:

![](/img/mac_to_nas_131b730b_28.png)

然后导入刚刚我们制作好img文件:

![](/img/mac_to_nas_1d7affac_29.png)

然后配置网络，这里我的案例是，我有两个网口，一个是我用usb给 MacMini 拓展的网口，这里将用桥接方式，后面进入到OpenWrt后会自动将它作为 lan 口，这里我们修改原本的`网络`:

> 这里留意下，如果你不知道这个是en几，可以直接到`系统信息`->`网络`里面找到。

![](/img/mac_to_nas_08a6fa2b_30.png)

然后另一个网口，就是 MacMini 自带的千兆以太网口，这里我们创建一个，然后用桥接方式，后面进入到OpenWrt后会自动将它作为 wan 口，这里我们`设备`->`新建`->`网络`：

![](/img/mac_to_nas_331f25d3_31.png)

自此网络这块配置完成了，需要特别注意的是，由于是桥接，在MacMini上这两个网口有自己的 IP 地址，但是在 OpenWrt 里面这两个网口也有自己的 IP，两者是不影响的，中间是一层虚拟的物理桥接。


### 配置并进入到 OpenWrt 管理页面

开机以后，我们手动设置下网络，让可以在外部局域网访问到OpenWrt的luci页面:

先编辑网络配置文件:

```
vim /etc/config/network
```

我们假设你家里的局域网网段是`10.0.0.x`，这里我们指定 `10.0.0.168`这里只需要确保这里的 IP 与你现在电脑在同一个局域网网段，并且这个 IP 没有和局域网中的其他 IP 冲突即可:

![](/img/mac_to_nas_6f9aa81c_32.png)


修改完后`:wq`退出，然后重启网络`/etc/init.d/network restart`

![](/img/mac_to_nas_427149c0_33.png)

重启后，此时你就已经可以在你当前电脑通过刚刚设定的IP访问到这台OpenWrt了:

![](/img/mac_to_nas_dcc6d8fe_34.png)

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

![](/img/mac_to_nas_63e7f64e_35.png)

然后将旧的OpenWrt上的 Lan 口 DHCP 能力关闭了，这样以来局域网里面就只有虚拟机里的 OpenWrt 提供 DHCP 服务，就可以完成迁移：

![](/img/mac_to_nas_ca82992b_36.png)

其他大家有任何问题，欢迎探讨，这块已经非常清晰了

![](/img/mac_to_nas_388eb4a4_37.png)

---

- [Disable ssh password authentication on High Sierra - Ask Different](https://apple.stackexchange.com/questions/315881/disable-ssh-password-authentication-on-high-sierra)
- [\[OpenWrt Wiki\] OpenWrt on UTM on Apple Silicon HowTo](https://openwrt.org/docs/guide-user/virtualization/utm)