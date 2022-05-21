title: iKuai主路由 + Openwrt旁路由 TrueNas中应用无法访问外网问题
date: 2022-05-21 17:39:03
updated: 2022-05-21
categories:
- 网络
tags:
- iKuai
- OpenWrt
- Nas
- TrueNas Scale

---

{% note info %}本文主要记录了TrueNas中的K8S网关指定为以OpenWrt旁路由的IP后，应用访问的问题。{% endnote %}

<!-- more -->

## 前言

主路由使用的是iKuai（`10.0.0.1`），旁路由是Openwrt（`10.0.0.169`），旁路由主要作用是科学上网。

旁路由与主路由的原理作用我觉得有网上的这张图比较形象:

![](/img/nas_ikuai_openwrt_k8s-1.png)

其中可以看到TrueNas的网关已经使用了旁路由的IP:

![](/img/nas_ikuai_openwrt_k8s-fa84af28.png)

另外应用的K8S配置的网关也已经使用了旁路由的IP:

![](/img/nas_ikuai_openwrt_k8s-9a6d265a.png)


## 问题描述

这种情况下，你会发现其实应用内的应用是访问不了外网的，可以很看到是被旁路由Openwrt拦截了:

![](/img/nas_ikuai_openwrt_k8s-2f12ab3f.png)

那么我们从Openwrt入手。

## 解决方案

很显然应该是防火墙的问题，这里我们到Openwrt。

### 1. 关闭SYN-Flood防御

这里的主要原因是，针对K8S服务与应用的请求过程会被误认为是SYN Flood攻击。

![](/img/nas_ikuai_openwrt_k8s-44ae3f56.png)

### 2. 打开IP动态伪装:

这里的主要原因是，Openwrt中的动态伪装就是NAT的开关。

![](/img/nas_ikuai_openwrt_k8s-58739119.png)

## 最后

经过上面解决后，就K8S可以正常上网了。

![](/img/nas_ikuai_openwrt_k8s-f7590001.png)

---

- [什么是SYN Flood攻击？](https://zhuanlan.zhihu.com/p/29539671)
- [openwrt避坑指南1：IP动态伪装和MSS钳制](https://www.jianshu.com/p/e7ccb32c0462)
