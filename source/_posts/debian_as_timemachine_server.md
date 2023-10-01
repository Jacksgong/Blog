title: 使用Debian 创建Mac的Timemachine
date: 2023-10-01 16:32:36
updated: 2023-10-01
categories:
- service
tags:
- nas
- timemachine
- debian

---

{% note info %} 这里我们使用`netatlk`与`avahi-daemon`服务来让debian实现支持局域网发现timemachine，提供timemachine服务。 {% endnote %}

<!-- more -->

## 安装依赖

```bahs
sudo apt install netatalk avahi-daemon
```

## 基本配置

创建用户以及添加一个有权限的目录，其中的`your-xx`自己根据情况修改即可。

```bash
sudo useradd --no-create-home your-username
sudo mkdir /srv/timemachine
sudo chown your-username:your-usergroup /srv/timemachine
```

如果需要给账户添加密码，在timemachine连接的时候登录该账号，就给账户添加下密码:

```bash
sudo passwd mbp
```

编辑配置`/etc/netatalk/afp.conf`，下面的配置中配置限制的大小为`700G`，其他的根据自己的想法进行配置即可

```conf
;
; Netatalk 3.x configuration file
;

[Global]
hostname = your-hostname

[TimeMachine]
path = /srv/timemachine
time machine = yes
valid users = your-username
vol size limit = 700000
```

## 启用服务

配置防火墙开启对应端口:

```bash
sudo ufw allow 548
sudo ufw allow 427
sudo ufw allow 4700
```

启用服务:

```bash
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
sudo systemctl enable netatalk
sudo systemctl start netatalk
```

此时就可以在mac上找到这个Timemachine磁盘了。

---

- [TimeMachine backup to a Linux server › maxhaesslein.de](https://www.maxhaesslein.de/notes/timemachine-backup-to-a-linux-server/)