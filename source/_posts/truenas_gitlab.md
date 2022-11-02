title: Truenas 安装gitlab并且通过trafik进行https转发
date: 2022-11-02 00:54:03
updated: 2022-11-02
categories:
- 网络
tags:
- truenas
- gitlab
- trafik

---

在Truenas的虚拟机里面安装gitlab，然后通过trafik来进行转发，会有点小问题，这里主要做一些记录。

<!-- more -->

## I. 安装gitlab

安装gitlab完全按照[这个教程](https://about.gitlab.com/install/)就行，需要注意的是可以先不指定`external_url`。

大概安装如下:

```
# 第一步
sudo apt-get update
sudo apt-get install -y curl openssh-server ca-certificates tzdata perl

# 第二步，期间选择Internet Site，然后确定就行
sudo apt-get install -y postfix

# 第三步
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash

# 第四步
 sudo apt-get install gitlab-ee
```

## II. 配置gitlab与nginx，并生效

- 假设你外网访问的域名是`gitlab.test.com`
- 假设你内网访问的端口是`:666`

![](/img/truenas_gitlab-f97bdcd4.png)

编辑gitlab配置:

```
sudo nvim /etc/gitlab/gitlab.rb
```

特别主要设置的`external_url`需要是http(原因参考[这里](https://gitlab.com/gitlab-org/omnibus-gitlab/-/issues/2283))，因为我们会用trafik来做https转发。

```
external_url 'http://gitlab.test.com'

gitlab_rails['gitlab_ssh_host'] = 'gitlab.test.com:2222'
```

配置使用自己的Nginx参考[这里就好](https://blog.dreamtobe.cn/maintain-website-server/)

配置好后，编辑nginx中gitlab.conf

```
...
listen 0.0.0.0:666;
listen [::]:666;
server_name gitlab.test.com; ## Replace this with something like gitlab.example.com
...
```

然后生效整体的配置

```
sudo gitlab-ctl reconfigure
sudo nginx -s reload
```

此时在内网通过`[IP]:666`已经可以正常访问。


## III. 通过trafik来进行https转发

1. 通过安装`external-service`来进行达成trafik转发
2. 注意做好外网端口转发

自此就可以进行通过外网访问了。
