title: Debian 11 安装与配置 SMB
date: 2023-08-27 17:01:41
updated: 2023-08-27
categories:
- service
tags:
- debian
- smb
- user

---

{% note info %} 本文主要假设你要将`/mnt/data/micamera`目录添加为smb访问，并且需要通过`mi`用户登录来访问。并确保了`mi`这个账户仅支持`smb`登录并且支持类似小米摄像机的访问。 {% endnote %}

<!-- more -->
## 安装服务

```bash
sudo apt install samba smbclient cifs-utils
```


## 配置用户

假设你要将`/mnt/data/micamera`目录添加为smb访问，并且需要通过`mi`用户登录来访问。

用户添加用户`mi`用户`micamera`的smb访问，并且将`mi`账户添加到一个`smbshare`的用户组里面方便管理。

```bash
sudo groupadd smbshare
sudo useradd -M -s /sbin/nologin mi
sudo usermod -aG smbshare mi
```

创建仅仅用于smb访问的`mi`账号的密码
```bash
sudo smbpasswd -a mi
```

启用账号

```bash
sudo smbpasswd -e mi
```

## 配置目录

设备目录权限，确保正常访问

```bash
sudo chgrp -R smbshare /mnt/data/micamera
sudo chmod 2770 /mnt/data/micamera
```

## 生效配置

编辑smb配置文件`/etc/samba/smb.conf`添加如下配置，让smb生效`mi`账户访问`micamera`目录，并且支持`SMB1`协议（这个国内一些旧设备探测需要（比如小米摄像头的NAS存储探测SMB服务需要））:


```conf
[global]
...
  min protocol = NT1
...

[micamera]
  comment = micamera
  force create mode = 0770
  force directory mode = 0770
  inherit permissions = yes
  path = /mnt/data/micamera
  writable = yes
  guest ok = no
  valid users = mi
```

此时配置完成，可以通过以下指令检查下看看配置是否有效:

```bash
sudo testparm
```

![](/img/debian_smb_791b4fbf_0.png)

然后重启服务，让配置生效

```bash
sudo systemctl restart nmbd
```

防火墙配置:

```bash
sudo ufw allow Samba
```

至此完成配置。

---

- [How To Configure Samba Share on Debian 11 / Debian 10 | ComputingForGeeks](https://computingforgeeks.com/how-to-configure-samba-share-on-debian/)