title: 米家智慧摄影机 云台版自动备份 FreeNAS/TrueNAS
date: 2020-06-21 22:51:03
updated: 2022-04-24 20:53:03
categories:
- Fun
tags:
- 小米
- 云台
- Nas

---

{% note info %} 小米智能摄像机 云台版如何备份到FreeNAS呢?{% endnote %}

<!-- more -->

首先要了解小米智能摄像机自带的备份FreeNAS的机制，网上资料比较少，试了以后才知道原来是基于SMB 1.0协议的。

不过默认情况下，用FreeNAS开启SMB后依然不行，那是因为FreeNAS自带的SMB服务不是SMB1，因此默认你开启后在米家上虽然能够识别的到，但是无论怎么弄都是提示错误。

因此你需要做以下修改:

1. 进入FreeNAS管理页面
2. 进入Service->SMB->config
3. 勾选`Enable SMB1 support`
4. 点击SAVE

另外如果你使用TrueNas 12.0及以上版本，由于NMBD服务默认被系统关闭了，所以即便你上面都操作了，其实依然会找不到，并且影响备份，此时你需要做以下操作:

1. 进入TrueNAS管理页面
2. 打开网络
3. 打开全局配置的设置页面
4. 勾选`NetBIOS-NS`
4. 点击保存

此时你再在米家上输入用户名密码就可以正常识别了，识别选择目录后，就会在你选择的目录上新增了xiaomi_camera_videos的目录，所有视频都会自动备份到里面了。

---

- [TrueNAS 12 & SMB 1?](https://www.truenas.com/community/threads/truenas-12-smb-1.88159/)
