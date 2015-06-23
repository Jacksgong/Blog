title: Falcon Pro 3 如何完成独立开发演讲分析
date: 2015-06-14 08:35:03
tags:Falcon,Joaquim,分析,Android,优化
---

> 演讲者: Joaquim
> 地址: http://realm.io/news/joaquim-verges-making-falcon-pro-3/

## I. 作者介绍

> 工作: UpThere, Palo Alto

主要是简述了，作者的业余项目: Falcon

## II. 所用到的库

### 加入了4个library:

1. Picasso
2. Retrofit
3. Otto(Event bus)(可选择)
4. Butter Knife

<!--more-->

### 新的页面使用Activity:

> 相对于目前盛行的用Fragment替代Activity来提高效率，Joaquim建议新的页面使用Activity

1. 目前在Lollipop上已经有了新的transition API
2. 可以事件驱动启动，如notification或者是Intent Filter，而不用写一些跳转的逻辑代码
3. 很好的恢复场景的机制
同一个Activity里面，复用Fragment(s)

### 缓存机制 ：

> 一个好的App需要一个非常出色的缓存机制

#### 1. ORMLite

> 基于SQLite、开源、基于Java

```
//表
@DatabaseTable(tableName = "accounts")
public class Account {
    
    @DatabaseField(id = true)
    private String name;
    
    @DatabaseField(canBeNull = false)
    private String password;
    
    // getters & setters
}
```

```
// 写入数据库

// if you need to create the 'accounts' table make this call
TableUtils.createTable(connectionSource, Account.class);

// instantiate the DAO to handle Account with String id
Dao<Account, String> accountDao =
        databaseHelper.getDao(Account.class);
        
//create an instance of Account
String name = "Jim Smith";
Account account = new Account(name, "_secret");

// persist the account object to the database
accountDao.create(account);
```

```
// 搜索，读取数据
QueryBuilder queryBuilder = databaseHelper
    .getDao(Account.class).queryBuilder();

Where where = queryBuilder.where();
where.or(
    where.and(
      where.eq("name", "foo"),
      where.eq("password", "_secret")),
    where.and(
      where.eq("name", "bar"),
      where.eq("password", "qwerty")
    )
);
where.query();
```

#### 2. Realm (胜出)
> 基于TightDB，基于C++闭源内核，开源Java绑定(bindings)

牺牲了灵活性，为了让开发更加简单(继承自`RealmObject`)

更加干净，简洁


```
// 表

public class Account extends RealmObject {
    
    private String name;
    private String password;
    
    // getters & setters
}
```

```
// 写入数据库

// instantiate
Realm realm = Realm.getInstance(this);// context

// begin transaction
realm.beginTransaction();

// create and fill objects to persist
Account account = realm.createObject(Account.class);
account.setUsername("Jim Smith");
account.setPassword("_secret");

// commit the transaction
realm.commitTransaction();
```

```
// 搜索，读取数据

RealmQuery query = realm.where(Account.class);

query.beginGroup()
        .equalTo("name", "foo")
        .equalTo("password", "_secret")
      .endGroup()
      .or()
      .beginGroup()
        .equalTo("name", "bar")
        .equalTo("password", "_qwerty")
      .endGroup();

query.findAll();
```

#### 速度对比
> 搜索 主线程搜索10000数据

Realm声称快**7倍**对比SQLite。

Falcon所有搜索都在主线程，对于作者而言，这是一种解放也是一种改革。

![](/img/Screenshot_6_2_15__3_18_PM.png)

