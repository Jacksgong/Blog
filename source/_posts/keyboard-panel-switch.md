title: Android键盘面板冲突 布局闪动处理方案
date: 2015-09-01 13:35:03
tags:
- 优化
- Android
- 键盘
- 面板
- 闪动
- 布局
- 项目

---

> 起源，之前在微信工作的时候，为了给用户带来更好的基础体验，做了很多尝试，踩了很多输入法的坑，特别是动态调整键盘高度，二级页面是透明背景，魅族早期的Smart bar等, 后来逐一完善了，考虑到拥抱开源，看业界还是有很多应用存在类似问题。就有了这个repo

---

> 之前有写过一篇核心思想: [Switching between the panel and the keyboard in Wechat](http://blog.dreamtobe.cn/2015/02/07/Switching-between-the-panel-and-the-keyboard/)。

<!-- more -->

![][non-fullscreen_resolved_gif]![][fullscreen_resolved_gif]
![][adjust_resolved_gif]![][adjust_unresolved_gif]


## 如何使用

在`build.gradle`中引入:

```
compile 'cn.dreamtobe.kpswitch:library:1.4.1'
```

## 使用引导

- [非全屏主题情况下使用引导](https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/NON-FULLSCREEN_TUTORIAL.md)
- [全屏主题情况下使用引导](https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/FULLSCREEN_TUTORIAL.md)

## 基本原理

- 键盘高度计算，以及键盘是否显示的计算，参看: [KeyboardUtil.KeyboardStatusListener#calculateKeyboardHeight][KeyboardUtil_calculateKeyboardHeight_link]、[KeyboardUtil.KeyboardStatusListener#calculateKeyboardShowing][KeyboardUtil_calculateKeyboardShowing_link]。
- 处理闪动问题，参看: [KPSwitchRootLayoutHandler][KPSwitchRootLayoutHandler_link]，以及如果是非全屏主题用到的面板布局: [KPSwitchPanelLayoutHandler][KPSwitchPanelLayoutHandler_link]；如果是全屏主题用到的面板布局: [KPSwitchFSPanelLayoutHandler][KPSwitchFSPanelLayoutHandler_link]。


## III. GitHub:

[JKeyboardPanelSwitch](https://github.com/Jacksgong/JKeyboardPanelSwitch)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---

[bintray_link]: https://bintray.com/jacksgong/maven/JKeyboardPanelSwitch/_latestVersion
[bintray_svg]: https://api.bintray.com/packages/jacksgong/maven/JKeyboardPanelSwitch/images/download.svg
[fullscreen_resolved_gif]: https://raw.githubusercontent.com/Jacksgong/JKeybordPanelSwitch/master/art/fullscreen_resolved.gif
[non-fullscreen_resolved_gif]: https://raw.githubusercontent.com/Jacksgong/JKeybordPanelSwitch/master/art/non-fullscreen_resolved.gif
[adjust_resolved_gif]: https://raw.githubusercontent.com/Jacksgong/JKeybordPanelSwitch/master/art/adjust_resolved.gif
[adjust_unresolved_gif]: https://raw.githubusercontent.com/Jacksgong/JKeybordPanelSwitch/master/art/adjust_unresolved.gif
[build_status_svg]: https://travis-ci.org/Jacksgong/JKeyboardPanelSwitch.svg?branch=master
[build_status_link]: https://travis-ci.org/Jacksgong/JKeyboardPanelSwitch
[KeyboardUtil_calculateKeyboardHeight_link]: https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/library/src/main/java/cn/dreamtobe/kpswitch/util/KeyboardUtil.java#L197
[KeyboardUtil_calculateKeyboardShowing_link]: https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/library/src/main/java/cn/dreamtobe/kpswitch/util/KeyboardUtil.java#L248
[KPSwitchRootLayoutHandler_link]: https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/library/src/main/java/cn/dreamtobe/kpswitch/handler/KPSwitchRootLayoutHandler.java
[KPSwitchPanelLayoutHandler_link]: https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/library/src/main/java/cn/dreamtobe/kpswitch/handler/KPSwitchPanelLayoutHandler.java
[KPSwitchFSPanelLayoutHandler_link]: https://github.com/Jacksgong/JKeyboardPanelSwitch/blob/master/library/src/main/java/cn/dreamtobe/kpswitch/handler/KPSwitchFSPanelLayoutHandler.java
