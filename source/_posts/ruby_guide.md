title: Ruby 入门学习整理
date: 2015-07-26 20:39:03
tags:
- 后端
- rails
- ruby
- 语言

---

> 简单哲学、高生产力、精巧、自然语法、高可读性&可维护性
> 灵感来自: Lisp(难以读懂)、Perl和Smalltalk
> 初衷: 让程序员能够更快乐的写代码
> 动态语言: 更少的代码做更多的事，更敏捷的开发;执行效率比静态语言（Java、C++、etc.）慢，没有编译期可以检查类型错误(单元测试/TTD来解决)

<!--more-->
### Ruby语言推荐入门

1. [20分钟体验Ruby](https://www.ruby-lang.org/zh_cn/documentation/quickstart/)
2. [Code School Try Ruby](http://tryruby.org/levels/1/challenges/0)
3. [其他语言与Ruby的对比，学过其他语言的再学习ruby有很大帮助](https://www.ruby-lang.org/zh_cn/documentation/ruby-from-other-languages/)

## 推荐学习网址

- [Ruby官方中文-文档](https://www.ruby-lang.org/zh_cn/documentation/)

- [如何快速学习RoR - 知乎](http://www.zhihu.com/question/19552402)


## DSL
> 目前应用于DSL(Domain-specific language)非常成功。

### 成功的SDL函数库:

- Rake构建工具
- RSpec测试工具
- Chef伺服器设定工具
- Cucumber验收测试
- ...

## RubyGems

> Ruby的套件管理系统，简化安装以及管理Ruby函数库

也可以通过[The ruby Toolbox](https://www.ruby-toolbox.com/)来查找套件，按照热度排列的。

### 常用指令

```
gem -v #告诉你RubyGems 的版本
gem update --system #升级RubyGems的版本
gem install gem_name #安装某个套件
gem install gem_name --no-ri --no-rdoc #安装套件，不产生期RDoc和ri文件
gem list #列出安装的套件
gem update gem_name #更新最新版本
gem update #更新所有你安装的Gems
gem install -v xxx gemname #安装特定版本
gem uninstall gem_name #反安装
```

## RoR(Ruby on Rails)

> 作者: David Heinemeier Hanson
> 2004年DDH将Rails从37sinals商业产品中独立开源出来
> 目标: 更少的代码，更多的功能，轻量&强大
> 特点: 社区活跃、轻量、开发周期短

- 采用MVC模式
- 内建支援单元测试和整合测试
- 支持Ajax
- 支持RESTful界面
- 支持ORM机制
- 支持HTML5、JQuery
- ...

### 指导原则

- DRY(Don't Repeat Yourself) 不要重复自己
- 惯例胜于设定(预设好设定，不需要我们去设定细节)
- REST -- 最佳模式(Resources和标准的HTTP verbs来组织代码)

### 安装

> 介于国内网络环境，导致rubygems.org放在Amazon S#上面的资源文件间歇性连接失败，Fuxk!! 所以需要配置到taobao以后再试。

国内用户: 以下步骤切换到taobao提供的rubygems.org镜像（15分钟一次与官网同步）

```
$ gem sources --remove https://rubygems.org/
$ gem sources -a https://ruby.taobao.org/
$ gem sources -l
*** CURRENT SOURCES ***

https://ruby.taobao.org
# 请确保只有 ruby.taobao.org
```

开始安装rails

```
# 为了节省安装时间,不安装文件档--no-ri、--no-rdoc(文档google上查更方便，不是吗)
gem install rails --no-ri --no-rdoc
```

输入`rails -v`可以看到当前rails的版本

### 开始使用


#### I. 创建一个demo的案例:

```
rails new demo --skip-test-unit
```

由于`rails new`会用到`bundle`，而介于国内的墙，因此国内用户需要配置下淘宝提供的镜像:

```
bundle config mirror.https://rubygems.org https://ruby.taobao.org
```

#### II. 目录分析

创建`demo`以后，会出现一个`demo`文件夹，进入以后的目录结构:

档案/目录 |	用途
:-:|:-
Gemfile|	设定Rails应用程式会使用哪些Gems套件
README|	专案说明：你可以用来告诉其他人你的应用程式是做什么用的，如何使用等等。
Rakefile|	用来载入可以被命令列执行的一些Rake任务
app/|	放Controllers、Models和Views档案，接下来的内容主要都在这个目录。
config/|	应用程式设定档、路由规则、资料库设定等等
config.ru|	用来启动应用程式的Rack伺服器设定档
db/|	资料库的结构纲要
doc/|	用来放你的文件
lib/|	放一些自定的Module和类别档案
log/|	应用程式的Log记录档
public/|	唯一可以在网路上看到的目录，这是你的图档、JavaScript、CSS和其他静态档案摆放的地方
bin/|	放rails这个指令和放其他的script指令
test/|	单元测试、fixtures及整合测试等程式
tmp/|	暂时性的档案

#### III. 启动服务器

```
#rails server可以间写为rails s
bin/rails server
```

屏幕上出现:

```
=> Booting WEBrick
=> Rails 4.2.3 application starting in development on http://localhost:3000
=> Run `rails server -h` for more startup options
=> Ctrl-C to shutdown server
[2015-07-26 20:00:19] INFO  WEBrick 1.3.1
[2015-07-26 20:00:19] INFO  ruby 2.2.2 (2015-04-13) [x86_64-darwin14]
[2015-07-26 20:00:19] INFO  WEBrick::HTTPServer#start: pid=23454 port=3000
```
说明已经运行在3000端口了:[http://localhost:3000](http://localhost:3000)

![](img/ruby_guide_1.png)

#### IV. 终端服务器

```
#开发模式下，除修改config或vender目录下的文件，其他都不用重启，正式上限模式，任何文件修改都需要重新启动服务器
<Ctrl> + <C>
```

### Hello World

> 基于Rails的MVC框架，由于Hello World不需要数据支持，因此我们只需要涉及到C-V

#### I. 创建一个welcome:

```
#rails generate 可以简写未rails g
bin/rails generate controller welcome
```

#### II. 对页面进行路由:

编辑`config/routes.rb`文件，新增一行:
```
Rails::Application.routes.draw do
    # 将http://localhost:3000/welcome/say_hello这样的网址对应到welcome Controller的say Action上。
    get "welcome/say_hello" => "welcome#say"
    ...
end
```

#### III. 在Control中添加`say`Action已经在View上也添加

编辑`app/controllers/welcome_controller.rb`,加入一个`say`方法

```
class WelcomeController < ApplicationController
    def say
    end
end
```

编辑`app/views/welcome/`下创建对应Action名称(`say`)的文件:`say.html.erb`(html表示是HTML格式文件)，(erb表示是ERb样式)，添加内容如下:

```
<h1>Hello, World!</h1>
```

#### IV. 验证

打开地址[http://localhost:3000/welcome/say_hello](http://localhost:3000/welcome/say_hello):

![](img/ruby_guide_2.png)
---
## 参考资料

- [Ruby on Rails实战圣经](https://ihower.tw/rails4)
- [RubyGems镜像 - 淘宝网](http://ruby.taobao.org/)


