title: Mac 作为NFS服务器
date: 2023-08-29 00:33:26
updated: 2023-09-02
categories:
- service
tags:
- nfs
- mount

---

{% note info %} 我们都知道Mac是自带NFS服务的，但是默认是没有开启，并且配置文件`/etc/exports`也不存在，这篇文章就简单介绍了如何将Mac的NFS服务开起来，并且共享某一个目录给到局域网。 {% endnote %}

<!-- more -->

## 配置需要共享的目录

假设你需要共享的目录是`/Volumes/BACKUP/dev/tools`，并且对外可以访问的权限等于当前Mac的用户`jacks`，你的局域网是`10.0.0.0`，那么你可以通过`sudo nvim /etc/exports`添加如下设置将其假如为共享目录:

```exports
/Volumes/BACKUP/dev/tools -mapall=jacks -network 10.0.0.0 -mask 255.255.255.0
```

## 生效配置

检查配置状态:
```bash
sudo nfsd checkexports
```

正常无报错会没有任何输出。如果报如下没有权限的错误:

![](/img/mac_nfs_service_a5f53e18_0.png)

需要到系统安全设置中针对完全磁盘访问权限点击`+`，然后按`cmd+shift+G`，输入`/sbin/nfsd`，将`nfsd`权限添加上即可。

![](/img/mac_nfs_service_8f76e6ba_1.png)

然后重启服务:
```bash
sudo nfsd restart
```

此时可以查看挂载状态:
```bash
showmount -e
```

![](/img/mac_nfs_service_151900c1_2.png)

至此完成，就可以在`10.0.0.x`的任意局域网下挂载Mac通过NFS协议共享出来的`tools`目录了。

---

- [How to share directory over NFS from Mac? (w/o macOS Server app)](https://apple.stackexchange.com/questions/282644/how-to-share-directory-over-nfs-from-mac-w-o-macos-server-app)
- [一文搞定 Linux，Mac，Windows 的 NFS 网络文件共享服务部署](https://blog.csdn.net/candyngwh/article/details/105427684)
- [NFS access issues on macOS 10.15 (Catalina)](https://blog.docksal.io/nfs-access-issues-on-macos-10-15-catalina-75cd23606913)