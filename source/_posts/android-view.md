title: Android绘制整理
date: 2015-10-20 00:48:03
tags:
- Android
- 视图
- View
- 优化
- 重绘

---

## I. `LayoutInflater`

- 使用XmlPull来解析
- `rInflate()`方法(中不断递归)遍历根布局下的子布局
- 由于`setContentView`默认是添加到id为`content`的`FrameLayout`中，因此`LyoautParams`有效。

### 最终结果:
是一个完整的DOM结构，返回的是顶层布局。

### 耗时点:

1. 其中的`createView()`方法中通过反射创建出View实例

## II. 绘制过程

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

## III. 视图状态

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

## IV. 状态变化回调

![](/img/android_view-1.jpg)

## V. View#invalidate

> 需要注意`invalidate`虽然最终调到`performTraversals()`但是很可能没有 **重新测量标志**，大小没有变化，因此不会执行`measure`和`layout`，只有`draw`可以执行到。
> 相比之下如果希望视图绘制流程完整重新走一遍，需要调用`requestLayout`。

![](/img/android_view-2.jpg)


---

> ps 第四篇是一些简单的应用层，就没有整理了

----

- [Android LayoutInflater原理分析，带你一步步深入了解View(一)](http://blog.csdn.net/guolin_blog/article/details/12921889)
- [Android视图绘制流程完全解析，带你一步步深入了解View(二)](http://blog.csdn.net/guolin_blog/article/details/16330267)
- [Android视图状态及重绘流程分析，带你一步步深入了解View(三)](http://blog.csdn.net/guolin_blog/article/details/17045157)
