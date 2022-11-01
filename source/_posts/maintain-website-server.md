title: 站点与服务器维护
date: 2017-03-06 15:59:03
updated: 2022-11-01
categories:
- 服务器
tags:
- Ubuntu
- Nginx
- Shell
- Swap
- BBR

---

由于早年做过论坛，以及一些小网站，因此已经习惯了搞一个VPS，自己折腾。本文主要记录了服务器(Ubuntu 16.04)以及一些站点的快速维护经。

<!-- more -->

{% note warning %} 下面的所有配置都是基于Ubuntu 16.04

如果你的服务器在国内，`gist.github.com`已经被墙，你可以将下面快速执行脚本中的`gist.github.com`改为`gist.dreamtobe.cn`即可(我架了一个代理) {% endnote %}

## Ubuntu 16.04环境

### 服务器环境配置

#### 1. 基本用户配置

<script src="https://gist.dreamtobe.cn/Jacksgong/6b2c118c9a1b1c064c5d5f6402c240d3.js"></script>

#### 2. 修改编辑器

```shell
sudo update-alternatives --config editor
```

#### 3. 配置sudo不用密码

我个人习惯，新创建的账户不给设置密码，只允许证书登录，并且允许无密码`sudo`

通过 `sudo visudo` 进入编辑，然后添加:

```
<用户名> ALL=(ALL) NOPASSWD: ALL
```

#### 4. 配置Shell

> 由于MacBook上对zsh长期的使用习惯，因此使用统一风格的zsh，并使用oh-my-zsh管理

![](/img/maintain-website-server-1.png)

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/12b7d677e6ce47e7684bb1afc0c5c629.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/9d0519f68b7940a07075a834b3178979.js"></script>

执行效果图:

<img src="/img/conf-zsh.png" width="450px">

P.S 如果`autojump`存在问题，请主动执行:

```shell
git clone https://github.com/joelthelion/autojump.git
cd autojump
python install.py
```

#### 5. 修改source

> **如果是海外的VPS** 可以忽略这一步。

这里之所以要修改，是因为国内的部分VPS，如阿里云、腾讯云等有篡改ubuntu与相关库的习惯。

先备份`/etc/apt/sources.list`文件，然后将其内容全部删除，然后使用下面的源:

<script src="https://gist.dreamtobe.cn/Jacksgong/2d960a5299ca67e728edc27ad4f284f9.js"></script>

配置完后，最好升级下所有的包(`sudo -- sh -c "apt-get update && apt-get upgrade"`)，这时候你就会发现有哪些被修改过了，我的做法是全部替换为原版(`maintainer's version`)

#### 6. 配置10分钟闲置后自动断开

在`/etc/ssh/sshd_config`中配置

```bash
ClientAliveInterval 600
ClientAliveCountMax 0
```

#### 7. 修改hostname

> 可以通过命令`hostname`输出当前的hostname

以下以将`hostname`修改为`new-host-name`为例子:

- 第一步: 通过`sudo hostname new-host-name`，让注销重新登录以后立马生效新的`hostname`
- 第二步: 通过修改`/etc/hostname`中的`hostname`来固化，让重启后依然使用新的`hostname`
- 第三步: 通过在`/etc/hosts`中修改(添加)`new-host-name`到本地`127.0.0.1`中，如`127.0.0.1 new-host-name`，让通过`hostname`访问本地时能够解析到本地

#### 8. 防火墙配置

> 内对外完全放开，外对内只开启22,80,443端口

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/7369e03bce09bab7d9e432012660094f.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/1151255d4bbcf10269b781820bf74531.js"></script>

执行效果图:

<img src="/img/conf-firewall.jpg" width="450px">

#### 9. 配置TCP BBR拥塞算法

