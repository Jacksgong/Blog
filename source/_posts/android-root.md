title: Android Root
date: 2017-05-13 21:22:03
categories:
- 工程师技能
tags:
- Root
- BootLoader
- Recovery
- Su

---

{% note info %}今天，我们就聊聊Android手机Root的一些知识。{% endnote %}

<!-- more -->

## BootLoader

Google亲儿子的Android手机(如Nexus的)，是可以直接通过进入fastboot模式后，执行`fastboot oem unlock`来解锁的。那么这个锁是干啥用呢?

- 一般来说BootLoader是lock的，是Android用于加密的一种方法。
- 一旦设备unlocked了，那么使用者便可以刷入不同的Recovery或者是不同的ROM，甚至是获取到所有的用户数据，这是十分危险的。
- 即便是用户自己去unlock，默认也是会先将用户数据全部清除，然后再unlock，目的是为了防止用户数据被盗。
- 早期的中国厂商的出厂手机默认就是解锁的，现在大多数都已经规范，默认BootLoader是锁住的，并且有配套的解锁工具，如小米就需要绑定账户到官网申请以后才能获得对应的解锁权利。

## Recovery

Android手机有一个独立的Recovery分区，用于存储Recovery，Recovery是一个Linux的最小集镜像，主要是用于一些简单的操作，如清除用户数据，检验与刷入Over-the-Air(OTA)升级包。

解锁以后，在recovery模式下，通常都是提供了完全访问权限的adb(作为root常驻运行)

最有名的第三方Recovery要数开源的TWRP了，你可以在[这里](https://twrp.me/Devices/)看看官网是否支持了你的设备。当然了由于是开源，在官网找不到支持的设备也不用担心，国内有很多厂商或者个人也在做这块的贡献与支持(如米6官网还没有支持，国内[奇兔](http://www.7to.cn/)就给支持了)。

#### 常用指令:

> 如我自己手机[常用的指令](https://git.jacksgong.com/home/miui)

- 可以通过`adb reboot recovery`来重启进入`recovery`模式
- 通过fastboot刷入recovery.img镜像: `fastboot flash recovery recovery.img`
- 刷入完成后进入recovery.img镜像的Recovery: `fastboot boot recovery.img`

## Root

所谓Root，就是让应用拥有管理者权限来执行相关的指令。

#### 系统是怎么防止Root的?

1. 默认情况下system分区是只读的。
2. 即便是要刷自己的刷机包，系统默认的recovery是会检验签名的，因此外接无法刷入非法的zip包

#### 如何拷贝到system分区下?

1. 利用系统漏洞（如有些linux kernal或者驱动存在UAF或者overflow的漏洞），KingRoot之类的软件就利用这些漏洞让自己的代码运行在内核态，让后把自己进程的uid与gid(这些存在内核态，用户态是没法直接改的)，等等改成0，这样这个进程权限就被提到root了：不推荐这种，因为对应的软件通常都很没有节操。
2. 将su的命令集(binary)放到`/system/xbin/`或者(最新版本SuperSu)`/su/bin/su`下，使得app可以通过`su -c xxxcmd`以最高管理员权限执行指令，但是要刷入包含Su指令集的刷机包需要绕过Recovery中的校验，因此就需要解锁来刷入第三方的Recovery: 推荐这种，因为目前有Supersu这种开源的软件，可以刷入其提供的su命令集，以及安装其提供的管理员权限管理APP，干净绿色。

---

- [Locked and Unlocked Android Boot Loaders](http://technotif.com/locked-unlocked-android-boot-loaders/)
- [安卓root原理过程相同吗？](https://www.zhihu.com/question/35735659)
