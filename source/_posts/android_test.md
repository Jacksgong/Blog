title: Android单元测试与模拟测试
date: 2016-05-15 16:53:03
tags:
- 单元测试
- 模拟测试
- UI测试
- 稳定性
- Android

---

> 测试驱动式编程(Test-Driven-Development)在RoR中已经是非常普遍的开发模式，是一种十分可靠、优秀的编程思想，可是在Android领域中这块还没有普及，今天主要聊聊Android中的单元测试与模拟测试及其常用的一些库。

<!-- more -->

## I. 测试与基本规范

#### 1. 为什么需要测试?

- 为了稳定性，能够明确的了解是否正确的完成开发。
- 更加易于维护，能够在修改代码后保证功能不被破坏。
- 集成一些工具，规范开发规范，使得代码更加稳定( 如通过 phabricator differential 发diff时提交需要执行的单元测试，在开发流程上就可以保证远端代码的稳定性)。

#### 2. 测什么?

- 一般单元测试: 列出想要测试覆盖的异常情况，进行验证。
- 模拟测试: 根据需求，测试用户真正在使用过程中，界面的反馈与显示以及一些依赖系统架构的组件的应用测试。

#### 3. 需要注意

- 考虑可读性，对于方法名使用表达能力强的方法名，对于测试范式可以考虑使用一种规范, 如 RSpec-style。
- 不要使用逻辑流关键字(If/else、for、do/while、switch/case)，在一个测试方法中，如果需要有这些，拆分到单独的每个测试方法里。
- 测试真正需要测试的内容，需要覆盖的情况，一般情况只考虑验证输出（如某操作后，显示什么，值是什么）。
- 考虑耗时，Android Studio默认会输出耗时。
- 不需要考虑测试`private`的方法，将`private`方法当做黑盒内部组件，测试对其引用的`public`方法即可。
- 尽可能的解耦对于不同的测试方法，不应该存在Test A与Test B存在时序性的情况。


## II. Android Studio中的单元测试与模拟测试

> control + shift + R (Android Studio 默认执行单元测试快捷键)。

### 1. 本地单元测试

> 直接在开发机上面进行运行测试。
> 在没有依赖或者仅仅只需要简单的Android库依赖的情况下，有限考虑使用该类单元测试。

#### 代码存储

> 如果是对应不同的flavor或者是build type，直接在test后面加上对应后缀(如对应名为`myFlavor`的单元测试代码，应该放在`src/testMyFlavor/java`下面)。

`src/test/java`

#### 激活测试

在一个功能测试或验证的测试方法前面添加`@Test`的annotation。

#### Google官方推荐引用

```
dependencies {
    // Required -- JUnit 4 framework，用于单元测试，google官方推荐
    testCompile 'junit:junit:4.12'
    // Optional -- Mockito framework，用于模拟架构，google官方推荐
    testCompile 'org.mockito:mockito-core:1.10.19'
}
```

### 2. 模拟测试

> 需要运行在Android设备或者虚拟机上的测试。

> 主要用于测试: 单元(Android SDK层引用关系的相关的单元测试)、UI、应用组件集成测试(Service、Content Provider等)。

#### 代码存储:

`src/androidTest/java`

#### Google官方推荐引用

```
dependencies {
    androidTestCompile 'com.android.support:support-annotations:23.0.1'
    androidTestCompile 'com.android.support.test:runner:0.4.1'
    androidTestCompile 'com.android.support.test:rules:0.4.1'
    // Optional -- Hamcrest library
    androidTestCompile 'org.hamcrest:hamcrest-library:1.3'
    // Optional -- UI testing with Espresso
    androidTestCompile 'com.android.support.test.espresso:espresso-core:2.2.1'
    // Optional -- UI testing with UI Automator
    androidTestCompile 'com.android.support.test.uiautomator:uiautomator-v18:2.1.1'
}
```

#### 常见的UI测试

> 需要模拟Android系统环境。

##### 主要三点:

1. UI加载好后展示的信息是否正确。
2. 在用户某个操作后UI信息是否展示正确。
3. 展示正确的页面供用户操作。

## III. 拓展工具

