title: SVG矢量预研期总结
date: 2015-02-04 08:35:03
permalink: 2015/02/04/SVG矢量预研期总结
tags:
- svg
- 总结
- Android

---

- 目前的现状：

	SVG能够在大小上、画质上对Apps进行优化，但是在解析效率上以及对各种图片的支持上是需要接下来持续优化的。

<!--more-->
- SVG代码特征：

	目前已有的几个库中，Android-SVG这个库支持的元素、属性最多，但是在效率上却不是最快的（大约90%的时间消耗在了解析SVG文件上），而虽然SVG-Android-JNI这个库在支持方面略有不足，如不支持阴影、不支持渐变，甚至很少的常见元素都不被支持，但是在效率方面却远领先于其他库，也是最接近RESOURCE库的，因此预计作为后期对SVG库开发的基础或参考。

	目前已有库的总体运行有两个步骤：（1）解析、（2）渲染

- 对Apps的影响

	(1) 提高清晰度，在所有屏幕分辨率上都能完美显示。

	(2) 安装包在大小上能够得到一定的缩减，主要来源于SVG XML格式的压缩

	(3) 初步评估在性能上，总体体验上可接受，但是可能在性能上存在潜在的风险，如一些过于复杂的图片加载时间过长可能会造成体验上的损失，需要在实施时考虑解决方案进行风险规避，可以考虑对加载时间进行监控

- 改进优化的空间：

	对于支持来说，是后期一个持续加入的过程，对于效率我们有下面一些考量：

	(1) 多中间格式的支持，SVG文件格式为XML，而对XML的解析效率其实是解析耗时的一个瓶颈，我们可以考虑直接支持更多更高效序列化、反序列化的中间格式的解析。

	(2) 目前Android-SVG库，在渲染方面表现出色，可以考虑，在解析部分借鉴SVG-Android-JNI的解析，而在渲染上对Android-SVG进行借鉴

	(3) 考虑实现一个体积更小、便于使用、同时不损失开发效率的库和调用框架，这点对于我们同样重要。

 经过前期对SVG的预研，矢量图在对任意屏幕的完美支持正是我们所需要的，同时SVG资源文件在打包过程中，经过压缩使得资源文件大小上能够得到优化，，而目前耗时上，大约在RESOURCE加载资源图片的3〜8倍之间不等。经过初步评估，资源图片（通常在100x100左右）加载时间大多在2~4毫秒，SVG的加载预计将在一个大体可接受的范围（也就是实际体验不会感知到区别）。最后目前Parser＋Render的解析方式还存在一定的优化空间，相信可以使SVG的效率得到进一步提升。

总的来说，好多于坏，值得研究与引入。




# 详细过程

## 1 主要考量
- 可行性
- TTF/SVG选择
- 与现存Android.getDrawable对比
- 预计对Apps的影响

## 2 可行性
其实在网页重构等领域已经被大量的使用，在终端上一般图片实现矢量量化的其实并不多。但就目前Android端分辨率越来越丰富，分辨率越来越高来说，这是一个不错的方向。

目前终端上实现矢量图的表达载体有`TTF`与`SVG`，两者在终端上的应用，在业界已经有了一定的基础，并且对于美工来说都有办法实现让图片转为对应载体的方法，因此可以作为选择对象。

## 3 TTF/SVG选择
### 3.1 TTF的淘汰
对于TTF而言其实Android自身就是支持的，只是我们需要将TTF转换为对应的Drawable，作为Drawable来使用，但是这其实也不是难点，因为业界已经有不少开源的TTF转为Drawable的库可供参考（如我们做比较的时候选用的iconfont），并且效率方面与Resource.getDrawable相当，甚至更快。

