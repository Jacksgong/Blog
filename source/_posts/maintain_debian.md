title: Debian 11 维护与环境配置
date: 2023-05-02 00:46:36
updated: 2023-05-02
permalink: maintain_debian/
categories:
- fun
tags:
- debian
- pve
- docker
- vnc
- maintain

---

{% note info %} 近期想要重新再在家里配置一台服务器，作为Truenas Scale的备用，另外也折腾一些GPT相关的东西，因此重新倒腾，服务器上的选择主要从Debian与Ubuntu中选，Debian从Docker、虚拟机还是ZFS上底层支持都比Ubuntu好，因此最终选用了Debian，折腾了几天，Debian的各类网上的资料都比较散，因此做了下整理。 {% endnote %}

<!-- more -->

## I. 安装

1. 从[这里官方](https://www.debian.org/distrib/netinst)下载amd64的iso文件
2. 用[Etcher](https://www.balena.io/etcher)写入到磁盘即可，不过我用下来有点问题，最后还是切到windows用UltraISO来写入，简单不出问题
3. 插入U盘，选择u盘启动，然后一步一步根据安装即可，参照[这个教程](https://zhuanlan.zhihu.com/p/574329452#:~:text=%E5%A6%82%E4%BD%95%E5%AE%89%E8%A3%85%20Debian%2011%20%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E5%9B%BE%E6%96%87%E6%95%99%E7%A8%8B%201%20%281%29%20%E4%B8%8B%E8%BD%BD%20Debian,continue%20%E7%BB%A7%E7%BB%AD%208%20%288%29%20%E5%88%9B%E5%BB%BA%E6%9C%AC%E5%9C%B0%E7%94%A8%E6%88%B7%E5%B9%B6%E9%85%8D%E7%BD%AE%E5%AF%86%E7%A0%81%20%E6%8C%87%E5%AE%9A%E6%9C%AC%E5%9C%B0%E7%94%A8%E6%88%B7%E7%9A%84%E5%85%A8%E5%90%8D%20...%20%E6%9B%B4%E5%A4%9A%E9%A1%B9%E7%9B%AE)即可

## II. 环境配置

### 基础环境

#### 源有效性

确定有效的源修改

```
sudo nvim /etc/apt/sources.list
```

修改为:

```bash
deb http://deb.debian.org/debian/ buster main contrib non-free
deb-src http://deb.debian.org/debian/ buster main contrib non-free

deb http://security.debian.org/debian-security buster/updates main contrib non-free
deb-src http://security.debian.org/debian-security buster/updates main contrib non-free

deb http://deb.debian.org/debian/ buster-updates main contrib non-free
deb-src http://deb.debian.org/debian/ buster-updates main contrib non-free
```

```bash
sudo apt update
```

#### 防火墙与开启ssh访问

安装
```bash
sudo apt-get update
sudo apt-get install ufw
sudo apt-get install openssh-server
sudo systemctl status ssh.service
```

配置防火墙
```bash
sudo ufw allow ssh
sudo ufw enable
sudo ufw status
```

此时就可以远程用ssh访问了，如果你不确定目前的ip是多少可以通过该方式确认下，查看当前接口名称`ip a`
![](/img/maintain_debian_0.png)

配置非密码访问，将本地的public key添加到`vi ~/.ssh/authorized_keys`，确保通过密钥登录有效。

禁止密码访问，并且限制登录账号，编辑`/etc/ssh/sshd_config`，找到相关字段并修改为:
```bash
ClientAliveInterval 600  
ClientAliveCountMax 0
PasswordAuthentication no
```

重启服务
```bash
service sshd restart
service ssh status
```

禁止休眠，防止休眠后断网导致远程ssh访问不了，可以参考[这个教程](https://blog.csdn.net/weixin_45980458/article/details/122952607)，具体操作如下:
```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

生成sshkey，用于后续使用
```bash
ssh-keygen -t ed25519
```

### 终端相关环境配置

#### 安装neovim

```bash
sudo apt-get install neovim
```

修改默认编辑器为`neovim`

```bash
sudo update-alternatives --config editor
```

#### 配置[oh-my-zsh](https://ohmyz.sh/#install)
```bash
sudo apt-get install zsh
sudo apt-get install git

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

#### 配置[autosuggestion](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#oh-my-zsh)
```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

然后在`~/.zshrc`中修改(我比较习惯用CTRL+SPACE来接受补全建议):
```bash
plugins=( 
    # other plugins...
    zsh-autosuggestions
)

bindkey '^ ' autosuggest-accept
```

#### 配置主题[powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k/wiki/Install-Instructions#option-2-install-for-oh-my-zsh):
```bash
git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
```

然后在`~/.zshrc`中修改:
```bash
ZSH_THEME="powerlevel9k/powerlevel9k"

POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(user host dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status time)
POWERLEVEL9K_TIME_FORMAT="%D{%H:%M:%S}"
POWERLEVEL9K_NODE_VERSION_BACKGROUND='022'
POWERLEVEL9K_SHORTEN_DIR_LENGTH=2
```

#### 配置[autojump](https://www.linode.com/docs/guides/faster-file-navigation-with-autojump/)
```bash
sudo apt install autojump
```

然后在`~/.zshrc`中添加:
```bash
. /usr/share/autojump/autojump.sh
```

#### 配置[fzf](https://github.com/junegunn/fzf#using-git)
```bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

#### 解决问题中文乱码与编码警告

1. 执行以下命令检查语言环境是否安装：

```bash
locale -a
```

如果当前语言环境未安装，则需要安装相应的语言支持包。

2. 执行以下命令打开` /etc/locale.gen` 文件：

```bash
sudo nvim /etc/locale.gen
```

将你需要的语言环境取消注释（去掉前面的 `#`）。

```bash
# zh_CN.UTF-8 UTF-8
# en_US.UTF-8 UTF-8
```

3. 执行以下命令重新生成语言环境：

```bash
sudo locale-gen
```

## III. 挂载与RAID


我的环境是有`/dev/sdb2`与`/dev/sdc2`组成的一个RAID1，我是需要将其挂载在`/mnt/dev`目录下的，这个组RAID1已经在安装的时候已经配置好了。对于RAID1相关的教程[这篇文章](https://www.server-world.info/en/note?os=Debian_11&p=raid1)也已经写的挺不错的了。

### 检测与初始化RAID

安装`mdadm`来进行管理
```bash
sudo apt install mdadm
```

查看磁盘情况`sudo fdisk -l`与`df -h`，如果是之前就已经配置好的RAID1想要恢复:
```bash
mdadm --create /dev/md0 --level=raid1 --raid-devices=2 /dev/sdb2 /dev/sdc2
```

查看当前RAID情况`cat /proc/mdstat`
![](/img/maintain_debian_1.png)

也可以使用`sudo mdadm --detail --scan`
![](/img/maintain_debian_2.png)

如果是首次，不是恢复，还需要对RAID格式化:
```bash
sudo mkfs.ext4 /dev/md/0
```
![](/img/maintain_debian_3.png)

### 挂载RAID

创建要挂载的目录
```bash
sudo mkdir /mnt/dev
```

挂载上
```bash
sudo mount -t ext /dev/md/0 /mnt/dev
```
![](/img/maintain_debian_4.png)

开机自动挂载，可以参照[这个教程](https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-debian-9)，使用`mdadm`来进行操作（这样在关机以及一些系统性操作的时候也会自动关联）:

```bash
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u
echo '/dev/md0 /mnt/md0 ext4 defaults,nofail,discard 0 0' | sudo tee -a /etc/fstab
```



## IV. Docker与服务


### 基础配置

> 参照[这个官方教程](https://docs.docker.com/engine/install/debian/)就挺好了，不过我记得我就直接这样安装也行:

```bash
sudo apt-get install docker
sudo apt-get install docker-compose
```

### 服务配置

我习惯于用`docker-compose`管理，这里就简单做两个案例，配置一个ddns-go与traefik

#### 配置Docker-Compose
我们用traefik进行反向代理

先创建一个虚拟网络`traefik_net`，让相关的服务的网络流量能够被`traefik`探知:

```bash
sudo docker network create traefik_net
```

找一个随意的可以存放`docker-compose`配置的目录，创建`.env`文件，添加下你后续想要反向代理用到的域名，以及这个网络名称:

```
MY_DOMAIN=yourdomain.com
DEFAULT_NETWORK=traefik_net
```

在`docker-compose.yml`下添加如下（这里留意这个文件可以放在任意你想放的地方，只是`docker-compose`指令执行的时候直接在这个目录下可以直接找到比较方便点）:
```
version: "3.7"

services:
  traefik:
    image: traefik
    container_name: traefik
    restart: always
    ports:
      - "8000:80"
      - "5533:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /opt/traefik/certificates:/opt/traefik/certificates:ro
      - /opt/traefik/traefik.yml:/traefik.yml:ro
      - /opt/traefik/config.yml:/etc/traefik/dynamic_conf/conf.yml:ro
  ddns-go:
    image: jeessy/ddns-go
    container_name: ddns-go
    restart: always
    expose:
      - "9876"
    volumes:
      - /dev/opt/ddns-go:/root
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ddns-go.rule=Host(`ddns.$MY_DOMAIN`)"
      - "traefik.http.routers.ddns-go.entrypoints=websecure"
      - "traefik.http.routers.ddns-go.tls=true"
networks:
  default:
    external:
      name: $DEFAULT_NETWORK
```

这里说明下，最终我需要通过`https://traefik.yourdomain.com:5533`访问到Traefik，ddns也同理。另外我的所有的配置都放在`/opt`中。这里的`8080`端口是访问DashBoard的

防火墙允许访问:
```
sudo ufw allow 5533
sudo ufw allow 8080
```

#### Traefik与DDNS配置

> 需要留意的是我使用的是Traefik V2版本，与V1版本的配置互不兼容，相关教程也可以[参考这里](https://cloud.tencent.com/developer/article/1829161)。

在`/opt/traefik/traefik.yml`(这个目录在前面的`docker-compose`中映射为了该服务的配置了)中编辑如下:

```yml
## STATIC CONFIGURATION
log:
  level: INFO

api:
  insecure: true
  dashboard: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
  file:
    directory: "/etc/traefik/dynamic_conf"

tls:
  certificates:
    - certFile: /opt/traefik/certificates/wildcard.crt
      keyFile: /opt/traefik/certificates/wildcard.key
```

然后在`/opt/traefik/config.yml`(这个路径已经在`docker-compose`中映射为`/etc/traefik/dynamic_conf/config.yml`为其文件providers)添加如下:

```yml
tls:
  certificates:
    - certFile: /opt/traefik/certificates/wildcard.crt
      keyFile: /opt/traefik/certificates/wildcard.key

http:
  routers:
    traefik:
      entryPoints: websecure
      rule: "Host(`traefik.yourdomain.com`)"
      tls: true
      service: traefik
  services:
    traefik:
      loadBalancer:
        servers:
          - url: "http://<your_local_ip>:8080"
        passHostHeader: true
```

这里如果不清楚`your_local_ip`是多少，就直接`ip a`查看下，这里主要就一方面是指定证书地址，另外一个就是配置 `https://traefik.yourdomain.com:5533` 直接访问Traefik的Dashboard。另外这里也就只是一个案例，后续你可以基于这个为各类ip端口访问做反向代理。

ddns不用配置，默认跑起来后会在我们配置的映射目录`/opt/ddns`下生成`.ddns_go_config.yaml`描述文件。

#### 跑起服务

这就比较简单了，到`docker-compose.yml`所在目录，执行:

```bash
sudo docker-compose up -d
```

### 常用指令

查看`traefik`日志
```bash
sudo docker-compose logs traefik
```

重启`traefik`服务
```bash
sudo docker-compose restart traefik
```

开启整体服务并后台运行(如果没有`-d`就直接当前指令运行可以实时看日志)
```bash
sudo docker-compose up -d
```

 关闭整体服务
```bash
sudo docker-compose down
```



## V. PVE虚拟机与配置


> [官网的教程](https://pve.proxmox.com/wiki/Main_Page)也没有大错但是有点小问题，整体我们会以[这个教程](https://computingforgeeks.com/how-to-install-proxmox-ve-on-debian-bullseye/)为主，然后修复下里面的一些小问题

### 准备工作

#### 必要的系统升级

```bash
sudo apt -y update && sudo apt -y upgrade
[ -f /var/run/reboot-required ] && sudo reboot -f
```

#### 设置Proxmox服务域名确保本地访问

> 这个**一定要做**，否则后面安装会各种提示连接不上

我们假设你的主机名是`debian`，你的域名是`debian.yourdomain.com`，你debian系统的ip是`<your_local_ip>`。

先通过`sudo -i`切换到`root`账户下

设置hostname:
```bash
sudo hostnamectl set-hostname debian.yourdomain --static
```

`/etc/hosts`要添加确保本地能访问:
```bash
127.0.0.1       localhost
<your_local_ip> debian.yourdomain.com debian

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

#### 添加相关源

```bash
echo "deb http://download.proxmox.com/debian/pve bullseye pve-no-subscription" | sudo tee /etc/apt/sources.list.d/pve-install-repo.list

wget http://download.proxmox.com/debian/proxmox-release-bullseye.gpg
sudo mv proxmox-release-bullseye.gpg /etc/apt/trusted.gpg.d/proxmox-release-bullseye.gpg
chmod +r /etc/apt/trusted.gpg.d/proxmox-release-bullseye.gpg

sudo apt update
sudo apt full-upgrade

echo "deb http://download.proxmox.com/debian/ceph-pacific bullseye main" | sudo tee /etc/apt/sources.list.d/ceph.list
```

### 安装PVE

```bash
sudo apt update
sudo apt install proxmox-ve postfix open-iscsi
```

安装过程中提示邮箱服务，如果你debian系统中没有安装没有，就直接选择`Local only`即可:
![](/img/maintain_debian_5.png)

过程提示的系统邮箱域名，直接使用前面提到的`debian.yourdomain.com`即可。

安装完成后重启系统

```bash
sudo systemctl reboot
```

重启后，留意会因为`/etc/network/interfaces`被修改导致网络无法访问，我们顺便添加一个桥接，从`Recovery`模式进去，然后编辑`/etc/network/interfaces`修改成:

```bash
# network interface settings; autogenerated
# Please do NOT modify this file directly, unless you know what
# you're doing.
#
# If you want to manage parts of the network configuration manually,
# please utilize the 'source' or 'source-directory' directives to do
# so.
# PVE will preserve these directives, but will NOT read its network
# configuration from sourced files, so do not attempt to move any of
# the PVE managed interfaces into external files!

source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

iface enp7s0 inet manual

auto enp8s0
iface enp8s0 inet dhcp

auto vmbr0
iface vmbr0 inet static
        address <your_local_ip>
        netmask 255.255.255.0
        gateway <your_gateway>
        bridge-ports enp8s0
        bridge-stp off
        bridge-fd 0
```

这里我说明下`<your_local_ip>`替换成你之前debian的局域网中的ip，`<your_gateway>`换成你的gateway（大多数情况下是`192.168.1.1`)，这里的`vmbr0`主要方便后面你创建虚拟机的时候可以对外网可访问。

至此重启可以正常访问网络，并且可以正常访问pve管理网页。

### 前端网页访问

重启后，检查端口`8006`，这个是默认的管理面板页面的访问端口，防火墙绕过下:
```bash
ss -tunelp | grep 8006
sudo ufw allow 8006
```

然后通过`https://<your_local_ip>:8006`就已经可以整访问了，具体如果域名反向代理，可以使用前面提到的Traefik去做到，这里就不赘述了。

![](/img/maintain_debian_6.png)

最后需要留意的是，如果你是使用的Nvidia，PVE这边需要做下配置，参考[PVE Nvidia教程](https://pve.proxmox.com/wiki/Developer_Workstations_with_Proxmox_VE_and_X11#Optional:_NVidia_Drivers):

```bash
su
echo "blacklist nouveau" >> /etc/modprobe.d/blacklist.conf
apt install pve-headers
apt-get update 
apt-get install  nvidia-driver
```



## VI. VNC与远程桌面访问


这里我比较推荐tigervnc，其他的我也用过，不过这里我觉得tigervnc就够用了，所以就不赘述其他的了。

tigervnc是基于tightvnc进行安全以及各方面延伸后的一个VNC工具。

### 安装

```bash
sudo apt-get install tigervnc-standalone-server tigervnc-common
sudo apt-get install kde-plasma-desktop
sudo apt-get install x11vnc xvfb xfonts-base xsession dbus-x11
```

防火墙配置，这里假如说后面是`:1`屏幕端口就是`5901`，`:2`就是`5902`以此类推，防火墙都要留意配置好。
```bash
sudo ufw allow from any to any port 5901 proto tcp
```

### 支持xfce4桌面的VNC

> 可以参考[这个教程](https://atetux.com/how-to-install-tigervnc-on-debian-11)

安装相关桌面
```bash
sudo apt install xfce4 xfce4-goodies dbus-x11 -y
```

配置`~/.vnc/xstartup`:
```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec /bin/sh /etc/xdg/xfce4/xinitrc
```

然后启动:
```bash
vncserver -localhost no
```

这里简单提下，如果没有`-localhost no`本地访问以外的都会被拒绝。

![](/img/maintain_debian_7.png)

### 支持gnome桌面的VNC

安装相关桌面
```bash
sudo apt install task-gnome-desktop dbus-x11
```

由于这个不用怎么特殊配置，直接启动即可
```bash
vncserver -xstartup /usr/bin/gnome-session -localhost no
```

![](/img/maintain_debian_8.png)

### 支持KDE桌面的VNC

> 参照[这个教程](https://superuser.com/questions/1510278/kde-panel-missing-on-tigervnc-vnc-session)

安装相关桌面

```bash
sudo apt install kde-plasma-desktop dbus-x11
```

配置`~/.vnc/xstartup`

```bash
#!/bin/sh
# Run a generic session
if [ -z "$MODE" ]
then
        xsetroot -solid grey &   #set the background picture
        export XKB_DEFAULT_RULES=base & #both should be needed for keyboard signals
        export QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb & 


#       export $(dbus-launch) &
#       exec startplasma-x11&
#       kstart5 plasmashell &
        # konsole & #starts konsole (kde terminal)
        # firefox & #starts firefox
        # ksysguard & #starts the kde system monitor
#       xrandr --dpi 144 & # 
        kstart5 plasmashell & #adds a task bar to the windows
        dbus-launch startplasma-x11  #starts the actual window + Dolphin

#       /opt/kde/bin/startkde &   
fi
```

然后启动:

```bash
vncserver -localhost no
```

![](/img/maintain_debian_9.png)

### 日常维护

检查当前是什么桌面: 
```bash
echo $DESKTOP_SESSION
```
![](/img/maintain_debian_10.png)

切换默认显示管理器
```bash
sudo dpkg-reconfigure lightdm
```
![](/img/maintain_debian_11.png)

检查当前有没有在跑的列表
```bash
vncserver -list
```
![](/img/maintain_debian_12.png)

关闭`:1`屏幕服务
```bash
vncserver -kill :1
```
![](/img/maintain_debian_13.png)




## VII. 驱动


### 网卡

> 参考[这个](https://www.jeffgeerling.com/blog/2021/check-your-driver-faster-linux-25g-networking-realtek-rtl8125b)教程也可以

检查网卡型号:
```bash
lspci | grep -i ethernet
```
![](/img/maintain_debian_14.png)

比如我这个RTL8125B的驱动，可以参考[这个](https://askubuntu.com/questions/1259947/cant-get-rtl8125b-working-on-20-04)，留意如果正在用到这个网卡，需要本地物理机接入进去更新。

1. 在[这里](https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-pci-express-software)下载`2.5G Ethernet LINUX driver r8125 for kernel up to 5.19`这个驱动
2. 解压缩后，执行目录下的`autorun.sh`后重启即可。

### 显卡

> 官方说明参考[这里](https://wiki.debian.org/NvidiaGraphicsDrivers)

查看显卡型号
```bash
lspci -nn | egrep -i "3d|display|vga"
```

我是Nvidia的显卡，可以参考[这个](https://phoenixnap.com/kb/nvidia-drivers-debian)教程，留意源和文章开头提到的源保持一致，需要有`non-free`

```bash
sudo apt update
sudo apt install nvidia-detect
sudo nvidia-detect
```

![](/img/maintain_debian_15.png)

执行`sudo apt install [driver name]`，通常如下:
```bash
sudo apt install nvidia-driver

systemctl reboot
```

检查状态`nvidia-smi`
![](/img/maintain_debian_16.png)




## VIII. 监控与管理

### 系统&显卡情况

主要是通过`node_exporter`与`nvidia-gpu-exporter`来拉取系统与GPU情况，用`prometheus`来进行数据存储与查询，用`grafana`来展现，其中`exporter`使用`systemctl`来进行管理，`prometheus`与`grafana`服务用`docker-compose`管理，接来来开始配置。

#### 准备Prometheus与Grafana

在`docker-compose.yml`文件添加如下:

```yml
services:
  ..
  grafana:
    image: grafana/grafana
    container_name: grafana
    restart: always
    user: '1000'
    ports:
      - 3000:3000
    volumes:
      - /opt/grafana:/var/lib/grafana
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.grafana.rule=Host(`grafana.$MY_DOMAIN`)"
      - "traefik.http.routers.grafana.entrypoints=websecure"
      - "traefik.http.routers.grafana.tls=true"
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    restart: always
    ports:
      - 9090:9090
    volumes:
      - /opt/prometheus:/etc/prometheus
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.prometheus.rule=Host(`prom.$MY_DOMAIN`)"
      - "traefik.http.routers.prometheus.entrypoints=websecure"
      - "traefik.http.routers.prometheus.tls=true"
```

添加`/opt/prometheus/prometheus.yml`文件，并添加如下内容:

```yml
# my global config
global:
  scrape_interval: 10s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]
  - job_name: 'node'
    static_configs:
      - targets: ['<your_local_ip>:9100']

  - job_name: 'nvidia'
    static_configs:
      - targets: ['<your_local_ip>:9835']
```

这里简单解释下，全局10s刷新一次，`9090`端口访问`prometheus`，`9100`是`node_exporter`对外暴露的端口，`9835`是`nvidia_gpu_exporter`对外暴露的端口。

开放端口
```bash
sudo ufw allow 9090
```

#### 准备Nvidia GPU Exporter

到[这里](https://github.com/utkuozdemir/nvidia_gpu_exporter/releases)下载最新的amd64.deb，然后执行安装`sudo dpkg -i nvidia-gpu-exporter_1.2.0_linux_amd64.deb`

安装后可以检查下其状态
```bash
systemctl status nvidia_gpu_exporter.service
```
![](/img/maintain_debian_17.png)

检查下端口情况
```bash
sudo lsof -i -P -n | grep LISTEN
```
![](/img/maintain_debian_18.png)

开放端口
```bash
sudo ufw allow 9835
```

#### 准备Node Exporter

到[这里]([Releases · prometheus/node_exporter (github.com)](https://github.com/prometheus/node_exporter/releases/))下载最新的amd64.tar.gz包，解压缩以后，里面有一个可执行的指令`node_exporter`

然后`nvim /etc/systemd/system/node_exporter.service`添加文件:
```bash
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=jacks
Group=jacks
Type=simple

ExecStart=/opt/node-exporter/node_exporter-1.5.0.linux-amd64/node_exporter

[Install]
WantedBy=multi-user.target
```

这里的`/opt/node-exporter/node_exporter-1.5.0.linux-amd64/node_exporter`假设就是你下载解压缩后的那个指令的路径

```bash
sudo systemctl daemon-reload 
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
sudo systemctl status node_exporter
```

开放端口
```bash
sudo ufw 9100
```

#### 检测与添加到Grafana

到`docker-compose.yml`的目录下执行`sudo docker-compose up -d`启动刚刚的Grafana与Prometheus，然后访问prometheus检查是否有正常链接上，搜索`up`如果后面数值是`1`则表示数据正常，连接成功。
![](/img/maintain_debian_19.png)

登录Grafana添加Prometheus作为其数据源，我就不过多赘述这里。
![](/img/maintain_debian_20.png)

##### 添加系统监控到Grafana

添加系统监控，可以考虑使用[这个](https://grafana.com/grafana/dashboards/15172-node-exporter-for-prometheus-dashboard-based-on-11074/)。

![](/img/maintain_debian_21.png)

然后拷贝这个ID: `15172`，选用好数据源为刚刚创建的Prometheus的，即可
![](/img/maintain_debian_22.png)

##### 添加GPU监控到Grafana

添加Nvidia GPU监控，可以考虑使用[这个](https://grafana.com/grafana/dashboards/14574-nvidia-gpu-metrics/)，添加方法和上面一样不赘述了

![](/img/maintain_debian_23.png)

### Docker情况

docker情况建议直接使用[Portainer](https://www.portainer.io/)，在`docker-compoase.yml`中添加:

```yml
services:
  ...
  portainer:
    image: portainer/portainer
    container_name: portainer
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /opt/portainer:/data
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.portainer.rule=Host(`portainer.$MY_DOMAIN`)"
      - "traefik.http.services.portainer.loadbalancer.server.port=9000"
      - "traefik.http.routers.portainer.entrypoints=websecure"
      - "traefik.http.routers.portainer.tls=true"
```

然后启动下`sudo docker-compose up -d`，搞定，这里我们使用`portainer.yourdomain.com`访问

![](/img/maintain_debian_24.png)

## IX. 最后附录

### 为什么选用Debian

Debian和Ubuntu在磁盘的读写速度，Docker不同的存储驱动方式，虚拟化的方式上的性能差别可能不是很大，因为它们都是基于Linux内核的操作系统，都可以调整和优化这些方面的参数。但是，根据不同的硬件配置和使用场景，可能会有一些细微的差异。

#### 共同点
它们都是开源的，都使用APT包管理器，都支持多种硬件架构，都有大量的用户和开发者社区。

#### 不同点
它们的稳定性、更新频率、软件支持和安装方式有所差别。一般来说，Debian更倾向于稳定性和简洁性，而Ubuntu更倾向于新颖性和易用性。

##### 系统更新上
Debian有三个分支，分别是稳定版（stable）、测试版（testing）和不稳定版（unstable）。稳定版的更新周期很长，一般是两年左右，但也更加稳定和安全。测试版和不稳定版的更新周期更短，但也更容易出现问题。Ubuntu有两种版本，分别是长期支持版（LTS）和非长期支持版（non-LTS）。LTS版本的更新周期是五年，非LTS版本的更新周期是九个月。Ubuntu的更新速度一般比Debian快，但也可能带来一些兼容性或稳定性的问题。

##### 软件支持
Debian和Ubuntu都使用APT包管理器，但它们的软件源不完全相同。Debian完全基于自由软件，所以它的软件源只包含自由软件。Ubuntu同时使用免费和专有软件，所以它的软件源包含了一些Debian没有的专有软件，例如NVIDIA驱动、Steam等。另外，Ubuntu还有一些自己开发或维护的软件，例如Unity桌面环境、Snap包格式等。这些软件可能在Debian上不容易安装或使用。

##### 性能稳定性考虑
Debian和Ubuntu在RAID，Docker和虚拟机这三者上的区别可能不是很明显，因为它们都是基于Linux内核的操作系统，都可以支持这些技术。但是，根据不同的使用场景和需求，可能会有一些细微的差异。

##### RAID上差异
RAID是一种磁盘阵列技术，可以提高磁盘的性能和可靠性。Debian和Ubuntu都可以使用RAID，但是它们的安装方式可能不同。Debian的安装过程中需要手动配置RAID，而Ubuntu的安装过程中可以自动检测RAID。另外，Debian和Ubuntu可能支持不同的RAID级别，例如Debian支持RAID 0、1、5、6、10等，而Ubuntu支持RAID 0、1、5等。

##### Docker上差异
Docker不同的存储驱动方式会影响容器的数据层的管理和性能。Debian默认使用overlay2存储驱动，而Ubuntu默认使用aufs存储驱动。overlay2和aufs都是基于联合文件系统（Union File System）的存储驱动，它们都可以实现容器之间的数据共享和隔离。一般来说，overlay2比aufs有更高的性能和稳定性，但是aufs可能对一些旧版的内核或文件系统有更好的兼容性。

##### 虚拟化上差异
虚拟化的方式会影响虚拟机的资源分配和性能。Debian和Ubuntu都可以使用KVM、Xen、VirtualBox等虚拟化软件，而Ubuntu还可以使用VMware等虚拟化软件。KVM和Xen都是基于内核模块（Kernel Module）的虚拟化软件，它们都可以实现虚拟机之间的资源隔离和高效利用。一般来说，KVM比Xen有更高的性能和易用性，但是Xen可能对一些特殊的硬件或场景有更好的支持。VirtualBox和VMware都是基于用户空间（User Space）的虚拟化软件，它们都可以实现虚拟机之间的资源共享和灵活配置。一般来说，VirtualBox比VMware有更低的资源消耗和更好的免费版功能，但是VMware可能对一些专业的功能或场景有更好的支持。