title: 360手机卫士 Android开发 InfoQ视频 总结
date: 2015-03-17 14:09:03
permalink: 2015/03/17/360手机卫士-Android开发-InfoQ视频-总结
categories:
- Android最佳实践
tags:
- 360手机卫士
- InfoQ
- Android
- 优化
- 总结

---

## 前言
演讲人: 姚彤,奇虎360公司技术委员会委员/手机核心安全事业部总经理

视频标题: 从360手机卫士的开发历程看如何实施大型移动应用开发

视频地址: http://www.infoq.com/cn/presentations/from-360-development-see-big-mobile-application-development


## 宗旨:

一个应用可以没用，但不要添乱

<!--more-->

## I. 大应用通病
1. 程序规模越来越大
2. 内存占用高，卡，慢
3. 崩溃
4. 耦合
5. 适配问题
6. 发布版本疲于奔命
7. 疑难问题定位

## II. 指标定位技巧

直接定位`AndroidManifest.xml` 大小变化即可，Android四大组件都是需要在里面定义的。

## III. 应用优劣定位
1. 安装包体积（用户会觉得包越小越不卡，虽然实际并非如此）
2. 内存暂用
3. 耗电情况
4. CPU
5. 兼容
6. 流量
7. 升级新版本（基本上以月为单位完成洗量）（升级所用的描述需要考究）（升级的时间点需要考究）
8. 应用自带主要需求的特殊问题

## IV. 应用优化方面
##### 1) 内存方面:
内存过多: 多进程化（按需创建）: 剥离需要常驻与不需要常驻的操作到不同的进程。这样也可以提高稳定性（主要的进程不会受影响）

##### 2) 代码方面:
- 代码过多: 插件化（插件话独立维护/升级），分模块独立升级、独立维护。
- 小改动不得不通过升级：云化，多用配置文件（如Lua啊之类的）

##### 3) 升级方面:
- 一定要稳定。
- 针对性升级（地域、机型、网络类型、历史版本号）
- 增量升级
- 考虑成功率问题，wifi下默认下载再提示用户
- 运营商cache，导致升级错包： 1. 检测包key, 2. 走自己的代理服务器/https


##### 4) 发布方面
- 渠道首页
- 内测群
- 灰度升级
- 论坛反馈收集（让产品去跟）


##### 4) 诊断方面:
制作诊断插件（插件需要根据目标问题自动选择诊断不同模块），运行以后自动上传日志。

## V. 工具
##### 1) Build工具:
1. release版
2. debug版
3. 每个包的代码扫描工具
4. 每个新包较上一个包的比较
5. 每个发布包检测大小变化原因（apk黑盒比较）

![](/img/360-1.png)

![](/img/360-2.png)

##### 2) 代码扫描
1. Checkstyle
2. Lint(error, safe)
3. 红线扫描(基于PMD)


##### 3) 自动化测试
1. uiautomator
2. 基于Robotium改造（改造用Lua写测试案例）

![](/img/360-3.png)

![](/img/360-4.png)

#### 4) BVT case check
- 每个包都可以跑
- 发布包必须跑

#### 5) 安全审核（发布最后一关（公司/部门），自动化，黑盒）
- 信息泄露
- DOS


#### 6) TIPS:
1. 外来代码检测更加严格(可追溯，代码审计，整合测试，黑盒逆向分析)


# VI. 安全建议
1. WebView各类安全问题(Js注入，Javascrip问题等等)
2. 防恶意二次打包
3. 明文传递敏感信息(https要用对)
4. 错误导出组件
5. 参数校验不严格(Intent不检测(导致DDOS))

# VII. 管理方面

1. 人员方面，现在水涨船高，人员可以多挖掘C++或做pc开发等的开发人员。
2. 代码方面，通过插件化，整个团队分模块达到解耦，独立维护，加快各模块独立维护速度。
3. 研发流程: 重视build break问题
4. 组织架构: 小团队；少开大会；专人维护Build系统；专门的架构组；专门的质量改进组（高手重点）；专门的自动化测试组；每周召开质量会

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
