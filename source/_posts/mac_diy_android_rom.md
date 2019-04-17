title: Mac下定制Android ROM
date: 2019-04-17 09:49:03
updated: 2019-04-17
categories:
- Android机制
tags:
- ROM
- ext4

---

{% note info %} 我们经常可以在网络上看到各类的魔改ROM，甚至在Windows上有很多定制ROM的工具，只不过这些工具都会在最终打包的时候内置一些广告应用作为系统应用甚至病毒，实际上这些工具无非就是对常规的各类`img`文件进行挂载、重打包的过程，由于编译出来的ROM的目录结构大同小异，因此不用做太多的适配，无非都是删除一些系统内置应用、添加所谓杜比音效包、添加Xposed框架、Root之类的(有关Android Root可以参看[这篇文章](https://blog.dreamtobe.cn/android-root/))。由于我常年使用Mac，今天我们就来看看在Mac下如何对ROM进行修改编辑以及重打包吧。 {% endnote %}

<!-- more -->

## I. Android开机过程

```
加载boot.img(加载linux内核，建立文件系统) => 加载recovery.img或system.img
```

## II. 常见img

### 1. `system.img`

- 系统镜像，包含所有app；二进制文件；字体；配置文件；核心库等；(除kernel外所有android项目)；
- AOSP中`out/target/product/$PRODUCT/system`目录下所有文件打包而来
- 通常为Android Sparse Image或者Ext4文件

结构:

- **system/app:** android出厂内置应用在此，同时，在这里的app可以获得一些特别的权限。
- **system/framework:** android框架在此，不宜乱动，开发者可以使用adb push + 拔电池开关机可以快速验证问题。（前提是eng版本)

### 2. `userdata.img`

- 保存用户，应用信息
- AOSP中`out/target/product/$PRODUCT/data`目录下所有文件打包而来
- 通常为Android Sparse Image或者Ext4文件

结构:

- **/data/app:**  所有安装后的app会移至此处，apk被拆成dex和apk，dex为目标文件，apk为资源包
- **/data/data:** 应用程序内部存储信息，sharepreference、database，etc

### 3. `ramdisk.img`

- Android的根文件系统
- AOSP中`out/target/product/$PRODUCT/root`目录所有文件打包而来
- 通常为gzip压缩文件(`gzip -S .img -d ramdisk.img`)，解压缩后为cpio文档(`cpio -i -F ramdisk`)

结构:

- **./default.prop:** 保存一些调试参数，对于开发者相当重要
- **./init.rc:** 一些启动参数
- **./system:** system.img挂载点
- **./data:** userdata.img挂载点

### 4. `recovery.img`

按power键+音量上键（android默认）可以进去，可以执行T卡升级，format，backup userdata,restore userdata

### 5. `boot.img`

包含一个Linux kernel(maybe named as zImage)和一个ramdisk.img文件结构在源码`system/core/mkbootimg/bootimg.h`中声明

- Unpack工具: [Split_bootimg.pl](http://www.mediafire.com/?i4omee9loaxawtk)
- Repack工具: [Repack_bootimg.pl](http://www.mediafire.com/?sthhkkkkctdvb3d)

解包后是一个gzip，可以用tar直接解。

## III. 从已有系统中导出img

这里我们以导出`system.img`为案例，我们通常通过修改`system.img`来进行编辑系统行为。

首先通过`adb shell`通过`adb`指令连接手机并进入其`shell`环境。

### 1. 查看系统挂载

```
cat /proc/mount
```

### 2. 将system的挂载导出

```
cat /dev/mtd/xxx > /sdcard/system.img
```

此时会发现导出的`system.img`是一个`ext4`格式的镜像文件。

## IV. 挂载修改

这里我们在Mac下对`system.img`进行挂载以便于修改其中的内容。

Mac上的挂载问题还是一个挺大的问题的。首先我们要做到的是在macOS Mojava上可以挂载可读可写，因此[ext4fuse](https://github.com/gerard/ext4fuse)就不work了，虽然可以正常挂载ext4格式，但是却不可读。

这边实测使用另外两个工具可以符合条件:

- 付费的[extFS](https://www.paragon-software.com/zh/home/extfs-mac/)
- 免费开源的[fuse-ext2](https://github.com/alperakcan/fuse-ext2)

### 1. 格式了解

开始之前我们先要了解从一般的ROM刷机文件zip包解压缩出来的img格式，通常拥有以下几种格式:

我们可以通过`file`指令来确定其格式，如:

```
file system.img
```

- `Linux rev 1.0 ext4 filesystem data`: raw文件
- `VMS Alpha executable`: yaffs2文件(通常GB版本，使用mkyaffs与unyaffs进行生成与解包)
- `Android sparse image`: Android稀疏镜像文件

我们先可以通过[simg2img](https://github.com/anestisb/android-simg2img)将`Android sparse image`格式转化为`raw`文件:

```
simg2img system.img system.raw
```

如果是`system.new.dat`以及`system.patch.dat`就需要用到[sdata2img](https://github.com/xpirt/sdat2img)这个工具:

```
python sdat2img.py system.transfer.list system.new.dat system.img
```
打包`system.img`为`transfer.list`与`new.dat`使用工具[img2sdat](https://github.com/xpirt/img2sdat)，可以将`Android Sparse Image`转为标准的`data`

```
python img2sdat.py system.img -o tmp -v 4
```

然后我们安装`fuse-ext2`，因为我们可以通过该工具免费的读写`ext4`格式的`raw`文件。

### 2. 安装`fuse-ext2`

先通过以下方式安装相关依赖:

```
brew install homebrew/dupes/m4
brew install e2fsprogs automake autoconf libtool
```

下载macOS Mojava的[git patch](https://github.com/alperakcan/fuse-ext2/files/2576060/0001-Fix-new-Xcode-compilation.patch.txt)文件(该文件来自[该issue](https://github.com/alperakcan/fuse-ext2/issues/81#issuecomment-438235743))，然后到fuse-ext2项目目录通过`git apply 0001-Fix-new-Xcode-compilation.patch.txt`生效diff，生效后进入`fuse-ext2`项目目录，然后执行:

```
./autogen.sh
CFLAGS="-idirafter/$(brew --prefix e2fsprogs)/include -idirafter/usr/local/include/osxfuse" LDFLAGS="-L$(brew --prefix e2fsprogs)/lib" ./configure
make
sudo make install
```

### 3. 挂载`ext4`

安装后，就可以通过`fuse-ext2`指令进行可读写挂载了。

```
fuse-ext2 system.raw system -o allow_other -o rw+
```

### 4. 重打包

最早是使用`make_ext4fs`进行重打包，因为网络上面到处都是使用这个对相关目录进行重打包，但是一直都是遇到一个问题:

```
can't set android permissions - built without android support
```

实际上，这里我们完全不用重新对目录进行重打包，只需要将挂载的`ext4`格式的`img`转成`Android Sparse Image`就可以了。这里直接使用前面下载的[img2simg](https://github.com/anestisb/android-simg2img)即可:

```
img2simg system.raw system_new.img
```

当然如果需要将`ext4`转为`dat`文件可以通过:

```
rimg2sdat system.img
```

### 5. 取消挂载

```
diskutil unmountDisk system/
```

> 对于一些img而言，需要进行压包签名，由于篇幅原因这里就不做拓展。

---

- [gerard/ext4fuse](https://github.com/gerard/ext4fuse)
- [imgtool](http://newandroidbook.com/tools/imgtool.html)
- [Extracting Android Factory Images on macOS](https://medium.com/@chmodxx/extracting-android-factory-images-on-macos-cc61e45139d1)
- [Mounting an Android system.img on Mac OS X](https://solumachines.wordpress.com/2015/08/15/mounting-an-android-system-img-on-mac-os-x/)
- [解压 Android 系统中的 system.img](https://www.jianshu.com/p/db70835d41c8)
- [macOS系统上读写Linux的ext4分区方法](https://zhuanlan.zhihu.com/p/45097848)
- [How do I install fuse-ext2 to use with OSXFuse](https://apple.stackexchange.com/questions/226981/how-do-i-install-fuse-ext2-to-use-with-osxfuse)
- [Android 镜像的解包](https://quanzhuo.github.io/2017/01/19/android-images/)
- [OSX分析rom刷机包](http://www.petershi.net/archives/2570)
- [如何制作Ext4文件系统镜像](https://blog.csdn.net/q123456789098/article/details/51912015)
- [android解析 ramdisk.img boot.img system.img](https://blog.csdn.net/wzw88486969/article/details/9350545)
- [How to unpack, edit and repack boot.img](https://forum.xda-developers.com/showthread.php?t=1159878)
- [从android手机中拷贝出system.img文件](https://vvsongsunny.iteye.com/blog/888994)
- [Android定制ROM，内嵌su和xposed](https://juejin.im/post/5a333ab55188251b950eb9ba)
- [各种ROM下载](http://www.romjd.com/)
- [9008工程线制作教程(实测整理)](https://wenku.baidu.com/view/7fb1e6617f21af45b307e87101f69e314232fa51.html)
- [windows Rom助手](http://www.romzhushou.com/)
- [内置Xposed](https://www.zhihu.com/question/30587181)
- [加Root](https://ahui3c.com/578/%E5%B0%8F%E7%B1%B3-3-miui-%E7%A9%A9%E5%AE%9A%E7%89%88-rom-%E6%89%8B%E5%8B%95%E5%8A%A0%E5%85%A5-root-%E4%BF%AE%E6%94%B9%E6%96%B9%E6%B3%95)
- [破解以及修改各类ROM](http://bbs.xiaomi.cn/t-11304836)
