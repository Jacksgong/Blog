title: Ubuntu 16.04 安装与配置 Phabricator
date: 2017-06-15 23:52:03
updated: 2022-11-03
categories:
- 工程师技能
tags:
- Phabricator
- Ubuntu

---


{% note info %}看到WunderList上面自己的point越来越多，并且很多是完成了一部分，虽然知道可以通过OmniFocus或者OmniOutliner之类的进行管理，但是介于之前对Phabricator的好感与熟悉，还有觉得Phabricator可以带来更多可能，以及自己所有的私有项目都是在自己的[gitlab](https://git.jacksgong.com)上维护了，因此决定搭建以后Phabricator后面所有的任务在WunderList有进度后，都用Phabricator维护: [https://phab.jacksgong.com](https://phab.jacksgong.com) (说实话，自己用刚开始还确实有点被我朋友言中 -- 略显孤单.. ){% endnote %}

<!-- more -->

## 前言

### 先上图吧

![](/img/install-config-phabricator-1.png)
![](/img/install-config-phabricator-2.png)

## I. 准备环境

根据[之前的服务器维护文章](https://blog.dreamtobe.cn/maintain-website-server/)，安装好git与nginx环境，而后进行以下操作

### 1. 创建Phabricator用户

> 并加入sudo群组

```shell
adduser phab --home /home/phab
adduser phab sudo
```

我们这里考虑后面将所有的Phabricator相关的都放到`/var/www/phab`下面因此

```shell
mkdir /var/www/phab
chown -R phab:phab /var/www/phab
```

### 2. 安装php7.1

> Phabricator不支持php7.0，而目前php7.1只有再ppa上有

```bash
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update
sudo apt install php7.4-common php7.4-fpm php7.4-cli php7.4-json php7.4-mysql php7.4-curl php7.4-intl php7.4-mcrypt php-pear php7.4-gd php7.4-zip php7.4-xml php7.4-mbstring
```

### 3. 安装Mariadb

> 这边选用Mariadb而非MySQL的原因是，Mariadb对MySQL兼容并且拓展了很多功能，已经修复了MySQL中的一些BUG以及各类优化

```bash
sudo apt-get install mariadb-server-10.0 mariadb-client-10.0
```

## II. 配置

### 1. 拉取Phabricator

这边我将Phabricator存放在`/var/www/phab`下:

```
cd /var/www/phab
git clone https://github.com/phacility/libphutil.git
git clone https://github.com/phacility/arcanist
git clone https://github.com/phacility/phabricator.git
```

### 2. 配置nginx

如果你的nginx环境就是在[服务器维护](https://blog.dreamtobe.cn/maintain-website-server/)这篇文章配的，那么到`/etc/nginx/sites-available`目录，创建`phabricator.conf`，添加以下内容。

> 注意将下面的`phab.jacksgong.com`替换为你的域名，如果你的phabricator不是在`/var/www/phab`下面就将`/var/www/phab/phabricator/webroot`改为你的路径。

```conf
server {

  # Change to your real subdomain, e.g. phabricator.mysite.com
  server_name phab.jacksgong.com;

  # Update to the directory where you've installed Phabricator.
  root /var/www/phab/phabricator/webroot;
  try_files $uri $uri/ /index.php;

  location /
  {
        index index.php;

        if ( !-f $request_filename )
        {
          rewrite ^/(.*)$ /index.php?__path__=/$1 last;
          break;
        }
  }

  location /index.php
  {
        fastcgi_pass unix:/var/run/php/php7.1-fpm.sock;
        fastcgi_index index.php;

        #required if PHP was built with --enable-force-cgi-redirect
        fastcgi_param REDIRECT_STATUS 200;

        #variables to make the $_SERVER populate in PHP
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param QUERY_STRING $query_string;
        fastcgi_param REQUEST_METHOD $request_method;
        fastcgi_param CONTENT_TYPE $content_type;
        fastcgi_param CONTENT_LENGTH $content_length;

        fastcgi_param SCRIPT_NAME $fastcgi_script_name;

        fastcgi_param GATEWAY_INTERFACE CGI/1.1;
        fastcgi_param SERVER_SOFTWARE nginx/$nginx_version;

        fastcgi_param REMOTE_ADDR $remote_addr;
  }
}
```

然后链接到`enable`中

```shell
cd ../sites-enabled
sudo ln -s ../sites-available/phabricator.conf phabricator.conf
```

重新加载Nginx:

```shell
sudo service nginx reload
```

至此站点应该可以访问了，但是打开站点以后你会看到提示要配置数据库。

### 3. 配置数据库


> 默认Mariadb的root账户在root用户下是不用密码的，因此通过`sudo`进入

```bash
sudo mysql -u root -p
```

登陆数据库以后，注意屏幕有前缀`mysql> `

> 可以将下面的账户密码替换为你想要的。

```
mysql> create user 'phabricator'@'localhost';
mysql> grant all privileges on *.* to 'phabricator'@'localhost';
mysql> set password for 'phabricator'@'localhost' = password('12345');
mysql> exit;
```

登记数据库用户信息到Phabricator(下面的账户密码替换为刚刚你添加的):

```bash
cd /var/www/phab/phabricator
./bin/config set mysql.host localhost
./bin/config set mysql.port 3306
./bin/config set mysql.user phabricator
./bin/config set mysql.pass 12345
```

至此Phabricator可以正常访问。

## III. 配置HTTPS(option)

首先根据[之前的服务器维护文章](https://blog.dreamtobe.cn/maintain-website-server/)为域名申请好证书

然后在原本的Nginx的conf基础上添加:

```shell
 server {
    listen 80;
    server_name phab.jacksgong.com;
    return 301 https://$host$request_uri;
}

server {
    ...
  listen 443 ssl http2;

   # ssl
   ssl_certificate /etc/letsencrypt/live/phab.jacksgong.com/fullchain.pem;
   ssl_certificate_key /etc/letsencrypt/live/phab.jacksgong.com/privkey.pem;

   ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
   ssl_prefer_server_ciphers on;
   ssl_dhparam /etc/ssl/certs/dhparam.pem;
   ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
   ssl_session_timeout 1d;
   ssl_session_cache shared:SSL:50m;
   ssl_stapling on;
   ssl_stapling_verify on;
   add_header Strict-Transport-Security max-age=15768000;
    ...
}
```

然后到Phabricator目录配置`base-uri`:

> 我们可以通过`./bin/config list`列出所有支持配置的参数。

```
./bin/config set phabricator.base-uri 'https://phabricator.yoursite.com/'
```

最后根据[官方文档](https://secure.phabricator.com/book/phabricator/article/configuring_preamble/)进行配置:

到`phabricator`目录: `/var/www/phab/phabricator`创建: `support/preamble.php`，这个php在每次加载站点的时候都会被加载，并且在版本管理中已经ignore了，所以不用担心后期升级的冲突。

由于我们是通过nginx进行负载均衡，往phabricator中请求的，所以添加以下到`preamble.php`文件中:

```php
<?php

// Overwrite REMOTE_ADDR with the value in the "X-Forwarded-For" HTTP header.

// Only do this if you're certain the request is coming from a loadbalancer!
// If the request came directly from a client, doing this will allow them to
// them spoof any remote address.

// The header may contain a list of IPs, like "1.2.3.4, 4.5.6.7", if the
// request the load balancer received also had this header.

if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
  $forwarded_for = $_SERVER['HTTP_X_FORWARDED_FOR'];
  if ($forwarded_for) {
    $forwarded_for = explode(',', $forwarded_for);
    $forwarded_for = end($forwarded_for);
    $forwarded_for = trim($forwarded_for);
    $_SERVER['REMOTE_ADDR'] = $forwarded_for;
  }
}
```

在`preamble.php`中配置开启HTTPS:

```php
<?php

$_SERVER['HTTPS'] = true;

...
```

至此以全部配置完成，我的phabricator: https://phab.jacksgong.com

P.S. 可以使用`php -l support/preamble.php` 来检查`preamble.php`中是否存在php语法错误。

## IV. 更多配置

### 1. 时区

> 亚洲时间表: http://php.net/manual/en/timezones.asia.php

使用php的date函数需要配置时区，如在`/etc/php/7.1/fpm/php.init`中配置上海时区:


```
date.timezone = Asia/Shanghai
```

### 2. 大文件存储

nginx配置，在service中增加:

```
client_max_body_size 32M;
```

php.init中配置:

> 每个参数的含义参考php官方文档与[phabricator大文件配置稳定](https://secure.phabricator.com/book/phabricator/article/configuring_file_storage/)

```
post_max_size = 32M
memory_limit = -1
max_input_vars = 1000
upload_max_filesize = 32M
```

### 3. MySQL相关配置

最大大小

```
./bin/config set storage.mysql-engine.max-size 8388608
```

本地文件系统配置

先创建一个phabricator可写入的文件夹(可以用前面创建的`phab`账户创建一个755权限的目录，或者是其他账户777的权限当然也可以访问啦)，好了以后执行:

```
./bin/config set storage.local-disk.path /path/to/store/phabricator/files
```

Small MySQL "max_allowed_packet"，可以通过(`sudo mysql -u root -p`)进到mysql后，执行以下命令:

```
SET GLOBAL max_allowed_packet=33554432;
```

其他性能调优，到`my.cnf`下配置(`sudo vim /etc/mysql/my.cnf`，如果是用了mariadb，可以设置`/etc/mysql/mariadb.conf.d/50-server.cnf`)

```
[mysqld]

innodb_buffer_pool_size = 2147483648
sql_mode=STRICT_ALL_TABLES
```

然后重启

```
sudo service mysqld restart
```

### 4. 配置Phabricator账户

> 我们前面步骤创建的

```
./bin/config set phd.user phab
```

### 5. 配置`environment.append-paths`

```
./bin/config set environment.append-paths '["/usr/bin", "/usr/lib/git-core"]'
```

### 6. 配置开启`pygments`

```
./bin/config set pygments.enabled true
```

### 7. 配置Outbound发邮件

首先根据[站点配置](https://blog.dreamtobe.cn/maintain-website-server/)中的`安装sendmail`教程，安装好sendmail，然后只需要进入Phabricator，打开`Config > Core > Mail`中配置:

![](/img/install-config-phabricator-3.png)

## V. 常用指令

### 1. 重置密码以及授权访问

```
./bin/auth recover <用户名>
```

### 2. 删除所有phabricator的数据

```
sudo ./bin/storage destory
```

### 3. 迁移数据

迁移数据可以直接参照[这里](https://secure.phabricator.com/book/phabricator/article/configuring_backups/)，需要注意的是不仅仅要迁移数据库，还有上传的各类文件等等


---

- [Installing Phabricator (Debian, nginx, MySql)](http://povilasb.com/phabricator/install.html)
- [Upgrade to the specific php 7.1 from php 7.0 in ubuntu 16.04](https://askubuntu.com/questions/856793/upgrade-to-the-specific-php-7-1-from-php-7-0-in-ubuntu-16-04)
- [HOWTO: Enable SSL, notifications, and auto-updates in Phabricator install](http://rosscampbell.blogspot.hk/2014/07/howto-enable-ssl-notifications-and-auto.html)
- [Configuration Guide](https://secure.phabricator.com/book/phabricator/article/configuration_guide/)
- [Restarting Phabricator](https://secure.phabricator.com/book/phabricator/article/restarting/)
- [Phabricator Ubuntu Installation Guide](https://gist.github.com/sparrc/b4eff48a3e7af8411fc1)
- [Configuring Outbound Email](https://secure.phabricator.com/book/phabricator/article/configuring_outbound_email/)
- [MySQL删除所有数据库](https://pein0119.github.io/2015/03/18/MySQL%E5%88%A0%E9%99%A4%E6%89%80%E6%9C%89%E6%95%B0%E6%8D%AE%E5%BA%93/)

---
