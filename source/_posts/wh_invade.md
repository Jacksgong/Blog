title: 如何从外围入各大公司内网
date: 2015-07-17 21:35:03
permalink: 2015/07/17/wh_invade
categories:
- 安全
tags:
- 2015乌云白帽大会
- 安全
- 白帽
- 会议笔记

---

> 演讲者: boooooom
> 乌云白帽子

## I. 为什么要进入内网

> 一切不以数据为目的的攻击行为，都是扯蛋。

- 攻击的核心目标: 数据
- 数据在哪？
- 内网的脆弱性!

<!--more-->
## II. 方式

### 1. 合法入口(和员工一起进入内网)

- vpn/mail，通过大数据获取 企业员工的用户名密码
- wifi，万能钥匙(京东内网暴露事件)

### 2. "非法"入口(跨边界的资产)

- 应用, 各种漏洞、弱点GETSHELL
- 服务，坑爹配置GETSHELL
- 员工PC，钓鱼种木马

## III. 说点实在的

> 小公司需要效率、大公司需要过招取其命门

### 1. 大公司

> 成也边界，败也边界

- 只关注边界
- 区域性的防守 (OA - IDC - HTTP)
- 划分边界，保护核心资产(数据)
- 制定规范，把玩法先说好

#### 问题所在(命门)

1. 规范越多，执行越差，无法统一固定唯一的规范
2. 合规性检查的盲区

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
