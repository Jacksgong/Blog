title: Android绘制
date: 2015-10-20 00:48:03
permalink: 2015/10/20/android-view
categories:
- Android性能与优化
tags:
- Android
- 视图
- View
- 优化
- 重绘

---

## I. 布局简单优化

1. 尽量少的布局层级
2. `LinearLayout`性能比`RelativeLayout` 稍高
3. `ViewStub`代替`include`来引用不常用的布局
4. 用`merge`来代替根节点是`FrameLayout`，并且不需要`background`或`padding`等属性时。
5. 用`merge`来代替`include`的顶节点，这样被引入时顶节点会自动被忽略。

<!-- more -->

## II. 绘制相关深度优化

> 可以通过[Hierarchy Viewer](http://developer.android.com/tools/help/hierarchy-viewer.html)可视化布局，直观的看布局层级分布以及各View `measure`、`layout`、`draw` 的耗时。
> 可以通过[traceview](http://developer.android.com/tools/debugging/debugging-tracing.html)，计算出每个方法所占用的CPU时间。

1. 已知View大小的，自定义View，`onMeasure`时直接`setMeasuredDimension`
2. 已知布局或者其他特定规律的，直接自定义View，达到减少层级，针对性`measure`、`layout`、`draw`
3. 如果布局含有复杂的动画，或者需要复杂的绘制，考虑在独立的绘制线程处理，而不block UI线程，此时考虑`SurfaceView`或`TextureView`(Android 4.0引入)(相比`SurfaceView`而言，可以像常规视图一样被改变)
4. 使用`OpenGL ES` API进行绘制，可以更加针对性的高性能绘图。
5. 如果资源图片比较大，考虑放在`drawable-nodpi`或者直接放在asset，防止获取资源的时候缩放暂用大量内存，也产生不必要的延时。

## III. `LayoutInflater`

- 使用XmlPull来解析
- `rInflate()`方法(中不断递归)遍历根布局下的子布局
- 由于`setContentView`默认是添加到id为`content`的`FrameLayout`中，因此`LyoautParams`有效。


### 最终结果:
是一个完整的DOM结构，返回的是顶层布局。

### 耗时点:

1. 其中的`createView()`方法中通过反射创建出View实例

## IV. 绘制过程

### 开始

`ViewRoot`的`performTraversals()`

### `onMeasure()`

从`measure()`中调用，每个`View`都有一次`measure()`的过程.

参数: 规格和大小: MeasureSpec = specSize | specMode

#### 规格说明:

名称 | 注解
-|-
EXACTLY | 希望子视图大小 由 specSize决定
AT_MOST | 希望子视图大小 保证不超过 specSize
UNSPECIFIED | 希望子视图 任意大小（很少遇到）


#### `widthMeasureSpec`、`heightMeasureSpec`参数由来:

- 一般情况: 由父布局计算得到
- 根布局: 由`getRootMeasureSpec()`处理得到:

根布局给的参数 | 规格 | 大小
-|-
`MATCH_PARENT` | `EXACTLY` | 视窗大小
`WRAP_CONTENT` | `AT_MOST` | 视窗大小
给定大小 | `EXACTLY` | 给定大小

#### `ViewGroup`的`measure`:

> 遍历child View，进行`measureChild`

结合`ViewGroup`的规格与大小，以及child规格与大小获得参数传入`child View`进行子布局的`measure`

#### 结束:
将最终结果通过`setMeasuredDimension`设置最终测量的结果，一次`measure`过程结束

> 注意: `setMeasuredDimension()`后`getMeasuredWidth`和`getMeasuredHeight`才是有效值。

### `onLayout()`

紧接着`measure`之后，就是布局，确定位置。调用`View`的`layout()`方法触发。

#### 决定是否需要`onLayout`

1.  `layout()`中，首先会调用`setFrame()`方法来判断 视图是否发生过变化。
2.  或者`layout()`中，有`LAYOUT_REQUIRED`(请求onLayout)


### `onDraw()`

紧接着`layout()`之后，就是真正的绘制。调用`View`的`draw()`方法触发

#### 步骤一，绘制背景

#### 步骤二，为了淡入淡出做准备（一般没有）

如果有的情况下，一般情况下没有，就是保存canvas的Layers

#### 步骤三，绘制内容

调用`onDraw(Canvas)`，默认是空方法，这一部分是case by case

#### 步骤四，绘制子View

调用`dispatchDraw(Canvas)`，默认空方法，这一部分也是case by case

#### 步骤五，绘制淡入淡出

如果有的情况下，绘制，然后还原canvas的Layer

#### 步骤六，绘制滚动条

其实每个View都可以有滚动条的。

## V. 视图状态

> 这里只提到需要特别注意到的。

> View的视图状态变化，会回调`View#drawableStateChange()`

### focused

- `requestFocus()`不能保证一定能获取到焦点，返回值为`true`才表示获取成功。需要focusable && focusable in touch mode
- 一个界面只有一个焦点

### window_focused

- 应用程序不能改变，由系统控制
- 表示视图是否处于正在交互的窗口中

### selected

- 一个界面中可以有多个选中态

### pressed

- 实际上应用程序也可以通过`setPressed()`方法来控制的

## VI. 状态变化回调

![](/img/android_view-1.png)

## VII. View#invalidate

> 需要注意`invalidate`虽然最终调到`performTraversals()`但是很可能没有 **重新测量标志**，大小没有变化，因此不会执行`measure`和`layout`，只有`draw`可以执行到。
> 相比之下如果希望视图绘制流程完整重新走一遍，需要调用`requestLayout`。

![](/img/android_view-2.png)


---

> ps [第四篇](http://blog.csdn.net/guolin_blog/article/details/17357967)是一些简单的应用层，就没有整理了

----

- [Google I/O 2013 - Writing Custom Views for Android](https://www.youtube.com/watch?v=NYtB6mlu7vA&t=1m41s)
- [Android LayoutInflater原理分析，带你一步步深入了解View(一)](http://blog.csdn.net/guolin_blog/article/details/12921889)
- [Android视图绘制流程完全解析，带你一步步深入了解View(二)](http://blog.csdn.net/guolin_blog/article/details/16330267)
- [Android视图状态及重绘流程分析，带你一步步深入了解View(三)](http://blog.csdn.net/guolin_blog/article/details/17045157)
- [Android 布局优化](http://www.stormzhang.com/android/2014/04/10/android-optimize-layout/)
- [性能优化之布局优化](http://www.trinea.cn/android/layout-performance/)

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
