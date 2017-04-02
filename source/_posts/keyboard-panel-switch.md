title: Android键盘面板冲突 布局闪动处理方案
date: 2015-09-01 13:35:03
updated: 2015-09-01 13:35:03
permalink: 2015/09/01/keyboard-panel-switch
categories:
- 开源项目
tags:
- 优化
- Android
- 键盘
- 面板
- 闪动
- 布局
- 项目

---

> 已开源 [JKeyboardPanelSwitch](https://github.com/Jacksgong/JKeyboardPanelSwitch)

- [版本迭代日志](https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/CHANGELOG.md)
- [中文说明文档](https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/README.md)
- [问题讨论区](https://github.com/Jacksgong/JKeyboardPanelSwitch/issues)

<!-- more -->

---

> 起源，之前在微信工作的时候，为了给用户带来更好的基础体验，做了很多尝试，踩了很多输入法的坑，特别是动态调整键盘高度，二级页面是透明背景，魅族早期的Smart bar等, 后来逐一完善了，考虑到拥抱开源，看业界还是有很多应用存在类似问题。就有了这个repo

---

> 之前有写过一篇核心思想: [Switching between the panel and the keyboard in Wechat](http://blog.dreamtobe.cn/2015/02/07/Switching-between-the-panel-and-the-keyboard/)。

## 简述所解决问题

当键盘与面板切换的时候，由于在不同的Window上面，布局发生闪动。

## 特征

- 覆盖正常主题。
- 覆盖透明主题。
- 覆盖透明状态栏主题。
- 覆盖`Activity`、`FragmentActivity`、`AppCompatActivity` 布局情况。

## Demo

![](/img/keyboard_pannel_switch-demo_snapshot.jpg)

![](/img/keyboard_pannel_switch-non-fullscreen_resolved.gif)![](/img/keyboard_pannel_switch-fullscreen_resolved.gif)
![](/img/keyboard_pannel_switch-adjust_resolved.gif)![](/img/keyboard_pannel_switch-adjust_unresolved.gif)

---
