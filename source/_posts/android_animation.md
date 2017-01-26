title: Android动画
date: 2015-11-02 20:58:03
permalink: 2015/11/02/android_animation
tags:
- Android
- 动画
- animation
- TimeInterpolator
- TypeEvaluator
- ObjectAnimator
- ValueAnimator
- AnimatorSet

---

> 再复杂的动画，都是简单动画的结合

<!-- more -->

## I. Tween Animation(补间动画)

形式 | 备注
-|-
alpha | 渐变透明度
scale | 渐变尺寸
translate | 画面位置移动
rotate | 画面旋转

#### 实现方式

`Animation`配合`AnimationUtils`，结合xml中`set`

## II. Frame Animation(关键帧动画)

> 顺序播放关键帧

#### 实现方式

`AnimationDrawable`结合xml中定义`animation-list`标签

> `AnimationDrawable`本身无法监听动画状态

## III. 对象属性动画

> Andorid 3.0加入(如果3.0以下想用使用，可以参考开源动画库: http://nineoldandroids.com/)
> 基本概念: 可以对对象属性进行动画，不仅仅是View

动画的默认帧率是一帧10ms(100帧/s(Android正常绘制60帧/s))

### 1. TimeInterpolator(时间插值器)

> 根据时间流逝的百分比来计算出当前属性值改变的百分比

#### 系统默认提供的

- `LinearInterpolator`: 线性插值器，匀速动画
- `AccelerateDecelerateInterpolator`: 加速减速插值器，动画两头慢中间快
- `DecelerateInterpolator`: 减速插值器，动画越来越慢
- `AccelerateInterpolator`: 加速插值器，动画越来越快
...

### 2. TypeEvaluator(类型估值算法)

> 根据当前属性改变的百分比来计算改变后的属性值

#### 系统默认提供的

- `IntEvaluator`: 针对整型属性
- `FloatEvaluator`: 针对浮点型属性
- `ArgbEvaluator`: 针对Color属性
...

> TypeEvaluator与TimeInterpolator是实现非匀速动画的神器。

#### 实现方式

TimeInterpolator与TypeEvaluator两者是配合使用的，

```
public class LinearInterpolator implements Interpolator {

    ...
    public float getInterpolation(float input) {
        // 返回时间流逝的百分比 input = (当前时间 - 开始时间)/ 总时间
        return input; // 匀速
        //return input * input; //加速
    }
}

public class IntEvaluator implements TypeEvaluator<Integer> {

    public Integer evaluate(float fraction, Integer startValue, Integer endValue) {
        // 返回需要变化的整型
        int startInt = startValue;
        // fraction: LinearInterpolator返回的流逝百分比
        return (int)(startInt + fraction * (endValue - startInt));
    }
}
```


### 3. ObjectAnimator、ValueAnimator、AnimatorSet

> 都可以直接在xml中定义 / 直接代码中实现，结合TimeInterpolator与TypeEvaluator，几乎可以实现所有想要的动画

---

#### 例子:

> 为了理解，直接看几个例子
> ps: 以下例子来自: [Android动画进阶—使用开源动画库nineoldandroids](http://blog.csdn.net/singwhatiwanna/article/details/17639987)与[Android属性动画深入分析：让你成为动画牛人](http://blog.csdn.net/singwhatiwanna/article/details/17841165)

##### 第二个参数PropertyName

> PropertyName: 如第一个例子的"translationY"

> 我们定义第一个例子中的myObject为target

1. 如果Animator中已经提供初始值，就只需要target包含Property的set方法(如第一个例子中myObject需要包含`setTranslationY(float)`)
2. 如果Animator中未提供初始值，除了需要set方法，还需要包含Property的get方法(如地i一个例子中myObject需要包含`getTranslationY():float`)
3. 满足以上两条，就可以定义为Property

> ps: 如果View/某对象没有满足上面的条件，如果可以，未尝不可自己封装一层实现。

```
// 默认时间内，移动其高度的距离
ObjectAnimator.ofFloat(myObject, "translationY", -myObject.getHeight()).start();
```

```
//  不断循环3s内背景颜色从红色渐变到蓝色再到红色
ValueAnimator colorAnim = ObjectAnimator.ofInt(
                this, "backgroundColor",
                /*Red*/0xFFFF8080,/*Blue*/0xFF8080FF);
colorAnim.setDuration(3000);
colorAnim.setEvaluator(new ArgbEvaluator());
colorAnim.setRepeatCount(ValueAnimator.INFINITE);
colorAnim.setRepeatMode(ValueAnimator.REVERSE);
colorAnim.start();
```

```
// 5s内同时对View旋转、平移、缩放、透明都进行了改变
AnimatorSet set = new AnimatorSet();
set.playTogether(
    ObjectAnimator.ofFloat(myView, "rotationX", 0, 360),
    ObjectAnimator.ofFloat(myView, "rotationY", 0, 180),
    ObjectAnimator.ofFloat(myView, "rotation", 0, -90),
    ObjectAnimator.ofFloat(myView, "translationX", 0, 90),
    ObjectAnimator.ofFloat(myView, "translationY", 0, 90),
    ObjectAnimator.ofFloat(myView, "scaleX", 1, 1.5f),
    ObjectAnimator.ofFloat(myView, "scaleY", 1, 0.5f),
    ObjectAnimator.ofFloat(myView, "alpha", 1, 0.25f, 1)
);
set.setDuration(5 * 1000).start();
```

```
// ValueAnimator的使用
// 5s内匀速修改target的宽度
private void performAnimate(final View target, final int start, final int end) {
    ValueAnimator valueAnimator = ValueAnimator.ofInt(1, 100);

    valueAnimator.addUpdateListener(new AnimatorUpdateListener() {

        //持有一个IntEvaluator对象，方便下面估值的时候使用
        private IntEvaluator mEvaluator = new IntEvaluator();

        @Override
        public void onAnimationUpdate(ValueAnimator animator) {
            //获得当前动画的进度值，整型，1-100之间
            int currentValue = (Integer)animator.getAnimatedValue();
            Log.d(TAG, "current value: " + currentValue);

            //计算当前进度占整个动画过程的比例，浮点型，0-1之间
            float fraction = currentValue / 100f;

            //直接调用整型估值器通过比例计算出宽度，然后再设给Button
            target.getLayoutParams().width = mEvaluator.evaluate(fraction, start, end);
            target.requestLayout();
        }
    });

    valueAnimator.setDuration(5000).start();
}
```

---

- [Property Animation](https://developer.android.com/intl/zh-cn/guide/topics/graphics/prop-animation.html)
- [android动画简介](http://blog.csdn.net/singwhatiwanna/article/details/9270275)
- [Android动画进阶—使用开源动画库nineoldandroids](http://blog.csdn.net/singwhatiwanna/article/details/17639987)
- [Animation 之 Interpolator 插补器理解](http://blog.csdn.net/qingye_love/article/details/8859347)
- [Android属性动画深入分析：让你成为动画牛人](http://blog.csdn.net/singwhatiwanna/article/details/17841165)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
