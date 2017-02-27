title: 快速集成平滑进度条
date: 2016-05-15 18:50:03
permalink: 2016/05/15/percent_smooth_handler
categories:
- 开源项目
tags:
- android
- Percent
- Progress
- github

---

> 已开源 [Jacksgong/PercentSmoothHandler](https://github.com/Jacksgong/PercentSmoothHandler)

- [版本迭代日志](https://github.com/Jacksgong/PercentSmoothHandler/blob/master/CHANGELOG.md)
- [说明文档](https://github.com/Jacksgong/PercentSmoothHandler/blob/master/README.md)
- [问题讨论区](https://github.com/Jacksgong/PercentSmoothHandler/issues)

<!-- more -->

---

## 简述所解决问题

常见的ProgressBar，或者是一些组件，如果在回调不够频繁或者跨度比较大的时候，就会出现不够平滑的问题。

## 特征

集成这个库，可以非常轻易的继承拓展出 `setSmoothPercent(percent:float)` 与 `setSmoothPercent(percent:float, durationMillis:long)` 接口。

## Demo

![demo gif](/img/percent_smooth.gif)