> 以下方法只在ubuntu 16.x上测试过，如果是使用ubuntu 22以及更高版本，可以参考[这里](https://www.linuxcapable.com/enable-bbr-on-ubuntu-22-04-boost-internet-speed/)，实际上只需要做如下操作
> ![](/img/maintain-website-server-b50eb67c.png)
> 也就是只需要在`/etc/sysctl.conf`中将对应模式修改即可，因为内核已经支持，不用再执行脚本去升级内核了。修改后同样的用`bbr-check.sh`来检测是否生效即可。

快速执行配置，安装与检测安装算法(需要OpenVZ以外虚拟技术的VPS平台):

安装:

<script src="https://gist.dreamtobe.cn/Jacksgong/bb011a5c48ef47ef6df0b3333c02b54f.js"></script>

执行效果图:

<img src="/img/install-bbr.jpg" width="450px">

检测安装结果:

<script src="https://gist.dreamtobe.cn/Jacksgong/684f423d5be270ce9610a053483e7a8b.js"></script>

检测安装结果时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/383df6722917610a4dd42308666703c4.js"></script>

执行效果图:

<img src="/img/check-bbr.png" width="450px">

#### 10. 配置Swap

> 考虑到gitlab等应用对内存使用比较多，因此可以通过`top`工具来查看内存的使用情况，考虑到有可能会有内存不足导致500，可以配置Swap来避免该问题的发生
> 在以前考虑到SSD硬盘的写入次数太过频繁很容易缩短使用寿命，因此不建议使用SSD做Swap，但是现在的[SSD已经逐渐改善](http://askubuntu.com/questions/652337/why-no-swap-partitions-on-ssd-drives/652342#652342?newreg=237ae587907241919402075b80ab6fa3)了类似的情况

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/5fab6a7d6cf7ee21c44d6cfeaecb400d.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/58a8421fb362b9763cfae050245e5577.js"></script>

执行效果图:

<img src="/img/conf-swap.png" width="450px">

也可以通过通过下面的命令从`检测情况`、`安装`、`固化`、`调优`，手动的一步一步配置Swap，需要注意的是一般来说比较好的Swap大小是等于现有RAM大小或是现有RAM的两倍:

<script src="https://gist.dreamtobe.cn/Jacksgong/d54e2b68e2b66faec7e671338ac4b85b.js"></script>

#### 11. 安装与配置Nginx

> 在ubuntu 22以及更高版本下，可以参考[这里](https://linuxhint.com/install-nginx-ubuntu-22-04/) ,只需要用`sudo apt install nginx`就可以完成安装。

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/4759813f74070cf123afdc683e0fcd0a.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/b582591df46dc6d2da43bbf8018f4e1c.js"></script>

执行效果图:

<img src="/img/install-nginx.jpg" width="450px">

#### 12. 安装PHP7

快速执行配置:

```bash
sudo apt install php7.0-common php7.0-fpm php7.0-cli php7.0-json php7.0-mysql php7.0-curl php7.0-intl php7.0-mcrypt php-pear php7.0-gd php7.0-zip php7.0-xml php7.0-mbstring
```

#### 13. 配置Java

检测版本:

```bash
java -version
```

安装默认jdk(OpenJDK):

```bash
sudo apt-get install default-jdk
```

安装Oracle-JDk-8:

```bash
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update

sudo apt-get install oracle-java8-installer
```

检查可用`JAVA_HOME`环境变量的路径:

```bash
sudo update-alternatives --config java
```

#### 14. 配置Shadowsocks Client用于国内VPS翻墙

先拉取shadowsocks-client-ubuntu项目:

```bash
git clone git@git.jacksgong.com:Jacksgong/shadowsocks-client-ubuntu.git
cd shadowsocks-client-ubuntu
```

安装:

> [install.sh](https://git.jacksgong.com/Jacksgong/shadowsocks-client-ubuntu/blob/master/install.sh)

```bash
./install.sh
```

创建配置文件:

在项目根目录创建`config.json`，然后输入配置:

```json
{
"server":"服务器ip地址",
"server_port":8388,
"local_port":10808,
"password":"密码与服务端配置一样",
"timeout":600,
"method":"aes-256-cfb"
}
```

后台运行并输出日志到log文件:

> [start.sh](https://git.jacksgong.com/Jacksgong/shadowsocks-client-ubuntu/blob/master/start.sh)

```bash
./start.sh
```

检测运行:

检测相关进程是否存在

> [check.sh](https://git.jacksgong.com/Jacksgong/shadowsocks-client-ubuntu/blob/master/check.sh)

```bash
./check.sh
```

关闭后台运行:

> [stop.sh](https://git.jacksgong.com/Jacksgong/shadowsocks-client-ubuntu/blob/master/stop.sh)

```bash
./stop.sh
```

#### 15. 安装sendmail用于发邮件

安装:

```shell
apt-get install sendmail
```

检测是否正在运行:

```shell
ps -aux | grep sendmail
```

配置php中的sendmail，编辑`/etc/php/7.1/fpm/php.ini`:

将其中的:

```
;sendmail_path=
```

替换为:

```
sendmail_path = /usr/sbin/sendmail
```

如果使用外部邮件提供商，需要进一步配置:

编辑`/etc/mail/sendmail.mc`文件，新增下面两行(将`jacksgong.com`替换为你的域名):

```m
define(`MAIL_HUB', `jacksgong.com.')dnl
define(`LOCAL_RELAY', `jacksgong.com.')dnl
```

然后生效配置:

```shell
sudo sendmailconfig
sudo service sendmail restart
```

#### 16. 安装python

先安装依赖:

```
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```

下载指令:

```
version=2.7.13
wget https://www.python.org/ftp/python/$version/Python-$version.tgz
```

解压缩:

```
tar -xvf Python-$version.tgz
cd Python-$version
```

编译安装:

```
./configure
make
sudo checkinstall
```

#### 17. DNS问题处理

如果发现DNS有问题，可以通过以下的方式进行配置，首先添加以下内容到`/etc/resolvconf/resolv.conf.d/base`:

```
nameserver 8.8.8.8
nameserver 8.8.4.4
```

DNS服务器如果不知道怎么选择，建议可以直接在[这里](https://ip.cn/dns.html)查找自己想要的DNS服务器。

然后通过执行以下指令进行生效:

```
sudo resolvconf -u
```

## 站点安装

### 1. ownCloud

> 私有云服务搭建

前置条件: 安装与配置好Nginx与PHP7

> 这边选用Mariadb而非MySQL的原因是，Mariadb对MySQL兼容并且拓展了很多功能，已经修复了MySQL中的一些BUG以及各类优化

整个流程比较简单，可以考虑直接参照: [How to Setup ownCloud 9.1 on Ubuntu 16.10 with Letsencrypt SSL](http://linoxide.com/storage/setup-owncloud-9-ubuntu-16-letsencrypt/)

- 创建云用户与表(例子)
- 配置nginx
- 打开页面输入配置

### 2. gitlab

> 这边我使用的是omnibus的版本，因为这个版本足够灵活也便于维护。

#### 通过脚本安装gitlab-omnibus版本

> [官方安装教程](https://about.gitlab.com/downloads/)

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/770871658d3511012a3b9decbf7b4454.js"></script>

#### 配置使用自己的Nginx

> [官方配置教程](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/nginx.md#using-a-non-bundled-web-server)

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/c5b1efd6da187e5ccd543e5461641bf8.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/599385bc7abc4b0c5b9aa6c91fde4082.js"></script>

执行效果图:

<img src="/img/conf-gitlab-non-bundled-nginx.png" width="450px">

#### 配置Gitlab的HTTPS

- 参考本文下面提到的配置SSL(HTTPS)https来生成对应用于gitlab访问域名的证书
- 将nginx配置文件调整为: [gitlab-omnibus-ssl-nginx.conf](https://gitlab.com/gitlab-org/gitlab-recipes/blob/master/web-server/nginx/gitlab-omnibus-ssl-nginx.conf)
- 修改`/etc/gitlab/gitlab.rb`中的`external_url`然后执行`sudo gitlab-ctl reconfigure`进行生效

#### 各类状态检测与修复

<script src="https://gist.dreamtobe.cn/Jacksgong/c3976d9e7e53a4ef81b22efcba7388d4.js"></script>

#### 查看当前状态

执行`sudo gitlab-ctl status`

#### 备份

通过命令`sudo gitlab-rake gitlab:backup:create`进行备份，备份完成后备份文件会在`/var/opt/gitlab/backups`目录下面，文件名为`[TIMESTAMP]_gitlab_backup.tar`。

#### 还原

1. 确保目前的版本与备份文件的版本是在同一个版本(检测当前版本: `sudo gitlab-rake gitlab:env:info`)
2. 将备份文件拷贝到`/var/opt/gitlab/backups`目录下，并且通过`chown git:git [backup-file]`确保备份文件所有权是`git`用户所有
3. 确保`/etc/gitlab/gitlab.rb`与`/etc/gitlab/gitlab-secrets.json`这两个配置文件与备份的一致，然后再生效下配置`sudo gitlab-ctl reconfigure`
4. 分别执行`sudo gitlab-ctl stop unicorn`、`sudo gitlab-ctl stop sidekiq`，然后通过`sudo gitlab-ctl status`检查下状态
5. 执行`sudo gitlab-rake gitlab:backup:restore BACKUP=[backup-file-name]`(这里的`[backup-file-name]`如: `1393513186_2014_02_27`)，进行还原
6. 执行`sudo gitlab-ctl start`重新启动gitlab，并执行`sudo gitlab-rake gitlab:check SANITIZE=true`进行检查与自动修复

#### 升级

执行`sudo apt-get update`与`sudo apt-get install gitlab-ce`即可，自动会升级到最新的版本。

#### 卸载

执行`sudo gitlab-ctl uninstall`

### 3. Phabricator

可以参照我的另外一篇文章: [Ubuntu 16.04.2 安装与配置 Phabricator](https://blog.dreamtobe.cn/install-config-phabricator/)

## 站点维护

### 1. 配置SSL(HTTPS)

通过配置如该博客的情况:

![](/img/maintain-website-server-2.png)

> 使用Let's Encrypt免费证书

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/feae66420a07315c389bc383ba03a25d.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/012b8be66ff15b2bfbcba81e21e73c40.js"></script>

执行效果图:

<img src="/img/conf-https.jpg" width="450px">


#### 安全检验

通过ssladbs站点进行校验即可: https://www.ssllabs.com/ssltest/analyze.html?d=example.com

#### 自动化刷新证书

由于Let's Encrypt的证书默认有效期是90天， 因此我们可以自己写一个计时器检测更加可靠(每周检查)，下面的脚本是每周一上午2:30自动执行`certbot-auto renew`，日志会写入`/var/log/le-renewal.log`，并且在随后5分钟重新加载nginx:

<script src="https://gist.dreamtobe.cn/Jacksgong/b9cc015e17ca259349caf97fef2a39bb.js"></script>

---

- [How To Set Up a Firewall with UFW on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)
- [本博客 Nginx 配置之完整篇](https://imququ.com/post/my-nginx-conf.html)
- [一键安装最新内核并开启 BBR 脚本](https://teddysun.com/489.html)
- [How To Secure Nginx with Let's Encrypt on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04)
- [How To Add Swap Space on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04)
- [How do I terminate all idle incoming ssh connections?](http://askubuntu.com/questions/137632/how-do-i-terminate-all-idle-incoming-ssh-connections)
- [Add a User to a Group (or Second Group) on Linux](https://www.howtogeek.com/50787/add-a-user-to-a-group-or-second-group-on-linux/)
- [Ubuntu Linux Change Hostname (computer name)](https://www.cyberciti.biz/faq/ubuntu-change-hostname-command/)
- [Gitlab Backup restore](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/raketasks/backup_restore.md)
- [Updating GitLab via omnibus-gitlab](https://docs.gitlab.com/omnibus/update/README.html#updating-from-gitlab-66-and-higher-to-the-latest-version)
- [How To Install Java on Ubuntu with Apt-Get](https://www.digitalocean.com/community/tutorials/how-to-install-java-on-ubuntu-with-apt-get)
- [各种系统下Shadowsocks客户端的安装与配置](http://www.jeyzhang.com/how-to-install-and-setup-shadowsocks-client-in-different-os.html)
- [Ubuntu下shadowsocks 安装与配置（server and client）](https://my.oschina.net/lieefu/blog/500774)
- [INSTALL SENDMAIL ON UBUNTU](https://www.leonardaustin.com/blog/technical/sendmail-on-ubuntu/)
- [How do I set my DNS when resolv.conf is being overwritten?](https://unix.stackexchange.com/questions/128220/how-do-i-set-my-dns-when-resolv-conf-is-being-overwritten)
- [How do I install the latest Python 2.7.X or 3.X on Ubuntu?](https://askubuntu.com/questions/101591/how-do-i-install-the-latest-python-2-7-x-or-3-x-on-ubuntu)

---
