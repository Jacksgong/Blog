title: ConstraintLayout
date: 2016-08-03 08:33:03
tags:
- Layout
- Android
- UI

---

> 目前`ConstraintLayout`(alpha-4)还是打包到`support library`中的，因此 属性前缀 `app:` 而非 `android:`，以后应该会放到包的命名区间。

## I. 位置:

### 1. 锚点

> View相对与其他元件(同级别View、父节点View、guideline)是如何布局的。

<!-- more -->

#### 格式

```
layout_constraint[SourceAnchor]_[TargetAnchor]="[TargetId]"
```

其中`SourceAnchor`/`TargetAnchor` 可以是:

- Top,Bottom,Start(Left),End(Right)
- CenterX、CenterY
- Baseline(只有Text-Based的View支持)

### 2. Bias:

- 横向比重: `layout_constraintHorizontal_bias=左方占比`
- 纵向比重: `layout_constraintVertical_bias=上方占比`

### 3. Guidelines:

> 特征:
> 1. measure大小始终是0;
> 2.它的`visibility`始终是`View.GONE`

#### 特有参数:

- 到开始边缘的绝对距离: `layout_constraintGuide_begin`
- 到结束边缘的绝对距离: `layout_constraintGuide_end`
- 到开始边缘的占比百分数: `layout_constraintGuide_Percent`

> P.S: Guideline是纵向还是横向的，由`android:orientation="<vertical|horizontal>"`决定。

### 4. 编辑器辅助

`layout_editor_absoluteX`与`layout_editor_absoluteY`是只有在编辑器中使用，设备上运行时这些是没有效果的。参数空间是在: `http://schemas.android.com/tools`。

## II. 大小


### 1. 没有了`match_parent`

**可替代** : 将`layout_width`/`layout_height`设为`0dp`: 填充满附属的锚点布局。

**原因** : 但是更加灵活，可以类似以前的`layout_weight`使用。

### 2. 支持长宽比

`layout_constraintDimensionRatio` 提供长宽比如: `4:3`。在给了这个参数的情况下，需要提供任意一边的值(指定值或`wrap_content`)

## III. 原理与性能

> 添加子View到`ContraintLayout`时，所有XML中`layout_`前缀的属性都会添加到`LayoutParams`实例中。

`ConstraintLayout`子View中的`LayoutParams`存储着`ConstraintWidget`，`ConstraintWidget`用于逻辑运算与分析，并且每个`ConstraintWidget`与`ConstraintLayout`中的`ConstraintWidgetContainer`相联系。

![ClassHierarchy](/img/constraint-layout_classHierarchy.png)

`ConstraintWidget`持有所有关于View位置与大小的信息，在measure与layout时作为数据依据。

![ConstraintWidget](/img/constraint-layout_constraintWidget.png)

在layout的期间，会根据`LayoutParams`中constraint的信息，为`ConstraintWidget`中每个连接的锚点定义`ConstraintAnchor`。

![AnchorConnection](/img/constraint-layout_anchorConnection.png)

### 1. measure

![MeasureFlow](/img/constraint-layout_measureFlow.png)

> 这里的"Any Size"View，指的是XML中给的长或宽为`0dp`的View。

"Any Size"View，需要两次运算，首次会直接不做检查在`ConstraintLayout#internalMeasureChildren`中直接使用`WRAP_CONTENT`用于计算大小(`ViewGroup#getChildMeasureSpec`)，第二次根据其他的计算结果在`ConstraintLayout#onMeasure`中计算出真正的大小。

> P.S: `Add Constraints to Equation Solver`、`Minimize Linear System`、`Update Child Bounds from solution` 都是在`ConstraintLayout#onMeasure`中在执行的`ConstraintLayout#internalMeasureChildren`。该算法计通过`LinearSystem`算出了View的bound。

### 2. layout

由于上面在measure时已经估算出各view的大小与位置，因此在此之后`ConstraintWidget`中已经有对应View适当的bound了。因此在`onLayout`中只需要遍历所有子View，设置他们的bound值就行，十分轻量。

```java
for(int i = 0; i < getChildCount(); ++i) {
  View child = this.getChildAt(i);
  ConstraintLayout.LayoutParams params =
      (ConstraintLayout.LayoutParams)child.getLayoutParams();
  ConstraintWidget widget = params.widget;
  int l = widget.getDrawX();
  int t = widget.getDrawY();
  int r = l + widget.getWidth();
  int b = t + widget.getHeight();
  child.layout(l, t, r, b);
}
```

## IV. 性能方面

由于`ConstraintLayout`有效的优化了layout与draw，并且从质上有效的减少了层级，因此相同的布局呈现上，通常情况下`ConstrantLayout`的性能都比其他的Layout性能要好。

---

> 文中图片全部来源: http://wiresareobsolete.com/2016/07/constraintlayout-part-2/

- [ConstraintLayout, Inside and Out: Part 1](http://wiresareobsolete.com/2016/07/constraintlayout-part-1/)
- [ConstraintLayout, Inside and Out: Part 2](http://wiresareobsolete.com/2016/07/constraintlayout-part-2/)
- [ConstraintLayout on Android – How Ready Is It?](http://leaks.wanari.com/2016/05/31/constraintlayout-android/)


---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
