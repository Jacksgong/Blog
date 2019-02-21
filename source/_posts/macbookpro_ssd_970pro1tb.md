title: MacBook Pro 自行升级SSD 固态970 Pro 1TB 碾压原厂
date: 2019-02-21 02:21:03
updated: 2019-02-21
wechatmpurl: https://mp.weixin.qq.com/s/2HEz_GNfjCx8DHGuCOuWhg
wechatmptitle: MacBook Pro 读写速度稳定翻倍 一毛没花还赚了100元!
categories:
- 硬件
tags:
- MacBookPro
- SSD

---

{% note info %} 我的Macbook Pro是15款的顶配，512G的固态，原本就有计划想要升级下，因为一些大项目的开发对硬盘的读写要求还是很高的，但是一直都是观望状态，直到一次偶然的机会在闲鱼以极地的价格入了970 Pro 1TB，换上后各项速度碾压原厂。{% endnote %}

<!-- more -->

## I. 写在前面

原本还在纠结是否要买860EVO，主要是肉疼，没想到刷闲鱼居然刷到全新三星970Pro 1TB只要1200，简直不敢相信，再三确定后直接秒了。。

不过秒了以后对方才反应过来是不是卖便宜了，也怪不了卖家，谁让是朋友送她这礼物，她也不懂，不过最后我还是多补了她300元，1500拿下，算了下，我原装512G的那个后面卖了估计都不止卖1500了，果断下单:

![](/img/macbookpro-ssd-970pro1tb-1.png)

不过也不全是捡便宜，对方这个是在美国买回来的无法享受国内保修，这个对我来说影响不大。顺丰还是比较给力的，第二天就到货了:

![](/img/macbookpro-ssd-970pro1tb-3.png)

真是香啊~~

在装机之前，我跑了下现在MacBook Pro原装512G SSD的速度数据(P.S 忘记截图了，速度与下图网友提供了差不多):

![](/img/macbookpro-ssd-970pro1tb-4.png)

OK，接下来我们就要开始换SSD了。

## II. 准备启动盘

首先需要先准备一个启动引导盘，毕竟整个硬盘都换了，大家可以直接参照[这个教程](https://support.apple.com/zh-cn/HT201372)，十分简单，大致如下:

先参照[这里](https://support.apple.com/zh-cn/HT201475)在App Store中下载macOS Mojave:

![](/img/macbookpro-ssd-970pro1tb-5.png)

下载好后，会在`/Application`中多出一个`Install macOS Mojave.app`大概是4G左右。然后你插入一个可以进行格式化的U盘，然后在终端执行:

```
sudo /Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
```

> P.S. 后面的那个`MyVolume`修改为你的U盘的分区名称即可

不过如果你对命令不熟悉，推荐直接下载[DiskMaker X](https://diskmakerx.com/)，使用这个工具的话，在下载完`macOS MoJava`后，直接打开，一路确定下一步即可，十分傻瓜。

准备好启动盘后，接下来就是拆机替换了。(P.S. 如果确保数据不丢失，此时先对原有数据此时可以通过TimeMachine进行备份。)

## III. 拆机替换

这块拆机我录制了视频:

<iframe src="//player.bilibili.com/player.html?aid=44216236&cid=77431757&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="100%" height="500px"> </iframe>

在拆机之前，这边需要先准备5星螺丝刀与6星的螺丝刀(淘宝上有卖很便宜几元钱一套MacBook维修的)，分别用户拆背盖与SSD固定螺丝。还有一点是我们会发现三星970 Pro的接口是M.2，这边我们需要在网上再买一个转接口，大概20元左右，在淘宝上搜索`macbook ssd 转接`还是很多的，随便买一个即可。

![](/img/macbookpro-ssd-970pro1tb-6.png)

拆下背盖后我们会发现SSD固定就只有一个螺丝:

![](/img/macbookpro-ssd-970pro1tb-7.png)
![](/img/macbookpro-ssd-970pro1tb-8.png)

用6星螺丝刀旋下这个螺丝后便可向左抽出了，我们放在桌面与970 Pro 1TB对比下:

![](/img/macbookpro-ssd-970pro1tb-9.png)

然后我们将转接头接上970 Pro，然后同样的方法装到主板上，旋上螺丝，大功告成!

![](/img/macbookpro-ssd-970pro1tb-10.png)
![](/img/macbookpro-ssd-970pro1tb-11.png)

盖上背盖，锁上螺丝搞定。接下来我们使用引导安装系统即可。

## IV. 使用引导安装macOS MoJava

这边插上刚刚制作的引导盘后，开机即可，默认就会进入引导。

进入引导后这边我们需要先使用磁盘工具对其'抹掉'以完成970 Pro的初始化:

![](/img/macbookpro-ssd-970pro1tb-12.png)

初始化后，我们此时选择安装后就可以选择安装到这里了:

![](/img/macbookpro-ssd-970pro1tb-13.png)

选择安装后，等待就可以啦！

![](/img/macbookpro-ssd-970pro1tb-14.png)

进度条完成后，就搞定进入系统啦！（P.S. 可以选择在进入系统的时候通过TimeMachine恢复刚刚备份的TimeMachine数据即可还原几乎所有的配置与文件）

## V. 进入系统

进入系统打开关于本机，你会发现已经大功告成啦:

![](/img/macbookpro-ssd-970pro1tb-15.png)

此时我们再跑下速度:

![](/img/macbookpro-ssd-970pro1tb-16.png)

爽！简直碾压，紧接着拆装下来的这个闲鱼上挂个1600，算了下换了970 Pro还赚了100元，哈哈哈哈哈。

## VI. 体验情况

整体用下来，我没有遇到任何无法休眠的问题，包括散热等都很正常，各方面十分稳定，并且电池电量依然可以使用10h以上，没有什么压力。至少到目前用了4天下来各方面还是十分稳定，对一些大项目开发以及编译这些对SSD读写要求较高，包括通过Final Cut Pro编辑视频都有较为明显的提升，总之目前还是很爽的。
