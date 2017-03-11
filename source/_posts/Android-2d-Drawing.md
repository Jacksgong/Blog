title: Android 2d-Drawing
date: 2015-04-18 08:35:03
permalink: 2015/04/18/Android-2d-Drawing
categories:
- Android UI交互
tags:
- Android
- 2d
- drawing
- canvas

---

## Android触发2d绘制的一般方式

### I. 由系统触发的一般View层级绘制

#### 哪些场景?

1. 静态的图形
2. 预定义的动画

### II. 由Canvas的调用触发

#### 哪些场景?

1. 一般的重绘或者一般的动态动画(如:视频、游戏)

<!--more-->

#### 哪些方式?

1. 一般UI线程中调用( `View.onDraw()` )
2. 非UI线程中调用( SurfaceView suport )

## Canvs

> 可控制的画布，所有的Canvas绘制调用会保存在画布上

### 需要注意的

- Android 中所有的View视图，其实最终都是在Canvas这个画板上画出来的
- View在绘制时，父组件调用dispatchDraw(Canvas)分发给各个子组件
- `canvas.translate(int, int)` 当前原点位置
- `canvas.clipRect(int, int, int, int)` 可见范围
- Android.animation 实际上 改变canvas的matrix以及通过clipRect改变可见范围，大小与布局并没有实质改变
- matrix矩阵的作用：对每个坐标点(x, y)转换为另外(x', y')
- Canvas.translate(int, int) 效果相同 matrix.postTranslate(int, int)

## 硬件加速原则

> 能使用GPU来加速2D图像的渲染速度

### 需要注意

> 针对自定义的View，硬件加速可能导致渲染错误，所以自定义View测试后不支持就需要在自定义View上关闭硬件加速

#### 会导致以下已知问题:

1. MenuDrawer和WebView结合使用时，发现当关闭MenuDrawer菜单没有选择任何项时，在webview中显示的内容会出现View错位(打开菜单时没有显示的区域还是没有显示)。
2. 在某些Andorid 4.0上，在View刷新时会出现花屏或者部分View错位，错误日志: `OpenGLRenderer: 0x501`

### 关闭硬件加速:

#### 1. 在Application中控制全局

```
<application android:hardwareAccelerated="false" ...>
```

#### 2. 在Activity中控制

```
<activity android:hardwareAccelerated="false" />
```

#### 3. Window级别控制

```
getWindow().setFlags(
    WindowManager.LayoutParams.FLAG_HARDWARE_ACCELERATED,
    WindowManager.LayoutParams.FLAG_HARDWARE_ACCELERATED);
```

#### 4. View级别控制

```
myView.setLayerType(View.LAYER_TYPE_SOFTWARE, null);
```
或
```
<View xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:orientation="vertical"
    android:paddingLeft="2dp"
    android:layerType="software"
    android:paddingRight="2dp" >
```

---
