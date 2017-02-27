title: Dalvik
date: 2014-12-25 08:35:03
permalink: 2014/12/25/dalvik
categories:
- Android机制
tags:
- Dalvik
- 虚拟机

---

## 什么是Dalvik?

是Java虚拟机，Android L 之前Android的核心组成部分之一(Android L 后被ART取代)。

<!--more-->

#### 作者

Dan Bornstein

#### 名字来源

作者祖先曾经居住过的小渔村（位于冰岛）:Dalvík

#### 诞生缘由

- **业界猜测:** 是对Sun尝试控制和保护来自Java ME收入来源的一次反应，以及对建立OpenJDK统辖理事会迟迟未果的回答。

- **官方解释:** Dalvik是对解决目前Java ME平台上分裂(与已有的JVM)的一次尝试，也是为了提供一个拥有较少限制许可证的平台。

## 作用是什么?

支持.dev(Dalvik Executable)运行

#### .dex

专为Dalvik设计的一种压缩格式（Java应用程序），适合内存和处理器速度有限的系统

#### 优化

Dalvik经过优化，允许有限内存中同时运行多个 虚拟机 实例，并在独立进程运行防止相互影响。

## 业界评价

一直被用户指责为拖慢安卓系统运行速度不如IOS的根源。2014年的Google I/O大会上，在Android L 中被Google 删除，取而代之的是ART。

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