但是相比SVG而言TTF只支持单一颜色（其实在网页端已经有人通过z轴绝对坐标叠加的方法实现(http://css-tricks.com/stackicons-icon-fonts/)，但是考虑到周期、效率等因素没有再做深究，可做学习），并且对于美工而言，编辑起来没有SVG方便。因此最终决定以SVG的方向进行研究。
### 3.2 SVG现状
- 同所有矢量图一样，在所有大小分辨率屏幕上都能完美呈现图片。
- Android端一张图片只需要一个SVG文件即可
- 对于SVG而言修改透明度等可以对一张SVG进行复用（如一般的点击效果其实只是颜色的改变）
- SVG文件大小与图片尺寸无关只与图片复杂度有关
- 目前已经有了很多开源SVG解析、渲染库可供学习、借鉴
- 对于美工而言SVG有很多成熟的编辑软件(如:Sketch、Illustrator、Inkscape work等)
- 相比TTF，SVG理论上可以呈现任意复杂度图片
- 目前海外的部分Android应用已经开始使用SVG

### 3.3 参与研究预言SVG库
库名称 | 地址 | 补充说明 | 支持表现 | Licenses
-|-| - |
Android-SVG | https://code.google.com/p/androidsvg/ | 代码结构清晰，支持元素较多，速度中，纯Java实现 | 一般图片支持良好，阴影不支持、渐变支持 | Apache License 2.0
SVG-Android-2 | https://code.google.com/p/svg-android-2/ | 速度慢，纯Java实现 |一般图片支持不好，阴影不支持，渐变不支持 | Apache License 2.0
SVG-Android-JNI | https://code.launchpad.net/~pltxtra/libsvg-android/main | 速度快，C++实现 | 一般图片支持一般，阴影不支持、渐变不支持 | Simplified BSD Licence, GNU GPL v3, GNU LGPL v2.1, GNU LGPL v3, MIT / X / Expat Licence
SVG-Android-AGG | http://www.antigrain.com/svg/index.html | 速度一般，C++实现，使用了AGG主要是让SVG更平滑 | 一般图片支持一般，阴影不支持、渐变不支持 | GNU GPL v3

**TIPS: 目前这些库的运行都可拆解为：解析SVG xml文件->目标对象->渲染->Drawable/Picture/Bitmap**

## 4 与现存Android.getDrawable对比
### 4.1 效率
对于效率，我们经过了比较多的对比来呈现，并且预演几个预计参考库的耗时点。

#### 结论

**TIPS: 目前来说在96px*96px这个级别的图片上，考虑进行参考开发的库解析，渲染的耗时是目前Android.getDrawable的3~8倍.但是在如480px*480px并且简单的大图片上，我们的解析，渲染的耗时小于等于Android.getDrawable的耗时**

![](/img/svg-s-1.png)

![](/img/svg-s-2.png)

#### 对比数据细节

**Tips: 我们举其中几组数据作为说明**

##### (1) 朋友圈(96px*96px)图标:

![](/img/svg-s-sns.png)

###### 数据

库名称 | 平均值 | 最大值 | 最小值 | 变异系数
-|-|-|-|-|
SVG-Android | 68.8 | 89 | 44 | 0.2755
SVG-Android-2 | 103.9 | 156 | 71 | 0.2897
SVG-Android-JNI | 14.2 | 29 | 5 | 0.4633
Resource.getDrawable | 2.5 | 4 | 2 | 0.2828

![](/img/svg-s-line-1.png)

##### (2) 手机(480px*480px)图标:

![](/img/svg-s-phone.png)


###### 数据

库名称 | 平均值 | 最大值 | 最小值 | 变异系数
-|-|-|-|-|
SVG-Android | 55.8 | 68 | 35 | 0.2310
SVG-Android-2 | 55.5 | 63 | 44 | 0.1089
SVG-Android-JNI | 15.2 | 25 | 9 | 0.3205
Resource.getDrawable | 36.3 | 55 | 23 | 0.2742

![](/img/svg-s-line-2.png)

##### （3）多图比较(96px*96px)图标：

![](/img/svg-s-call.png)

![](/img/svg-s-nearby.png)

![](/img/svg-s-qq.png)

![](/img/svg-s-scan.png)

![](/img/svg-s-shake.png)

![](/img/svg-s-sns.png)


###### 数据

库名称 | 平均值 | 最大值 | 最小值 | 变异系数
-|-|-|-|-|
SVG-Android | 196.7 | 246 | 162 | 0.1274
SVG-Android-2 | 362.9 | 425 | 319 | 0.0811
SVG-Android-JNI | 33.4 | 51 | 17 | 0.3296
Resource.getDrawable | 12.3 | 22 | 6 | 0.4757

![](/img/svg-s-line-3.png)

### 4.2 文件大小

#### SVG的大小相比栅格图像特性主要体现在以下几点：
- SVG文件是xml格式，在打包时支持压缩，而栅格图像在apk打包时已经不能再被压缩。
- SVG文件只需要一份，就可以适配所有屏幕，并且可以在代码中修改其特性就可以得到更多复用，而栅格图像为了保证一定程度上的清晰度，需要分别提供多张不同倍数的图片。
- SVG文件大小只和图片的复杂程度有关与图片尺寸大小无关（正是这个原因，在一些复杂的小图上才出现栅格图像更小的情况，但往往相差不大）。

#### 取一些Apps常用大小与复杂度切图对比（⚠这里只是单张图片对比）：
NAME | PNG | SVG | PNG SIZE | 图片元素个数 | 图片元素深度
-|-|-| - |-|
cell phone | 2kb | 2kb | 96px*96px | 7 |3
near friend | 2kb | 3kb | 96px*96px | 9 | 4
qq | 2kb | 2kb| 96px*96px | 7 |3
scaner | 2kb | 3kb| 96px*96px | 7 | 3
shake | 3kb | 4kb| 96px*96px | 14 | 4
sns | 5kb | 3kb| 96px*96px | 15 | 4
mobile | 8kb|2kb| 480px*480px | 9 | 3

### 4.3 清晰程度
SVG完胜栅格化图片形式

## 5 预计对Apps的影响
### 5.1 前期预计适用范围
预计前期不支持部分如下：

不适用项目 | 支持情况 | 原因
-|-|-|
.9图|暂时不做支持 | 暂时SVG没有对.9图进行支持，如果需要后期会引入自定义规则
.jpg图片|暂时不做支持|由于在Apps中看到的.jpg图片大多是图片复杂，并且模拟现实场景的图片
.gif图片|暂时不做支持|由于在Apps中看到.gif都是兔斯基带动画帧率的图片
一部分模拟实物的图片|暂时不做支持|由于构图较为复杂，对于美工来说要把实物图转换为一条一条线的SVG图片工作量较大
带有阴影的图片|暂时不做支持|目前Apps中采用阴影的图片不多，并且根据@koalaliang提供Apps以后会减少对阴影的使用（目前以扁平化作为基础的一方面）

其余部分为适用范围。

### 5.2 优点

（1） 目前已经出现2k屏幕，如果需要让Apps在这样屏幕的手机上很好的显示，就需要xxxhdpi，用更大倍数的栅格图像来填充这个需求，未来可能还会有更大分辨率的手机，因此在这个角度考虑，SVG的引入是十分必要的。

（2） 参考某App中（解压缩RB6.1的apk）所有的图片情况如下:

项目 | 个数 | 所占大小
-|-|-|
所有图片 | 2700 | 7.7MB
.9图 | 721 | 1.3MB
.jpg | 45 | 856kb
.gif | 16 | 703kb
预计第一期不支持的剩余png图片| 666 | 2.2MB

目前而言，我们预计第一阶段，不对.9图支持，以及部分较复杂图片支持（如包含阴影、包含模拟实物的图片），因为可进行替换成SVG的图片情况如下：

 个数 | 所占大小
 -|-|
 2700-721-45-16-666 = 1252 | 7.7MB - 1.3MB - 856kb - 703kb - 2.2MB = 2.68MB

 大小可压缩比较:
 虽然从4.2文件大小对比来看，其实在App大多数图片都是小图的情况来看，对于单张图片从栅格图像转为SVG而言并没有多少的压缩，二者是差不多大的。

 对于jpg、png、gif等栅格图像而言，在打包应用时是得不到压缩的：

![](/img/svg-s-file-1.png)

 但是对于xml的压缩，在打包时，根据xml大小可以压缩2/3，甚至更多的大小：

![](/img/svg-s-file-2.png)

 一般的xml压缩:

![](/img/svg-s-file-3.png)

（3） App在任意屏幕下都得到完美适配（对后期需求需要做到全局大小调整也可以得到很好的助攻）
### 5.3 缺点
（1） 就目前而言，Apps中大多数的资源图片都是96px*96px甚至更小的小图，在资源加载速度方面预计会比目前慢3~8倍。

（2） 对于后期维护以及使用来说，无论如何SVG都是引入新的框架，都需要大家耗费时间去熟悉以及使用。

（3） 目前的库来说都没有对SVG所有元素得到支持，一些甚至是只支持了少数很常见的元素，都需要后期去拓展，比如预计作为开发参考的JNI库，虽然效率很高，但是由于不支持`linearGradient`与`radialGradient`元素，因此还不支持渐变。




## 拓展链接
1. [SVG-Android库 深入浅出 解析篇](http://blog.dreamtobe.cn/2014/12/10/SVG-Android库-深入浅出-解析篇/)
2. [SVG Android应用探究之路 【一】](http://blog.dreamtobe.cn/2014/11/08/SVG-Android应用探究之路/)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
