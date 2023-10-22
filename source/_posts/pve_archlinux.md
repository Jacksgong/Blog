title: PVE 安装Arch Linux
date: 2023-10-22 16:24:55
updated: 2023-10-22
categories:
- devops
tags:
- arch linux
- pve

---

{% note info %} 近期看了比较多Arch Linux的文章，刚开始是在一台Nas的主机上做的arch Linux的尝试，因此做了记录。 {% endnote %}

<!-- more -->

## I. 虚拟机上进行上传安装

### 1. 下载
下载: 打开[官网](https://archlinux.org/download/)，提供了多种下载方式，建议使用种子或者磁力下载:

![](/img/pve_archlinux_7d07ec35_0.png)

### 2. 上传iSO
![](/img/pve_archlinux_37c6e357_1.png)

### 3. 创建

![](/img/pve_archlinux_14e69f12_2.png)

至少30G
![](/img/pve_archlinux_7391c96b_3.png)

host类型cpu
![](/img/pve_archlinux_ae984d21_4.png)

至少4096MiB
![](/img/pve_archlinux_6d6ea7e4_5.png)

最后确认
![](/img/pve_archlinux_0ba32f29_6.png)

## II. 安装

![](/img/pve_archlinux_7d3ab382_7.png)

### 1. 分区
![](/img/pve_archlinux_9453e49c_8.png)
![](/img/pve_archlinux_1989bbcc_9.png)

![](/img/pve_archlinux_ee28bfe6_10.png)

安装到`/dev/sda1`

```bash
pacstrap /mnt base linux linux-firware
```

安装完成后会提示:
![](/img/pve_archlinux_172d3d85_11.png)

### 2. 生成系统挂载配置文件，并修改目录权限为`root`

```bash
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
```

其他配置

```bash
# set hostname
echo archlinux-vm >> /etc/hostname
# install grub
pacman -S grub
grub-install /dev/sda
# create grub config
grub-mkconfig -o /boot/grub/grub.cfg
# install gnome desktop environment
pacman -S gnome networkmanager qemu-guest-agent

```


```bash
# enable required services（gdm就是上面安装的gnome用的图形界面服务）
systemctl enable gdm.service
systemctl enable NetworkManager.service
# set root passwd
passwd
# shutdown
exit
shutdown now
```

![](/img/pve_archlinux_e27c5f54_12.png)

## III. 退出安装盘

![](/img/pve_archlinux_601f4177_13.png)

## IV. 启用桌面
![](/img/pve_archlinux_10fb5a6f_14.png)

## V. 开机启动
![](/img/pve_archlinux_c5d8b444_15.png)


---

- [Running a Arch Linux VM in Proxmox VE](https://i12bretro.github.io/tutorials/0874.html)
- [Running an Arch Linux VM in Proxmox VE - YouTube](https://www.youtube.com/watch?v=XlYL2JHgH6k)
