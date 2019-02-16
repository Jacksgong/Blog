title: Mac 直播游戏，斗鱼直播，bilibili直播
date: 2019-02-16 16:32:03
updated: 2019-02-16
categories:
- 教程
tags:
- obs
- 直播
- 娱乐

---

{% note info %} 目前其实很少有平台有提供在Mac上进行直播的工具，因此这边不得不依赖一些第三方的工具通过推流的方式进行直播，另外还有是对将手机投屏到电脑上也是一个问题，如何做到流畅，高清呢，今天我们就来解决这些问题。{% endnote %}

<!-- more -->

## 前言

其实各大平台，无论是bilibili、斗鱼还是其他直播平台，国内的大多数都是支持通过开放一个rtmp提供rtmp地址与直播码来进行推流来实现直播的。比如:

![](/img/live-guideline-1.png)
![](/img/live-guideline-2.png)

因此我们只需要有工具将相关的视频流推送到直播平台提供的rtmp即可。

## 推流

这里推流我们使用的是: [OBS Studio](https://obsproject.com/)，这是一款非常好用的推流工具，特别在Mac上，其支持MacOS、Windows、Linux，这里我们直接点击下载MacOS版本:

![](/img/live-guideline-3.png)

下载后直接进行安装，安装后可以在设置中，将语言设置为中文

![](/img/live-guideline-4.png)

然后就是设置我们刚刚提到的`rtmp地址`与`直播码`:

![](/img/live-guideline-5.png)

设置好后，我们可以通过添加来源来添加需要直播的视频流与音频流等。这里我们添加最常见的来源:

![](/img/live-guideline-6.png)

- `视频捕捉设备`: 我这边设置的是前置摄像头
- `音频输入捕获`: 默认的麦克风/Aux输入，其实在混音器中就已经添加了，我这里其实添加的是我音乐播放器的输入，这边使用的是`Sound Siphon`，后面会提到
- `显示捕获`: 这里我设置的就是我的主显示器

全部准备好后，这边直接通过点击右侧的`开始推流`即可(特别需要注意的是通常来说需要在直播网站上先点击开播)

## 手机投屏

这边我试过很多软件，其中包括AirDroid、Vysor等等，AirDroid存在的问题由于使用的是Wifi无线连接不清晰并且卡顿，而Vysor不用说了，由于是付费的，最后我找到了一个更好的解决方案，先看效果:

![](/img/live-guideline-7.png)

免费、高清、流畅、灵活调节大小等等，完全符合需求。

这个工具就是用C写的开源的[Scrcpy](https://github.com/Genymobile/scrcpy)，其在Mac上的安装方法也十分简单，支持直接通过HomeBrew进行安装，具体可以参看[官方的方法](https://github.com/Genymobile/scrcpy#mac-os):

```
brew install scrcpy
```

安装完成后，直接在终端输入`scrcpy`便可以进行使用，各方面的调整(如比率等)也可以通过`scrcpy --help`获得教程


## 播放器的音频流

首先OBS支持添加不同的音频流入来进行混音，我们这边通过前面提到的[Sound Siphon](https://staticz.com/soundsiphon/)进行添加(其付费是需要49刀购买，这边免费可以试用14天)，首先通过[官网](https://staticz.com/soundsiphon/)进行试用下载:

![](/img/live-guideline-8.png)

下载完成后进行，安装后打开:

![](/img/live-guideline-9.png)

打开后，这边添加一个音频输入，选择你的播放器，已经这边对该音频输入进行命名(这边为了便于教程我就命名为(`New Input`))，然后大家在OBJ上的来源添加`音频输入捕获`，此时就会看到你刚刚添加的`New Input`音频输入源了，这个输入源就只包含播放器的音效。

## 写在最后的话

5G时代马上到来，随着流量越来越廉价、视频质量越来越高，再加上AI视频分析技术越来越成熟，视频能够记录的细节也越来越多，要不你也开播玩一玩？

---

- [使用OBS在B站直播（Mac平台）](http://augix.me/archives/5018)
