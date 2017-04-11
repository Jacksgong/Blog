title: NDK与JNI
date: 2015-11-08 23:16:03
permalink: 2015/11/08/ndk
categories:
- Android Native Develop
tags:
- ndk
- jni
- Android
- C
- C++

---

{% note info %}本文比较全面的介绍了NDK与JNI的使用与基础知识。{% endnote %}

<!-- more -->

## I. 初识

#### 1. NDK

> Native Development Kit

是一套让你的Android应用一部分代码可以使用像C/C++语言的工具包。

**一般什么时候可以使用NDK**

> 谷歌建议真正要使用NDK的情况是在很少数情况。

- 需要提高执行性能（e.g. 大数据排序）
- 需要使用c/c++实现的第三方库（如 Ffmpeg，OpenCV）
- 需要调用更加底层的代码(如，你想调用Dalvik以外的代码)

#### 2. JNI

> Java Native Interface

是一套在Java虚拟机控制下代码执行的标准机制。使得Java可以调用c/c++的方法，或者c/c++中可以调用Java。

**JNI标准机制的实现**

由汇编或c/c++的代码，组装(assembled)成动态库(允许非静态绑定），由此实现Java与c/c++双向调用。

**JNI的优势**

相比其他类似的(Netscape Java运行接口、Microsoft的原始本地接口、COM/Java接口)相比，它的优势在于兼容性:

- 对二进制兼容(c/c++的代码编译后是二进制，由于二进制是程序兼容性类型(不用改变执行文件，就可以直接在不同环境下执行)，所以c/c++编译后的代码可以在任何平台下执行)
- 对所有用Java虚拟机的具体平台兼容

## II. 基本知识

为了更清晰，本地(虚拟机所在环境原生语言(通常是c/c++))这里都用native单词表示，而不直译。

### 参数与引用

#### 1. 方法参数说明

虚拟机需要追踪所有传递到native层的参数，使得GC不会在native层还在用这些参数引用的时候被清除了。

**需要注意**

1. 原始类型直接通过相互拷贝传递
2. 对象 通过引用传递

**JNI原始类型**

Java类型 | Native类型 | 备注
:-: |:-: |:-:
boolean | jboolean | unsigned 8 bits
byte | jbyte | signed 8 bits
char | jchar | unsighned 16 bits
short | jshort | signed 16 bits
int | jint | signed 32 bits
long | jlong | signed 64 bits
float | jfloat | 32 bits
double | jdouble | 64 bits
void(指针/对象引用) | void | N/A

**JNI对象引用关系**

![](/img/ndk-1.png)

**JNI接口指针**

![](/img/ndk-2.png)

P.S. 上图的JNI函数表就好像C++的虚方法表一样。虚拟机可以运行多张JNI函数表(如一张用于调试，另外一张用于调用)。

**例子**

```java
/**
 * @param *env JNI接口指针
 * @param obj 在native方法中定义的对象引用
 * @param i 原始类型 整数型
 * @param s 对象引用 string
 */
jdouble Java_pkg_Cls_f__ILjava_lang_String_2 (JNIEnv *env, jobject obj, jint i, jstring s)
{
     const char *str = (*env)->GetStringUTFChars(env, s, 0);
     (*env)->ReleaseStringUTFChars(env, s, str);
     return 10;
}
```

#### 2. 其他引用类型说明

> JNI定义了三种引用类型: 局部引用、全局引用、全局弱引用。

**局部引用**

- 所有通过JNI方法返回的Java对象都是局部引用
- 局部引用只对创建该引用所在线程可见

局部引用在方法结束时释放，但是也可以调用JNI方法`DeleteLocalRef`对其马上进行释放。

**全局引用**

只有在主动调用释放方法时才释放，对其释放的JNI方法: `DeleteGlobalRef`; 创建全局引用的方法: `NewGlobalRef`。

**例子**

```
jclass localClazz;
jclass globalClazz;

localClazz = (*env)->FindClass(env, "java/lang/String");
globalClazz = (*env)->NewGlobalRef(env, localClazz);

// 立即释放localClazz局部引用
(*env)->DeleteLocalRef(env, localClazz);

// 立即释放globalClazz全局引用
(*env)->DeleteGlobalRef(env, globalClazz);
```

### 错误机制

JNI不会像Java一样检测像`NullPointerException`、`IllegalArgumentException`、`ArrayIndexOutOfBoundsException`、`ArrayStoreException`等这样的错误。

**不报错原因**

1. 错误检测会导致性能下降
2. 在大多数C库函数中，很难对错误进行处理

**处理方式**

> JNI允许使用Java的异常处理。

处理JNI函数中对应的出错的代码(因为即使出现异常, JNI层只会返回错误码，自己并不会报异常), 然后在JNI函数中错误对象抛异常到Java层(根据返回的错误代码)。

```
// 如果是一些数组操作的异常，可以使用ArrayIndexOutOfBoundsException、ArrayStoreException
jthrowable ExceptionOccurred(JNIEnv *env);
```

### JNI的编码

- 标准UTF-8主要用在C，而Java使用的是UTF-16
- JNI 使用的是 修改过的UTF-8: [Modified UTF-8 Strings](https://docs.oracle.com/javase/8/docs/technotes/guides/jni/spec/types.html#modified_utf_8_strings)

**结果**

被编码过的"修改过的UTF-8"字符串只包含非空ASCII字符串，其中每个字符只需一个字符就可表示。但是所有的Unicode字符串都可以被表示。

**与标准UTF-8的差别**

1. `null`字符(0)使用两个字节的格式而非一个字节进行编码，因为修改过的UTF-8不再有嵌入的null(`\0`)。
2. 只使用标准UTF-8的一字节、两字节、三字节的格式，而四字节的将使用两个三字节来代替表示。


### JNI函数

- JNI接口不仅仅包含数据集(dataset)，也包含了它的大量方法。
- 官方文档: http://docs.oracle.com/javase/6/docs/technotes/guides/jni/spec/functions.html

**例子**

```
#include <jni.h>
...
//用于创建与销毁Java虚拟机的接口指针
JavaVM *jvm;

// 包含大多数的JNI函数的JNI接口指针
JNIEnv *env;

// 存储Java虚拟机的参数
JavaVMInitArgs vm_args;

// 存储Java虚拟机的配置选项
JavaVMOption* options = new JavaVMOption[1];
options[0].optionString = "-Djava.class.path=/usr/lib/java";

// 初始化Java虚拟机参数
vm_args.version = JNI_VERSION_1_6;
vm_args.nOptions = 1;
vm_args.options = options;
vm_args.ignoreUnrecognized = false;

// 载入Java虚拟机，返回JNI接口指针给*env
JNI_CreateJavaVM(&jvm, &env, &vm_args);

// 释放 Java虚拟机配置选项
delete options;

// 调用Java虚拟机中的Main#text方法
jclass cls = env->FindClass("Main");
jmethodID mid = env->GetStaticMethodID(cls, "test", "(I)V");
env->CallStaticVoidMethod(cls, mid, 100);

// 释放Java虚拟机
jvm->DestroyJavaVM();
```

### JNI线程

运行在Linux(Android)上的所有线程统一由内核管理的。

**JNI中的线程附加到虚拟机中**

我们可以通过`AttachCurrentThread`和`AttachCurrentThreadAsDaemon`函数将线程附加到虚拟机中，以保证可以正常访问JNI接口指针(JNIEnv)(注意上文JNI接口指针那张图提到的JNI接口指针只在当前线程可见)。

**需要注意**

Android将不会主动释放在JNI中创建的线程(GC不会对其进行主动释放)，所有一定要记得不用时，主动调用`DetachCurrentThread`方法，进行释放。

### Java中调用native方法

**需要注意**

- 在方法前需要保留关键字`native`
- Google建议方法名带`native`前缀，如`nativeGetStringFromFile`

**例子**

```
native String nativeGetStringFromFile(String path) throws IOException;
native void nativeWriteByteArrayToFile(String path, byte[] b) throws IOException;
```

## III. 项目结构

项目结构一般如下图:

![](/img/ndk-3.jpeg)

**需要注意**

- 所有的native代码都存储在jni文件夹下
- 每个子目录对应一种处理器架构
- 如果只带有armeabi，将对armeabi-v7a默认支持（通常只带armeabi的话，armeabi-v7a架构的处理器也支持，只是多一步翻译的过程，也会因此速度会变差）
- 假若你有多种库(so文件)，要么支持处理器架构的，同时都支持，要么同时都不支持。例子: 如果`a.so`一个带了mips的，`b.so`的没有带，则在mips处理器架构的手机上，执行到需要`b.so`的地方，发现在mips中找不到`b.so`，就会crash

**针对简单的Android项目, 创建native项目**

1. 创建jni文件夹，用于存储native源代码
2. 创建`Andorid.mk`文件，用于构建项目
3. 创建`Application.mk`文件（非必须），用于存储编译配置相关，能够灵活的配置编译。

#### 1. `Android.mk`

- 构建native项目的`MAKEFILE`文件
- 官方介绍: https://developer.android.com/intl/zh-cn/ndk/guides/android_mk.html

**例子**

```
# 通过函数调用my-dir返回当前目录文件所在路径
LOCAL_PATH :=$(call my-dir)

# 清理所有除LOCAL_PATH以外的变量，由于所有文件的编译都是在同一个全局的GNU MAKE中执行的，所以这些变量都是全局的
include$(CLEAR_VARS)

# 所输出模块的名称，这里定义的是NDKBegining，
# 编译完成后会在libs目录下创建libNDKBeginin库(Android给这加了前缀lib，但是要注意在java代码中申明时不用带这个前缀)
LOCAL_MODULE    := NDKBegining

# 列出需要被编译的源码文件
LOCAL_SRC_FILES := ndkBegining.c \
                ndkBegining2.c

# 将要输出的模块类型
include$(BUILD_SHARED_LIBRARY)
```

**自定义变量**

可以在`Android.mk`中定义自定义变量，但是必须使用规范前缀: `LOCAL_`、`PRIVATE_`、`NDK_`、`APP_`、`MY_`(Google推荐)。

```
# 定义了自定义变量$(MY_SOURCE)
MY_SOURCE := MYNDKfile.c

# 将$(MY_SOURCE)变量连接起来到$(LOCAL_SRC_FILES)
LOCAL_SRC_FILES += $(MY_SOURCE)
```

#### 2. `Application.mk`

- 用于定义多种变量使得编译更加灵活的MAKEFILE文件
- 官方文档: https://developer.android.com/intl/zh-cn/ndk/guides/application_mk.html

```
# (可选变量)
# 指定是debug或是release
# debug: 用于调试，将生成未被优化的二进制机器码
# release: 将生成优化后的二进制机器码，默认是release，但是默认值会受manifest<application>中的android:debuggable影响
APP_OPTIM := release

# 定义另外的Android.mk的路径
# APP_BUILD_SCRI :=

# (最重要的变量之一)，用于罗列目标编译的处理器架构。默认是armeabi
# NDK 7或以上版本，直接指定APP_ABI := all就可以覆盖所有的架构，不用一一枚举
APP_ABI := armeabi armeabi-v7a x86 mips

# 目标平台名称
APP_PLATFORM := android-9

# 申明需要使用的C++标准库(Android默认只提供了精简的`libstdc++`)
APP_STL := stlport_shared

# GCC编译器版本
# NDK_TOOLCHAIN_VERSION := 4.9
```

**APP_ABI**

架构 | 参数名
- | -
FPU指令集基于ARMv7 | armeabi-v7a
ARMV8 AArch64 | arm64-v8a
IA-32 | x86
Intel64 | x86_64
MIPS32 | mips
MIPS64(r6) | mips64

**APP_STL**

更多C++ Library Support可以参考这里: https://developer.android.com/intl/zh-cn/ndk/guides/cpp-support.html#runtimes

```
# static STLport library
APP_STL := stlport_static

# shared STLport library
APP_STL := stlport_shared

#default C++ runtime library
APP_STL := system
```

#### 3. `NDK-BUILDS`

- 基于`GNU MAKE`的封装
- 官方文档: http://developer.android.com/intl/zh-cn/ndk/guides/ndk-build.html

```
# 清除之前生成的二进制文件
clean

# 强制进行debug构建(如果是要release构建: NDK_DEBUG=0)，如果没有指定，将会受到Manifest.xm中的android:debuggable影响(Google不建议使用android:debuggable参数，如果使用的是NDK版本大于8)
NDK_DEBUG=1

# 用于调试的时候，显示NDK内部的log信息
NDK_LOG=1

# 强制指定使用32位(如果系统支持，默认将会使用64位)
NDK_HOST_32BIT=1

# 编译的时候使用一个特殊的Application.mk的路径
NDK_APPLICATION_MK=<file>

```

**NDK_HOST_32BIT**

64-Bit and 32-Bit Toolchains: http://developer.android.com/intl/zh-cn/ndk/guides/ndk-build.html#6432

## IV. JNI实践

- **Sample: hello-jni:** https://developer.android.com/ndk/samples/sample_hellojni.html#ap
- **Create Hello-JNI with Android Studio:** https://codelabs.developers.google.com/codelabs/android-studio-jni/index.html#0

#### 1. 简单的JNI

可直接参照: https://github.com/Jacksgong/android-ndk#i-sample-try-hello-jni

- **Sample: hello-jni:** https://developer.android.com/ndk/samples/sample_hellojni.html#ap
- **Create Hello-JNI with Android Studio:** https://codelabs.developers.google.com/codelabs/android-studio-jni/index.html#0

#### 2. 引用已有库拓展

可直接参照: https://github.com/Jacksgong/android-ndk#ii-reference-prebuilt-libraries-hello-libs

- **Using Prebuilt Libraries:** https://developer.android.com/ndk/guides/prebuilts.html
- **Android NDK with multiple pre-built libraries:** http://labs.hyperandroid.com/android-ndk-with-multiple-pre-built-libraries

这里提到的引用已有库，是指引用已有的Shared libraries(`.so`)，或是引用已有的Static libraries(`.a`)。

**Shared libraries(`.so`)**

在Windows中是`.dll`, 在OSX中是`.dylib`。

**运行时引用它:** 在Android中，我们只能通过`System.loadLibrary("..")`加载它。

**Static libraries(`.a`)**

在Windows中是`.lib`。

**直接在编译期Link它:** 在Android中，我们可以直接在`Android.mk`中配置，在编译时与我们的代码合成一个`.so`。

---

- [本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/ndk.md)

---

本文已经发布到JackBlog公众号: [Android NDK与JNI - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483711&idx=1&sn=7b3f68b9131b57a6e58925840bacc863)

---
- [Building Your Project](http://developer.android.com/intl/zh-cn/ndk/guides/build.html)
- [Introduction to Android NDK](http://elekslabs.com/2013/12/introduction-into-android-ndk.html)
- [Chapter 5: The Invocation API](https://docs.oracle.com/javase/8/docs/technotes/guides/jni/spec/invocation.html)
- [Android NDK介绍（上）](http://www.importnew.com/8038.html)
- [Android NDK介绍（下）](http://www.importnew.com/8052.html)
- [NDK Application.mk使用手册](http://www.oschina.net/question/565065_93983)
- [Working Around JNI UTF-8 Strings](http://banachowski.com/deprogramming/2012/02/working-around-jni-utf-8-strings/)
- [Java Fundamentals Tutorial: Java Native Interface (JNI)](https://newcircle.com/bookshelf/java_fundamentals_tutorial/_java_native_interface_jni)
- [JNI Functions](http://docs.oracle.com/javase/6/docs/technotes/guides/jni/spec/functions.html)

---
