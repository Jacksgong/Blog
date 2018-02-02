title: AndroidThings安装与配置
date: 2017-04-07 02:07:03
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483704&idx=1&sn=beaa1ab0205888bfdcc9d4b165849ce4
wechatmptitle: AndroidThings安装与配置
updated: 2017-04-07
categories:
- IoT
tags:
- AndroidThings
- Raspberry Pi
- IoT

---

{% note info %}这段时间看了很多AndroidThings的文章，因此买了树莓派3代，毕竟作为物联网(IoT)系统，AndroidThings对Android工程师非常的友好。{% endnote %}

<!-- more -->

![](/img/install-androidthings-1.jpeg)

### I. 你需要准备以下

1. 树莓派3代B型(Raspberry Pi Model B)主板
2. 树莓派电源
3. 至少8G的microSD卡
4. 连接显示器的视频线(注意: 树莓派上的口是HDMI口)

### II. 安装AndroidThings

#### 第一步: 下载镜像并解压缩

下载[最新版本镜像](https://developer.android.com/things/preview/download.html)，并解压缩下载的镜像压缩文件(通过unzip指令)。

![](/img/install-androidthings-2.png)

#### 第二步: microSD卡准备

将microSD卡插入电脑，确保其是FAT32的文件格式(如果格式不对可以通过Disk Utility对其进行格式化)。

![](/img/install-androidthings-3.png)

#### 第三步: 写入`.img`

下载安装[Etcher](https://etcher.io/) 并通过Etcher将解压缩出来的`.img`文件写入microSD卡。

![](/img/install-androidthings-5.png)
<p style="text-align: center;"> 写入 </p>

![](/img/install-androidthings-6.png)
<p style="text-align: center;"> 校验 </p>

![](/img/install-androidthings-7.png)
<p style="text-align: center;"> 完成 </p>

#### 第四步: microSD插入树莓派

通过Finder的Eject取出microSD卡，插入树莓派。

<img src="/img/install-androidthings-8.jpeg" width="450px">

#### 第五步: 运行AndroidThings

使用视频线连接树莓派到显示器，接上网线，然后接上电源，至此AndroidThings已经运行起来了。

![](/img/install-androidthings-9.jpeg)
![](/img/install-androidthings-10.jpeg)

### III. 基本配置

#### 1. 连接AndroidThings

`adb connect <ip-address>`

![](/img/install-androidthings-11.png)

#### 2. 断开AndroidThings

`adb disconnect <ip-address>`

![](/img/install-androidthings-12.png)

#### 3. 关机

`adb shell reboot -p`

![](/img/install-androidthings-13.png)

#### 4. 配置连接Wi-Fi

```
 adb shell am startservice \
    -n com.google.wifisetup/.WifiSetupService \
    -a WifiSetupService.Connect \
    -e ssid <Network_SSID> \
    -e passphrase <Network_Passcode>
```

![](/img/install-androidthings-14.png)

#### 5. 检测Wi-Fi是否连接上

`adb logcat -d | grep Wifi`

![](/img/install-androidthings-15.png)
<p style="text-align: center;"> 通过logcat查看 </p>

![](/img/install-androidthings-16.png)
<p style="text-align: center;"> 通过路由器查看连接 </p>

---

有任何问题欢迎留言评论。

---

- [INSTALLING OPERATING SYSTEM IMAGES ON MAC OS](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md)
- [Raspberry Pi 3 - AndroidThings](https://developer.android.com/things/hardware/raspberrypi.html#flashing_the_image)

---
