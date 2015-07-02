title: Git学习整理
date: 2015-03-16 07:51:03
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
`git push [<远程库分支名>] [<标签名>]`

- 效果: 将标签推送到远程库分支

`git push [<远程库分支名>] --tags`

- 效果: 将本地所有标签推送到远程库分支
	
`git push [<远程库分支名>] :refs/tags/[<标签名>]`

- 效果: 将删除的标签同步到远程库分支

## X. 其他需要注意的

1. 由于Mac下文件名大小不敏感，造成git下如果改了名字，git不识别有变化，因此改名字需要使用下面命令:

`git mv --force myfile MyFile`

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

## XI. GitHub

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
----

> 最后如果想要完整学习的，推荐这个站点: http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000