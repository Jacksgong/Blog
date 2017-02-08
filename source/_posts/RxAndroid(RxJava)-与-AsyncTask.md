title: RxAndroid(RxJava) 与 AsyncTask
date: 2015-05-9 08:35:03
permalink: 2015/05/9/RxAndroid(RxJava)-与-AsyncTask
tags:
- AsyncTask
- RxJava
- 异步
- Java
- Android
- 框架

---

> 整理自[使用RxJava.Observable取代AsyncTask和AsyncTaskLoader](https://github.com/bboyfeiyu/android-tech-frontier/tree/master/androidweekly/使用RxJava.Observable取代AsyncTask和AsyncTaskLoader)

<!--more-->
## I. `AsyncTask`包含的问题:

```
private class CallWebServiceTask extends AsyncTask<String, Result, Void> {

        protected Result doInBackground(String... someData) {
            Result result = webService.doSomething(someData);
            return result;
        }

        protected void onPostExecute(Result result) {
            if (result.isSuccess() {
                resultText.setText("It worked!");
            }
        }
    }
```

1. 书写复杂
2. 异常处理困难（`try/catch`?）
3. `Activity/Fragment`的生命周期导致`AsyncTask`有不可预见的问题
4. 无法足够简单的做复杂的异步（串行异步/并行异步 同步UI）
5. 难以测试（[如何成功测试AyncTask的帖子](http://www.making-software.com/2012/10/31/testable-android-asynctask/)）
6. 异步数据无法得到良好的缓存



## II. 利用`RxAndroid(RxJava)`解决这些问题

#### 1. 关于书写复杂的问题:

> RxJava结合lambda是一个很好的解决方案

```
webService.doSomething(someData)
    .observeOn(AndroidSchedulers.mainThread())
    .subscribe(
        result -> resultText.setText("It worked!")),
        e -> handleError(e)
    );
```

#### 2. 关于异常处理困难的问题:

> RxJava 中所有的错误都会回调到onError

```
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
```

#### 3. 关于`Activity/Fragment`生命周期导致`AsyncTask`难以维护的问题:

> RxAndroid给出了很好的解决方案

```
 AppObservable.bindFragment(this, webService.doSomething(someData))
    .subscribe(
        result -> resultText.setText("It worked!")),
        e -> handleError(e)
    );
```

#### 4. 关于`AsyncTask`无法足够简单做复杂的异步的问题:

> RxJava中的各类"操作"可以解决这个问题，这里如果有较多的线程切换，可以考虑[使用`compose`](http://www.pythonnote.com/archives/bu-yao-da-po-lian-shi-shi-yong-rxjavade-composecao-zuo-fu.html)

```
//这里是一个链式Web Service调用的例子，这些请求互相依赖，在线程池中运行第二批并行调用，然后在将结果返回给Observer之前，对数据进行合并和排序。
public Observable<List<CityWeather>> getWeatherForLargeUsCapitals() {
    return cityDirectory.getUsCapitals()
        .flatMap(cityList -> Observable.from(cityList))
        .filter(city -> city.getPopulation() > 500,000)
        .flatMap(city -> weatherService.getCurrentWeather(city)) //each runs in parallel
        .toSortedList((cw1,cw2) -> cw1.getCityName().compare(cw2.getCityName()));
    }
```

#### 5. 关于`AsyncTask`难以测试:

> RxJava通过`toblocking()`将一个异步方法变为同步方法来完成测试

```
List results = getWeatherForLargeUsCapitals().toBlocking().first();
assertEquals(12, results.size());
```

#### 6. 关于`AsyncTask`异步数据无法得到良好的缓存

> 通过RxAndroid提供的方法，保存一个对Observable 的缓存的引用

```
 @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setRetainInstance(true);
        weatherObservable = weatherManager.getWeatherForLargeUsCapitals().cache();
    }

    public void onViewCreated(...) {
        super.onViewCreated(...)
        bind(weatherObservable).subscribe(this);
    }
```

> 如果你想要**避免缓存的Fragment**，可以通过使用**AsyncSubject实现缓存**（无论何时被订阅，AsyncSubject 都会重新发出最后的事件。或者我们可以使用BehaviorSubject获得最后的值和新值改变整个应用程序。）

```
//WeatherListFragment.java

public void onViewCreated() {
    super.onViewCreated()
    bind(weatherManager.getWeatherForLargeUsCapitals()).subscribe(this);
}
```

```
//WeatherManager.java

    public Observable<List<CityWeather>> getWeatherForLargeUsCapitals() {
    if (weatherSubject == null) {
        weatherSubject = AsyncSubject.create();

        cityDirectory.getUsCapitals()
            .flatMap(cityList -> Observable.from(cityList))
            .filter(city -> city.getPopulation() > 500,000)
            .flatMap(city -> weatherService.getCurrentWeather(city))
            .toSortedList((cw1,cw2) -> cw1.getCityName().compare(cw2.getCityName()))
            .subscribe(weatherSubject);
    }
    return weatherSubject;
    }

// weatherManager.invalidate(); //invalidate cache on fresh start
```

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
