title: SVG-Android库 深入浅出 解析篇
date: 2014-12-10 08:35:03
tags:
- parse
- svg
- Android
- 解析

---

- 入口
- 通过解析得到SVG
- 将得到的SVG渲染到Picture\Canvas上

## 1. 入口
`1.getFromInputStream(InputStream) : SVG` `2.getFromString(String) : SVG` `3.getFromResource(Resources, int) : SVG` `4.getFromAsset(AssetManager, String) : SVG`

<!--more-->

	// *************** com.caverock.androidsvg.SVG ***************

	/**
    * Read and parse an SVG from the given {@code InputStream}.
    *
    * @param is the input stream from which to read the file.
    * @return an SVG instance on which you can call one of the render methods.
    * @throws SVGParseException if there is an error parsing the document.
    */
	getFromInputStream(InputStream) : SVG

	/**
    * Read and parse an SVG from the given {@code String}.
    *
    * @param svg the String instance containing the SVG document.
    * @return an SVG instance on which you can call one of the render methods.
    * @throws SVGParseException if there is an error parsing the document.
    */
	getFromString(String) : SVG

	/**
    * Read and parse an SVG from the given resource location.
    *
    * @param context the Android context of the resource.
    * @param resourceId the resource identifier of the SVG document.
    * @return an SVG instance on which you can call one of the render methods.
    * @throws SVGParseException if there is an error parsing the document.
    */
    getFromResource(Context, int) : SVG

    /**
    * Read and parse an SVG from the given resource location.
    *
    * @param resources the set of Resources in which to locate the file.
    * @param resourceId the resource identifier of the SVG document.
    * @return an SVG instance on which you can call one of the render methods.
    * @throws SVGParseException if there is an error parsing the document.
    */
    getFromResource(Resources, int) : SVG

    /**
    * Read and parse an SVG from the assets folder.
    *
    * @param assetManager the AssetManager instance to use when reading the file.
    * @param filename the filename of the SVG document within assets.
    * @return an SVG instance on which you can call one of the render methods.
    * @throws SVGParseException if there is an error parsing the document.
    * @throws IOException if there is some IO error while reading the file.
    */
    getFromAsset(AssetManager, String) : SVG

## 2. 通过解析得到SVG
### 2.1 输入
xml InputStream 或 zip InputStream
### 2.2 输出
SVG
### 2.3 XML解析器
SAX
### 2.4 解析引擎
- SVGParser // 主要引擎 继承自 com.xml.sax.ext.DefaultHandler2
- CCSSVGParser //主要用于解析CSS样式

### 2.5 解析工具
- NumberParser //解析SVG/Style中 'number'元素内容（速度快于系统）
- IntegerParser //解析SVG/Style中 'integer'元素或者哈希（速度快于系统）
- PreserveAspectRatio //在这里用于存储位置与缩放

### 2.6 解析流程

#### startDocument
![](/img/svg-parse-1.jpg)
#### startElement
![](/img/svg-parse-2.jpg)
#### characters
![](/img/svg-parse-3.jpg)
#### endElement
![](/img/svg-parse-4.jpg)
#### endDocument
![](/img/svg-parse-5.jpg)

### 2.7 层级管理
#### startDocument
	svgDocument = new SVG();
#### startElement
	......
	SVG.SVGObject obj = new SVG.SVGObject();
	......
	if (currentElement == null) {
		svgDocument.setRootElement(obj);
	} else {
		currentElement.addChild(obj);
	}
	currentElement = obj;
#### characters

	......
	if (currentElement instanceof SVG.TextContainer) {
		// The SAX parser can pass us several text nodes in a row. If this happens, we
		// want to collapse them all into one SVG.TextSequence node				
		SVG.SvgConditionalContainer parent = (SVG.SvgConditionalContainer) currentElement;
		int numOlderSiblings = parent.children.size();
		SVG.SvgObject previousSibling = (numOlderSiblings == 0) ? null : parent.children.get(numOlderSiblings - 1);
		if (previousSibling instanceof SVG.TextSequence) {
			// Last sibling was a TextSequence also, so merge them.
			((SVG.TextSequence) previousSibling).text += new String(ch, start, length);
		} else {
			// Add a new TextSequence to the child node list
			((SVG.SvgConditionalContainer) currentElement).addChild(new SVG.TextSequence(new String(ch, start, length)));
		}
	}

