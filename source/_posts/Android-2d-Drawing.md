title: Android 2d-Drawing
date: 2015-04-18 08:35:03
tags:
- Android
- 2d
- drawing
- canvas

---

##Typically Way

###I. Drawing is handled by the system's normal View hierarchy drawing process.

Which scene?

1. static graphic
2. predefined animation

<!--more-->
###II. Drawing is handled by calling canvas draw mannual.

#####Which scene?

1. regualrly re-draw/dynamic animation : ( e.g. video、game )

#####Which way?

1. The same thread as UI Activity( View.onDraw() )
2. A separate thread( SurfaceView suport )

##Canvs

##### In one word

> As a pretense or interface, to the actual surface upon which your graphics will drawn - it holds all of your "draw" calls.


##### 特征

- Android 中所有的View视图，其实最终都是在Canvas这个画板上画出来的
- View在绘制时，父组件调用dispatchDraw(Canvas)分发给各个子组件
- `canvas.translate(int, int)` 当前原点位置
- `canvas.clipRect(int, int, int, int)` 可见范围
- Android.animation 实际上 改变canvas的matrix以及通过clipRect改变可见范围，大小与布局并没有实质改变
- matrix矩阵的作用：对每个坐标点(x, y)转换为另外(x', y')
- Canvas.translate(int, int) 效果相同 matrix.postTranslate(int, int)