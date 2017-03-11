title: Android中尽量不用Storage Permission
date: 2015-11-30 09:00:03
permalink: 2015/11/30/android_storage_permission
categories:
- Android最佳实践
tags:
- FileProvider
- URI
- 演讲

---

> 演讲主题: Forget the Storage Permission
> 演讲者: Lan Lake(Google Android Team Developer, Facebook Developer)
> PPT: [Forget the Storage Permission: Alternatives for sharing and collaborating](https://speakerdeck.com/ianhanniballake/forget-the-storage-permission-alternatives-for-sharing-and-collaborating#stargazers)
> 视频: [Forget the Storage Permission: Alternatives for sharing and collaborating (Big Android BBQ 2015)](https://www.youtube.com/watch?v=C28pvd2plBA&feature=iv&src_vid=BKU-wmTAPdc&annotation_id=annotation_3791593857)

<!-- more -->

----

#### 演讲中提到的权限是什么权限?

文件读写权限

#### 为什么在此时提出?

1. 在Android M中更重视权限，Android M是一个运行时权限管理的模型，并且存储权限会被视为危险权限(当应用想要获取该权限时，会弹窗类似提示: 是否允许该应用访问你的所有图片与视频，并且在存储卡做任何的写操作)；
2. 有效管理文件与文件权限谨慎使用，更有益于健康生态以及用户的数据安全规范；


## I. 文件目录

### 1. Android SDK提供的APP目录

> 在应用卸载时，会清除这些目录

#### 应用私有存储目录:

- `Context.getFileDir()`: 真实数据、用户数据
- `Context.getCacheDir()`: 缓存数据、网络上下载的大图片; 在地存储空间不足的时候，有可能会被清除。

##### 是否需要读写权限申请

< API 19 | API 19-22 | API 23+
:-: | :-: | :-: |
不需要 | 不需要 | 不需要

#### 应用拓展存储目录:

> 所有 应用可读
> 不建议用户存储敏感数据
> 这里的所有目录的写不需要特别的申请权限

- `Context.getExternalFilesDir()`
- `Context.getExternalCacheDir()`
- `Context.getExternalMediaDirs()`: api 21新增，用于存储图片、视频便于媒体相册扫描

> 禁止当前目录以及子目录被相册等扫描，只需要在当前目录新建空文件`.nomedia`即可

##### 是否需要读写权限申请

< API 19 | API 19-22 | API 23+
:-: | :-: | :-: |
需要 | 不需要 | 不需要

> 如果需要只指定< API 19 才申请存储权限，可以使用以下方式

```
<uses-permission
    android:name="android.permission.READ_EXTERNAL_STORAGE"
    android:maxSdkVersion="18" />
<uses-permission
    android:name="android.permission.WRITE_EXTERNAL_STORAGE"
    android:maxSdkVersion="18" />
```

### 2. Android SDK提供的公用目录

- `Environment.getExternalStorageDirectory()`
- `Environment.getExternalStoragePublicDirectory(String)`

##### 是否需要申请读写权限申请

< API 19 | API 19-22 | API 23+
:-: | :-: | :-: |
需要 | 需要 | 需要


---

## II. 文件应用间共享

> 基于URI基本权限(URI-Based Permissions)
> Intent底层架构也是依附于URI基本权限来完成的应用间调用

#### 添加URI基本权限

1. startActivity/startService的时候在Intent中添加Flag(接收者对于该URI的权限(如URI是一个图片，那么接收者就有了该图片的对应权限)): `Intent.FLAG_GRANT_READ_URI_PERMISSION`、`Intent.FLAG_GRANT_WRITE_URI_PERMISSION`
2. 手动调用: `Context.grantUriPermission()`(会使当前包名下所有URI都有了对应权限)、`Context.revokeUriPermission()`(URI撤销权限对应权限)

> 如果是Files URI将会时刻在文件读写权限的保护下，因此即使相互通信了，也还是需要读写权限


### 方式

#### 1. 直接写到公共目录

> 不推荐

发送文件的应用需要有写权限，而接受文件的需要有读权限，然后传输一个路径。

#### 2. FileProvider (support.v4)

> 继承自 ContentProvider，但是非常轻量，所有ContentProvider需要做的多余工作都在FileProvider中已经给我们实现好了

- 发送方与接收方都不需要读写权限申请；
- 接收方可以访问应用文件目录(`getFilesDir()`、`getCacheDir()`、`getExternal*Dir()`)中的所有文件；
- 双方通信是基于URI基础权限，而非文件路径

#### 方式一: 发送者主动发送

> 该权限支持一直传递下去

>  推荐方式

##### 1. 发送端`FileProvider`中的定义:

```
// build.gradle

defaultConfig {
    def filesAuthorityValue = applicationId + ".files"

    // Now we can use ${filesAuthority} in our Manifest
    manifestPlaceholders = [filesAuthority: filesAuthorityValue]

    // Now we can use BuildConfig.FILES_AUTHORITY in our code
    buildConfigField "String", "FILES_AUTHORITY", "\"${filesAuthorityValue}\""
}
```

```
<!-- AndroidManifest.xml -->
<provider
    android:name="android.support.v4.content.FileProvider"
    android:authorities"${filesAuthority}"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```

```
<!-- res/xml/file_paths.xml -->
<!-- 这里定义了以下的路径允许FileProvider访问 -->

<paths>
    <!-- new File(getFileDir(), "internal") -->
    <files-path name="private" path="internal/" />

    <!-- new File(getCacheDir(), "images") -->
    <cache-path name="image_cache" path="images/" />

    <!-- getExternalFilesDir() -->
    <external-path name="external_files" path="files/" />
</paths>
```

##### 2. 发送端的使用

```
// Directory must be in file_paths.xml
File imagePath = new File(context.getFilesDir(), "internal");
File newFile = new File(imagePath, "not_usually_accessible.jpg")
Uri contentUri = FileProvider.getUriForFile(context,
    BuildConfig.FILES_AUTHORITY, newFile);
    // content://${files_authority}/private/not_usually_accessible.jpg

Intent shareIntent = ShareCompat.IntentBuilder.from(activity)
    .setType("image/jpeg").setStream(contentUri).getIntent();
// Provide read access
shareIntent.setData(contentUri);
// 接收者对于Data只有读的权限
shareIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
```

##### 3. 接收端的使用

```
Uri uri = ShareCompat.IntentReader.from(activity).getStream();
Bitmap bitmap = null;
try {
    // Works with content://, file://, or android.resource:// URIs
    InputStream inputStream = getContentResolver().openInputStream(uri);
    bitmap = bitmapFactory.decodeStream(inputStream);
} catch(FileNotfoundException e){
    // Inform the user that things have gone horribly wrong
}
```

---
