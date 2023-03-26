title: OpenClash 常用与维护
date: 2023-03-27 00:15:13
updated: 2023-03-27
permalink: openclash_maintain
categories:
- fun
tags:
- openclash
- clash
- kcptun

---

{% note info %} 这篇文章主要是介绍日常对openclash维护遇到的一些问题的记录，特别是有很多在国内找不到很好方法探究了一小段时间的。  {% endnote %}

<!-- more -->

## I. 常用规则配置

直接参看这篇文章极客: [规则设置（访问控制） · vernesong/OpenClash Wiki (github.com)](https://github.com/vernesong/OpenClash/wiki/%E8%A7%84%E5%88%99%E8%AE%BE%E7%BD%AE%EF%BC%88%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6%EF%BC%89).     

## II. 如何使用kcptun

> 参考: [能否支持kcptun配置 · Issue #313 · vernesong/OpenClash (github.com)](https://github.com/vernesong/OpenClash/issues/313)

### 1. 安装kcptun-luci

![](/img/openclash_maintain_0.png)

### 2. 配置kcptun服务

就正常根据kcptun服务配置即可

![](/img/openclash_maintain_1.png)

### 3. 启动kcptun服务

正常启动就行

![](/img/openclash_maintain_2.png)

显示运行中就代表已经在正常运行了，通常这个时候你在termianl中能看到已经在运行的服务

![](/img/openclash_maintain_3.png)

### 4. 在OpenClash中配置服务

> 你也可以通过案例熟悉，怎么在openclash中自定义添加服务

![](/img/openclash_maintain_4.png)

往下滑

![](/img/openclash_maintain_5.png)

点击添加

![](/img/openclash_maintain_6.png)

可以将策略添加到所有策略组:

![](/img/openclash_maintain_7.png)

之后保存配置，回到一键生成，勾选保留配置，将新节点默认添加到所有策略组

![](/img/openclash_maintain_8.png)

应用配置就可完成配置，这里只勾选保留配置，不勾选上面的生成配置文件，因为如果勾选下面的策略组等都会被替换，如果你配置的有问题会比较麻烦。