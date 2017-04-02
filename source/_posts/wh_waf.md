title: 多角度对抗WAF
date: 2015-07-17 21:35:03
updated: 2015-07-17 21:35:03
permalink: 2015/07/17/wh_waf
categories:
- 安全
tags:
- 2015乌云白帽大会
- 安全
- 白帽
- 会议笔记

---

> MayIKissYou
> 完美世界高级安全工程师

Nginx-lua-waf Modsecurity


> 安全狗 有很多bug

<!--more-->
> 很好的方法 模糊测试, 遍历%xx

## WAF在哪里

请求到最终请求转发，中间经过的多少设备

## 如何绕过

通过一些没有考虑到的特性

### 数据库层绕过

> 利用数据库特性

#### 1. mysql、sqlserver、oracle、postgress

```
[1]select[2][3]from[4]

// 1、2、4: a-z, A-Z,_,数字
// 3: a-z, A-Z, _

```

http://zone.wooyun.org/content/13270


### WEB服务器层绕过


1. asp+IIS: %
2. aspx+IIS: %u
3. php+apache: 畸形的method
4. java+tomcat

> 模糊测试来模拟 and的a，如%uxxxnd : widechar，widechar iis可以处理，多个widechar会有可能转换为同一字符。

### WAF层绕过

> 留意WAF自身的点点滴滴，特有的功能可能就是你的绕过的利器。

- 如果上传一个1G大小的流，WAF肯定不会扫描的，要保障大小。
- post请求加了很多数据，并发的请求，会有部分请求绕过
- 通过%26是&绕过了360安全卫士

---
