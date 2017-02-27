title: PhotoGallery、Volley、Picasso 比较
date: 2015-04-28 07:48:03
permalink: 2015/04/28/PhotoGallery、Volley、Picasso-比较
categories:
- Android UI交互
tags:
- PhotoGallery
- Vollery
- Picasso
- 分析
- Android

---

> 整理自: [solving-the-android-image-loading-problem-volley-vs-picasso](https://www.bignerdranch.com/blog/solving-the-android-image-loading-problem-volley-vs-picasso/)

<!--more-->
## I. PhotoGallery

> 一个很简单的图片加载库

#### 特点:
- 优点:

`简单`、`小`、`易于理解`

- 缺点

`使用不够简单`（每次初始化不得不按照生命周期调用/需要手动去清除已经不用的请求等）、`改起来相对复杂`

> ps: 图片下载，单线程串行。


#### 代码:

- 创建使用

```
@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ...

        mThumbnailThread = new ThumbnailDownloader<ImageView>(new Handler());
        mThumbnailThread.setListener(new ThumbnailDownloader.Listener<ImageView>() {
            public void onThumbnailDownloaded(ImageView imageView, Bitmap thumbnail) {
                if (isVisible()) {
                    imageView.setImageBitmap(thumbnail);
                }
            }
        });
        mThumbnailThread.start();
        mThumbnailThread.getLooper();
    }
```


- 清理下载队列

```
@Override
    public void onDestroyView() {
        super.onDestroyView();
        mThumbnailThread.clearQueue();
    }
```

- 完全退出

```
 @Override
    public void onDestroy() {
        super.onDestroy();
        mThumbnailThread.quit();
    }
```

- 图片加载

```
 private class GalleryItemAdapter extends ArrayAdapter<GalleryItem> {

        ...

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ...

            GalleryItem item = getItem(position);
            ImageView imageView = (ImageView)convertView
                    .findViewById(R.id.gallery_item_imageView);
            imageView.setImageResource(R.drawable.brian_up_close);
            mThumbnailThread.queueThumbnail(imageView, item.getUrl());

            return convertView;
        }
    }
```

## II. Picasso

> - 组织: [Square](http://square.github.io)
> - 地址: [https://github.com/square/picasso](https://github.com/square/picasso)
> - 官方描述: Picasso通常使用一行代码就能够解决复杂的图片加载问题

#### 代码:

- 使用

```
private class GalleryItemAdapter extends ArrayAdapter<GalleryItem> {

        ...

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ...

            GalleryItem item = getItem(position);
            ImageView imageView = (ImageView)convertView
                    .findViewById(R.id.gallery_item_imageView);

            imageView.setImageResource(R.drawable.brian_up_close);
            Picasso.with(getActivity())
                .load(item.getUrl())
                .placeholder(R.drawable.brian_up_close) // 如果不提供占位，Picasso会复写你的imageview的缩放比例，因此最好是提供一个占位
                .centerCrop()  
                .noFade() //取消默认的淡入动画
                .into(imageView);

            return convertView;
        }
    }
```

#### 特点

- 优点:

1. Picasso 提供了很多图片处理能力（如缩放、裁剪等等）（也支持加入我们个性化的图片处理），并且缓存的是**图片处理以后**的。

2. Picasso 的调用接口十分简单清晰，调用起来很爽。

3. Picasso 提供了一个自己的网络层，但是如果我们的网络层是使用基于`ExecutorService`，那么我们可以通过Picasso提供的接口，让Picasso的网络层也运行在相同的线程池中。

4. Picasso 支持接入我们的**图片加载器**(image loads)，如果我们需要使用一些预加载之类的。

5. Picasso 支持传入自定义的一些目标，而不是Imageview，如果我们需要最终的加载图片结果不是要作用在ImageView上的话。

- 无法做到以下几点:

1. 无法自动创建单独的图片下载器

2. 无法存储 未压缩的图片到内存或者本地

3. 无法 取消请求

4. 无法 一次同时多个下载

> ps: 由于缓存的是缩放以及裁剪过的图片，因此Picasso需要在调用时就获知需要多大的图片
>     catch了`OutOfMemoryError`的crash

## III. Volley

> - 来自: Android dev team
> - 官方: [https://android.googlesource.com/platform/frameworks/volley](https://android.googlesource.com/platform/frameworks/volley)
> - 视频介绍: [https://developers.google.com/events/io/sessions/325304728](https://developers.google.com/events/io/sessions/325304728)
> - 官方定位: 网络异步框架（一般我们只用到其中的网络与缓存部分）

#### 代码:

- 初始化

```
 @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ...

        // 在实际的开发过程中，一般是在进入app的时候，初始化这两个共享实例，全局使用。
        mQueue = Volley.newRequestQueue(getActivity());

        mImageLoader = new ImageLoader(mQueue, new ImageCache() {
            @Override
            public void putBitmap(String key, Bitmap value) { }

            @Override
            public Bitmap getBitmap(String key) {
                return null;
            }
        });

        ...
    }
```

- 使用

```
 private class GalleryItemAdapter extends ArrayAdapter<GalleryItem> {

        ...

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ...

            GalleryItem item = getItem(position);

            // Volley可以用在一个普通的ImageView中，不过为了更简单的使用，Volley提供了一个NetworkImageView。
            NetworkImageView imageView = (NetworkImageView)convertView
                    .findViewById(R.id.gallery_item_imageView);
            imageView.setDefaultImageResId(R.drawable.brian_up_close);
            imageView.setImageUrl(item.getUrl(), mImageLoader);

            return convertView;
        }
    }
```


#### 特点

- 优点:

1. 网络部分，并不是仅仅用于图片，它打算作为前端不可或缺的一部分。对于简单的REST服务的应用，这是一个很大的优势。

2. `NetworkImageview`在清理这块相比Picasso而言，更暴力，并且GC方面更加保守。`NetworkImageView`依赖专门的强引用，并且清除所有的请求数据当ImageView发起了新的请求，或者是ImageView已经被移除了显示范围。

3. 性能方面，本文并没有提及性能，但是在内存使用部分，更加着合理的管理。Volley还通过一系列有效的回调来到主线程来减少上下文的切换

4. 支持`RequestFuture`（同步网络请求）(Volley apparently has futures, too. Check out RequestFuture if you’re interested.)

5. 当需要处理高分辨率的图片压缩，Volley的唯一一个较好的解决方案。(目前Android的`high-res`的处理方法并不是很好，作者表示对报`OutOfMemoryError`这样的处理方法表示不解，但是又觉得这应该是保证可靠的图片处理的唯一方法)（作者在Volley与Picasso上测试了原图(高分辨率)的图片，结果: Picasso与Volley都没有crash，但是由于图片太大了，Picasso无法正常显示，但是Volley所有图片都很稳定的显示了）

- 缺点:

1. 由于Volley更好的处理NetworkImageView这种它提供的自定义View，因此替换起来可能会比较蛋疼。

2. Volley的网络层完全自己实现，不支持如自定义的`ExecutorService`传入这种类似Picasso的机制，因此无法像Picasso一般支持我们自己统一的线程管理。

3. 不像Picasso一样专注图片加载，而是专注与处理一个简单的，独立的网络框架。唯一一个可以diy接入的就是ImageCache这部分。

4. 如果前端有某个请求是多重http请求，那么我们无法如此拓展Volley，只能通过在其之上建立。

> ps: 缓存 Http 返回结果（也就是，每次都需要 解码数据 => 图片, 当需要正常显示的时候）

## IV. Picasso vs Volley

> Picasso 专注图片处理，Volley 解决更通用的问题


#### 作者建议：
- 如果已经有一个稳定的，大型的项目，那么Picasso是更好的选择。

- 另一方面，如果是一个新的app，或者项目很小，可以直接让Volley充当后端网络架构，它可以解决绝大多数HTTP的负担。（这里不是很认同作者，如果是网络框架这边，我个人建议先看看Retrofit，具体可以看看这篇[Retrofit开发指南](https://github.com/bboyfeiyu/android-tech-frontier/tree/master/issue-7/Retrofit开发指南)）

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
