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

###II. Drawing is handled by calling canvas draw mannual.

#####Which scene?

1. regualrly re-draw/dynamic animation : ( e.g. video、game )

#####Which way?

1. The same thread as UI Activity( View.onDraw() )
2. A separate thread( SurfaceView suport )

##Canvs

##### In one word

> As a pretense or interface, to the actual surface upon which your graphics will drawn - it holds all of your "draw" calls.

##### Acts on/Output
Canvas