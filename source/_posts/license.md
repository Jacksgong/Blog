title: 开源协议
date: 2016-1-3 01:48:03
tags:
- MIT
- BSD
- Apache License
- GPL
- LGPL

---

目前一共有近60种开源协议: [Open Source Initiative](http://opensource.org/licenses/alphabetical)

常见的协议:BSD、GPL、LGPL、MIT都是OSI批准的协议

<!-- more -->

## MIT

#### 使用者权限:

1. 自由使用
2. 修改源代码
3. 修改后开源
4. 闭源发布

#### 约束:

1. 源码/闭源 都需要在发行版里包含原许可协议申明

---

## BSD

> original BSD license、FreeBSD license、Original BSD license

> 估计代码共享，但需要尊重代码作者的著作权

#### 使用者权限:

1. 自由使用
2. 修改源代码
3. 修改后开源
4. 闭源发布

#### 约束:

> 修改了使用BSD协议的代码 || 以BSD协议的源代码作为基础

1. 如果包含源代码，需要源代码带有`原来代码中的BSD协议`
2. 如果都是二进制类库/软件(闭源)，需要在文档和版权声明中包含`原来代码中的BSD协议`
3. 不可用开源代码的 `作者/机构名字`和原来`产品的名字`做市场推广

---

## Apache Licence 2.0

> Apache License, Version 2.0、Apache License, Version 1.1、Apache License, Version 1.0

> 鼓励代码共享，尊重原作者著作权

> 是著名非盈利开源组织Apache采用的协议

#### 使用者权限:

1. 自由使用
2. 修改源代码
3. 修改后开源
4. 闭源发布

#### 约束:

1. 如果包含源代码，需要包含Apache Licence
2. 如果修改了代码/衍生代码，需要在被修改的文件/衍生的代码中带上`原来代码中的协议`
3. 如果发布的产品(闭源)包含Notice，需要在Notice中带有 Apache Licence
4. 可以在产品(闭源)的Notice中增加自己的许可，但是不可以表现为对apache licence构成更改

---

## LGPL

> GNU Lesser General Public License

> 是GPL的一个主要为类库使用设计的开源协议

#### 使用者权限:

1. 自由使用
2. 修改源码
3. 修改后开源
4. 对于只是引用 允许 闭源发布


#### 约束:

1. 修改、衍生代码，必须也使用LGPL协议

---

## GPL

> GNU General Public License

> Linux采用GPl

> 开源/免费使用和引用/修改/衍生代码的开源

#### 使用者权限:

1. 自由使用
2. 修改源码
3. 修改后开源


#### 约束:

1. 使用/引用源码或者修改过的代码/衍生代码，则该产品也必须采用GPL协议

---

- [五种开源授权规范的比较(BSD, Apache, GPL, LGPL, MIT)](http://inspiregate.com/internet/trends/74-comparison-of-five-kinds-of-standard-open-source-license-bsd-apache-gpl-lgpl-mit.html)
- [【Git】认识各种开源协议及其关系](http://jasonding1354.github.io/2015/05/11/Git/%E3%80%90Git%E3%80%91%E8%AE%A4%E8%AF%86%E5%90%84%E7%A7%8D%E5%BC%80%E6%BA%90%E5%8D%8F%E8%AE%AE%E5%8F%8A%E5%85%B6%E5%85%B3%E7%B3%BB/)
- [详细介绍 MIT 协议](http://www.oschina.net/question/12_2829)
