title: 将MacMini/Macbook改为家庭服务器
date: 2023-09-02 00:41:54
updated: 2023-09-05
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
UsePAM no
```

3. 重启服务

```bash
sudo launchctl stop com.openssh.sshd
sudo launchctl start com.openssh.sshd
```

### 远程smb访问

![](/img/mac_to_nas_c8067a2b_9.png)

### 缓存服务器

![](/img/mac_to_nas_b55986f4_10.png)

## III. 常用服务

### Plex

Plex Server已经支持Silicon，直接到[官网](https://www.plex.tv/media-server-downloads/)，下载后打开即可。

![](/img/mac_to_nas_8fbdee35_11.png)

### Nezha监控

参照[官方](https://nezha.wiki/guide/agent.html#%E5%9C%A8-macos-%E4%B8%AD%E5%AE%89%E8%A3%85-agent)教程，即可，唯一需要留意的是`1`代表正常启动，`0`代表没有启动，负数代表有错误。在启动时需要在设置里面点击仍然打开。

![](/img/mac_to_nas_762e59a0_12.png)