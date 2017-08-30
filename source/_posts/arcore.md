title: ARCore
date: 2017-08-30 16:58:03
updated: 2017-08-30
categories:
- Android最佳实践
tags:
- Android
- AR

---

{% note info %}今天Google Android Team突然公布[ARCore](https://developers.google.com/ar/)，这是一款对标苹果的ARKit的一套摄像头AR的解决方案。激动不已的我，终于把持不住，停下手上工作，实验了下..{% endnote %}

<!-- more -->

通过其官网，很欣喜的发现其已经开源: [https://github.com/google-ar/arcore-android-sdk](https://github.com/google-ar/arcore-android-sdk)

## 探究试验

拉下来开源库后，比较出乎意料的是lib居然是一个优化后的aar包，这........

不过还是希望了解下内部，初略看了下，ARCore俨然是对Tango的封装与拓展，各类核心处理还是在Google早年没怎么宣传，并且由于Android碎片化，各类兼容问题，只有几台设计适配了的Tango的NDK来处理。好吧，那跑跑Demo吧，猛然发现虽然官网说明可以运行在各类运行在Android N或者更高版本的Android设备上，但是目前Preview版本只适配了Pixel、Pixel XL与三星S8，并且是在代码中写死的：

```java
private static boolean deviceCalibrationAvailable() {
    return Build.FINGERPRINT.contains("sailfish:7") || Build.FINGERPRINT.contains("sailfish:O") || Build.FINGERPRINT.contains("sailfish:8") || Build.FINGERPRINT.contains("marlin:7") || Build.FINGERPRINT.contains("marlin:O") || Build.FINGERPRINT.contains("marlin:8") || Build.FINGERPRINT.contains("walleye:O") || Build.FINGERPRINT.contains("walleye:8") || Build.FINGERPRINT.contains("taimen:O") || Build.FINGERPRINT.contains("taimen:8") || Build.FINGERPRINT.contains("SC-02J/SC-02J:7") || Build.FINGERPRINT.contains("SCV36_jp_kdi/SCV36:7") || Build.FINGERPRINT.contains("dreamqlteue/dreamqlteue:7") || Build.FINGERPRINT.contains("dreamqltesq/dreamqltesq:7") || Build.FINGERPRINT.contains("dreamqlteldusq/dreamqltesq:7") || Build.FINGERPRINT.contains("dreamqltezm/dreamqltecmcc:7") || Build.FINGERPRINT.contains("dreamqltevl/dreamqltecan:7") || isSupportedExynosDevice();
}
```

好吧，由于手头只有Mi6与Nexus 6P，我选择反射修改`Build.FINGERPRINT`试了下。反射了以后，看了看文档，发现在使用前还需要安装[ARCore Service](https://github.com/google-ar/arcore-android-sdk/releases/download/sdk-preview/arcore-preview.apk)这个APK，看代码lib中并没有带任何`so`，没猜错的话，这些应该都是这个APK提供的。

## 上手体验

安装发现，Mi6在NDK层Crash

<img src="/img/arcore-1.png" width="200px"/>
<center>Mi6上Crash堆栈</center>

不过，Nexus 6P可以运行，不过相比ARKit，ARCore在Nexus 6p上的效果似乎不是很乐观，主要体现在识别速度上（Demo中平面的识别速度)，还有使用ARCore的时候，经常发现摄像头没有对焦，大概效果如下:

<video width="100%" height="480" controls>
<source src="http://ovh3ykgmr.bkt.clouddn.com/arcore-test.mp4">
</video>

## 总结

初步窥探下来，感觉目前来说ARCore还属于Preview，并且从性能、稳定性方面还存在一些问题；适配方面，即便是要适配大多数的Android N或更高版本的设备，估计还是挺大一个问题，毕竟Android有各类奇奇怪怪的手机配置与手机摄像头，不过介于ARKit已经带来了很好的反馈，无论是应对ARKit也好，未来发展也好，相信Google还是会想办法发力与各大手机厂商进行合作支持的。ARCore的进一步发展目前只能是不以待了。

---