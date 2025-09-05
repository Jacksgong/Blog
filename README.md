# Blog

![](https://img.shields.io/badge/Blog-hexo-orange.svg) ![](https://img.shields.io/badge/Blog-dreamtobe.cn-blue.svg) ![Build Status](https://drone.partyland.cc:2443/api/badges/jacks/Blog/status.svg)

> 博客地址: https://blog.dreamtobe.cn

## 站点框架

- 基于框架: [Hexo](https://github.com/hexojs/hexo)
- 基于主题: [NexT](https://github.com/iissnan/hexo-theme-next)
- 本站点服务器搭建教程: [站点与服务器维护](https://blog.dreamtobe.cn/maintain-website-server/)

## 博客索引

- [文章标签](https://blog.dreamtobe.cn/tags/)
- [文章归档](https://blog.dreamtobe.cn/archives/)

## 博客事件

- 2008年 通过百度空间 建立自己的第一个博客: 王者博客（现百度博客已经关闭）。
- 2012年 注册`dreamtobe.cn`域名原本打算创业搞个点子分享站点，阴差阳错做了自己博客的域名。
- 2012年 基于框架[Joomla](http://www.joomla.cn/)，搭建博客并进行迁移。
- 2013年 博客域名`dreamtobe.cn`备案成功。
- 2013年 基于框架[Wordpress](https://cn.wordpress.org/), 搭建博客并进行迁移。
- 2014年 基于框架[OctoPress](http://octopress.org/)，搭建博客并进行迁移。
- 2015年6月 博客使用git进行管理，托管在自己服务器上的gitlab。
- 2015年6月 基于架构[Hexo](https://github.com/hexojs/hexo)，搭建博客并进行迁移。
- 2015年6月 博客服务器迁到韩国，并接入腾讯云CDN。
- 2016年1月 博客开源并两个远端，双备份。
- 2016年5月 博客开通线上公众号(微信号: `jacksblog`)。
- 2016年9月 为了防止国内万恶运营商的劫持，上了[HTTPS-ORIGIN](https://www.ssllabs.com/ssltest/analyze.html?d=blog.jacksgong.com)，[HTTPS-CDN](https://www.ssllabs.com/ssltest/analyze.html?d=blog.dreamtobe.cn)。
- 2017年2月 网站源支持了HTTP/2: https://nocdn.dreamtobe.cn/ (腾讯CDN要在2017年第二个季度才支持HTTP/2)
- 2017年3月 博客服务器迁到日本，并改用KVM架构VPS，并将TCP拥塞控制算法改为BBR: https://nocdn.dreamtobe.cn/
- 2017年3月 压缩站点，考虑到腾讯CDN优化缓慢(BBR、HTTP2等)，深受牵制，只将js/css图片等放到CDN，站点地址直接解析回自己的VPS
- 2017年3月 考虑到出口有时候丢包与延时严重，另外租了一台腾讯VPS，域名解析国内的走腾讯在广州的VPS，海外的走日本的VPS
- 2022年 考虑到性能与自动化考虑搭建[Gitea](http://gitea.partyland.cc:2443/)+[Drone](https://drone.partyland.cc:2443/)+[Webhook](https://github.com/adnanh/webhook)组合实现提交自动部署
- 2023年 考虑到绝大多数笔记都已经是用Obsidian管理，有很长一段时间只在Obsidian上做私有笔记记录，考虑到做开放笔记更有易于认真梳理+需要做隔离，编写[脚本](https://github.com/Jacksgong/Blog/blob/master/obsidian2post.py)做Obsidian上日志指定迁移，并支持图片、差量等能力

## 当前部署方式

1. 使用脚本将Obsidian上的笔记进行转录，比如: `./postob.sh ~/note/dev/ops/将MacMini改为家庭服务器.md mac_to_nas`
2. 使用本地脚本进行编译与部署，直接执行：`./local-deploy.sh`
3. 将变更推送到远端：`./push-double-end.sh`

## LICENSE

#### 网站框架(Hexo)

```
Copyright (c) 2012-2016 Tommy Chen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```



#### 网站所有文章

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/
