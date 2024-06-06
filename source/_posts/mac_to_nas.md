title: 将MacMini/Macbook改为家庭服务器
date: 2023-09-02 00:41:54
updated: 2024-06-06
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


---

- [Disable ssh password authentication on High Sierra - Ask Different](https://apple.stackexchange.com/questions/315881/disable-ssh-password-authentication-on-high-sierra)
- [如何在 macOS 中停用 SMB 1 或 NetBIOS - 官方 Apple 支持 (中国)](https://support.apple.com/zh-cn/102050)