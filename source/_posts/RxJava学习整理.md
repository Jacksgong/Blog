title: RxJava
date: 2015-04-29 08:35:03
tags:
- java
- RxAndroid
- RxJava
- 响应式编程
- 架构
- 模式
- 观察者模式

---

> 响应式编程（观察者模式）

ps: 如果不了解Lambda的话，最好先看下[Lambda](http://blog.dreamtobe.cn/2281.html), 文中都是使用Lambda语法

## I. 核心

**被观察者:** Observables (发出一系列事件)

**观察者:** Subscribers (处理这些事件)

<!--more-->
1. Observable和Subscriber可以做任何事情

2. Observable和Subscriber是独立于中间的变换过程的。


## II. 基本原型

```
//创建 Observable
Observable<String> myObservable = Observable.create(
    new Observable.OnSubscribe<String>() {
        @Override
        public void call(Subscriber<? super String> sub) {
            sub.onNext("Hello, world!");
            sub.onCompleted();
        }
    }
);

//创建 Subscriber
Subscriber<String> mySubscriber = new Subscriber<String>() {
    @Override
    public void onNext(String s) { System.out.println(s); }

// 如果正确的终结，最后会调到这里
    @Override
    public void onCompleted() { }

// 只要有异常抛出（包括操作符中的调用），会调到这里
    @Override
    public void onError(Throwable e) { }
};

//mySubscriber订阅myObservable
myObservable.subscribe(mySubscriber);  
```

## III. 通用接口

```
// Action1<T>(){ call(String): void}
myObservable.subscribe(onNextAction, onErrorAction, onCompleteAction);  

myObservable.subscribe(onNextAction);  
```

上面的代码最终可以变成这样

```
//Action1<T>
Observable.just("Hello, world!")
    .subscribe(s -> System.out.println(s));
```

## IV. 一些典型的操作符(Operators)

> 操作符用于在Observable和最终的Subscriber之间修改Observable发出的时间(RxJava提供了很多有用的操作符)

```
//假设定义了以下方法，接下来有些地方为了举例有用到
query(String) : Observable<List<String>> // 根据链接搜索结果
getTitle(String) : Observable<String> // 获取标题
saveTitle(String) : boolean // 保存标题
```

#### 1. map操作符

> 把一个事件转换为另一个事件 ( 不必返回Observable对象返回的类型，如下面就返回了int，而Observable返回的是String )

[map官方文档](http://reactivex.io/documentation/operators/map.html)

![](/img/rxjava-map.png)


```
Observable.just("Hello, world!")
    .map(s -> s.hashCode())
    .map(i -> Integer.toString(i))
    .subscribe(s -> System.out.println(s));
```



#### 2. from操作符

> 接收一个集合作为输入，然后每次输出一个元素给subscriber

[from官方文档](http://reactivex.io/documentation/operators/from.html)

![](/img/rxjava-from.png)

```
Observable.from("url1", "url2", "url3")  
    .subscribe(url -> System.out.println(url));
```

#### 3. flatMap操作符

> 接收一个Observable的输出作为输入，同时输出另外一个Observable （可以用来很好的解决多重嵌套回调的问题）

[flatMap官方文档](http://reactivex.io/documentation/operators/flatmap.html)

![](/img/rxjava-flatmap.png)

```
// 这里通过flatMap，输入一个Observable<List<String>>返回了一个新的Observable<String>

query("Hello, world!")  
    .flatMap(urls -> Observable.from(urls))
    .flatMap(url -> getTitle(url))
    .subscribe(title -> System.out.println(title));
```

#### 4. filter操作符

> 输入与输出为相同元素，过滤掉不满足检查条件的

[filter官方文档](http://reactivex.io/documentation/operators/filter.html)

![](/img/rxjava-filter.png)

```
query("Hello, world!")  
    .flatMap(urls -> Observable.from(urls))  
    .flatMap(url -> getTitle(url))  
    .filter(title -> title != null)  // 这里过滤掉了 title 为 null 的情况
    .subscribe(title -> System.out.println(title));  
```

#### 5. take操作符

> 输出最多指定数量的结果

[take官方文档](http://reactivex.io/documentation/operators/take.html)

![](/img/rxjava-take.png)

```
query("Hello, world!")  
    .flatMap(urls -> Observable.from(urls))  
    .flatMap(url -> getTitle(url))  
    .filter(title -> title != null)  
    .take(5) // 最多5个结果
    .subscribe(title -> System.out.println(title));  
```

#### 6. doOnNext操作符

> 在每次输出一个元素之前做一些额外的事情
```
query("Hello, world!")  
    .flatMap(urls -> Observable.from(urls))  
    .flatMap(url -> getTitle(url))  
    .filter(title -> title != null)  
    .take(5)  
    .doOnNext(title -> saveTitle(title))  // 做保存标题操作
    .subscribe(title -> System.out.println(title));  
```

#### 7. subscribeOn/observerOn操作符

> 通过`subscribeOn()`指定观察者运行的线程，`observerOn()`指定订阅者运行的线程

[What's the difference between SubscribeOn and ObserveOn](http://stackoverflow.com/questions/7579237/whats-the-difference-between-subscribeon-and-observeon)
```
Observable.from(someSource)  
    .map(data -> manipulate(data)) //将会在io线程执行
    .subscribeOn(Schedulers.io())
    .observeOn(AndroidSchedulers.mainThread())
    .subscribe(data -> doSomething(data)); // 将会在主线程(UI线程）执行
```

这里值得一提的是：看到了这里的`Schedulers.io()`来定义I/O线程十分的欣喜，之前在看`Fresco`的时候其中的一个Pipeline结构，它通过按照硬件资源占用比例，分类线程池，提高了`Fresco`的整体速度，由于`CPU`/`GPU`的速度远快于其他模块, 可以利用**尽量占满CPU资源**的原则，创建了多个线程池（如`CPU`、`I/O`、`NET`）来完成。使得资源得到最大的利用以提升速度。而`Schedulers.io`这种方式，也是通过架构的层面达到这种效果。

## V. 取消订阅(Subscriptions)

> 当调用`Observable.subscribe()`，会返回一个`Subscription`对象。这个对象代表了被观察者和订阅者之间的联系。

```
ubscription subscription = Observable.just("Hello, World!")
    .subscribe(s -> System.out.println(s));

subscription.unsubscribe(); //调用会停止整个调用链（会在当前正在执行的操作符的地方就终止）
System.out.println("Unsubscribed=" + subscription.isUnsubscribed());
// Outputs "Unsubscribed=true"
```

## VI. RxAndroid

> 是RxJava的一个针对Android平台的扩展。它包含了一些能够简化Android开发的工具
> **地址:** [https://github.com/ReactiveX/RxAndroid](https://github.com/ReactiveX/RxAndroid)

#### 1. AndroidSchedulers

> 提供了针对Android的线程系统的调度

```
retrofitService.getImage(url)
    .subscribeOn(Schedulers.io()) //操作符中间操作在I/0线程
    .observeOn(AndroidSchedulers.mainThread()) // subscribe 在UI线程
    .subscribe(bitmap -> myImageView.setImageBitmap(bitmap));
```

#### 2. AndroidObservable

> 它提供了跟踪Android生命周期的功能。`bindActivity()`和`bindFragment()`方法默认在UI线程调用，并且这两个方法会在生命周期结束的时候通知Observable停止发出新的消息。

```
AndroidObservable.bindActivity(this, retrofitService.getImage(url))
    .subscribeOn(Schedulers.io())
    .subscribe(bitmap -> myImageView.setImageBitmap(bitmap);
```

#### 3. AndroidObservable.fromBroadcast

> 功能类似`BroadcastReceiver`

```
// 实现了网络变化被通知到
IntentFilter filter = new IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION);
AndroidObservable.fromBroadcast(context, filter)
    .subscribe(intent -> handleConnectivityChange(intent));
```

#### 4. ViewObservable

> 可以很轻易的在View触发某些Action时，被通知

```
// 这里监听了mCardNameEditText的点击时间
ViewObservable.clicks(mCardNameEditText, false)
    .subscribe(view -> handleClick(view));

// 还可以进行很多监听，如ViewObservable.text就可以监听TextView的内容变化
```

## VII. 常见问题解决

#### 1. 在configuration改变（比如转屏）之后继续之前的Subscription/使用Retrofit发出了一个REST请求，接着想在listview中展示结果。如果在网络请求的时候用户旋转了屏幕怎么办？你当然想继续刚才的请求，但是怎么搞？

> 通过RxJava内置缓存机制解决
> **原理:** `cache()`(或者`replay()`)不会使`unsubscribe`打断，网络请求，因此在`unsubscribe`以后直接从`cache()`的返回值中创建一个新的`Observable`对象。

```
Observable<Photo> request = service.getUserPhoto(id).cache(); //缓存请求结果，缓存的地方需要具体实现(在这个案例中，应该缓存在生命周期以外的地方)
Subscription sub = request.subscribe(photo -> handleUserPhoto(photo));

//当Activity将需要重建(一般是销毁)的时候
sub.unsubscribe();

//一旦Activity重建
request.subscribe(photo -> handleUserPhoto(photo));
```
#### 2. Observable持有Context导致的内存泄露

> 参考解决方案: 在生命周期的某个时刻取消订阅
> **原理:** 利用`CompositeSubscription`持有所有的`Subscriptions`，然后在`onDestory()`或者`onDestroyView()`里取消所有的订阅。

```
// 一般可以在Activyt/Fragment的基类里面定义这个，达到系统化处理
private CompositeSubscription mCompositeSubscription
    = new CompositeSubscription();

private void doSomething() {
    mCompositeSubscription.add(
        AndroidObservable.bindActivity(this, Observable.just("Hello, World!"))
        .subscribe(s -> System.out.println(s)));
}

@Override
protected void onDestroy() {
    super.onDestroy();

    //一旦调用了CompositeSubscription.unsubscribe，CompositeSubscription对象就不可用了
    mCompositeSubscription.unsubscribe();
}
```

## VIII. 拓展

#### 1. Retrofit

> **功能:**  REST的网络架构，目前有[测试结果](http://themakeinfo.com/2015/04/retrofit-android-tutorial/)比Volley、AsyncTask快
> 目前Retrofit库内置了对RxJava的支持

```
//请求是获取照片
@GET("/user/{id}/photo")
Observable<Photo> getUserPhoto(@Path("id") int id);
//请求元数据
@GET("/user/{id}/photo/metadata")
Observable<Photo> getPhotoMetadata(@Path("id") int id);

// 将这两个请求并发的发出，并且等待两个结果都返回之后再做处理
Observable.zip(
    service.getUserPhoto(id),
    service.getPhotoMetadata(id),
    (photo, metadata) -> createPhotoWithData(photo, metadata))
    .subscribe(photoWithData -> showPhoto(photoWithData));
```

#### 2. 旧代码整合RxJava

> 比较简单的办法

如果`oldMethod`足够快:

```
private Object oldMethod() { ... }

public Observable<Object> newMethod() {
    return Observable.just(oldMethod());
}
```

如果`oldMethod`很慢，为了防止阻塞所在线程:

```
private Object slowBlockingMethod() { ... }

public Observable<Object> newMethod() {
    return Observable.defer(() -> Observable.just(slowBlockingMethod()));
}
```

----

[更多了解请移步>>](https://github.com/ReactiveX/RxJava/wiki)

#### 参考以下文档整理:

[Grokking RxJava, Part 1: The Basics](http://blog.danlew.net/2014/09/15/grokking-rxjava-part-1/)
[Grokking RxJava, Part 2: Operator, Operator](http://blog.danlew.net/2014/09/22/grokking-rxjava-part-2/)
[Grokking RxJava, Part 3: Reactive with Benefits](http://blog.danlew.net/2014/09/30/grokking-rxjava-part-3/)
[Grokking RxJava, Part 4: Reactive Android](http://blog.danlew.net/2014/10/08/grokking-rxjava-part-4/)


#### 参考以下博客的翻译校对:

[大头鬼Bruce](http://blog.csdn.net/lzyzsd)

#### 拓展阅读:

[不要打破链式：使用Rxjava的compose()操作符](http://www.pythonnote.com/archives/bu-yao-da-po-lian-shi-shi-yong-rxjavade-composecao-zuo-fu.html)

[RxAndroid(RxJava) 与 AsyncTask](http://blog.dreamtobe.cn/2312.html)

---

> © 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
