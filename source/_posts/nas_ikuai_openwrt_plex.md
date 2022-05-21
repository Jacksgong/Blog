title: iKuai主路由 + Openwrt旁路由 Plex外网无法访问问题
date: 2022-05-21 17:04:03
updated: 2022-05-21
categories:
- 网络
tags:
- Plex
- iKuai
- OpenWrt
- Nas

---

{% note info %} 本文主要记录在特定场景下Plex外网无法正常访问的解决方案。 {% endnote %}

<!-- more -->

## 前言

我的主路由是iKuai，旁路由是Openwrt，旁路由与主路由都是运行在Nas上的虚拟机，Plex是运行在TrueNas Scale内的应用集群上。

- 主路由iKuai的IP是: 10.0.0.1
- 旁路由Openwrt的IP是: 10.0.0.169
- Plex所在TruneNas的IP是: 10.0.0.167

其中需要特别注意的是，为了让所有科学上网正常运行，TrueNas的全局网络设置的网关以及Plex所在K8S的网关都是设置的Openwrt的IP。


## Plex外网无法访问情况说明

这里出现的问题是，检测可以连接，但是过一会儿又提示无法访问。

## 解决方案

首先为了保险起见，在Openwrt的SSR或者ByPass中加下白名单:

![](/img/nas_ikuai_openwrt_plex-1.png)


### 方案一（推荐）

在OP网关与主路由之间做两层转包:

1. 在主路由上将对应端口转发到旁路由
2. 在旁路由将对应端口转发到plex即可

![](/img/nas_ikuai_openwrt_plex-2.png)

### 方案二（不推荐）

将K8S与TrueNas的网关与直接设置为不走科学上网的主路由IP，这个方案会使得TrueNas与所有K8S中的应用都无法科学上网，但确实也可行。

## 最后

至此就可以正常访问了:

![](/img/nas_ikuai_openwrt_plex-3.png)

---

- [OpenWrt中，旁路由的设置与使用](https://zhuanlan.zhihu.com/p/112484256)
