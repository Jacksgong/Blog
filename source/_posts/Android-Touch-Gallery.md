title: Android Touch Gallery
date: 2014-12-14 08:35:03
tags:
- imageview
- viewpager
- Android
- 缩放

---

`Android touch gallery with net、local file or cache.`

## 1. 申明
	本项目library_gallery基于Truba的AndroidTouchGallery，往上封装一层，实现简单快速实现Viewpager上协调图片的缩放以及数据来源的自动选择.

## 2. 拓展部分

实现相关接口，底层即可完成自动选择从网路加载、从本地文件加载或者从Cache加载

<!--more-->

下面是简单的案例：

	public class GalleryPagerAdapter extends BaseGalleryPagerAdapter {

	public GalleryPagerAdapter() {
		super();
	}

	public GalleryPagerAdapter(Context context, List<String> resources) {
		super(context, resources);
		setLruSoftCache(CacheImage.CACHE_IV);
	}

	@Override
	public void save(String url, Bitmap bm) {
		saveBitmap(url, bm);
	}

	@Override
	public String getKey(String url) {
		return url;
	}

	@Override
	public String getPath(String url) {
		return Path.IV + AppUtil.md5(url);
	}
	}


	public class DemoHorizontalGalleryActivity extends Activity {

	private GalleryViewPager mViewPager;

	private GalleryPagerAdapter mAdapter;

	final List<String> urls = new ArrayList<String>();

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_viewpager_gallery);

		initDemoData();

		mViewPager = (GalleryViewPager) findViewById(R.id.viewpager);
		mAdapter = new GalleryPagerAdapter(this, urls);

		mViewPager.setAdapter(mAdapter);
	}
	}

详情可参看GallerySample

## 3. 运行效果
![image](https://github.com/Jacksgong/Android-Touch-Gallery/raw/master/readme/demo1.jpg)
![image](https://github.com/Jacksgong/Android-Touch-Gallery/raw/master/readme/demo2.jpg)
![image](https://github.com/Jacksgong/Android-Touch-Gallery/raw/master/readme/demo3.jpg)
![image](https://github.com/Jacksgong/Android-Touch-Gallery/raw/master/readme/demo4.jpg)
![image](https://github.com/Jacksgong/Android-Touch-Gallery/raw/master/readme/demo5.jpg)
License

## 4. 源码

GITHUB: https://github.com/Jacksgong/Android-Touch-Gallery

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
