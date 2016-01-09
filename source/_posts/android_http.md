title: HttpURLConnection、HttpClient
date: 2015-10-31 15:12:03
tags:
- Android
- 网络
- HttpURLConnection
- HttpClient

---

## I. HttpClient

> 具体实现: `DefaultHttpClient`、`AndroidHtppClient`

#### 特点:

API数量繁多，官方升级维护较少

<!-- more -->

## II. HttpURLConnection

#### 特点:

多用途、轻量。API简单，易于使用、拓展。

#### 坑点:

Android 2.2以前: 可读的InputStream调用close时，可能导致连接池失效（通常解决方法禁用连接池功能）。

#### 迭代亮点:

##### Andorid 2.3

- 默认请求接受gzip。
- 后会使用SNI([Server Name Indication](https://en.wikipedia.org/wiki/Server_Name_Indication))
- 断线重连

##### Android 4.0

- 响应缓存机制(`HttpResponseCache#install`):

1. 都由本地提供的响应，没有必要发起网络连接的请求，都直接从本地缓存直接取得
2. 视情况而定的缓存响应，由服务器确定(304 Not Modified代表不需要更新，就不会下载任何数据，将直接用本地缓存);
3. 没有缓存的响应，都由服务器直接下载。

## III. 选择

推荐Android 2.2以前使用`HttpClient`，由于Android 2.2以前的`HttpURLConnection`存在坑点，而相比而言`HttpClient`在Android 2.2以前比较稳定。

---

- [Android访问网络，使用HttpURLConnection还是HttpClient？](http://blog.csdn.net/guolin_blog/article/details/12452307)
- [Android’s HTTP Clients](http://android-developers.blogspot.com/2011/09/androids-http-clients.html)

---

> © 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
