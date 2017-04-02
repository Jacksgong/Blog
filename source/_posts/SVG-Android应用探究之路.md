title: SVG Android应用探究之路
date: 2014-11-08 15:46:03
updated: 2014-11-08 15:46:03
permalink: 2014/11/08/SVG-Android应用探究之路
categories:
- SVG
tags:
- svg
- Android

---

> 《Forms for Kids》开发总结翻译

## I. 结论

#### 优点:

1. vector
2. 在所有大小分辨率屏幕上完美显示
3. SVG图片更小
4. 一张图片可以更具需求多次使用？(One picture is used some times for different permissions)
5. 减少加载时间

<!--more-->

#### 缺点:

1. 图片只能按照比例缩放
2. 不支持透明度？
3. svg文件还可以近一步优化，里面有一些不可取（The schedule needs to be simplified — the more vector elements, the the file more weighs. It is undesirable to use shades and luminescences as it in times increases the size of SVG-files）

#### SVG 的探索来源于：

> No sooner said than done. So, under katom history of introduction of vector images in one of our applications. In article we will impart experience also features of use of vector images in format SVG in applications Android.


##### projects on guglokode

- code.google.com/p/svg-android/
- code.google.com/p/svg-android-2/
- Detailed article about use NDK:
- horribileru.blogspot.ru/2011/10/android-imageview-svg.html
- And some links to dead projects at different forums.

#### SVG可用编辑器

Adobe Illustrator 、Inkscape work.

## II. SVG-Android：

> GitHub: [pents90/svg-android](https://github.com/pents90/svg-android)

他们项目通过底层封装的接口方式：

```java
SVG svg = SVGParser.getSVGFromResource(getResources(), R.raw.filename);
Drawable drawable = svg.createPictureDrawable();
imageView.setImageDrawable(drawable);
```

- **缺点:** 只支持 SVG basic 1.1(不支持Inkspace编辑、只支持AdobeIllustrator编辑)

## III. SVG-Android-2:

> URL: [svg-android-2](https://code.google.com/p/svg-android-2/wiki/Introduction)

#### 第一个发现：SVG在包含 阴影的情况下大小会飙升：

![icon 1](/img/svg-k-1.png)

izorbrazhenija with a shade and without: 118 KB vs 1 KB

- **解决方法：** 删除对应的阴影

#### 第二个发现：显示梯度颜色，不支持！

The problem with gradients has dared removal of superfluous tags from svg (it is described further in article). But basically, and with it it would be possible to live and in our simple images to replace a gradient with homogeneous pouring, if not other nuance — considerable load time of images.

- **解决方法：** 用简单的图片代替
- **后文(第三个发现)提到解决方法：** After we have got rid of the given links, having edited code SVG in some images, the gradient began to be displayed correctly.

![icon 2](/img/svg-k-2.png)

 at the left — the black sky in the form of a gradient, on the right — a correct picture.

#### 第三个发现：加载时间

- **根源：** 为什么SVG-Android-2这么耗时，
- **原因：** SVGParser 解析Image XML file ，解析了两次，第一次 为第二次解析收集多余的属性。多余信息是：

> that the most interesting, — is analyzed only attribute xlink:href which is a semblance of hyperlinks in the document. In our problem images just there were such links, and they conducted anywhere.

- **成果：** 耗时，加载35个SVG的图片(PNG 500px*500px)：从原8s 减少到 1.8-2s。

#### 第四个发现：透明与颜色适配器

- **原因：** 库不是加载 典型的bitmapDrawable与pictureDrawable,并且源码中的setColorFilter、setAlpha方法都是空的：

```java
@Override
public void setColorFilter(ColorFilter colorFilter) {}
@Override
public void setAlpha(int alpha) {}
```

- **成果：** 在SVGHandler中发现一个Paint类型的fillPaint组件，如果能够在加载元素之前 创建colorFilter即可，略微调整SVGHandler加载SVG的代码：

```java
public void setFilterColor(int filterColor) {
      fillPaint.setColorFilter(new PorterDuffColorFilter(filterColor, Mode.MULTIPLY));
}
```

接口调整为：

```java
SVG svg = SVGParser.getSVGFromResource(getResources(), rawSvgId, filterColor);
```

因此我们能够在多张图片上通过引用一张图片使用不同的阴影颜色（As a result we could receive some images of different shades from one picture.）

对于透明度，建议并不适用setAlpha去实现（实际上是可以的通过fillPaint）:

> Also it is possible to establish and Alpha for fillPaint, but in games this property is required in the dynamic form (have pressed an element — has become translucent), and podgruzhat each time the new image is inconvenient. Therefore this effect have replaced with scaling (have pressed — the element has decreased).

#### 第五个发现：异常处理：

```java
java.lang.UnsupportedOperationException
    at android.view.GLES20Canvas.drawPicture(GLES20Canvas.java:895)
    at android.graphics.drawable.PictureDrawable.draw(PictureDrawable.java:73)
```

低版本不支持gpu(api < 11)

```java
public static void setSoftwareLayerType(View view) {
     try {
       view.setLayerType(View.LAYER_TYPE_SOFTWARE, null);
     } catch (NoSuchMethodError e) {
         //Do nothing - this happens on API < 11
     }
}
```

#### 其使用SVG的项目：

http://play.google.com/store/apps/details?id=com.whisperarts.kids.forms

> 本文总结自：http://sysmagazine.com/posts/166093/

---

- [本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/SVG-Android%E5%BA%94%E7%94%A8%E6%8E%A2%E7%A9%B6%E4%B9%8B%E8%B7%AF.md)。

---
