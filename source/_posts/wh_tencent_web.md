title: 腾讯web安全
date: 2015-07-17 21:35:03
permalink: 2015/07/17/wh_tencent_web
categories:
- 安全
tags:
- 2015乌云白帽大会
- 安全
- 白帽
- 会议笔记

---

> 演讲者: 腾讯安全架构师
> 腾讯8年老员工，一直做腾讯安全

#### 开发

安全规范、安全培训、安全API、安全JS

#### 测试

- 接入WAF
- 上线前安全扫描

<!--more-->

## 扫描器:

- 扫描程序架构: 全异步事件驱动 ＋ 协程
- 规则: 检测逻辑、配置(lua脚本(性能高(1/4 c))、实时更新
- 任务调度系统: Gearman: 系统优先级，多任务类型、任务出错重试、超时
- 爬虫: webkit后台server，与调度系统结合

## WAF方案

1. 本地服务器模块模式
2. 反向代理模式（在反向代理上切入WAF)
3. 硬件防护（在硬件中嵌入)


### 大型网络复杂情况下WAF的选择:

> 多种方案并存, 用WAF集群来专门处理

##### 服务器Agent + WAF集群:

- DDOS设备
- CDN
- Nginx反向代理
- 通用性webserver
- 自研webserver



## 技术点:

### 1. Nginx agent的实现(数据分发)

> Nginx以性能著称

需要对Nginx的处理流程&通讯机制进行介入。

通过Nginx一些api的方式进行网络通信监控。

WAF回来以后做网络通信: 通过Nginx1.4.4＋的对外接口来获得回调。  

### 2. 性能

### 3. 负载均衡、容灾、防雪崩、流量穿透


## WAF运营


### 1. 业务web服务器配置

### 2. 规则管理

公司类、WAF、旁路分发。
编辑环境、测试环境、线上运营

### 3. 大数据分析

解决: 误报、漏报

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
