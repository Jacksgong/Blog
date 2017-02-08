title: Android Touch Event派发分析
date: 2016-03-10 09:49:03
permalink: 2016/03/10/touch_event
tags:
- Android
- Touch

---

> 早前画了touch事件派发草图，重新整理了下

<!-- more -->

## Touch Event: Down

> Down事件，无论 `clickable` 与否都会各层级传递

![](/img/touch_event-down-not-cliable.png)

## Touch Event: Move

| Hierarchy | `clickable`/`longClickable`
| --- | ---
| Parent | `false`
| Child | `false`

![](/img/touch_event-move-not-cliable.png)

| Hierarchy | `clickable`/`longClickable`
| --- | ---
| Parent | `false`/`true`
| Child | `true`


![](/img/touch_event-move-child-cliable.png)

| Hierarchy | `clickable`/`longClickable`
| --- | ---
| Parent | `true`
| Child | `false`

![](/img/touch_event-move-cliable.png)

## Touch Event: Up


| Hierarchy | `clickable`/`longClickable`
| --- | ---
| Parent | `false`
| Child | `false`

![](/img/touch_event-up-not-cliable.png)


| Hierarchy | `clickable`/`longClickable`
| --- | ---
| Parent | `true`/`false`
| Child | `true`

![](/img/touch_event-up-child-cliable.png)


| Hierarchy | `clickable`/`longClickable`
| --- | ---
| Parent | `true`
| Child | `false`

![](/img/touch_event-up-cliable.png)

---

本文已经发布到JackBlog公众号，可请直接访问: [Android Touch Event派发分析 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483664&idx=1&sn=9871b049b89ec0b5198e85759986f50b)

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
