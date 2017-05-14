title: 各类跨平台开发对比
date: 2017-05-11 10:44:03
updated: 2017-05-11
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483729&idx=1&sn=caffc39ece5afa40e36d00f6f0f2c73c
wechatmptitle: 各类跨平台开发对比
categories:
- 工程师技能
tags:
- Xamarin
- Hybrid
- J2Obj
- Native

---

其实之前看到Google Inbox中Android先行，70%的代码使用[j2objc](http://j2objc.org/)的时候，就有对比过这块，昨天微软[将Xamarin Studio 更名为Visual Studio for Mac](https://www.visualstudio.com/zh-hans/vs/visual-studio-mac/?rr=https%3A%2F%2Fcheeaun.github.io%2Fhackerweb%2F)让我重新提起笔，整理之前这块的思路。

<!-- more -->

## Xamarin的现状

<img src="/img/cross-platform-compare-xamarin.png" width="300px">

- 已有140w的开发者
- 基于[Mono](http://www.mono-project.com/): 开源的，基于.NET Framework(2001年第一次发布)的跨平台平台
- Xamarin在被微软收购之前是闭源商业的产品
- 使用C#为所有移动平台创建应用
- natively compiled: 高性能的app
- 在.Net层使用native libraries来跨平台开发

## Xamarin天然的缺陷

- Xamarin Studio免费，但Visual Studio Xamarin专业版付费
- 一些Android/iOS的新的sdk与feature，由于需要等待Xamarin的支持，所以很难在短时间内就使用上
- 无法使用Android与iOS的开源库，只能使用[平台提供的](https://components.xamarin.com/)以及.Net的一些开源库
- 脱离官方支持如Google对Android Studio等的支持、iOS对Xcode等的支持
- 脱离大的社区(如iOS、Android)进入一个小众社区，问题解决等更加困难

## Xamarin的一些优势

- 很多大公司在用: Trello, Slack、GitHub
- 只用C#语言，基于.Net framework创建所有平台的app
- 由于跨平台各类逻辑复用，基于prebuid app快速开启新App的开发: [prebuilt](https://www.xamarin.com/prebuilt)
- 支持Mac(Xamarin IDE)与Windows(Visual Studio)开发
- 允许不同平台定制自己的UI与交互(基于Xamarin.Forms统一开发，也可以基于Xamarin.iOS与Xamarin.Android分开开发)

## 各类方案对比

#### 技术栈:

- Xamarin: 只需要学习C#，一份代码，一个架构.Net framework + native libraries
- Native: 不同的平台不同的栈
- Hybrid: 只需要学习一种平台开发(JS、H5，CSS)
- J2Obj: 以Android为主，iOS为辅

#### 代码复用:

- Xamarin: 除了UI部分，基于Xamarin.Forms最多96%的的代码复用
- Native: 无代码复用
- Hybrid: 100%代码复用
- J2Obj: 除了UI部分，大部分都可以通过Android先行然后转换到iOS使用

#### UI/UX

- Xamarin: 支持不同平台不同UI/UX(基于Xamarin.Android与Xamarin.iOS)
- Native/J2Obj: 不同平台不同
- Hybrid: 都用相同的

#### 性能

- Xamarin: 好，接近Native，不断在提高让其尽量接近native app的性能， 提供了完整的测试与追踪工具用于应用性能测试: Xamarin Test Cloud 与 Xamarin Test Recorder工具用来运行UI自动测速与性能问题挖掘
- Native/J2Obj: 非常好，平台支持
- Hybrid: 差，基于网页的

#### 硬件支持

- Xamarin: 使用平台特殊的API并且支持连接native library
- Native/J2Obj: Native工具完全支持系统的各类功能
- Hybrid: 可以通过一些第三方的API与插件来支持调用一些硬件但是稳定性无法保证

#### 发布周期

- Xamarin: 开发周期变短但是市场发布依然需要新包
- Native/J2Obj: 市场发布需要新包
- Hybrid: 随时可以部署新特性

#### 社区与支持

- Xamarin/Hybrid: 小众社区、非官方支持、新SDK更新延后
- Native: 大众社区、官方支持
- J2Obj: Android同Native，但是iOS有些社区开源库需要自行转换适配

---

- [The Good and The Bad of Xamarin Mobile Development](https://www.altexsoft.com/blog/mobile/the-good-and-the-bad-of-xamarin-mobile-development/)
- [google/j2objc](https://github.com/google/j2objc)
