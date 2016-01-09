title: Android应用程序通用自动脱壳方法研究
date: 2015-07-17 21:35:03
tags:
- 2015乌云白帽大会
- 安全
- 白帽
- 会议笔记

---

> 演讲者: 杨文博
> 上海交通大学计算机系在读博士
> GoSSIP软件安全小组

## Android加壳保护

#### 加固保护市场

- 阿里聚安全

#### 可保护

- 程序逻辑: 算法、协议
- 完整性: 盗版、外挂

<!--more-->

#### 不可保护

- 安全问题: 数据存储传输
- 程序漏洞: 权限

## 为什么要做脱壳

> 最近一年多(2014年开始)，加壳的恶意程序大爆发，通过加壳逃避杀毒软件

## 脱壳的影响

- 暴露真实的逻辑
- 降低分析门槛配合自动化扫描
- 篡改App

## 加固程序特点

- `Manifest`保留
- 增加入口点类(转到Native库)
- Native执行
- 隐藏DEX
- 静态逆向难
- 变化快
- 反分析：反调试、反内存dump、反反汇编

### Native也被加壳

- ARM ELF 头部破坏
- `.init_array`段花指令


## 制作脱壳机

> 不需要知道方法，就可以过滤掉

### Dalvik源码插桩

- Portable 解释器
- 绕过反调试: Dalvik源码中做
- 运行时数据
- 任意脱壳: 任何一个指令后面插一个脱壳点的插桩
- 真机部署

内存中的Dalvik数据结构

## 一个Native的实现

### 读取DexFile结构体

> dalvik/dexdump/DexDump.app (谷歌提供的)

- 基于源码: C/C++ 实现
- 以DexFile为输入

## 效果

> 几乎可以对付市面所有的壳

- 脱壳点: `MainActivity.onCreate()` in Manifest
- 输出: 一个纯文本，这是一个很大的问题!

CTF?

## 更加复杂的脱壳实现

> DEX文件重组，真正执行的时候，Dex在内存中肯定是正确的。

- 获取内存中的Dalvik数据（应该是在内存中是连续的区域):、不同的数据块有较多的寻址方式
- 排列顺序: dalvik/libdex/DexFile.h
- 调整偏移: stringDataOff, parametersOff, interfacesOff, classDataOff, codeOff...
- 重新计算: DexHeader

## 10种壳(ALL-KILL)

1. bangbang
2. 爱加密
3. 360
4. 百度
5. 阿里
6. 腾讯
7. APKProtect
8. 网泰
9. LIAPP
10. DEXProtector

> 最佳防御 混淆&Java自动转为 Native

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
