title: APK漏洞 "Shadows Everywhere"
date: 2015-12-06 00:46:03
tags:
- Android
- 安全
- META-INFO
- 证书
- 签名
- 攻击

---

## I. 作用

有效逃避安全软件的扫描

<!-- more -->

## II. 原理

> 通过两个APP协作，将调用者与攻击代码分拆在两个APP

### APP1

将攻击性代码放入合法App的/META-INFO目录下

#### 始末

为什么可以逃避安全检查?

因为没有修改合法App的原始证书与数字签名。因此可以被正常安装或升级

![](/img/shadows_everywhere-1.png)

### APP2

通过读取`/data/app`或`/system/app`或`/system/priv-app` 目录下的APP1.apk文件的/META-INFO中已经准备好的代码，实行攻击

#### 始末

由于这三个目录都是所有人可读的: `-rw-r--r--`


---

- [APK 漏洞“黑影无处不在(Shadows Everywhere)”详解](http://jaq.alibaba.com/blog.htm?spm=0.0.0.0.Ioo2FE&id=77)
