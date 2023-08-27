title: Debian PVE 下磁盘分区调整
date: 2023-08-27 15:56:05
updated: 2023-08-27
categories:
- fun
tags:
- debian
- pve
- e2fsck
- disk

---

{% note info %} 在之前的文章里面我们介绍了[基于Debian我们如何迁移为可通过PVE管理运行虚拟化](https://blog.dreamtobe.cn/maintain_debian/#V-PVE%E8%99%9A%E6%8B%9F%E6%9C%BA%E4%B8%8E%E9%85%8D%E7%BD%AE)，但是完成后默认的配置会发现所有的分区配置会把所有的大小都挂载在了`/home`目录下，今天的目标就是将挂载在`/home`挂载的900G分出600G挂载给`/var`，这里主要涉及到`lvresize`、`resize2fs`等分区工具，主要的坑点在于基于PVE后，磁盘的格式被修改为了`lvm`，通过这个小案例我们解决这个坑点。{% endnote %}

<!-- more -->

## 前言

查看情况`df -h`与`lsblk`，这里的情况是我已经完成了分区调整的情况。

![](/img/debian_pve_disk_format_resize_6959b3da_0.png)
![](/img/debian_pve_disk_format_resize_4fa898ee_1.png)

先重启到Recovery因为需要`umount /home`，在正常模式下该挂载目录上有运行的服务，无法被`umount`，重启Debian后进入Recovery。


##  1. `/home`挂载的900G调整为300G

```bash
sudo umount /dev/mapper/debian--vg-home
sudo lvresize -L 300G /dev/mapper/debian—vg-home
sudo resize2fs /dev/mapper/debian—-vg-home
```

## 2. `/var`调整为610G

```bash
sudo lvresize -L 600G /dev/mapper/debian—-vg-var
```

到这里其实已经被分配到了600G，但是会发现执行`resize2fs`与`e2fsck`都会一直报错:

```bash
# 这两个指令都会报错
sudo e2fsck -y /dev/mapper/debian--vg-var
sudo resize2fs /dev/mapper/debian—vg-var
```

> `e2fsck`这个指令刚开始报`mounted`，取消挂载后报`in use.`感受上是pve的一些映射原因，一直生效不了，接下来就是解决这个问题。
 
后来发现是是因为是`lvm`的格式，因此重启直接进入系统以后，然后直接执行下面这步，然后就行了:

```bash
sudo lvresize --extents +100%FREE --resizefs /dev/mapper/debian--vg-var
```