#### 1. AssertJ Android

> [square/assertj-android](https://github.com/square/assertj-android)
> 极大的提高可读性。

```
// 一般的JUnit
assertEquals(View.GONE, view.getVisibility());
// AssertJ Android
assertThat(view).isGone();
```

#### 2. Robolectric

> [Robolectric](http://robolectric.org/)
> 让模拟测试直接在开发机上完成，而不需要在Android系统上。

主要是解决模拟测试中耗时的缺陷，模拟测试需要安装以及跑在Android系统上，也就是需要在Android虚拟机或者设备上面，所以十分的耗时。基本上每次来来回回都需要几分钟时间。针对这类问题，业界其实已经有了一个现成的解决方案: Pivotal实验室推出的[Robolectric](http://robolectric.org/)。通过使用Robolectrict模拟Android系统核心库的`Shadow Classes`的方式，我们可以像写本地测试一样写这类测试，并且直接运行在工作环境的JVM上，十分方便。

#### 3. Mockito

> [Mockito](https://code.google.com/archive/p/mockito/)
> 快速模拟控制系统架构返回参数。

不同于Roblectric，Mockito可以通过模拟并控制或修改一些方法的行为。

```
// 无论什么时候调用 myQueryObject.getCurrentTime，返回值都会是 1363027600
Mockito.doReturn((long) 1363027600).when(myQueryObject).getCurrentTime();
```

#### 4. Robotium

> [RobotiumTech/robotium](https://github.com/robotiumtech/robotium)
> (Integration Tests)模拟用户操作，事件流测试。

通过模拟用户的操作的行为事件流进行测试，这类测试无法避免需要在虚拟机或者设备上面运行的。是一些用户操作流程与视觉显示强相关的很好的选择。

#### 5. Test Butler

> [linkedin/test-butler](https://github.com/linkedin/test-butler)
> 避免设备/模拟器系统或者环境的错误，导致测试的失败。

通常我们在进行UI测试的时候，会遇到由于模拟器或者设备的错误，如系统的crash、ANR、或是未预期的Wifi、CPU罢工，或者是锁屏，这些外再环境因素导致测试不过。Test-Butler引入就是避免这些环境因素导致UI测试不过。

> 该库被[谷歌官方推荐过](https://www.youtube.com/watch?v=aHcmsK9jfGU)，并且收到谷歌工程师的Review。

## IV. 拓展思路

#### 1. Android Robots

> [Instrumentation Testing Robots - Jake Wharton](https://realm.io/news/kau-jake-wharton-testing-robots/)

假如我们需要测试: 发送 $42 到 "foo@bar.com"，然后验证是否成功。

##### 通常的做法

![](/img/android-test_1.png)

![](/img/android-test_2.png)

##### Robot思想

在写真正的UI测试的时候，只需要关注要测试什么，而不需要关注需要怎么测试，换句话说就是让测试逻辑与View或Presenter解耦，而与数据产生关系。

首先通过封装一个Robot去处理How的部分:

![](/img/android-test_3.png)

然后在写测试的时候，只关注需要测试什么:

![](/img/android-test_4.png)

最终的思想原理

![](/img/android-test_5.png)

---

本文已经发布到JackBlog公众号，可请直接访问: [Android单元测试与模拟测试 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483680&idx=1&sn=a81f0b86696f243bf32c032fc7b09574)

---

- [Building Local Unit Tests](http://developer.android.com/training/testing/unit-testing/local-unit-tests.html)
- [Testing the Android way](https://www.bignerdranch.com/blog/testing-the-android-way/)
- [timber中的单元测试实例](https://github.com/JakeWharton/timber/blob/master/timber/src/test/java/timber/log/TimberTest.java)
- [timber/build.gradle](https://github.com/JakeWharton/timber/blob/master/timber/build.gradle)
- [A BDD (RSpec-like) testing library for Java](http://stackoverflow.com/questions/30675748/a-bdd-rspec-like-testing-library-for-java)
- [Open Sourcing Test Butler](https://engineering.linkedin.com/blog/2016/08/introducing-and-open-sourcing-test-butler--reliable-android-test)


---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