#### endElement
	......
	currentElement = ((SvgObject) currentElement).parent;
#### endDocument
	......

## 3. 将得到的SVG渲染到Picture\Canvas上
### 3.1 渲染入口
`1.renderToPicture() : Picture` `2.renderToPicture(int, int) : Picture` `3.renderViewToPicture(String, int, int) : Picture` `4.renderToCanvas(Canvas) : void` `5.renderToCanvas(Canvas, RectF) : void` `6.renderViewToCanvas(String, Canvas) : void` `7.renderViewToCanvas(String, Canvas, RectF) : void`

	/**
    * Renders this SVG document to a Picture object.
    * <p>
    * An attempt will be made to determine a suitable initial viewport from the contents of the SVG file.
    * If an appropriate viewport can't be determined, a default viewport of 512x512 will be used.
    *
    * @return a Picture object suitable for later rendering using {@code Canvas.drawPicture()}
    */
	renderToPicture() : Picture

	/**
    * Renders this SVG document to a Picture object.
    *
    * @param widthInPixels the width of the initial viewport
    * @param heightInPixels the height of the initial viewport
    * @return a Picture object suitable for later rendering using {@code Canvas.darwPicture()}
    */
	renderToPicture(int, int) : Picture

	/**
    * Renders this SVG document to a Picture object using the specified view defined in the document.
    * <p>
    * A View is an special element in a SVG document that describes a rectangular area in the document.
    * Calling this method with a {@code viewId} will result in the specified view being positioned and scaled
    * to the viewport.  In other words, use {@link #renderToPicture()} to render the whole document, or use this
    * method instead to render just a part of it.
    *
    * @param viewId the id of a view element in the document that defines which section of the document is to be visible.
    * @param widthInPixels the width of the initial viewport
    * @param heightInPixels the height of the initial viewport
    * @return a Picture object suitable for later rendering using {@code Canvas.drawPicture()}, or null if the viewId was not found.
    */
	renderViewToPicture(String, int, int) : Picture

	/**
    * Renders this SVG document to a Canvas object.  The full width and height of the canvas
    * will be used as the viewport into which the document will be rendered.
    *
    * @param canvas the canvas to which the document should be rendered.
    */
	renderToCanvas(Canvas) : void

	 /**
    * Renders this SVG document to a Canvas object.
    *
    * @param canvas the canvas to which the document should be rendered.
    * @param viewPort the bounds of the area on the canvas you want the SVG rendered, or null for the whole canvas.
    */
	renderToCanvas(Canvas, RectF) : void

	/**
    * Renders this SVG document to a Canvas using the specified view defined in the document.
    * <p>
    * A View is an special element in a SVG documents that describes a rectangular area in the document.
    * Calling this method with a {@code viewId} will result in the specified view being positioned and scaled
    * to the viewport.  In other words, use {@link #renderToPicture()} to render the whole document, or use this
    * method instead to render just a part of it.
    * <p>
    * If the {@code <view>} could not be found, nothing will be drawn.
    *
    * @param viewId the id of a view element in the document that defines which section of the document is to be visible.
    * @param canvas the canvas to which the document should be rendered.
    */
	renderViewToCanvas(String, Canvas) : void

	/**
    * Renders this SVG document to a Canvas using the specified view defined in the document.
    * <p>
    * A View is an special element in a SVG documents that describes a rectangular area in the document.
    * Calling this method with a {@code viewId} will result in the specified view being positioned and scaled
    * to the viewport.  In other words, use {@link #renderToPicture()} to render the whole document, or use this
    * method instead to render just a part of it.
    * <p>
    * If the {@code <view>} could not be found, nothing will be drawn.
    *
    * @param viewId the id of a view element in the document that defines which section of the document is to be visible.
    * @param canvas the canvas to which the document should be rendered.
    * @param viewPort the bounds of the area on the canvas you want the SVG rendered, or null for the whole canvas.
    */
	renderViewToCanvas(String, Canvas, RectF) : void

	---

	> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

	---
