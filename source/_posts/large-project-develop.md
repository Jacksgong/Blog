title: Android大项目开发
date: 2017-03-01 12:48:03
sticky: 4
categories:
- 架构
tags:
- Android
- 开发流程
- Architecture
- Decoupling

---

## I. 开发流程

### 1. 代码风格与质量

##### 统一风格自动审查

在提交Review之前，可以借助IDEA的审查功能(`Inspect Code`)，制定一致自动审计风格，保证远端代码质量的一致性。并且之后在代码提交远端以后，CI系统再跑一次统一风格的审计，避免落网之鱼。

<!-- more -->
##### Unit Test

在大项目中的单元测试尤为重要，避免代码裸奔，还可以结合Android Studio顺便做代码覆盖，目前Android的单元测试社区已经十分成熟活跃，可以参考[Android单元测试与模拟测试](https://blog.dreamtobe.cn/2016/05/15/android_test/)，在提交Review之前，先本地强制跑过相关代码的单元测试(推荐使用[Facebook phabricator的Arc Diff](https://www.phacility.com)便于这块流程配置)

### 2. 版本管理

#### Review

代码的Review是十分的必要的，通常我们需要在提交Review前，自己先Review修改，然后在提交给相关人员Review(推荐使用[Facebook phabricator的Arc Diff](https://www.phacility.com)便于这块流程配置)，需要尽可能的保证以下规范:Gk

- 尽量细的提交，保证代码尽可能的可追溯
- 如果多个Commit一起提交Review时，尽量保证相关性，以及可拆分性

#### Commit Message Convention

优秀统一的Commit Message Convention可以带来几大好处:

- 代码可追溯
- Commit类型与目的辨识度高
- 发布版本时，修改点一目了然，甚至可通过脚本自动生成

因此作为大团队，优秀的统一的Commit Message Convention是十分必要的，推荐采用[AngularJS's commit message convention](https://github.com/angular/angular.js/blob/master/CONTRIBUTING.md#-git-commit-guidelines)，官方地址: https://angularjs.org/ ，效果可以参考: [这里](https://github.com/Jacksgong/JKeyboardPanelSwitch/commits/master)

#### Git Flow

清晰的Git Flow可以带来几大好处:

- 减少多团队协作带来错误的代码覆盖、冲突处理等问题
- 整个团队提交有规矩可寻，使得每个提交井然有序
- 清晰明辨统一的提交规范使得可追溯性明显的提高

目前业界比较常见的Git Flow主要为两种:

- 一般工具(如Source Tree)提供的Git Flow: 这种流主要是规范比较细，相对繁琐，但是十分稳定，作为版本发布项目开发中可以考虑使用: 保障了`master`分支的稳定性，`develop`分支的灵活性与机动性，除了开发过程中，相互不影响的`feature`分支，还有结合发布场景，发布时提测时的`release`分支、发布后`master`分支打的版本TAG，出现问题的`hotfix`分支，使得整个版本流程都在可控范围，但是为了保障整个流的干净与稳定，长期开发的`feature`分支需要定期rebase`develop`分支，并且在merge回`develop`分支前，必须要rebase`develop`分支，使得操作起来略显繁琐，推荐参考[这里](http://datasift.github.io/gitflow/IntroducingGitFlow.html)
<img src="/img/large-project-develop-1.png" width="400px">
- Github Flow: 这种流兴起于Github与GitLab，十分简单清晰，是持续开发的一种流，因为一旦`feature`开发完，便直接merge回`master`分支了，大型项目如果使用GitLab，结合PR可以很好接入，但是可能需要结合场景对该流规范进行进一步规范，以保证`master`分支的稳定性
<img src="/img/large-project-develop-2.png" width="400px">


### 3. 可持续开发

#### 定期打包

结合各类可持续开发系统(如: Travis-CI、Gitlab-CI等)，可以定制tag-build、daily-build、feature-build进行以下检测:

- CI系统的规范性检查，包差异检查、安全检查等(这块检测数据，可以参考[360手机卫士 Android开发 InfoQ视频 总结](https://blog.dreamtobe.cn/2015/03/17/360%E6%89%8B%E6%9C%BA%E5%8D%AB%E5%A3%AB-Android%E5%BC%80%E5%8F%91-InfoQ%E8%A7%86%E9%A2%91-%E6%80%BB%E7%BB%93/))
- 测试人员尽快接入release包

#### 提交/Review绑定需求

需求任务管理可以采用: [Facebook phabricator - T5132](https://secure.phabricator.com/T5132)或者[GitLab/GitHub的Closing issue via commit message](https://help.github.com/articles/closing-issues-via-commit-messages/)，支持识别Commit Message中的关键字:

- 让任务需求可以直接绑定到对应的Commit，十分便于定位问题
- 在Commit提交远端以后，可以通过Commit Message上面的关键字操作对应的任务状态

#### 修改消息同步

- 可以通过GitLab-CI与Slack的Web hook，在有任务被提交到远端的时候通知到对应的频道，便于协同开发时修改点被同步到。
- 可以通过编写脚本，在CI系统打包完成以后，整理这次打包距离上一次打包的Commit Messages(此时如果采用了统一的Commit Message规范，就可以直接生成Change Log)，以及其他(如: 包大小变化)数据到相关频道
- 可以配置CI系统，在远端打包失败的时候，通过邮箱或通过其他紧急渠道进行通知到

## II. 大项目完全解耦架构

考虑到大的项目体系，特别是项目中的小组数目达到几十个以上时，为了提高每个小组在保证协同工作的效率同时也需要让每个小组能够充分的独立。

该架构的设计宗旨:

- 拆分大型模块，各模块符合开发流程却保证独立开发
- 符合社区标准，利于哺乳社区与反哺社区
- 优秀组件快速转变成公用组件
- 尽量轻量，严格的性能监控
- 严谨的架构扩张
- 严格、行而有效的开发流程
- 对上层尽量无感知，将学习成本降到最低，减少整合门槛

![](/img/large-project-develop-3.png)

其中的api与impl的打包可以参照[gradle-sample](https://github.com/Jacksgong/gralde-sample)。

---

- [本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/large-project-develop.md)。

---

本文已经发布到JackBlog公众号: [Android大项目开发 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483691&idx=1&sn=a1fef6b8842b63b99457afe552a70654)

---

- [Git Flow vs Github Flow](https://lucamezzalira.com/2014/03/10/git-flow-vs-github-flow/)

---