线程方面：
[NanoTasks](https://github.com/fabiendevos/nanotasks) 对AsyncTasks封装

```
Tasks.executeInBackground(context, new BackgroundWork<Data>() {
    @Override
    public Data doInBackground() throws Exception {
        return fetchData(); // expensive operation
    }
}, new Completion<Data>() {
    @Override
    public void onSuccess(Context context, Data result) {
        display(result);
    }
    @Override
    public void onError(Context context, Exception e) {
        showError(e);
    }
});
```


## III. UI

### 1. 使用RecyclerView 替代ListView

#### 缺点:
ListView: 3,905行代码 + AbsListView中7,314行代码
RecyclerView: 一个巨大的class，中8,427行

#### 优点:
1. 提供了插入和删除的附加动画
2. 更好的处理未知变化

```
RecyclerView recyclerView = new RecyclerView(getActivity());
LinearLayoutManager layoutManager = new LinearLayoutManager(getActivity());
recyclerView.setLayoutManager(layoutManager);

layoutManager.scollToPosition(0);
recyclerView.scrollToPosition(0);
```

## IV. 动画

#### Android L:
1. Activity Transitions
2. Shared elements

实际应用的时候，需要注意的是，动画应该是在Vieww已经完全加载好了（有可能需要动画的部分数据是需要来自网络）之后开始，可以采用的解决方法:
1. 延时启动过渡(postpone start transition)
2. 启动延时过渡(start postpone transition)

ps: support包有一个简单的判断是Android L的静态方法:`versionUtils.isAtLeastL`

#### LayoutTransitions ( API 1开始就有): 

非常强大，布局变化或者Visible/Gone这类的切换动画。考虑用这个，简单强大。

#### AnimationUtils

一般的动画，可以参考下github上其他人的一些好的封装，做一些简单的fade啊、slide啊、缩放啊非常方便。


## V. 帧率控制

> Android 保持在60Hz，16ms 每次draw

### 1) 不要做

#### 1. View层级不要太深

 保持Layout平坦，不要有深层级
 
#### 2. 谨慎创建对象(避免在View draw流程中（onMearsure、onLayout、onDraw...）创建对象

因为gc会带来很多帧率上的损失

#### 3. 减少重绘

保证尽量少的 不透明背景 相互覆盖，因为GPU 不得不一遍又一遍的画这些图层。

### 2) 可以使用的Android系统的工具

> 这些在 1、2在设置->开发者选项 里面，3、4是Android Studio上的功能

#### 1. GPU 呈现模式分析(GPU Rendering Profiling)

> 可以分析出哪些是在16ms以内，什么时候超过了16ms（60Hz，掉帧哦~...）

**千万避免在View中设置透明度**，特别是在自定义的View上（一般来说ImageView、TextView(ButtonView..)是没有问题的），Falcon作者，在一次检测GPU呈现模式的时候，发现一个设置透明度，导致了Frame的渲染慢了一倍多。

具体原因是由于，一旦设置了Alpha，每次draw 那个View都不得不 清除绘制缓存(Flush Buffer)，然后再绘制到屏幕上，效果如右图(顶部的那几个小点setAlpha(0.5*255))。
 
![](/img/The_Making_of_Falcon_Pro_3_by_Joaquim_Vergès__Video__-_Realm_is_a_mobile_database__a_replacement_for_SQLite___Core_Data.png)

#### 2. 调试CPU过渡绘制

检测重绘神器。

#### 3. 内存监控

Android Studio上的一个功能。

#### 4. 内存创建跟踪(Allocation tracker)

也是Android Studio上的一个功能。

具体教程可以看这里: [https://developer.android.com/tools/debugging/debugging-studio.html#allocTracker](https://developer.android.com/tools/debugging/debugging-studio.html#allocTracker)


## VI. 设计

> Falcon 可是 Joaquim自己设计的!

#### 1. 草图
可以使用软件sketch

#### 2. 颜色选择方面

可以使用[coolors.co](http://coolors.co/)，可以很快的定位好整个app的颜色。Joaquim大概就用了10分钟

这边我也推荐一个[Paletton.com](http://paletton.com/#uid=72P0+0kllllaFw0g0qFqFg0w0aF),也很不错。

#### 3. Icon

说实话作为开发，确实不愿意花太多时间去设计icon，但是Google对外开放了200多个icon素材。

**更好的方法**: 一款intellij(或者Android Studio（同一平台idea）)的插件: [https://github.com/konifar/android-material-design-icon-generator-plugin](https://github.com/konifar/android-material-design-icon-generator-plugin) 自动生成Material icon确实好屌。

#### 4. 字体方面

Joaquim只用了Android SDK的: `android:font_family`，完全够用：

![](The_Making_of_Falcon_Pro_3_by_Joaquim_Vergès__Video__-_Realm_is_a_mobile_database__a_replacement_for_SQLite___Core_Data 2.png)

#### 5. 视觉宗旨定义

Joaquim定位Falcon是内容至上。

## VII. Crash报告与分析

Falcon使用了: [Crashlytics](https://try.crashlytics.com/)，评价很高，一行代码，搞定90%的需求。

## VIII. 安全

### 1. 混淆

最基本的保障，反编译以后极大减小可读性。

### 2. LVL

> The License verification library from Google

不值得，如果说要保证交易安全，应该在成交之前，在自己的服务器上做更多的验证（EAPs）

## IX. Beta

Joaquim不建议到Google+ communites做测试，没啥用。

## X. 发布

### 1. 视频肯定要的

adb shell screenrecord

### 2. Banner

选取好的截图，附上网址、logo等等。

### 3. 截图

Joaquim不喜欢 赤裸裸的截图，喜欢重构布局、装饰以后的截图。

### 4. Icon

用心设计

## XI. 迭代

> 让用户来驱动，通过不断，快速的对用户的反馈评论做出应答的方式，来升级应用。

1. 通过尽量快的应答用户，让用户感觉他们也是产品项目的一员。
2. 通过用户反馈，来生成项目接下来要做的清单。
3. 解决用户的问题，因为他们将会成为你最好的客户。