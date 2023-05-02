title: Workflows Proxy
date: 2014-12-08 08:35:03
updated: 2014-12-08 08:35:03
permalink: 2014/12/08/Workflows-Proxy/
categories:
- 开源项目
tags:
- mac
- proxy
- python
- 代理
- 项目

---

## 1. 准备工具:

- Android Application: fqrouter
- Mac Application: Alfred

## 2. 工具配置

2.1 为Alfred 安装上proxy插件

2.2 进入插件目录，双击Authenticate.app输入Mac的用户名密码（由于代理修改需要权限）

<!--more-->
## 3. 使用

1. fqrouter开启以后，会提示在同一局域网下，配置自动web代理为：http://xxx.xxx.xxx.xxx:2515即可实现翻墙
2. 此时Mac端用Alfred输入对应的即可：


`switch Tencent proxy and Home Proxy `

### 1. Switch to the Tencent Proxy:
![image](https://github.com/Jacksgong/workflows-proxy/raw/master/readme/raw_qq.png)
### 2. Switch to the DIY Home Proxy:
![image](https://github.com/Jacksgong/workflows-proxy/raw/master/readme/raw_diy.png)
### 3. Close Automatic Proxy:
![image](https://github.com/Jacksgong/workflows-proxy/raw/master/readme/raw_off.png)
### 4. Show Automatic Proxy Status:
![image](https://github.com/Jacksgong/workflows-proxy/raw/master/readme/raw_show.png)

## 4. DIY

这个Alfred workflow我是根据我的个人需求定制的，如果需要调整的，可以在对应根目录下的proxy.py进行修改:

```python
__author__ = 'jacksgong'

import sys
import os
from workflow import Workflow, ICON_WEB, web

def main(wf):

    params = wf.args[0]

    # please replace the following value to your own proxy.pac url
    echo_qq = 'http://xxx.xxx/proxy.pac'
    echo_off = 'off'
    echo_pre = 'networksetup -setautoproxyurl Wi-Fi '
    echo_diy_pre = 'http://192.168.'
    echo_diy_end = ':2516'

    if params.startswith('q') :
        wf.add_item(echo_qq,'switch to Tencent proxy',arg =echo_qq,uid=0,valid=True, icon = './qq-proxy.png')
    elif params.startswith('o') :
        wf.add_item(echo_off,'off wifi proxy',arg = echo_off, uid = 0, valid= True, icon = './off.png')
    elif params.startswith('s') :
        status  = os.popen('networksetup -getautoproxyurl wi-fi').read()
        statusList = status.splitlines()
        ip = statusList[0]
        enable = statusList[1]

        wf.add_item(ip,enable, arg =('current status: '+ status),uid = 0)
    else:
        diy = echo_diy_pre + params + echo_diy_end
        wf.add_item(diy,'switch to ' + diy + ' proxy', arg =diy, uid = 0, valid = True, icon = './others-proxy.png')


    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
```

## 5. 开源

GITHUB: https://github.com/Jacksgong/workflows-proxy

---
