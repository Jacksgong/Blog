title: Git
date: 2015-03-16 07:51:03
permalink: 2015/03/16/Git学习整理
categories:
- 工程师技能
tags:
- git
- 管理

---

# Git特点:
1. 在2002由Linus花了两周写的，用在Linux版本维护，后来由Linux社区高手维护
2. git是维护修改
3. git是分布式版本控制


<!--more-->
# Git使用
### I. 创建:
##### 本地:
`git init`

- 效果:
创建版本库(.git)

##### 远程:
`git remote add [<远程库分支名>] [<远程库地址>]`

- 效果: 关联本地库与远程库

`git clone [<远程库地址>]`

- 效果: 克隆远程库到本地（包括工作区与版本库）（一般而言只checkout了远程origin分支到本地master分支）.

`git clone -b <远程分支名> <远程库地址>`

- 效果: 克隆远程分支到本地（本地分支名和远程分支名相同）.


##### 分支:

`git branch [<分支名>]`

- 效果: **1** 创建分支; **2** 若没有提供<分支名>直接`git branch`将列出所有分支，并在当前分支前面显示`*`

`git checkout [-b] [<分支名>]`

- 效果: **1** 切换到<分支>(HEAD指针指向[分支]); **2** 若有`-b`则表示创建并切换到<分支>

`git checkout [-b] [<本地分支名>] [<远程分支名>]/[<本地分支名>]`

- 效果: 创建远程分支到本地分支


### II. 提交:
`git add [file]`
`git rm [file]`

- 效果: 将修改/删除添加到版本库中的`stage`的暂存区

`git commit -m [<描述>]`

- 效果: 把暂存区的内容提交到当前分支

`git push [<远程库分支名>] [<本地分支名>]`

- 效果: 把分支内容推到远程库相对应的分支上

##### 合并:

