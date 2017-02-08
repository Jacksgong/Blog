title: zsh[oh my zsh]
date: 2015-03-29 15:08:03
permalink: 2015/03/29/zsh[oh-my-zsh]学习整理
tags:
- zsh
- Linux
- shell

---

### I. 安装

```
apt-get install zsh
apt-get install git-core

git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh

cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

chsh -s `which zsh`

sudo shutdown -r 0
```

<!--more-->
### II. 配置文件所在路径

##### 全局设置:
`~/.zshrc`

##### 文件地址:
`~/.oh-my-zsh/`

如主题路径: `~/.oh-my-zsh/themes/`

######* 修改主题举例:

如果要修改主题里面的特性。直接编辑`~/.oh-my-zsh/themes/` 下对应主题

如果要选择主题，编辑`~/.zshrc`里面对应的`ZSH_THEME`参数

```
PROMPT='%{$fg_bold[red]%}➜ %{$fg_bold[green]%}%p%{$fg[cyan]%}%d %{$fg_bold[blue]%}$(git_prompt_info)%{$fg_bold[blue]%}% %{$reset_color%}>'

#PROMPT='%{$fg_bold[red]%}➜ %{$fg_bold[green]%}%p %{$fg[cyan]%}%c %{$fg_bold[blue]%}$(git_prompt_info)%{$fg_bold[blue]%} % %{$reset_color%}'
```

其中的`%d`表示绝对路径，`c`表示相对路径

######* 别名添加:

直接在`~/.zshrc`中添加


推荐别名:

```
alias cls='clear'
alias ll='ls -l'
alias la='ls -a'
alias vi='vim'
alias javac="javac -J-Dfile.encoding=utf8"
alias grep="grep --color=auto"
alias -s html=mate   # 在命令行直接输入后缀为 html 的文件名，会在 TextMate 中打开
alias -s rb=mate     # 在命令行直接输入 ruby 文件，会在 TextMate 中打开
alias -s py=vi       # 在命令行直接输入 python 文件，会用 vim 中打开，以下类似
alias -s js=vi
alias -s c=vi
alias -s java=vi
alias -s txt=vi
alias -s gz='tar -xzvf'
alias -s tgz='tar -xzvf'
alias -s zip='unzip'
alias -s bz2='tar -xjvf'
```

### III. 插件

##### 添加插件:
编辑`~/.zshrc`中的plugins字段。默认是:`plugins=(git)`默认已经添加了git插件。

如果需要添加插件，只要在括号里添加即可，如:`plugins=(git autojump)`

##### 插件目录:
`~/.oh-my-zsh/plugins`

如想要修改`git`插件的带的`git`相关别名或其他配置，只需要编辑:`~/.oh-my-zsh/plugins/git/git.plugin.zsh`文件即可

### IV. 其他

#### 推荐使用插件

```
// vim 模式
vi-mode

// 快速用sublime打开当前目录等互动
sublime

```

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
