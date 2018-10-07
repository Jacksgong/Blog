title: 小米VR一体机投屏到电脑
date: 2018-10-07 14:02:03
updated: 2018-10-07
categories:
- VR
tags:
- VLC
- 小米VR一体机
- Oculus
- VR

---

{% note info %} 原理比较简单是基于ADB的`screenrecord`指令以及VLC的持续对输入流的解码展示，最终的效果是能够在Window或者Mac上进行投屏小米VR一体机，并且支持缩放操作。该教程同样适用与Oculus Go{% endnote %}

<!-- more -->

![](/img/xiaomi-vr-standalone-to-pc-1.png)

## 准备

1. 下载[VLC](https://www.videolan.org/vlc/index.html)到电脑上
2. 在电脑上配置ADB环境
3. 参照[小米VR官方教程](https://dev.mi.com/console/doc/detail?pId=815)开启小米VR的开发者模式，大概如下: 打开小米VR App，“我的”页面→设置→关于帮助，在关于帮助页面有一个小米VR 的logo，连续点击logo5次为开启/关闭开发者模式。（默认关闭开发者模式，开启开发者模式需要使用开发者账号登录，并且确保一体机和手机均连接网络）

## 有线投影

在完成准备工作后，通过数据线，将小米VR一体机连接电脑(ADB也是支持通过wifi连接的，收到无线信号的影响会比有线慢一些，后文会提到)。

### Windows电脑

打开CMD在命令行中输入:

```
adb exec-out "while true; do screenrecord --bit-rate=8m --output-format=h264 --time-limit 180 -; done" | "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" --demux h264 --h264-fps=60 --clock-jitter=0 --network-caching=100 --sout-mux-caching=100 -
```

### Mac电脑

打开Terminal在命令行中输入:

```
adb exec-out "while true; do screenrecord --bit-rate=8m --output-format=h264 --time-limit 180 -; done" | "/Applications/VLC.app/Contents/MacOS/VLC" --demux h264 --h264-fps=60 --clock-jitter=0 --network-caching=100 --sout-mux-caching=100 -
```

### 特别说明

- 命令中的`--bit-rate`是指定比特率，单位为Mbps，值越大质量越高，但是可能会带来更高的延时
- 命令中的`path-to-VLC`是电脑上的VLC应用的地址

输入指令后就会打开VLC显示投影内容了。

## 无线投影

在开始无线投屏之前，我们需要通过有线先开启VR一体机中adb对某个端口的监听。

先将VR一体机连接到电脑，通过`adb shell ip route`获取当前VR一体机在局域网中的IP地址，如:

```
$ adb shell ip route
192.168.99.0/24 dev wlan0  proto kernel  scope link  src 192.168.99.177
```

其中的`192.168.99.177`就是当前一体机在局域网中的IP地址。然后输入`adb tcpip 5555`，以此在VR一体机中开启一个adb服务监听`5555`端口的连接。

此时，可以将数据线断开了。

接下来你需要确保PC与小米VR一体机在同一个局域网，然后通过:

```
adb connect <一体机的IP地址>
```

此时完成连接，最后再参照有线投影中的命令就可以完成投影了。

## 缩放

如果你想要放大某个区域，可以通过VLC的功能来进行放大:

- **Windows用户:** 在VLC中，Tools > Adjustments and Effects > Video effects，然后选中 Interactive Zoom
- **Mac 用户:** 在VLC中，Windows > Video Effects > Geometry，然后选中Magnification/Zoom

然后就可以通过调整左上角小图上的区域来选择需要放大的区域了:


![](/img/xiaomi-vr-standalone-to-pc-2.png)



---

- [How to Screen-Mirror and Record the Oculus Go’s Screen Onto a PC/Mac](https://pixvana.com/sharing-your-oculus-go-screen-on-your-laptop/)
