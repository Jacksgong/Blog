title: 去哪儿安全0~1
date: 2015-07-17 21:35:03
permalink: 2015/07/17/wh_qunaer0_1
tags:
- 2015乌云白帽大会
- 安全
- 白帽
- 会议笔记

---

> 演讲者：郭添森
> 去哪儿安全总监
> 联系微信: eyasguo

## ESG信息安全

> Enterprise Strategy Group

<!--more-->
### 愿景:

1. 初始阶段: 可有可无，运维
2. 进阶: 被提出，比较独立
3. 高阶: 被重视


## 如何建立安全威信

> 领导力

#### 1. 专业

进行决策的时候，能够有专业的主见与方向的把控

#### 2. 人格

替对方考虑: 每个人都是为别人服务，也需要对方来为你来服务。

权衡ROI等

#### 3. 职权

- 组织架构：

    他之前的公司: 运维 <- 安全工程师 | 安全独立 | 安全上升到VP级别(阿里巴巴)

- 参与关键流程
- 奖惩

## 去哪儿安全发展

### 第一阶段

> 公司500人左右。网络规模: 千人，第一年

- 组建团队

#### 网络模块

##### 问题&解决方案:

- 办公网: 未隔离

    做VLAN隔离: 只能出不能进

- 生产网: 无ACL

    设置ACL: 只开http/https端口 &只开给指定的IP
    Web统一由nginx做反向代理
    Nginx配置走变更流程

- VPN: 用户名/密码验证

### 第二阶段

> 公司10000人左右，网络规模下一个数量级，2~3年

#### 主要升级方面

- 流程制度的标准: 技术标准
- 合规: SOX404、PCI DSS
- 建立自动化系统、确保安全规划能落地执行

##### 操作系统层面问题

- 用户名/密码认证

    双因素认证 : 登陆服务器，先登陆堡垒机

- 弱口令

    tcp wrapper

- 离职人员账号

##### 数据库

- 空口令/弱口令: mysql, pg, mongod

    检测配置文件，把密码的hash拿出来

##### 系统应用

- 软件?版本?配置?漏洞?

    收集软件版本、配置等 & 漏洞检测 & 警告邮件

##### Web server

> 百分百覆盖以下问题

- 默认管理后台: tomcat，jboos等
- 启动账号:nobody
- 目录权限:root,755
- 解析漏洞:nginx fastcgi, apache httpd等
- Auto index
- 压缩文件

> 默认情况下保证Web server 写不了

##### Spring/struts
##### Jenkins/es等命令执行
##### rsyncd
##### Redis


##### Web应用

- 账号密码?复杂度?定期改

    QSSO系统: 集中管理，双因素认证

    QWAF: 静态、动态(静态 ＋ 动态策略规则)

- OWASP TOP 10

    制定安全标准
    内部测试、终测

### 第三阶段

> 10000人，第4年

#### 数据安全

##### 用户隐私、交易详情、产品技术文档，源码保护

- 制定标准
- PCI DSS(支付卡行业数据安全标准)认证
- 数据加密(加密算法只有几个人知道)、清洗、大码
- 自动抽样（发现问题，进行跟进处理)
- 授权
- 人工巡查github

#### 业务安全

##### 账号安全：垃圾注册？撞库?

- 统一入口，收缩防线
- 动静结合

##### 反欺诈:用户/商业作弊

- 异常行为分析

#### 业务和安全平衡

> 消除风险还是控制风险。

##### 基础架构: OPS

> 安全稳定高效

- 运维部门合作

- 业务部门: 开发/QA/产品

    产品流程切入，一般会在后期切入

- 冲突: 汇报人员级别不断升级

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
