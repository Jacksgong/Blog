title: zsh[oh my zsh]
date: 2015-03-29 20:29:03
updated: 2017-03-01 20:29:0
permalink: 2015/03/29/zsh[oh-my-zsh]学习整理/
categories:
- 工程师技能
tags:
- zsh
- Linux
- shell

---

## I. 安装

```
apt-get install zsh
apt-get install git-core

git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh

cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

chsh -s `which zsh`

sudo shutdown -r 0
```

<!--more-->
### 配置文件

- 全局配置文件: `~/.zshrc`
- oh-my-zsh目录: `~/.oh-my-zsh/`

## II. 插件

### 添加插件:

编辑`~/.zshrc`中的plugins字段。默认是:`plugins=(git)`默认已经添加了git插件。如果需要添加插件，只要在括号里添加即可，如:`plugins=(git autojump)`

### 插件目录:

```
~/.oh-my-zsh/plugins
```

如想要修改`git`插件的带的`git`相关别名或其他配置，只需要编辑:`~/.oh-my-zsh/plugins/git/git.plugin.zsh`文件即可

### 推荐插件

- **git**: git着色、git别名
- **autojump**: 根据目录名称中的几个关键字符串，快速跳转到以前访问过的对应的目录
- **vi-mode**: vim 模式
- **atom**: 快速用atom打开当前目录
- **zsh-autosuggestions**: 类似FishShell的根据历史纪录给出输入建议，该插件需要[单独安装](https://github.com/zsh-users/zsh-autosuggestions)，我是配置"ctrl"+"空格"为选择快捷键，因此在`~/.zshrc`中添加`bindkey '^ ' autosuggest-accept`即可

## III. 主题配置

这是我目前的主题配置情况:

![](/img/maintain-website-server-1.png)

主题
采用的是[powerlevel9k](https://github.com/bhilburn/powerlevel9k)主题，色系是[Neutron](https://github.com/Ch4s3/iTerm2-Neutron)。

字体
2022.11月之前我使用的是: [这里](https://github.com/powerline/fonts/tree/master/SourceCodePro)下载`Source Code Pro Powerline xxx`

2022.11月后由于重度实用spacevim，上面那个字体对一些符号支持不太好，改用了`hack-nerd`这款字体:

```
brew tap homebrew/cask-fonts
brew install font-hack-nerd-font --cask
```

无论是主题、字体还是色系，这边都需要在iTerm2的设置中(Profiles)进行配置。

样式配置(在`~/.zshrc`中添加):

```
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status time)
POWERLEVEL9K_TIME_FORMAT="%D{%H:%M:%S}"
POWERLEVEL9K_NODE_VERSION_BACKGROUND='022'
POWERLEVEL9K_SHORTEN_DIR_LENGTH=2
```

> 更多可参看: [主题](https://github.com/robbyrussell/oh-my-zsh/wiki/Themes)、[色系](https://github.com/mbadolato/iTerm2-Color-Schemes)

---

- [入坑SpaceVim之：解决乱码](https://www.jianshu.com/p/8bc57f7095ef)
