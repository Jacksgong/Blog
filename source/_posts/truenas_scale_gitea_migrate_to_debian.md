title: 从Truenas Scale下迁移Gitea到Debian
date: 2023-08-30 01:28:50
updated: 2023-08-30
categories:
- service
tags:
- docker-compose
- gitea
- truenas scale

---

{% note info %} 本文主要介绍了如何从Truenas Scale的应用中迁移Gitea 迁移到 Debian下，其中踩到不少坑点，都在文中一一提到解决方案，如果你也有类似诉求希望能够有所帮助。 {% endnote %}

<!-- more -->

## 1. 从Truenas中通过备份的dump指令导出zip

需要留意的是使用命令`/bin/bash`，另外所在容器参考下面的截图
![](/img/truenas_scale_gitea_migrate_to_debian_9da5eef7_0.png)

执行指令，这里特别留意:

1. 默认的`dump`是根据配置文件路径`/data/gitea/conf/app.ini`来生成的，如果你之前没有配置过默认就是这个不用管，如果配置过，可以通过`-c <your app.ini path>`指令来指定就行。
2. 不要在所挂载的`/data`目录下执行指令，默认是生成一个迁移`.zip`文件到执行命令的目录下的，而这个迁移的`.zip`文件会不断的将`/data`目录所有内容写入到`.zip`中，如果你放在`/data`目录下，就会循环写入。解决方案，可以到`/tmp`目录下执行指令，执行后再将生成的`.zip`文件拷贝到挂载的`/data`中，再导出即可。

```bash
gitea dump
```

另外也可以通过ssh访问Nas服务器后，通过[这里的教程](https://blog.dreamtobe.cn/truenas_scale_command_apt/#%E8%BF%9B%E5%85%A5%E5%88%B0%E6%9F%90%E4%B8%AApods%E9%87%8C%E9%9D%A2)在终端上直接操作（考虑到网页端的登录session不太可控的因素下建议这样去操作好些）。

## 2. 在Debian上安装相同版本

可以到Debian下安装相同版本的gitea（安装后后面再升级到新版本比较稳妥），需要特别注意的是，安装后不要打开网页进行初始化的填参数，直接接着下面的迁移动作就行。

类似我是用的`docker-compose`部署的，部署内容就类似下面这样（你假如也需要使用，留意里面的文件路径映射以及对必要端口的开启），截图中gitea我已经使用的是`latest`版本了，是因为截图时已经完成迁移后截的图，实际你可以先配上指定版本：

![](/img/truenas_scale_gitea_migrate_to_debian_711c0c7a_1.png)

## 3. 迁移内容

解压zip文件会有以下一些文件:
![](/img/truenas_scale_gitea_migrate_to_debian_821c5064_2.png)

将zip解压后，会有一些文件，拷贝到对应的目录下即可，需要特别注意这里需要结合实际情况，比如用户权限，各类关联服务的IP等，都需要在`app.ini`中进行略微调整。

```bash
mv app.ini /mnt/dev/opt/gitea/app.ini  
chown -R git:git /mnt/dev/opt/gitea/app.ini
```

类似我拷贝后就对以下内容进行了修改与调整:
![](/img/truenas_scale_gitea_migrate_to_debian_e60352e5_3.png)

```bash
mv data/* /mnt/dev/data/gitea/gitea/  
mv repos/* /mnt/dev/data/gitea/git/gitea-repositories
chown -R git:git /mnt/dev/data/gitea/gitea /mnt/dev/data/gitea/git/gitea-repositories
```

## 4. 导入sql（注意remote）

```bash
psql -h 10.0.0.xx -d gitea -U jacks < gitea-db.sql
```

![](/img/truenas_scale_gitea_migrate_to_debian_c82adc96_4.png)

## 5. 重启

```bash
sudo docker-compose restart gitea
```

至此成功完成迁移工作。

![](/img/truenas_scale_gitea_migrate_to_debian_a2a9f97c_5.png)

![](/img/truenas_scale_gitea_migrate_to_debian_9d2f8fba_6.png)

---

-  [官方教程](https://docs.gitea.com/zh-cn/administration/backup-and-restore)
- [其他辅助教程](https://blog.csdn.net/weixin_43525185/article/details/120371347)