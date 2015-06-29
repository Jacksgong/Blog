title: 键盘面板切换 布局闪动处理方案
date: 2015-06-29 23:35:03
tags:
- 优化
- Android
- 键盘
- 面板
- 闪动
- 布局

---

> 之前有写过一篇核心思想: [Switching between the panel and the keyboard in Wechat](http://blog.dreamtobe.cn/2015/02/07/Switching-between-the-panel-and-the-keyboard/)

我们可以看到微信中的 从键盘与微信的切换是无缝的，而且是无闪动的，这种基础体验是符合预期的。

但是实际中，简单的 键盘与面板切换 是会有闪动，问题的。今天我们就实践分析与解决这个问题。

## I. 准备

> 以下建立在`android:windowSoftInputMode`带有`adjustResize`的基础上。

> 如图，为了方便分析，我们分出3个View:

![](img/wechat-keybord-panel.jpg)

- `CustomRootView`: 除去statusBar与ActionBar(ToolBar...balabala)
- `FootRootView`: 整个底部（包括输入框与底部面板在内的整个View）
- `PanelView`: 面板View

> 整个处理过程，其实需要分为两块处理:

1. 从`PanelView`切换到`Keybord`
 
**现象: ** 由于显示`Keybord`时直接`PanelView#setVisibility(View.GONE)`，导致会出现整个`FooterRootView`到底部然后又被键盘顶起。

**符合预期的应该: ** 直接被键盘顶起，不需要到底部再顶起。

2. 从`Keybord`切换到`PanelView`

**现象: ** 由于隐藏`Keybord`时，直接`PanelView#setVisibility(View.VISIBLE)`，导致会出现整个`FootRootView`先被顶到键盘上面，然后再随着键盘的动画，下到底部。

**符合预期的应该: ** 随着键盘收下直接切换到底部，而配有被键盘顶起的闪动。

## II. 处理

### 1. 从`PanelView`切换到`Keybord`

#### 原理 

屏蔽由于`PanelView#setVisibility(View.GONE)`导致，到底部的那一帧。

#### 方法: 

> 不直接调用`PanelView#setVisibility(View.GONE)`来隐藏`PanelView`，由于调用`setVisiblility`会促发`requestLayout`，将直接导致这帧被绘制。而是设置一个标志位，在由于键盘显示导致`PanelView`重新mearsure调用`onMeasure`的时候处理。

如代码:

```
@Override
	protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
		if (isHide) {
			setVisibility(View.GONE);
			widthMeasureSpec = MeasureSpec.makeMeasureSpec(0, MeasureSpec.EXACTLY);
			heightMeasureSpec = MeasureSpec.makeMeasureSpec(0, MeasureSpec.EXACTLY);
		}
		super.onMeasure(widthMeasureSpec, heightMeasureSpec);
	}
```

### 2. 从`Keybord`切换到`PanelView`

#### 原理

在真正由`Keybord`导致布局**真正**将要变化的时候，才给`PanelView`有效高度。否则直接给0高度。（**注意**，所有的判断处理要在`Super.onMeasure`之前完成判断）

#### 方法:

> 通过`CustomRootView`高度的变化，来保证在`Super.onMeasure`之前获得**真正**的由于键盘导致布局将要变化，然后告知`PanelView`，让其在`Super.onMeasure`之前给到有效高度。

> 在`adjustResize`模式下，键盘弹起会导致`CustomRootView`的高度变小，键盘收回会导致`CustomRootView`的高度变大。因此可以通过这个机制获知真正的`PanelView`将要变化的时机。

> 由于到了`onLayout`以后，clipRect的大小已经确定了，又要避免不多次调用`onMeasure`因此要在`Super.onMeasure`之前 

> 由于键盘收回的时候，会触发多次`measure`，如果不判断真正的由于键盘收回导致布局将要变化，就直接给有效高度，依然会有闪动的情况。

代码:

`CustomRootView`

```
 private int mOldHeight = -1;

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {

        do {
            final int width = MeasureSpec.getSize(widthMeasureSpec);
            final int height = MeasureSpec.getSize(heightMeasureSpec);

            Log.d(TAG, "onMeasure, width: " + width + " height: " + height);
            if (height < 0) {
                break;
            }

            if (mOldHeight < 0) {
                mOldHeight = height;
                break;
            }

            final int offset = mOldHeight - height;
            mOldHeight = height;

            if (offset >= 0) {
                //键盘弹起 (offset > 0，高度变小)
                Log.d(TAG, "" + offset + " >= 0 break;");
                break;
            }

            final PanelView bottom = getPanelView(this);

            if (bottom == null) {
                Log.d(TAG, "bottom == null break;");
                break;
            }

            bottom.IsNeedHeight(true);

        } while (false);

        super.onMeasure(widthMeasureSpec, heightMeasureSpec);

    }
```

`PanelView`

```
@Override
    public void setVisibility(int visibility) {
        if (visibility == getVisibility()) {
            return;
        }
        mIsNeedHeight = false;

        ViewGroup.LayoutParams l = getLayoutParams();
        l.height = 0;
        setLayoutParams(l);
        super.setVisibility(visibility);
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {

        if (getVisibility() == View.VISIBLE && mIsNeedHeight) {
            ViewGroup.LayoutParams l = getLayoutParams();
            setVisibility(View.VISIBLE);
            l.height = mHeight;
        }

        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
    }

    private boolean mIsNeedHeight = false;

    public void IsNeedHeight(final boolean isNeedheight) {
        this.mIsNeedHeight = isNeedheight;
    }
```

## III. GitHub:

明天补上。