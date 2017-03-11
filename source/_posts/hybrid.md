title: Hybrid Apps
date: 2016-01-20 20:45:03
permalink: 2016/01/20/hybrid
categories:
- Html5
tags:
- platform
- hybrid
- phoneGap

---
#### Native app

> 主要问题: 平台局限性，迭代不够灵活，开发代价高

- 平台局限性
- 更好的兼容性与UI适配与更好的用户体验

<!-- more -->

#### Hybrid app

> 主要问题: 用户体验

- 无平台界限
- 更小的开发代价(时间/经费/人员)
- 迭代更加灵活

---

> 推荐辅助开发工具[Adobe PhoneGap](http://phonegap.com/)

## 使用PhoneGap创建demo简要说明

> 先安装[桌面端](http://docs.phonegap.com/getting-started/1-install-phonegap/desktop/)与[手机端](http://docs.phonegap.com/getting-started/2-install-mobile-app/)

![](/img/hybrid-1.png)

> 将底部的ip与端口输入手机端，点击`Connect`进行连接即可(仅可以与一个项目进行连接)。

![](/img/hybrid-2.png)

#### 编辑与开发

> 选用适合自己的编辑器(如Atom)到对应的项目中进行编辑即可。

可以参考demo中的`index.html`



```
<!-- 配置是否允许缩放，初始化的缩放比例，允许最大缩放比例，允许最小缩放比例，以及默认的宽度与高度-->
<meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1,
width=device-width, height=device-height, target-densitydpi=device-dpi" />
<!-- cordova.js 来自开源的Apache Cordova项目，用于支持硬件的传感器 -->
<script type="text/javascript" src="cordova.js"></script>
```

---

- [创建demo应用文档](http://docs.phonegap.com/getting-started/3-create-your-app/desktop/)
- [创建demo应用视频](https://www.youtube.com/watch?v=pggw-9b8RVY)
- [demo中代码说明](http://docs.phonegap.com/develop/hello-world-explained/)

---

- [Difference Between Native vs Hybrid Android App Development](http://www.multidots.com/difference-native-vs-hybrid-android-app-development-2/)

---
