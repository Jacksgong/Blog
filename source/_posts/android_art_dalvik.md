title: ART、Dalvik
date: 2015-11-01 12:23:03
tags:
- ART
- Dalvik
- Android
- 安装
- 运行

---
> ART虚拟机的实现在libart.so中，而Dalvik再libdvm.so中
> 实现了Java虚拟机的接口，内部却提供完全不一样的东西， --- 为了兼容。

<!-- more -->

## I. Dalvik

#### dex字节码解释器

逐条逐行的执行字节码指令

#### JIT(Just-In-Time)编译器

当多次运行速度稍慢的代码时，JIT编译器则会自动将热点代码编译并缓存起来，由此执行速度会逐渐加快

## II. ART

> Ahead-Of-Time(AOT)编译

在安装时就已经编译成本地代码，因此只需要编译一次，运行时直接执行（应用运行更快(少去该部分的资源竞争)的同时，更省电）。

- 占用内存空间变大。
- 运行速度更快，且更省电 - 运行程序时无需额外的编译、加载转换等，少去这块的CPU资源竞争。


## III. ART与Dalvik相同之处


接口名 | 备注
-|-
`JNI_GetDefaultJavaVMInitArgs` | 获取虚拟机的默认初始化参数
`JNI_CreateJavaVM` | 在进程中创建虚拟机实例
`JNI_GetCreatedJavaVMs` | 获取进程中创建的虚拟机实例


> `persist.sys.dalvik.vm.lib`: 系统属性，若等于`libdvm.so`则当前使用的是Dalvik虚拟机，若等于`libstart.so`，则当前使用的是ART虚拟机

## IV. ART与Dalvik不同之处

ART执行的是本地机器码 -> 在应用Android安装时进行

虚拟机名 | 安装时 | 每次重新运行apk时 |
:-: | - | - |
ART | 解析翻译dex字节码为本地代码(AOT) | 直接执行本地代码
Dalvik | 将dex字节码优化生成odex文件(`PackageManagerService`请求守护进程`installd`来执行) | 通过解释器(Android 2.2引入JIT(缓存热点代码的解释结果))对dex字节码解释为机器码，再执行机器码


## V. 推敲

### 1. 安装
> 最终安装优化/翻译 结果都是保存在`odex`文件中

![](/img/android_dvm_art-1.png)

> 系统启动时，系统除了对/system/app和/data/app目录下所有apk进行翻译以外，还会对/system/framework目录的apk/jar以及这些apk所引用的外部jar进行翻译，保证不对Dalvik虚拟机产生任何依赖。

### 2. 运行

![](/img/android_dvm_art-2.png)

---

#### 运行相关代码段:

```
// frameworks/base/core/jni/AndroidRuntime.cpp
void AndroidRuntime::start(const char* className, const char* options)
{
    ......

    /* start the virtual machine */
    JniInvocation jni_invocation;
    jni_invocation.Init(NULL);
    JNIEnv* env;
    if (startVm(&mJavaVM, &env) != 0) {
        return;
    }

    ......

    /*
     * Start VM.  This thread becomes the main thread of the VM, and will
     * not return until the VM exits.
     */
    char* slashClassName = toSlashClassName(className);
    jclass startClass = env->FindClass(slashClassName);
    if (startClass == NULL) {
        ALOGE("JavaVM unable to locate class '%s'\n", slashClassName);
        /* keep going */
    } else {
        jmethodID startMeth = env->GetStaticMethodID(startClass, "main",
            "([Ljava/lang/String;)V");
        if (startMeth == NULL) {
            ALOGE("JavaVM unable to find main() in '%s'\n", className);
            /* keep going */
        } else {
            env->CallStaticVoidMethod(startClass, startMeth, strArray);

#if 0
            if (env->ExceptionCheck())
                threadExitUncaughtException(env);
#endif
        }
    }

    ......
}

int AndroidRuntime::startVm(JavaVM** pJavaVM, JNIEnv** pEnv)
{
    ......

    /*
     * Initialize the VM.
     *
     * The JavaVM* is essentially per-process, and the JNIEnv* is per-thread.
     * If this call succeeds, the VM is ready, and we can start issuing
     * JNI calls.
     */
    if (JNI_CreateJavaVM(pJavaVM, pEnv, &initArgs) < 0) {
        ALOGE("JNI_CreateJavaVM failed\n");
        goto bail;
    }

    ......
}
```

