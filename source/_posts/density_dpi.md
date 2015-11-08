title: Android 切图与标注
date: 2015-11-08 22:35:03
tags:
- 9patch
- density
- densityDPI
- dp
- dpi
- ppi

---

## I. 标注

> 下文中提到的density是指: `DisplayMetrics#density`

> 在显示器设置时，dpi = ppi
> 手机的ppi: 对角线像素点个数px / 对角线英寸inch

<!-- more -->
- dpi(dot per inch): 点/英寸
- ppi(pixel per inch): 像素/英寸

> dp = px /density
> 让设计师给标注的时候，最好是能够给160dpi屏幕上的标注，此时密度是1,px=dp

- dp(Density-independent pixel): 1dp为屏幕点密度为160dpi(density=1)时像素点数: dp = px/(dpi /160 ) = px / density
- dpi(dot per inch): dip = dp
- sp : 一般系统没有特殊配置，sp = dp

> 市面主要的Android手机屏幕尺寸: 5.5寸、5寸、4.7寸、3.7寸


> 这个值并不是非常准确的依据真实的屏幕大小

屏幕分辨率(px) | 宽inch * 长inch | 对角线(inch) | 宽dip * 长dip | 屏幕ppi | density | 标准densityDPI | 默认资源目录 | 常见手机
:-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
240 x 320 | 2.00 x 2.67 | 3.3 | 120 x 120 | 121 | 0.75 | 120 | ldpi | -
240 x 320 | 1.50 x 2.00 | 2.5 | 160 x 160 | 160 | 1 | 160 | mdpi| -
340 x 480 | 1.50 x 2.00 |  2.5| 227 x 240 | 235 | 1.5 | 240 | hdpi | -
480 x 800 | 1.90 x 3.17 | 3.7 | 253 x 252 | 252 | 1.5 | 240 | hdpi | Nexus One
720 x 1280 | 2.3 x 4.10 | 4.7 | 313 x 312 | 312 | 2 | 320 | xhdpi | 红米2A、红米2、美图M4
768 x 1280 | 2.42 x 4.03 | 4.7 | 317 x 317 | 317 | 2 | 320 | xhdpi | Nexus 4
1080 x 1920 | 2.79 x 4.97 | 5.7 | 387 x 386 | 386 | 2.5 | 400 | 400dpi | 小米Note标准
1080 x 1920 | 2.45 x 4.36 | 5 | 441 x 440 | 441 | 2.625 | 420 | 420dpi(api 23才添加api 23前xxhdpi) | 小米3、小米4、小米4c
1080 x 1920 | 2.42 x 4.31 | 4.95 | 446 x 445 | 445 | 3 | 480 | xxhdpi | Nexus5
1440 x 2560 | 2.92 x 5.20 | 5.96 | 493 x 492 | 492 | 3 | 480 | xxhdpi |  Nexus 6
1440 x 2560 | 2.79 x 4.97 | 5.7 | 516 x 515 | 515 | 3 | 480 | xxhdpi |  小米Note顶配，Nexus 6P
- | - | - | - | - | 4 | 640 | xxxhdpi | -


#### Android 取资源原则

如果存在匹配的就取对应文件夹资源，否则取最高清的资源根据density进行缩放。

#### 常用工具

Android Virtual Device Manager

## II. 9patch

> 俗称点9图
> 腾讯ISUX (http://isux.tencent.com/android-ui-9-png.html)

![](/img/density_dpi-1.png)

- 1、2 拉伸区域
- 3、4 内容区域

#### 内容区域作用如下图

> 其中的内容布局是: 垂直居中，水平靠左
> 注意其中3、4的内容区域

![](/img/density_dpi-2.png)

#### 不想被拉伸

> 点在透明区域即可

![](/img/density_dpi-3.png)

---
- [Supporting Multiple Screens](https://developer.android.com/intl/zh-cn/guide/practices/screens_support.html)
- [DPI、PPI、DP、PX 的详细计算方法及算法来源是什么？](http://www.zhihu.com/question/21220154)
- [Android设计中的.9.png](http://isux.tencent.com/android-ui-9-png.html)
- [Dashboards](https://developer.android.com/intl/zh-cn/about/dashboards/index.html)
- [友盟指数](http://www.umindex.com/)
