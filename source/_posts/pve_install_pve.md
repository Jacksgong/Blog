title: PVE 下安装黑群晖
date: 2023-09-27 22:03:21
updated: 2023-09-27
categories:
- service
tags:
- dsm
- pve
- disk

---

{% note info %} 本文主要简单介绍了当前常规的PVE下安装黑群晖的方法，另外也说明了直通与添加PVE独立磁盘给到黑群晖使用的方法。 {% endnote %}

<!-- more -->

### 创建虚拟机

硬件配置如下，只需要配置框框的部分即可，留意是磁盘是SATA，网络用e1000，内存至少2G，核心至少2核。

![](/img/pve_install_pve_cf4a6fc3_0.png)

### 引导

下载[arpl-i18n](https://github.com/wjz304/arpl-i18n/releases)最新的镜像

![](/img/pve_install_pve_f53748da_1.png)

解压缩后会有一个img，然后导入到服务器，然后导入到虚拟机中

```bash
sudo qm importdisk 100 arpl.img local
```

导入后，在硬件的地方，双击，改为SATA模式添加

![](/img/pve_install_pve_6f6dad86_2.png)

然后在选项处将其选为引导

![](/img/pve_install_pve_b57569c3_3.png)

### 确保有足够的空间

#### 方案一. 直通

直通方案直接参照[这个](https://senjianlu.com/2020/01/pve-synology/)教程就行。

主要步骤就是，通过下面的指令找到要直通的硬盘

```bash
ls -l /dev/disk/by-id/
```

![](/img/pve_install_pve_bcd7f9bb_4.png)

然后通过以下指令直通进去就行：

```bash
sudo qm set 100 -sata1 /dev/disk/by-id/ata-xxx
```

![](/img/pve_install_pve_5f196bec_5.png)

#### 方案二给pve添加空闲磁盘

> [Proxmox VE（PVE）添加硬盘做存储 - GXNAS博客](https://wp.gxnas.com/10402.html)
> [PVE挂载nfs虚拟磁盘(亲测可用)\_pve挂载新硬盘\_MoYoung、的博客-CSDN博客](https://blog.csdn.net/yyhyoung/article/details/130707829)

比如我先通过`lsblk`确定有一个`sdh`空闲盘:

![](/img/pve_install_pve_f7e76bfc_6.png)

挂载到随意一个目录

```bash
sudo mkdir /mnt/pvedisk
sudo mount -t ext4 /dev/sdh1 /mnt/pvedisk
echo /dev/sdh1 /mnt/pvedisk ext4 defaults,nofail,discard 0 0 >> /etc/fstab
```

打开网页端，数据中心->存储->添加->目录

![](/img/pve_install_pve_9b3a2827_7.png)

然后起个名字，并且将挂载的目录填写到目录上，内容可以根据情况（我是全选上，表示可以用于所有的内容存储）。

![](/img/pve_install_pve_7e67b652_8.png)

### 启动安装

直接参照这个教程就可以: [从零开始的all in one之pve安装黑群晖 - 知乎](https://zhuanlan.zhihu.com/p/639066104)。

在虚拟机里面启动后，进入到这个界面就可以通过[ip:7681]进行配置安装了。

![](/img/pve_install_pve_cf223436_9.png)

安装过程中可以添加上需要的sn与mac地址，安装后，会进入选择从Synology网站下载并安装即可。

![](/img/pve_install_pve_5927a076_10.png)

这一步结束后，再往后的根据自己的情况补充即可。