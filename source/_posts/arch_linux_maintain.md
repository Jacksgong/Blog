title: Arch Linux 维护与配置
date: 2023-10-22 21:08:52
updated: 2023-10-22
permalink: 
categories:
- fun
tags:
- python

---

{% note info %} 为什么要玩Arch Linux？这是我近期加入一些社团后一个主要的矛盾，因为对比Ubuntu，Debian，CentOS等Linux系统来说，各类场景覆盖还不够用吗？直到我深入了解才发现主要是几个原因，这些点也是说服了我去试试这个系统：

1. 超强的可定制性，让我们更好的学习与理解Linux，并且拥有对系统极致的掌控
2. Arch Linux中的软件丰富度并不比另外几款系统来的差，能够达到的能力上限很高很便捷
3. 没有企业参与，又社区推动更加纯粹极客 {% endnote %}

<!-- more -->

![](/img/arch_linux_maintain_31149cf2_0.png)

## I. PVE下安装

可以参考[这篇文章](https://blog.dreamtobe.cn/pve_archlinux/)。

## II. MacbookPro 安装ArchLInux 系统

可以参考[这篇文章](https://blog.dreamtobe.cn/macos_to_archlinux/)。

## III. 系统配置

更新系统

```bash
pacman -Syyu
```

安装帮助文档
```bash
pacman -S man
```

安装基础编译工具
```bash
pacman -S base-devel
```

安装oh-my-zsh
```bash
pacman -S zsh
pacman -S git
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

安装编辑器，用于一会儿`visudo`要用到的编辑器:
```bash
pacman -S neovim
ln -s /usr/bin/nvim /usr/bin/vi
```

添加用户
```bash
useradd -m -G wheel jacks
passwd jacks
visudo
```
![](/img/arch_linux_maintain_09f696a0_1.png)

配置远程ssh访问

```bash
sudo pacman -S openssh
sudo systemctl enable sshd
sudo systemctl start sshd
```

然后在 `~/.ssh/authrozied_keys`中添加你的public key，然后禁用密码登录。
![](/img/arch_linux_maintain_96b02ed8_2.png)

AUR软件管理，可以用[yay](https://github.com/Jguer/yay)来辅助安装，直接参照里面的教程就行了。

[TLP](https://wiki.archlinux.org/title/TLP)用于电量管理（非常有用，会根据CPU等特性进行省电管理）:

```bash
sudo pacman -S tlp
sudo systemctl enable tlp.service
sudo systemctl start tlp.service
```

火狐浏览器
```bash
sudo pacman -S firefox
```

[yay](https://github.com/Jguer/yay)
```baskkkkkh
pacmakkkkkkkn -S --needed git base-devel
gitkk clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

中文字体
```bash
sudo pacman -S wqy-zenhei
# chinese
yay -S wqy-bitmapfont wqy-microhei wqy-microhei-lite wqy-zenhei adobe-source-han-mono-cn-fonts adobe-source-han-sans-cn-fonts adobe-source-han-serif-cn-fonts

yay -S noto-fonts
yay -S nerd-fonts
```

终端
```bash
yay -S st
```

## IV. 桌面服务

#### Deepin

![](/img/arch_linux_maintain_c7b4e98f_3.png)

图形服务:
```bash
sudo pacman -S xorg xorg-server
```

deepin主题
```bash
sudo pacman -S deepin
```

需要注意的是deepin中的`pdfium`与deepin-extra中的`render`是有一些冲突的，建议是先安装deepin，如上面的指令，安装以后，然后再通过`sudo pacman -S deepin-extra`然后选择一些要安装的，比如我就选择了terminal啊之类的安装了。（下面的截图里面的21我独立安装了，其他是后面再进行了一次性安装）
![](/img/arch_linux_maintain_948e7e86_4.png)

确定是否已经有`lightdm`服务
```bash
pacman -Qs lightdm
```

比如启用deepin:
```bash
sudo nvim /etc/lightdm/lightdm.conf
```
然后编辑下一面这行`greeter-session`:
![](/img/arch_linux_maintain_667d9bce_5.png)

启用桌面
```bash
由于前面我们启用了gdm，这里我们使用的是另外一个display-manager，我们可以先把gdm关闭了
sudo systemctl stop gdm.service
sudo systemctl diable gdm.service

# 启用并切换到deepin桌面
sudo systemctl enable lightdm
sudo systemctl start lightdm
```

#### KDE Plasma

> 可参考[该教程](https://itsfoss.com/install-kde-arch-linux/)

![](/img/arch_linux_maintain_614f1425_6.png)

```bash
pacman -S xorg plasma plasma-wayland-session kde-applications
```

安装后启用服务
	
```bash
systemctl enable sddm.service
systemctl enable NetworkManager.service
```

关机
```bash
shutdown now
```

开机，进入系统。

### DWM

> https://suckless.org

![](/img/arch_linux_maintain_85e7dbf4_7.png)

比较方便是每次都是通过源码直接编译，在`config.h`中配置
#### 安装
```bash
git clone git://suckless.org/dwm
cd dwm
sudo make install
```

在安装完后，我们会发现自动已经在`/usr/share/xsessions`目录下添加了`dwm.desktop`文件了。

我这里以我使用sddm管理登录引导+原本是kde plasma的session为案例。需要切换到dwm，可以在开机的时候选择，当然也可以参考[SDDM说明](https://wiki.archlinux.org/title/SDDM)直接修改`/etc/sddm.conf.d/kde_settings.conf`文件:

```conf
[Autologin]
Relogin=false
Session=dwm
```
#### 改用`xinit`来启动

不过这里要留意，由于后面我们有较多需要做开机启动执行的，为了方便，这里推荐使用[`xinit-xsession`](https://wiki.archlinux.org/title/Display_manager#Run_~/.xinitrc_as_a_session)，这样就可以后面直接在`~/.xinitrc`中配置被执行，具体如下:

1. 先安装`x11`与`xinit-xsession`
```bash
sudo pacman -S xorg xorg-xinit
yay -S xinit-xsession
```

2. 将sddm的session配置为`xinit`的，打开`/etc/sddm.conf.d/kde_settings.conf`文件，编辑为:

```conf
[Autologin]
Relogin=false
Session=xinitrc
```

3. 在`~/.xinitrc`的最后加上:
```bash
exec dwm
```

其他不变，重启即可生效。

更新，直接更新仓库，重新执行`sudo make install`编译安装后就完成更新，重启下dwm就生效了。

#### 终端 alacritty

安装
```bash
sudo pacman -S alacritty
```

可以在这里找到关于`alacritty` 的配色 [alacritty themes](https://cloud.tencent.com/developer/tools/blog-entry?target=https%3A%2F%2Fgithub.com%2Feendroroy%2Falacritty-theme)

从 `/usr/share/doc/alacritty/example/alacritty.yml` 拷贝一份到`~/.config/alacritty/alacritty.yml` 作为配置文件，然后找到自己喜欢的配色，修改里面关于color的部分

修改dwm中启动终端的快捷键

```javascript
static const char *termcmd[] = {"alacritty", NULL};
```

#### 程序启动器 rofi

关于`rofi`的主题，可以在这个网站中找到 [rofi theme](https://cloud.tencent.com/developer/tools/blog-entry?target=https%3A%2F%2Fgithub.com%2Fadi1090x%2Frofi)

```javascript
git clone --depth=1 https://github.com/adi1090x/rofi.git
cd rofi
./setup.sh # 安装
```

这里以misc里面的simple_kde主题为例, 在`~/.config/rofi/launcher/misc`中有`launcher.sh` ，找到最后一行

```javascript
rofi -no-lazy-grab -show drun -modi drun -theme $dir/"$theme"
```

将这行写入dwm的配置文件中，修改最后的路径为对应的`.rasi`文件

```javascript
static const char *dmenucmd[] = { "rofi", "-no-lazy-grab","-show", "drun", "-modi", "drun", "-theme", "~/.config/rofi/launchers/misc/kde_simplemenu.rasi", NULL };
```

#### 状态 slstatus

参考官方[教程](https://tools.suckless.org/slstatus/):

```bash
git clone https://git.suckless.org/slstatus
cd slstatus
sudo make install
```

音箱声音
```bash
sudo modprobe snd-pcm-oss
```

#### 其他补丁

- view-on-tag: [dwm - dynamic window manager | suckless.org software that sucks less](https://dwm.suckless.org/patches/viewontag/)
- hide_vacant_tags: [dwm - dynamic window manager | suckless.org software that sucks less](https://dwm.suckless.org/patches/hide_vacant_tags/)
- fullscreen: [dwm - dynamic window manager | suckless.org software that sucks less](https://dwm.suckless.org/patches/fullscreen/)
- alpha: [dwm - dynamic window manager | suckless.org software that sucks less](https://dwm.suckless.org/patches/alpha/)

## V. 各类配置

### [neovim](https://github.com/jdhao/nvim-config)

> 详细建议直接看这个教程，避免有更新: [README.md](https://github.com/jdhao/nvim-config/blob/master/docs/README.md)
> 各类详细使用说明参考[官网](https://github.com/jdhao/nvim-config)

![](/img/arch_linux_maintain_4ce4f0c9_8.png)

```bash
yay -S nerd-fonts
sudo pacman -S python python-pip
sudo pacman -S python-pynvim python-lsp-server python-pylsp-mypy python-pylint
```

安装node
```bash
# Ref: https://johnpapa.net/node-and-npm-without-sudo/
wget https://nodejs.org/dist/v14.15.4/node-v14.15.4-linux-x64.tar.xz

mkdir -p $HOME/tools
# extract node to a custom directory, the directory should exist.
tar xvf node-v14.15.4-linux-x64.tar.xz --directory=$HOME/tools
```

在`.zshrc`中添加

```bash
export PATH="$HOME/tools/node-v14.15.4-linux-x64/bin:$PATH"
```

然后继续各类安装

```bash
source ~/.zshrc
npm install -g vim-language-server
yay -S ctag ripgrep
yay -S flake8 vlint
yay -S neovim
mkdir ~/.config/nvim
cd ~/.config/nvim
git clone --depth=1 https://github.com/jdhao/nvim-config.git .
nvim
```

### dwm配置

可以考虑直接用[这个作者的dwm配置](https://github.com/theniceboy/dwm):

```bash
mkdir ~/code
cd ~/code
git clone git@github.com:theniceboy/dwm.git
cd dwm
sudo make clean install
```

### st配置

可以考虑直接用[这个作者的dwm配置](https://github.com/theniceboy/st):

```bash
mkdir ~/code
cd ~/code
git clone git@github.com:theniceboy/st.git
cd st
sudo make clean install
```

### 其他配置

- `.config`: 可以直接参考[这个](https://github.com/theniceboy/.config)
- `scripts`: [theniceboy/scripts: useful scripts](https://github.com/theniceboy/scripts)
- 里面的`auto_start`可以参考下，包含了背景设置等：[fengdongfa1995/dotfiles](https://github.com/fengdongfa1995/dotfiles)
- [从零开始配置自己的Arch Linux桌面（极简） - 知乎](https://zhuanlan.zhihu.com/p/112536524)
- [dwm美化-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/1998516)
- 图标可以来源[nerd font](https://www.nerdfonts.com/cheat-sheet)，直接拷贝其中的icon即可。


## V. 常见软件推荐

### chrome
```bash
yay -s google-chrome
```

### 壁纸(feh)
```bash
sudo pacman -S feh
```

可以打开浏览器访问[必应首页](https://link.zhihu.com/?target=https%3A//www.bing.com/)，把它的每日一图下载下来当壁纸。图片下载完成以后，进入图片下载目录，使用`feh --bg-fill <filename>`将该图片设置为壁纸。下次登录的时候，设置好的壁纸又会失效，需要在`~/.xinitrc`当中添加一行，使其在启动图形界面后自动设置壁纸。

```bash
~/.fehbg &
```

### 中文输入法（fcitx5）

```bash
sudo pacman -S fcitx5-im fcitx5-chinese-addons fcitx5-qt fcitx5-gtk
```

使用vim打开`~/.bash_profile`，在最后添上：

```bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export INPUT_METHOD=fcitx
export SDL_IM_MODULE=fcitx
```

然后在`~/.xinitrc`当中的`exec dwm`的前面加上：

```bash
fcitx5 -d &
```

加上了这句，才会在启动X窗口时在后台运行`fcitx5`。

打开`fcitx5-configtool`，将`Pinyin`添加到输入法列表当中，可能需要去除仅显示当前语言的勾选项（Only Show Current Language）。然后还可以调整激活输入法、切换输入法的快捷方式等等。

获取更多词库和颜色主题，词库会自动应用，但是颜色主题需要在`fcitx5-configtool`当中配置一下才会生效：

```bash
sudo pacman -S fcitx5-pinyin-zhwiki fcitx5-material-color fcitx5-nord
```

### 支持vim键位的pdf阅读器 

```bash
sudo pacman -S zathura
```

### VNC远程桌面访问

> 参考[官方教程](https://wiki.archlinuxcn.org/wiki/TigerVNC)

```bash
yay -S tigerVNC
```

注意防火墙配置，我们以`:1`的session为案例:
```bash
sudo ufw allow from any to any port 5901 proto tcp
```

配置访问的密码，直接输入`vncpasswd`后进行设置即可，然后可以配置访问时用的用户，可以直接编辑`/etc/tigervnc/vncserver.users`来进行映射，如添加`:1`session的用户为`jacks:

```bash
1:jacks
```

配置session，这里我配置使用的是`xinitrc`的session，编辑`~/.vnc/config`添加如下:

```
session=xinitrc
geometry=1920x1080
```

启动`:1`session的服务:

```bash
sudo systemctl start vncserver@:1
```

此时就可以远程访问了。

## VI. 常见问题处理

### pacman报错

当出现`failed to synchronize all databases ( unable to lock database)`错误时，通常是之前安装过程中出现错误，没有有效的清理缓存，可以通过如下方式解决

```bash
rm -rf /var/lib/pacman/db.lck
```

或者是
```bash
pacman -Scc
```

写在所有分析，并且允许忙碌
```bash
umount -R /mnt
```

### 执行软件出现问题排查

当运行软件出现问题的时候可以通过直接执行对应指令来检查，比如：
我之前运行`sudo systemctl start NetworkManager.service`一直报失败原因也不清晰，后来执行了`sudo /usr/bin/NetworkManager --no-daemon`看到具体输出才知道原来是我之前在`/etc/NetworkManager/NetworkManager.conf`里面的一个配置是错误的，去掉就可以了。

如果引导出现错误，启动不了系统，可以考虑通过安装盘进入，将引导的`efi`挂载到`/mnt`中，然后执行:

```bash
sudo rm -rf /mnt/bootx64.efi
sudo cp /mnt/bootx64_original.efi /mnt/bootx64.efi
```
![](/img/arch_linux_maintain_299675b1_9.png)

### 查看当前一共有哪些字体

```bash
fc-list
```


### 强制卸载包含被依赖的包

```bash
sudo pacman -Rc xxx
```

archlinux关闭自动休眠方法(这里mask的作用可以参考[这个说明](https://www.sunxiaolong.net/linux/archlinux-mask-autosleep/)):

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

如果是笔记本还要防止盖下盖子时被休眠，编辑`/etc/systemd/logind.conf`文件，修改下面几行:
```bash
HandleLidSwitch=ignore
IdleAction=ignore
```

这里需要留意的是几个关键词的定义: `ignore`无任何操作，`poweroff`关机，`suspend`休眠。

### 查看有哪些可用的桌面(session)

```bash
ls /usr/share/xsessions
```

### 查看是否安装了程序（如yay)

```bash
sudo pacman -Qs yay
```

---