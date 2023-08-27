title: Truenas Scale 指令与apt使用
date: 2023-08-26 15:58:40
updated: 2023-08-27
permalink: 
categories:
- fun
tags:
- python

---

{% note info %} Truenas Scale默认是限制了apt使用，有时候ssh进去不是太方便，因此需要手动的进行做下修改，才能正常安装包，正常在terminal上使用。 {% endnote %}

<!-- more -->
## I. 仓库管理

### 没有找到`apt-get`处理方法

```bash
chmod +x /bin/apt-get
```

### 不是信任仓库解决方法

> https://superuser.com/questions/1331936/how-can-i-get-past-a-repository-is-not-signed-message-when-attempting-to-upgr

```bash
apt-get update --allow-insecure-repositories
```

## II. 改为zsh

```bash
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```

### 安装主题

> https://github.com/romkatv/powerlevel10k#oh-my-zsh

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

### 安装ausosuggestion

> https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#oh-my-zsh

### 安装fzf

```bash
apt-get install fzf
```

然后直接在`~/.zshrc`的`plugins`里面添加`fzf`即可。

## III. 常见Truenas Scale指令

Truenas scale中使用的是轻量的k3s，因此注意管理应用时候需要使用k3s而非k8s。

### 访问k3s的指令

> 更多指令可以参看这里: https://www.truenasscale.com/2021/12/19/340.html

```
k3s kubectl get pods -o wide --all-namespaces
```

![](/img/truenas_scale_command_apt_bde7380e_0.png)

### k3s内应用相互访问的ip

这个是以loki为案例:

```
http://loki.ix-loki.svc.cluster.local:3100
```


### 查看k3s event状态

```
k3s kubectl describe pod openebs-zfs-controller-0 -n kube-system
```

### 刷新时区

```
service ntp restart
ntpq -p
```

![](/img/truenas_scale_command_apt_96c3132f_1.png)