```
// libnativehelper/JniInvocation.cpp
#ifdef HAVE_ANDROID_OS
static const char* kLibrarySystemProperty = "persist.sys.dalvik.vm.lib";
#endif
static const char* kLibraryFallback = "libdvm.so";

bool JniInvocation::Init(const char* library) {
#ifdef HAVE_ANDROID_OS
  char default_library[PROPERTY_VALUE_MAX];
  property_get(kLibrarySystemProperty, default_library, kLibraryFallback);
#else
  const char* default_library = kLibraryFallback;
#endif
  if (library == NULL) {
    library = default_library;
  }

  handle_ = dlopen(library, RTLD_NOW);
  if (handle_ == NULL) {
    if (strcmp(library, kLibraryFallback) == 0) {
      // Nothing else to try.
      ALOGE("Failed to dlopen %s: %s", library, dlerror());
      return false;
    }
    // Note that this is enough to get something like the zygote
    // running, we can't property_set here to fix this for the future
    // because we are root and not the system user. See
    // RuntimeInit.commonInit for where we fix up the property to
    // avoid future fallbacks. http://b/11463182
    ALOGW("Falling back from %s to %s after dlopen error: %s",
          library, kLibraryFallback, dlerror());
    library = kLibraryFallback;
    handle_ = dlopen(library, RTLD_NOW);
    if (handle_ == NULL) {
      ALOGE("Failed to dlopen %s: %s", library, dlerror());
      return false;
    }
  }
  if (!FindSymbol(reinterpret_cast<void**>(&JNI_GetDefaultJavaVMInitArgs_),
                  "JNI_GetDefaultJavaVMInitArgs")) {
    return false;
  }
  if (!FindSymbol(reinterpret_cast<void**>(&JNI_CreateJavaVM_),
                  "JNI_CreateJavaVM")) {
    return false;
  }
  if (!FindSymbol(reinterpret_cast<void**>(&JNI_GetCreatedJavaVMs_),
                  "JNI_GetCreatedJavaVMs")) {
    return false;
  }
  return true;
}


extern "C" jint JNI_CreateJavaVM(JavaVM** p_vm, JNIEnv** p_env, void* vm_args) {
  return JniInvocation::GetJniInvocation().JNI_CreateJavaVM(p_vm, p_env, vm_args);
}

jint JniInvocation::JNI_CreateJavaVM(JavaVM** p_vm, JNIEnv** p_env, void* vm_args) {
  return JNI_CreateJavaVM_(p_vm, p_env, vm_args);
}
```

---
#### 安装相关代码段:

```
// frameworks/base/services/java/com/android/server/pm/Installer.java
public final class Installer {
    ......

    public int dexopt(String apkPath, int uid, boolean isPublic) {
        StringBuilder builder = new StringBuilder("dexopt");
        builder.append(' ');
        builder.append(apkPath);
        builder.append(' ');
        builder.append(uid);
        builder.append(isPublic ? " 1" : " 0");
        return execute(builder.toString());
    }

    ......
}
```

