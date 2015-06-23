title: Google 2015 Material Design Summit
date: 2015-04-21 04:05:03
tags:
- Codelab
- google
- Android
- 优化
- Material Design

---

> 会议主持人: Michael Yeung

## I. 新制度
#### New Review Process
1. 发布前先人工审核(加速上架时间)
2. 新分级制度(IARC)(5月前没做，就会列入未分级，甚至会被下架或找不到)
    符合不同年龄层的app

    1) 严禁app有root行为; 2) 不能自己升级; 3) 不允许应用内部的应用推荐（必须经过Google Play）
    

## II. 应用质量

#### 该做
- **返回键:** 
    应该回到上个界面 ，上部分返回键(up)可以相同与不同。
    Webview: back button: 返回上一页; up button(通常会更重一些): 返回上一个Activity

- **正确支持ActionBar**
    1) 推荐使用Google主题的 2) 推荐widget用 Android 标准的; 3) TabBar推荐放上面 4) 可以考虑不需要返回键(up); 5) 推荐不用右箭头 6) 不推荐使用弃用的一些UI（如：右下角三点推荐不用, 放在ActionBar右上角(overflow)）

- **参考Android语言风格**
    尽量简短、精简。

- **在Tabs上支持滑动手势**
    强烈建议
<!--more-->


#### 不该做的

- 风格上不该模范平台上的用户体验（应该用Android的标准）
- 不该使用其他平台的图标（应该用: `github`上Google有发布一些通用的图标）
- 不该两个bar都放在下面，（应该分上bar与下bar）(上bar浏览、nav通常是下)
- 不该使用 标记back buttons
- 不应该使用`右箭头`按钮
- 不应该(不建议)使用一些弃用的按钮(如底部的menu button)(Target SDK尽量高)


## III. Android风格演进
- 2011 年 所有Google的应用体验一致 Android(Holo)

- 2014 年 新的Android设计语言 Android(MATERIAL DESIGN)([google.com/design](google.com/design))

 > 获得2014 UX Awards Gold Award Winner
 
 > 宗旨: 界面由电子的纸 z轴叠加而成
 
```
会叠加影子(**android.support.v7.cardview**带有md属性)
高度可能根据交互变化
用影子的深度来诠释当前内容的重要性(如dialog)）
顶部黏合
规范的字体大小、颜色深浅来呈现整体布局
字体大小规范，google有给出建议
字体类型也有建议(英文(**ROBOTO**))
整体排版Android Studio给出排版工具
颜色重要性(primary、primaryDark、accent)
Google Api，给一张图片，会给出几种颜色
有意义的动画（考虑动作的连接性）(交互反馈)(可以有一些调皮的动画(取悦用户))
```

## IV. Links
 
- [Google Design](http://google.com/design)
- [Google Developers Share Video](youtube.com/GoogleDevelopers)
- [Android API](http://developer.android.com)
- [Google Android Developers Blog](android-developers.blogspot.com)
- [The Google I/O 2014 Android App](github.com/google/iosched)
- [Instagram with Material Design concept is getting real - The Summary](http://frogermcs.github.io/Instagram-with-Material-Design-concept-is-getting-real-the-summary/)

## V. Codelab

Github: [https://github.com/Jacksgong/Sunshine(Material Design 教程)](https://github.com/Jacksgong/Sunshine)