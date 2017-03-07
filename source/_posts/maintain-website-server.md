title: 站点与服务器维护
date: 2017-03-08 00:40:03
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

> 下面的所有配置都是基于Ubuntu 16.04

## Ubuntu 16.04环境

### 服务器环境配置

#### 1. 配置Shell

> 由于MacBook上对zsh长期的使用习惯，因此使用统一风格的zsh，并使用oh-my-zsh管理

![](/img/maintain-website-server-1.png)

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/12b7d677e6ce47e7684bb1afc0c5c629.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/9d0519f68b7940a07075a834b3178979.js"></script>

执行效果图:

<img src="/img/conf-zsh.jpg" width="400px">

#### 2. 防火墙配置

> 内对外完全放开，外对内只开启22,80,443端口

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/7369e03bce09bab7d9e432012660094f.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/1151255d4bbcf10269b781820bf74531.js"></script>

执行效果图:

<img src="/img/conf-firewall.jpg" width="400px">

#### 3. 配置TCP BBR拥塞算法

快速执行配置，安装与检测安装算法(需要OpenVZ以外虚拟技术的VPS平台):

安装:

<script src="https://gist.dreamtobe.cn/Jacksgong/bb011a5c48ef47ef6df0b3333c02b54f.js"></script>

执行效果图:

<img src="/img/install-bbr.jpg" width="400px">

检测安装结果:

<script src="https://gist.dreamtobe.cn/Jacksgong/684f423d5be270ce9610a053483e7a8b.js"></script>

检测安装结果时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/383df6722917610a4dd42308666703c4.js"></script>

执行效果图:

<img src="/img/check-bbr.png" width="400px">

#### 4. 配置Swap

> 考虑到gitlab等应用对内存使用比较多，因此可以通过`top`工具来查看内存的使用情况，考虑到有可能会有内存不足导致500，可以配置Swap来避免该问题的发生
> 在以前考虑到SSD硬盘的写入次数太过频繁很容易缩短使用寿命，因此不建议使用SSD做Swap，但是现在的[SSD已经逐渐改善](http://askubuntu.com/questions/652337/why-no-swap-partitions-on-ssd-drives/652342#652342?newreg=237ae587907241919402075b80ab6fa3)了类似的情况

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/5fab6a7d6cf7ee21c44d6cfeaecb400d.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/58a8421fb362b9763cfae050245e5577.js"></script>

执行效果图:

<img src="/img/conf-swap.png" width="400px">

也可以通过通过下面的命令从`检测情况`、`安装`、`固化`、`调优`，手动的一步一步配置Swap，需要注意的是一般来说比较好的Swap大小是等于现有RAM大小或是现有RAM的两倍:

<script src="https://gist.dreamtobe.cn/Jacksgong/d54e2b68e2b66faec7e671338ac4b85b.js"></script>

#### 5. 安装与配置Nginx

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/4759813f74070cf123afdc683e0fcd0a.js"></script>

快速执行配置时，所执行的脚本:

<script src="https://gist.dreamtobe.cn/Jacksgong/b582591df46dc6d2da43bbf8018f4e1c.js"></script>

执行效果图:

<img src="/img/install-nginx.jpg" width="400px">

#### 6. 安装PHP7

快速执行配置:

<script src="https://gist.dreamtobe.cn/Jacksgong/bcc821847daa693dbb49452bdd0deb25.js"></script>

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

<img src="/img/conf-gitlab-non-bundled-nginx.png" width="400px">

#### 配置Gitlab的HTTPS

- 参考本文下面提到的配置SSL(HTTPS)https来生成对应用于gitlab访问域名的证书
- 将nginx配置文件调整为: [gitlab-omnibus-ssl-nginx.conf](https://gitlab.com/gitlab-org/gitlab-recipes/blob/master/web-server/nginx/gitlab-omnibus-ssl-nginx.conf)
- 修改`/etc/gitlab/gitlab.rb`中的`external_url`然后执行`sudo gitlab-ctl reconfigure`进行生效

#### 各类状态检测与修复

```
gitlab-rake gitlab:check SANITIZE=true
```

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

<img src="/img/conf-https.jpg" width="400px">


#### 安全检验

通过ssladbs站点进行校验即可: https://www.ssllabs.com/ssltest/analyze.html?d=example.com

#### 自动化刷新证书

> TODO 有时间以后，考虑也将这个写成自动化bash脚本

Let's Encrypt的证书默认有效期是90天， 不过我们可以通过`certbot-auto`进行`renew`

```
certbot-auto renew
```

由于这个是失效30天内重新执行生成的，因此我们可以自己写一个计时器检测更加可靠(每周检查):

```
sudo crontab -e
```

添加(每周一上午2:30自动执行`certbot-auto renew`并且在2:35重新加载Nginx)，日志会写入`/var/log/le-renewal.log`

```
30 2 * * 1 /usr/local/sbin/certbot-auto renew >> /var/log/le-renew.log
35 2 * * 1 /etc/init.d/nginx reload
```

---

- 文章创建时间: 2017-03-06，[本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/maintain-website-server.md)。

---

- [How To Set Up a Firewall with UFW on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)
- [本博客 Nginx 配置之完整篇](https://imququ.com/post/my-nginx-conf.html)
- [一键安装最新内核并开启 BBR 脚本](https://teddysun.com/489.html)
- [How To Secure Nginx with Let's Encrypt on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04)
- [How To Add Swap Space on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04)

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
