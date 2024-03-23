title: OpenClash 常用与维护
date: 2023-03-27 00:15:13
updated: 2024-03-24
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

## III. DNS海外解析出现问题解决方案

OpenClash由于有时候DNsmasq转发会与其他的一些服务冲突，导致所有的海外域名都无法正常解析，这种情况下可以考虑尝试以下方案处理。

### 方案一.  关闭使用Dnsmasq转发

缺点: 很明显，就是会发现一些域名相关的openclash配置会失效
优点: 配置比较简单

如下图配置即可

![](/img/openclash_maintain_d94ccf94_25.png)

### 方案二. 指定覆写DNS服务器

缺点: 配置麻烦，需要多启一个DNS服务器，对域名响应会有略微影响；需要用到Meta内核，不清楚有没有未知坑
优点: openclash所有功能可用

第一步. 安装Adguard

![](/img/openclash_maintain_3453ac12_26.png)

第二步. 启动Adguard，并且查看其监听DNS端口(这里我们看到的是1745)

![](/img/openclash_maintain_119a8a7f_27.png)

第三步. 在插件设置里勾选 使用Meta内核

![](/img/openclash_maintain_5aeb2af6_28.png)

第四步. 配置覆写设置->DNS设置

1. 勾选自定义上游DNS服务器
2. 将NameServer中所有的启用勾勾都去掉，把第一个勾上，配置为如下截图（这里的1745，是上面Adguard监听的DNS端口)
![](/img/openclash_maintain_eb965948_29.png)
3. 点击第一个勾上并且修改好的右边的编辑进去，将"节点域名解析"勾上，然后保存配置
![](/img/openclash_maintain_3970ef25_30.png)
4. 将FallBack中所有的启用勾勾去掉，把第一个勾上，保留默认配置即可，然后点击右侧的编辑
![](/img/openclash_maintain_62b6b384_31.png)
5. 进入编辑后，指定一个可用的策略组，然后保存配置
![](/img/openclash_maintain_2447c322_32.png)
6. 应用配置，可以看看是不是可以了，不行再重启下路由器即可

如果还有问题，确认下Adguard的6060重定向是否是选择"无"，如果不是记得选择"无"保存。
![](/img/openclash_maintain_d06f23ee_33.png)

## IV. 其他常见说明

### 订阅的规则太少，如何一次性添加?

一般我们的规则是来自`配置订阅`中拉取的:

![](/img/openclash_maintain_87a80080_34.png)

但是拉取后会发现，默认提供可配置的策略不多，如只有：`NetFlix`、`OpenAI`之类的，我们想要一次性添加所有Ihie1洞主的规则，那么可以在`覆写设置`->`开发者选项`->`设置第三方规则`中添加即可:

![](/img/openclash_maintain_8eb5e6ae_35.png)

这里温馨提示：如果说发现代理没有走到制定的规则，也可以在这里，点击编辑，检查是否配置了对应规则走了对应的策略组：

![](/img/openclash_maintain_f34ad884_36.png)

### 出现问题的时候如何排查?

一般可以在`运行日志`->`内核日志`中找到问题:

![](/img/openclash_maintain_aedeaab8_37.png)

---

- [Game.list](https://github.com/LM-Firefly/Rules/blob/master/Game.list)
- [2023最新 OpenClash添加自定义规则和策略组，详细规则设置添加策略组配置方法|openclash使用教程](https://www.youtube.com/watch?v=enmv0UZtW48)