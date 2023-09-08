title: OpenClash 常用与维护
date: 2023-03-27 00:15:13
updated: 2023-09-05
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

直接参看这篇文章即可: [规则设置（访问控制） · vernesong/OpenClash Wiki (github.com)](https://github.com/vernesong/OpenClash/wiki/%E8%A7%84%E5%88%99%E8%AE%BE%E7%BD%AE%EF%BC%88%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6%EF%BC%89) 里面的内容，这里就简单举个栗子，比如我们希望加`okx.com`添加为直连:

如下图，先找到`覆写设置`->`规则设置`，如果说`*自定义规则`没有勾选，将其勾选，此时下面会出现两个可编辑区域:

![](/img/openclash_maintain_f170e89b_0.png)

然后我们在`*自定义规则`中第一个可编辑区域（优先匹配）的`rules:`下面添加`DOMAIN-SUFFIX,okx.com,DIRECT`:

![](/img/openclash_maintain_755cf9ed_1.png)

然后保存配置，应用配置即可，我们可以简单检查下配置，发现已经被正常添加到生效配置的开头了:

![](/img/openclash_maintain_752e7fbd_2.png)

再检查下日志，发现已经生效:

![](/img/openclash_maintain_d4eec0cd_3.png)

## II. 如何使用kcptun

> 参考: [能否支持kcptun配置 · Issue #313 · vernesong/OpenClash (github.com)](https://github.com/vernesong/OpenClash/issues/313)

### 1. 安装kcptun-luci

![](/img/openclash_maintain_8a181645_4.png)

### 2. 配置kcptun服务

就正常根据kcptun服务配即可

![](/img/openclash_maintain_b20f4695_5.png)

### 3. 启动kcptun服务

正常启动就行,

![](/img/openclash_maintain_9a5c0db9_6.png)

显示运行中就代表已经在正常运行了，通常这个时候你在termianl中能看到已经在运行的服务

![](/img/openclash_maintain_5a7b8da8_7.png)

### 4. 在OpenClash中配置服务

> 你也可以通过案例熟悉，怎么在openclash中自定义添加服务

![](/img/openclash_maintain_22c4ba1d_8.png)

往下滑

![](/img/openclash_maintain_691ea759_9.png)

点击添加

![](/img/openclash_maintain_079b5c15_10.png)

可以将策略添加到所有策略组:

![](/img/openclash_maintain_005957b1_11.png)

之后保存配置，回到一键生成，勾选保留配置，将新节点默认添加到所有策略组

![](/img/openclash_maintain_5b80186a_12.png)

应用配置就可完成配置，这里只勾选保留配置，不勾选上面的生成配置文件，因为如果勾选下面的策略组等都会被替换，如果你配置的有问题会比较麻烦。


## II. 为NS Switch添加独立的策略组

### 添加策略组

在一键生成->策略组配置中点击添加，之后点击编辑进入:
![](/img/openclash_maintain_37958af3_13.png)

进入后添加好名字，需要添加到的配置文件，以及策略组类型，后点击保存配置:
![](/img/openclash_maintain_73ca8365_14.png)

此时移动到最后，点击应用配置后，就可以看到这个策略组了。
![](/img/openclash_maintain_99ffbcac_15.png)

### 为策略组添加可选服务器节点

为策略组添加可选的服务器节点，以添加香港01节点为例:
![](/img/openclash_maintain_c0d16551_16.png)

然后滑动到最后添加到策略组，中选择刚添加的策略组的名称，完成添加:
![](/img/openclash_maintain_0a90497d_17.png)

保存返回完成添加，要添加其他服务器节点也是一样的，最后别忘了还是要到最后，应用配置。

![](/img/openclash_maintain_b49a4d01_18.png)

### 为策略组添加走该策略组的规则

#### 方式一：通过网络上的策略添加

在规则附加->滑到页面最后管理三方规则集下载想要的规则
![](/img/openclash_maintain_afab6bc5_19.png)

然后，在规则附加->第三方规则集附加->添加后，以此配置配置文件，选择规则集，选择策略组，最后点击底部的应用配置完成生效。
![](/img/openclash_maintain_5b9b8701_20.png)

#### 方式二：通过自定义的方式添加

比如这里，我们假设Nitendo的域名就是: `nintendo.net`，如拦截到的:
![](/img/openclash_maintain_961658bd_21.png)

那么我们可以在覆写设置->规则设置->自定义规则框中添加如下:
![](/img/openclash_maintain_4bfd0bdd_22.png)

当然也可以直接添加Rule set比如：
![](/img/openclash_maintain_da4b65da_23.png)

最后保存配置，应用配置完成设置。

![](/img/openclash_maintain_90fa3968_24.png)

---

- [Game.list](https://github.com/LM-Firefly/Rules/blob/master/Game.list)
- [2023最新 OpenClash添加自定义规则和策略组，详细规则设置添加策略组配置方法|openclash使用教程](https://www.youtube.com/watch?v=enmv0UZtW48)