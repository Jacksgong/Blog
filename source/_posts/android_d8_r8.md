title: Android新Dex编译器D8与新混淆工具R8
date: 2017-08-13 22:50:03
updated: 2017-08-13
categories:
- Android编译
tags:
- Dex
- Proguard
- D8
- R8
- Android


---

{% note info %} 将`.class`自己码转化为`.dex`字节码作为Apk打包的关键步骤，Google打算在Android 3.0中引入D8作为原先Dex的升级版，以及R8作为原本Proguard 压缩与优化（minification、shrinking、optimization)部分的替代品。{% endnote %}

<!-- more -->

## I. D8

D8目前还在preview阶段，不过Google Android团队测试了多款应用结果都是很不错的，因此他们很有信心将D8编译器引入到AOSP中，预计会在接下来的几个月中对其进行Release，如果你使用中有遇到任何问题可以到[这里](https://issuetracker.google.com/issues/new?component=317603&template=1018721)给他们提。

### 1. D8优化部分

- Dex编译时间更短
- `.dex`文件大小更小
- 相同或者是更好的运行时性能

根据Google Android团队对[这个项目](https://github.com/jmslau/perf-android-large/tree/android-30)进行分别使用Dex与D8的测试数据:

![](/img/d8-r8-1.png)
![](/img/d8-r8-2.png)


### 2. D8的使用

> 已经在[Android Studio 3.0 Beta release](https://developer.android.com/studio/preview/index.html)中引入

#### Android Studio 3.0

需要主动在`gradle.properties`文件中新增:

```
android.enableD8=true
```

#### Android Studio 3.1或之后的版本

在3.1或之后的版本D8将会被作为默认的Dex编译器。


## II. R8

R8作为原本Proguard 压缩与优化（minification、shrinking、optimization)部分的替代品，依然使用与Proguard一样的keep规则。

目前R8已经开源: [r8/r8](https://r8.googlesource.com/r8)，其包含了D8与R8。

目前R8还没有整合进Android Gradle plugin，不过由于其已经开源，根据文档可以很快的在python环境下运行起来:

1. 确保本地已经安装了python 2.7或更高版本(macOS Sierra自带python 2.7)。
2. 由于R8项目使用chromium项目提供的depot_tools管理依赖，因此先安装[depot_tools](https://www.chromium.org/developers/how-tos/install-depot-tools)
3. Clone R8项目：`git clone https://r8.googlesource.com/r8 && cd r8`
4. 下载一个Gradle版去编译，并且声称两个jar文件: `build/libs/d8.jar`与`build/libs/r8.jar`: `python tools/gradle.py d8 r8`
5. 根据[r8文档](https://r8.googlesource.com/r8)进行使用即可

---

- [Next-generation Dex Compiler Now in Preview](https://android-developers.googleblog.com/2017/08/next-generation-dex-compiler-now-in.html)