> 推荐merge工具: [p4Merge](https://gist.github.com/tony4d/3454372)

`git merge [<目标分支>]`

- 效果: 与目标分支合并(如果默认优先Fast-forward说明是快进模式（很快的合并）(ps: 该模式如果删掉分支，会丢掉分支信息))

`git merge --no-ff -m [<描述>]`

- 效果: 跳过Fast forward模式，保留版本库中分支结构(`git log --graph`)

`git fetch <远程仓库名> <远程分支名>(:本地新分支名)`

- 效果: 从远程的仓库(通常是`origin`)的分支下载最新版本到 本地的新的分支上，如果不提供默认:下载到 本地分支远程仓库/分支名 (例子: `origin/master`) 上。

`git fetch`和`git pull`

- 区别: `git pull` = `git fetch` + `git merge`

```
// 以下命令等同于 git pull
git fetch origin master
git merge origin/master
```

##### 删除:
`git branch -d [<分支名>]`

- 效果: 删除目标分支（`-D`大写D是强行删除（未进行merge就直接删除时使用））

##### 撤销:
`git reset [<版本参数>] [<文件名>]`

- 效果: 从暂存区撤销某文件的提交

`git checkout -f`

- 效果: 撤销未提交的文件

### III. 状态:
`git status`

- 效果: 显示状态

`git log -1`

- 效果: 查看最后一次提交

`git remote`

- 效果: 远程库信息(`-v`查看详情(fetch地址与push地址))

`git stash`

- 效果: 存储当前工作现场（通常用在:用于工作一半，想要切换分支的时候）

##### 存储现场:
`git stash list`

- 效果: 所有储存的工作现场列表

`git stash apply [<现场id>]`

- 效果: 应用现场id指定的现场

`git stash stop [<现场id>]`

- 效果: 删除现场id指定的现场

`git stash pop`

- 效果: 应用最早的现场，并删除它

### IV. 对比:
`git diff [<文件名>]`

###### 拓展:
`git diff HEAD -- [<file>]`

- 效果: 工作区和版本库分支里的最新版本对比

### V. 日志:
`git log`

- 效果: 查看git日志

`git log -p`

- 效果: 查看git并且显示具体文件修改点

`git commite --amend -m [msg]`

- 效果: 修改上次提交的commit message

###### 查看历史git命令（可以用来找`commit id`）
`git reflog`

###### 简化:
`git log --pretty=online`

###### 查看分支合并图:
`git log --graph`

### VI. 回退代码:
`git reset --hard [commit id/版本参数]`
###### 版本参数定义:
`HEAD`表示当前版本，上一个版本:`HEAD^`,上n个版本就是加n个`^`或者`HEAD~[n]`

###### 拓展:
`git checkout -- [<文件名>]`

- 效果:

```
	如果 暂存区中有该文件:
		替换为暂存区的.
	否则:
		替换为分支上的.

```

`git reset HEAD [file]`

- 效果:  撤销`stage`暂存区中[file]文件的修改

### VII. 冲突
修改好冲突文件后，直接重新提交即可.

冲突文件一般的表示：

```
<<<<<<< HEAD
Head 的内容
=======
分支的内容
>>>>>>> <分支名>
```

> 强烈推荐mergetool: [p4merge](https://gist.github.com/tony4d/3454372)

### VIII. 同步远程
`git pull`

- 效果: 同步远程库（如果提示`no tracking information`，说明本地分支与远程分支的链接关系没有创建，用命令`git branch --set-upstream [<本地分支名>] [<远程分支名>]/[<本地分支名>]`进行创建链接）

### IX. 标签

##### 创建:

`git tag [<标签名>] [<commit id>]`

- 效果: 给对应commit id打上标签，如果不提供comit id，默认给最新一次提交打上标签

`git tag -a [<标签名>] -m [<标签描述>] [<commit id>]`

- 效果: 给对应commit id打上标签，并给标签加上了描述，如果不提供comit id，默认给最新一次提交打上标签
`git tag -s [<标签名>] -m [<标签描述>] [<commit id>]`

- 效果: 给对应commit id打上标签，并给标签加上了描述，并且加上PGP签名，如果不提供comit id，默认给最新一次提交打上标签

##### 显示:

`git tag`

- 效果: 查看所有标签

`git show [<标签名>]`

- 效果: 显示标签那次提交的信息

##### 删除:

`git tag -d [<标签名>]`

- 效果: 删除标签

##### 远程:

> [Push a tag to a remote repository using Git?](http://stackoverflow.com/questions/5195859/push-a-tag-to-a-remote-repository-using-git)

> [How to: Delete a remote Git tag](https://nathanhoad.net/how-to-delete-a-remote-git-tag)

`git push [<远端仓库名>] [<标签名>]`

- 效果: 将标签推送到远程库分支

`git push [<远程库分支名>] --tags`

- 效果: 将本地所有标签推送到远程库分支

`git push [<远端仓库名>] :refs/tags/[<标签名>]`

- 效果: 将删除的标签同步到远程库分支

## X. 子模块

> [使用Git Submodule管理子模块](https://segmentfault.com/a/1190000003076028)

#### 1. 添加子模块:

```
// 添加外部项目为当前项目的子模块, 添加完后，会配置到`.gitmodules`内
git submodule add [<远程库地址>] [<存储本地路径>]
// 添加 .gitmodules 与 新拉下来的子模块文件夹 到 stage.
git add .gitmodules [<子模块目录>]
// 提交对子模块文件的添加
git commit -m "[<描述>]"
// 完成子模块添加
git submodule init
```

#### 2. 修改子模块

```
cd [<子模块目录>]/
// 修改子模块中的文件->提交对子模块中的文件的修改->推到远端
...
// 回到父目录
cd ..
// 提交子模块中的修改->推到远端
```

#### 3. 更新子模块

##### 方式一:

在父项目目录下运行: `git submodule foreach git pull`

##### 方式二:

进入对应的子项目目录: `git pull`

#### 4. 拉取存在子模块的项目

##### 方式一:

在父项目目录下运行: `git clone [<远程库地址>] --recursive`

##### 方式二:

```
// 先clone父项目
git clone [<远程库地址>]
cd [<子模块目录>]
git submodule init
// 拉取子模块 配置文件中的所有子模块文件
git submodule update
```

#### 5. 删除项目中的子模块

```
git rm --cached [<子模块目录>]
rm -rf [<子模块目录]
// 编辑 .gitmodules 删除其中对于要删除的子模块相关的内容
// 提交对应的修改即可
```

## XI. 其他需要注意的

#### 1. 由于Mac下文件名大小不敏感，造成git下如果改了名字，git不识别有变化，因此改名字需要使用下面命令:

`git mv --force myfile MyFile`

#### 2. 如果需要修改提交过的历史用户资料

[Changing author info](https://help.github.com/articles/changing-author-info/)

#### 3. 修改Commit Message

> 当然若修改的那个Commit已经在远端，需要`git push --force`覆盖远端。

- 如果只是修改最后一条Commit Message: `git commit --amend`
- 如果需要修改更早之前的一些Commit Message: `git rebase -i [<Commit Id>]`


# Git 配置

##### 配置文件:

局部: 项目工作区`.git/config`

全局: `~/.gitconfig`

##### 命令配置:

`git config --global color.ui true`

- 效果: Git会适应当地显示不同颜色

##### 忽略特殊文件:

在项目工作区根目录下直接创建`.gitignore`文件然后望里面添加文件名即可

可以参考: [https://github.com/github/gitignore](https://github.com/github/gitignore)

##### 别名配置:

`git config --global alias.[<别名>] [对应命令]`

推荐别名:

```
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD'
git config --global alias.last 'log -1'
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

## XII. GitHub

### fork同步问题

> A项目是B项目的fork，如果同步B项目的更新:

#### 1. 先把B clone到本地

```
git clone B_REPOSITORY_URL
```

#### 2. 再cd到本地B的目录，把A作为一个remote加到本地的B中（一般命名为upstream）

```
git remote add upstream A_REPOSITORY_URL
```

#### 3. pull另一个A的remote（upstream）的相应分支（比如master）就可以

```
git pull upstream master
```

#### 4. 最后push回github的B_REPOSITORY

```
git push origin master
```

## XIII. 其他疑难问题

调用`git fetch`的时候，出现:

```
Auto packing the repository in background for optimum performance.
See "git help gc" for manual housekeeping.
```

你执行`git fack`会发现一堆的挂起的`dangling blob xxxxxxxxxxxxxxx`

此时只需要: **gc** 下 `git gc --prune=now`

----

- [Git教程](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
- [6.6 Git 工具 - 子模块](https://git-scm.com/book/zh/v1/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)
- [Git Submodule的坑](http://blog.devtang.com/blog/2013/05/08/git-submodule-issues/)

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
