title: Magic Progress Widget
date: 2015-12-13 15:45:03
tags:
- draw
- sweep
- gradient
- open source

---

> 渐变的圆形进度条与轻量横向进度条

<!--more-->

## I. 最终效果

![demo gif][demo_gif]

## II. 如何使用

> 建议参考github中的demo

```
<com.liulishuo.magicprogresswidget.MagicProgressCircle
            android:id="@+id/demo_mpc"
            android:layout_width="@dimen/mpc_size"
            android:layout_height="@dimen/mpc_size"
            app:mpc_percent="0.8"
            app:mpc_start_color="@color/mpc_start_color"
            app:mpc_end_color="@color/mpc_end_color"
            app:mpc_stroke_width="@dimen/mpc_stroke_width"
            app:mpc_default_color="@color/mpc_default_color"/>

<com.liulishuo.magicprogresswidget.MagicProgressBar
                    android:id="@+id/demo_2_mpb"
                    android:layout_width="match_parent"
                    android:layout_height="@dimen/mpb_height"
                    app:mpb_color="@color/mpb_color"
                    app:mpb_default_color="@color/mpb_default_color"/>
```

#### Magic Progress Circle

参数 | 含义
:-: | :-
mpc_percent | 填充的百分比[0, 1]
mpc_stroke_width | 描边宽度
mpc_start_color | 渐变颜色起点颜色(percent=0)
mpc_end_color | 渐变颜色终点颜色(percent=1)
mpc_default_color | 未填充部分的描边的颜色


## III. Github

[lingochamp](https://github.com/lingochamp/MagicProgressWidget)

## IV. bintray

[![Download][bintray_svg]][bintray_link]

[demo_gif]: https://github.com/lingochamp/MagicProgressWidget/raw/master/art/demo.gif
[bintray_svg]: https://api.bintray.com/packages/jacksgong/maven/MagicProgressWidget/images/download.svg
[bintray_link]: https://bintray.com/jacksgong/maven/MagicProgressWidget/_latestVersion
