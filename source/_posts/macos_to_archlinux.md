title: MacbookPro 安装ArchLInux 系统
date: 2023-10-22 15:02:57
updated: 2023-10-22
categories:
- fun
tags:
- archlinux
- macbookpro

---

{% note info %} 家里刚好有一台2019年的macbook pro，这台intel的macbook 在多数情况下已经是有点卡了，最近在网上看了比较多的arch linux的资料，想着放着也没用因此就开动搞搞。 {% endnote %}

<!-- more -->

## I. 前置在MacOS上进行准备

### 1. 创建分区

先在Macbook中使用磁盘工具创建一个分区，这个分区后面会给到ArchLinux使用:

选择分区：
![](/img/macos_to_archlinux_3d5192bd_0.png)

选择创建分区:
![](/img/macos_to_archlinux_b9cb073b_1.png)

设置想要的大小，然后点击完成等待创建完成。

### 2. 制作引导盘

可以直接参考[这里](https://wiki.t2linux.org/guides/preinstall/#create-linux-installation-usb)

1. 在这里下载最新的t2的[arch linux](https://github.com/t2linux/archiso-t2/releases/latest)
2.  插入一个U盘到Mac
3. 打开terminal
4. 执行`diskutil list`来查看插入的U盘名称，假设是`/dev/disk2`
5. 执行以下指令（假设你的上面提到的iso已经下载到了`path/to/linux.iso`目录）

```bash
sudo diskutil unmountDisk /dev/disk2
sudo dd if=path/to/linux.iso of=/dev/disk2 bs=1m
```

在执行过程中可以按`ctrl+T`来查看进度。

### 3. 创建Wifi与蓝牙驱动引导

> 参考这个[教程](https://wiki.t2linux.org/guides/wifi-bluetooth/#on-macos)

由于这块的驱动Linux与Mac系统是共用的，因此这里我们直接创建一个分区并且拷贝这个引导，便于一会儿使用。

下载这个[脚本](https://wiki.t2linux.org/tools/firmware.sh)执行即可。后面安装ArchLinux时候会用到。

## II. 关闭安全引导

> 参照[这里](https://wiki.t2linux.org/guides/preinstall/#disable-secure-boot)

禁用安全启动。 Apple 的安全启动实现在启用时不允许启动除 macOS 或 Windows 之外的任何系统（甚至不允许启动 shim 签名的 GRUB）。我们需要禁用它：

1.  关机
2. 开启并按住 `Command-R` 直到黑屏闪烁，Mac 将在 macOS 恢复模式下启动
3. 从菜单栏中选择“实用程序”>“启动安全实用程序”
4. 进入启动安全实用程序后
5. 将安全启动设置为无安全
6. 将允许启动媒体设置为允许从外部或可移动媒体启动

## III. 启动安装

1. 关机
2. 插入U盘
3. 按住`option`按键，并且开启，使Mac进入启动引导管理页面
4. 选择EFI的选项，如果有多个就选择最后一个（前一个应该是前面你创建的wifi与蓝牙驱动的efi分区）
5. 此时就进入了ArchLinux安装页面

### 1. 创建分区

```bash
fdisk /dev/nvme0n1
```

这里需要注意的是这里是**抹除了整个macos**，如果不希望抹掉macos，可以参考[该教程](https://wiki.t2linux.org/roadmap/#can-i-completely-remove-macos)

具体的`fdisk`操作不懂的可以可以直接参考这个作者: [Macbook Pro安装arch linux - 知乎](https://zhuanlan.zhihu.com/p/161350432)(当然也可以考虑使用`cfdisk`，这个更可视化些)，如下图:

![](/img/macos_to_archlinux_175ce44e_2.png)

分区写入后，进行格式化:
```text
mkfs.fat -F32 /dev/sda1   #把第一个引导分区格式化成fat32格式的。
mkfs.ext4 /dev/sda2       #把第二个主分区格式化成ext4格式的
mkswap /dev/sda3          #制作SWAP交换分区并打开
swapon /dev/sda3 
```

然后进行挂载操作:
```text
mount /dev/sda2 /mnt             #将根分区挂在到/mnt 
mkdir -p /mnt/boot/efi           #创建boot目录
mount /dev/sda1 /mnt/boot/efi        #将EFI分区并挂载
```

### 2. wifi驱动还原并联网

通过`fdisk -l`查看有一个分区是就几百兆的efi，我们假设叫`/dev/nvme0n1p1`，那么执行:

```bash
sudo umount /dev/nvme0n1p1
sudo mkdir -p /tmp/apple-wifi-efi
sudo mount /dev/nvme0n1p1 /tmp/apple-wifi-efi
bash /tmp/apple-wifi-efi/firmware.sh
```

检查是否正常恢复:

```bash
sudo journalctl -k --grep=brcmfmac
```

此时如果输出类似的说明成功:

```bash
Dec 24 22:34:19 hostname kernel: usbcore: registered new interface driver brcmfmac Dec 24 22:34:19 hostname kernel: brcmfmac 0000:01:00.0: enabling device (0000 -> 0002) Dec 24 22:34:20 hostname kernel: brcmfmac: brcmf_fw_alloc_request: using brcm/brcmfmac4377b3-pcie for chip BCM4377/4 Dec 24 22:34:20 hostname kernel: brcmfmac 000:0:01:00.0: Direct firmware load for brcm/brcmfmac4377b3-pcie.apple,tahiti-SPPR-m-3.1-X0.bin failed with error -2 Dec 24 22:34:20 hostname kernel: brcmfmac 0000:01:00.0: Direct firmware load for brcm/brcmfmac4377b3-pcie.apple,tahiti-SPPR-m-3.1.bin failed with error -2 Dec 24 22:34:20 hostname kernel: brcmfmac 0000:01:00.0: Direct firmware load for brcm/brcmfmac4377b3-pcie.apple,tahiti-SPPR-m.bin failed with error -2 Dec 24 22:34:20 hostname kernel: brcmfmac 0000:01:00.0: Direct firmware load for brcm/brcmfmac4377b3-pcie.apple,tahiti-SPPR.bin failed with error -2 Dec 24 22:34:20 hostname kernel: brcmfmac 0000:01:00.0: Direct firmware load for brcm/brcmfmac4377b3-pcie.apple,tahiti-X0.bin failed with error -2 Dec 24 22:34:20 hostname kernel: brcmfmac: brcmf_c_process_txcap_blob: TxCap blob found, loading Dec 24 22:34:20 hostname kernel: brcmfmac: brcmf_c_preinit_dcmds: Firmware: BCM4377/4 wl0: Jul 16 2021 18:25:13 version 16.20.328.0.3.6.105 FWID 01-30be2b3a Dec 24 22:34:20 hostname kernel: brcmfmac 0000:01:00.0 wlp1s0f0: renamed from wlan0
```

连接wifi，参考[iwctl](https://wiki.archlinux.org/title/Iwd#iwctl)的教程:

```bash
iwctl
```

检测有哪些可用的:

```bash
device list
```

检测有哪些wifi（假设你检测出来可用的device叫`wlan0`:

```bash
station wlan0 scan
station wlan0 get-networks
```

连接wifi（假设你检测出来可用的Wifi叫`WE`）：

```bash
station wlan0 connect WE
```

此时网络已经正常连接上了。

###  3. 时区配置

修改为中国时区
默认为UTC 0的时区，修改为亚洲上海时区:
```bash
timedatectl set-timezone "Asia/Shanghai"
```

将你的硬件时钟设置为协调世界时（UTC）：

```
timedatectl set-local-rtc 0
```

自动同步到NTP服务器：

```
timedatectl set-ntp true
```

查看状态

```
timedatectl status
```


## II. 安装

> 参考[该教程](https://wiki.t2linux.org/distributions/arch/installation/)

### 1. pacstrap安装

如果您打算使用 systemd-boot 作为引导加载程序，请省略其中的 `grub efibootmgr` 软件包，您可以选择使用 Xanmod 内核。在这种情况下，请将 `linux-t2` 替换为 `linux-xanmod-t2` 。

```bash
pacstrap /mnt base linux-t2 apple-t2-audio-config apple-bcm-firmware linux-firmware iwd grub efibootmgr touchbard t2fand
```

通过添加以下内容将存储库添加到 `/mnt/etc/pacman.conf` ：
```
[arch-mact2] Server = https://mirror.funami.tech/arch-mact2/os/x86_64 SigLevel = Never
```

将 `apple-bce` 添加到 `/etc/mkinitcpio.conf` 中的 `MODULES` 列表中，然后运行 ​​ `mkinitcpio -P`

### 2. 配置

1. 生成挂载配置到系统中，确保启动时正确挂载: `genfstab -U /mnt >> /mnt/etc/fstab`
2. 切换到新系统: `arch-chroot /mnt`
3. 其他配置直接参考[这个教程](https://zhuanlan.zhihu.com/p/161350432)即可:
```bash
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt           #Change root到新安装的系统
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime   #设置时区为上海
hwclock --systohc         #这个命令假定硬件时间已经被设置为URC时间
vim /etc/locale.gen   #然后移除需要的地区的注释，即前面的#号。我去除的下面4个前面的#号
en_US.UTF-8
zh_CN.UTF-8
zh_HK.UTF-8
zh_TW.UTF-8
locale-gen    #本地化的程序与库若要本地化文本，都依赖Locale，其明确规定地域、货币、时区日期
               的格式、字符排列方式和其他本地化标准等等。
vim /etc/locale.conf  #创建locale.conf并编辑LANG这一变量。
写入LANG=en_US.UTF-8   #将系统locale设置为en_US.UTF-8，系统的Log就会用英文显示，更容易
                       判断和处理问题。不推荐在此设置任何中文 locale，会导致 TTY 乱码。
```
4. 网络设置
```bash
vim /etc/hostname       #写入mbp，我把mbp作为计算机名
vim /etc/hosts         #写入以下内容
127.0.0.1	localhost
::1		localhost
127.0.1.1	mbp.localdomain	mbp
```
5. 设置密码
```bash
passwd        #密码输入的时候看不到，只能盲输。
```


### 3. 安装Grub并chroot到系统盘

1. 编辑 `/etc/default/grub`在 `GRUB_CMDLINE_LINUX="quiet splash"` 中，添加参数（添加到参数内）： `intel_iommu=on iommu=pt pcie_ports=compat`
2. `grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --removable` 。
3. `grub-mkconfig -o /boot/grub/grub.cfg`
4. `pacman -S dialog dhcpcd zsh`

退出 `chroot` （Control-d 或 `exit` ）并重新启动。现在，您可以通过在启动时按住选项来在 macOS 启动管理器中选择 Arch 安装。

### 4. 网络与通用配置

1. （可选）禁用ipv6
类似我在酒店，使用的是手机热点，ipv6有点问题可以考虑先禁用掉，参考[教程](https://wiki.archlinux.org/title/IPv6#Disable_IPv6):

编辑`/etc/sysctl.d/40-ipv6.conf`，并添加如下，让所有接口都禁用ipv6

```conf
# Disable IPv6
net.ipv6.conf.all.disable_ipv6 = 1
```

也可以直接执行如下来处理:

```bash
sysctl -w net.ipv6.conf.all.disable_ipv6=1
```


2. 配置dhcp
> 参考[官网](https://wiki.archlinux.org/title/dhcpcd#Running)
与dns可以采用[这个systemd-networkd](https://wiki.archlinux.org/title/Systemd-networkd)的方式，也可以采用下面的方式:
```bash
systemctl enable dhcpcd.service
systemctl start dhcpcd.service
```

3. 配置dns
编辑`/etc/resolv.conf` 添加`nameserver 119.29.29.29`

配置完成后重启系统即可正常使用archlinux系统了。

## III. 其他必要配置

#### 风扇
配置参考[这里](https://wiki.t2linux.org/guides/fan/):

```bash
sudo pacman -S t2fand
sudo systemctl enable --now t2fand
```

#### 触摸板

```bash
wget https://wiki.t2linux.org/tools/touchbar.sh
chmod +x touchbar.sh
sudo ./touchbar.sh
```

比如我是喜欢默认是F1-F12，功能键后再切换到媒体键，就做下配置:

![](/img/macos_to_archlinux_cdbc5b47_3.png)

#### 显卡
配置参考[这里](https://wiki.t2linux.org/guides/hybrid-graphics/#enabling-the-igpu):

先检测是否符合要求，通过指令`uname -r`，如果输出的版本是大于等于6.1.12-2即可，创建`/etc/modprobe.d/apple-gmux.conf`并添加如下内容:

```conf
# Enable the iGPU by default if present 
options apple-gmux force_igd=y
```

然后安装固件:

```bash
sudo pacman -Syu base-devel gnu-efi
```

重启系统后，通过如下方式检测:

运行`journalctl -k --grep=gmux`，如果输出类似说明说已经正常运行:
![](/img/macos_to_archlinux_2b490a96_4.png)

运行`glxinfo | grep "OpenGL renderer"`，输出类似:

![](/img/macos_to_archlinux_7c9fbb73_5.png)

#### 声卡

直接参考这里即可: 
- [Audio - t2linux wiki](https://wiki.t2linux.org/guides/audio-config/)
- [GitHub - kyoz/mac-arch: :computer: Arch installation guide on Mac](https://github.com/kyoz/mac-arch#sound)

#### 键盘按键映射

推荐直接使用`xmodmap`，可以直接在`~/.xmodmaprc`编辑:

下面这段是将`caps lock`与`left ctrl`替换:
```
remove Lock = Caps_Lock
remove Control = Control_L
keysym Control_L = Caps_Lock
keysym Caps_Lock = Control_L
add Lock = Caps_Lock
add Control = Control_L
```

#### 其他

其他可以参考这个作者的一些说明进行配置 [GitHub - kyoz/mac-arch: :computer: Arch installation guide on Mac](https://github.com/kyoz/mac-arch#install-to-make-arch-usable)


---

- [Macbook Pro安装arch linux - 知乎](https://zhuanlan.zhihu.com/p/161350432)
- [Installation - t2linux wiki](https://wiki.t2linux.org/distributions/arch/installation/)
- [Installation guide - ArchWiki](https://wiki.archlinux.org/title/Installation_guide#Set_the_console_keyboard_layout)
- [Installing Arch on Intel Macbook Pro with T2 Security Chip | Matt Gibson](https://mattgibson.ca/installing-arch-linux-on-an-intel-macbook-pro-with-t2-security-chip/)