```
// frameworks/native/cmds/installd/commands.c
int dexopt(const char *apk_path, uid_t uid, int is_public)
{
    struct utimbuf ut;
    struct stat apk_stat, dex_stat;
    char out_path[PKG_PATH_MAX];
    char dexopt_flags[PROPERTY_VALUE_MAX];
    char persist_sys_dalvik_vm_lib[PROPERTY_VALUE_MAX];
    char *end;
    int res, zip_fd=-1, out_fd=-1;

    ......

    /* The command to run depend ones the value of persist.sys.dalvik.vm.lib */
    property_get("persist.sys.dalvik.vm.lib", persist_sys_dalvik_vm_lib, "libdvm.so");

    /* Before anything else: is there a .odex file?  If so, we have
     * precompiled the apk and there is nothing to do here.
     */
    sprintf(out_path, "%s%s", apk_path, ".odex");
    if (stat(out_path, &dex_stat) == 0) {
        return 0;
    }

    if (create_cache_path(out_path, apk_path)) {
        return -1;
    }

    ......

    out_fd = open(out_path, O_RDWR | O_CREAT | O_EXCL, 0644);

    ......

    pid_t pid;
    pid = fork();
    if (pid == 0) {
        ......

        if (strncmp(persist_sys_dalvik_vm_lib, "libdvm", 6) == 0) {
            run_dexopt(zip_fd, out_fd, apk_path, out_path, dexopt_flags);
        } else if (strncmp(persist_sys_dalvik_vm_lib, "libart", 6) == 0) {
            run_dex2oat(zip_fd, out_fd, apk_path, out_path, dexopt_flags);
        } else {
            exit(69);   /* Unexpected persist.sys.dalvik.vm.lib value */
        }
        exit(68);   /* only get here on exec failure */
    }

    ......
}

static void run_dexopt(int zip_fd, int odex_fd, const char* input_file_name,
    const char* output_file_name, const char* dexopt_flags)
{
    static const char* DEX_OPT_BIN = "/system/bin/dexopt";
    static const int MAX_INT_LEN = 12;      // '-'+10dig+'\0' -OR- 0x+8dig
    char zip_num[MAX_INT_LEN];
    char odex_num[MAX_INT_LEN];

    sprintf(zip_num, "%d", zip_fd);
    sprintf(odex_num, "%d", odex_fd);

    ALOGV("Running %s in=%s out=%s\n", DEX_OPT_BIN, input_file_name, output_file_name);
    execl(DEX_OPT_BIN, DEX_OPT_BIN, "--zip", zip_num, odex_num, input_file_name,
        dexopt_flags, (char*) NULL);
    ALOGE("execl(%s) failed: %s\n", DEX_OPT_BIN, strerror(errno));
}

static void run_dex2oat(int zip_fd, int oat_fd, const char* input_file_name,
    const char* output_file_name, const char* dexopt_flags)
{
    static const char* DEX2OAT_BIN = "/system/bin/dex2oat";
    static const int MAX_INT_LEN = 12;      // '-'+10dig+'\0' -OR- 0x+8dig
    char zip_fd_arg[strlen("--zip-fd=") + MAX_INT_LEN];
    char zip_location_arg[strlen("--zip-location=") + PKG_PATH_MAX];
    char oat_fd_arg[strlen("--oat-fd=") + MAX_INT_LEN];
    char oat_location_arg[strlen("--oat-name=") + PKG_PATH_MAX];

    sprintf(zip_fd_arg, "--zip-fd=%d", zip_fd);
    sprintf(zip_location_arg, "--zip-location=%s", input_file_name);
    sprintf(oat_fd_arg, "--oat-fd=%d", oat_fd);
    sprintf(oat_location_arg, "--oat-location=%s", output_file_name);

    ALOGV("Running %s in=%s out=%s\n", DEX2OAT_BIN, input_file_name, output_file_name);
    execl(DEX2OAT_BIN, DEX2OAT_BIN,
          zip_fd_arg, zip_location_arg,
          oat_fd_arg, oat_location_arg,
          (char*) NULL);
    ALOGE("execl(%s) failed: %s\n", DEX2OAT_BIN, strerror(errno));
}
```
---

- [Android ART运行时无缝替换Dalvik虚拟机的过程分析](http://blog.csdn.net/luoshengyang/article/details/18006645)
- [Dalvik VM vs. ART (Android Runtime): Impact for end-users?](http://android.stackexchange.com/questions/56773/dalvik-vm-vs-art-android-runtime-impact-for-end-users)
- [Dalvik、ART虚拟机小结](http://www.itlipan.info/android/2015/08/07/android-dalvik.html)
- [ART运行时垃圾收集（GC）过程分析](http://blog.csdn.net/luoshengyang/article/details/42555483)
- [浅谈为什么Java运行环境是虚拟机，而Python运行环境是解释器](http://www.xrpmoon.com/blog/archives/jripple1105.html)
