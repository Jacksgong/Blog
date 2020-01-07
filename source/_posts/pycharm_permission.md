title: PyCharm Python运行权限问题
date: 2020-01-07 11:30:03
updated: 2020-01-07
categories:
- Tips
tags:
- PyCharm
- Python
- Permission

---

{% note info %} 在PyCharm中安装模块或者是运行，默认都是直接使用`python`执行，一般在当前用户下是没有`sudo`权限的。{% endnote %}

<!-- more -->

## 第一步 创建一个sudo执行脚本

先通过`which python`获得`python`指令所在路径:

```
$ which python
/usr/bin/python
```

如上得到了其所在路径是`/usr/bin/python`，因此我创建了一个文件`~/bin/python-sudo.sh`，然后填入:

```
#!/bin/bash
sudo /usr/bin/python "$@"
```

给到其执行权限:

```
chmod +x ~/bin/python-sudo.sh
```

## 第二步 让当前用户执行`sudo python`不需要输入密码

执行:

```
sudo visudo -f /etc/sudoers.d/python
```

此时会自动创建`/etc/sudoers.d/python`，并打开，我们在其中填写:

```
jacks ALL = (root) NOPASSWD: /usr/bin/python
```

上文将`jacks`替换为你的用户名，保存退出即可。

## 第三步 在PyCharm项目中配置使用`~/bin/python-sudo.sh`

我们打开`Settings`，在`Project Interpreter`中找到设置的图标，然后在下拉中点击`Add..`，选择`Existing environment`，然后配置为我们刚刚创建的`~/bin/python-sudo.sh`文件。

接着在当前项目的`Project Intercepter`选用，刚刚添加的这个即可，如:

![](/img/pycharm_permission-1.jpg)

---

- [Run/Debug as root in PyCharm](https://esmithy.net/2015/05/05/rundebug-as-root-in-pycharm/)
