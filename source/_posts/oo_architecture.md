title: 架构设计基础知识整理
date: 2016-03-09 22:41:03
updated: 2020-01-02
permalink: 2016/03/09/oo_architecture/
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&amp;mid=2247483731&amp;idx=1&amp;sn=4084630e41a91848d9c72408d737a368
wechatmptitle: 架构设计基础知识整理(一)
categories:
- 架构
tags:
- 架构
- Android
- MVC
- MVP
- MVVM

---

> 星星点点的知识点，很早就想做这块整理了，持续维护...

## I. 原则:

> 灵活运用，而非刻意遵循

### 1. 基础原则

> 尽量少的重复代码，低耦合(尽量小的影响)，高内聚
> 模块，可小到一个类，大到一个系统

<!-- more -->

#### 模块间耦合因素

> 构建架构时，需要谨慎耦合的因素

- 模块间调用
- 模块间传递的数据量
- 模块间控制
- 模块间接口复杂度

#### 模块间耦合从弱到强顺序

> 构建架构或简单的类时，需要根据实际情况尽量契合弱的模块间耦合关系
> 做到职责分明，简单轻量，尽量少的潜在性的数据流动，尽量少的相互影响，避免牵一发而动全身

1. 非直接耦合: 相互之间没有直接关系，而是由第三方模块控制和调用
2. 数据耦合: 通过传递`java的内置数据类型`通讯
3. 标记耦合: 都引用了共同的数据结构，并且通过传递该数据结构通讯
4. 控制耦合: 通过传递开关、标志、名字等控制信息，明显的控制选择另一个模块的功能
4. 外部耦合: 都访问一个`java的内置数据类型`的全局变量
5. 公共耦合: 都访问了一个公共代码块( 全局数据结构、公共通讯区、内存公共覆盖区等)
6. 内容耦合: 一个模块直接修改另外一个模块的数据。

#### 降低耦合度的方法

- 少用类继承，多用类接口隐藏实现细节
- 模块功能尽量单一
- 拒绝重复代码
- 尽量不使用全局变量(Android中的全局变量会有一些坑，因为Attach在ClassLoader上的，因此根据不同ROM的优化，可能会在未预料的情况被unload，导致数据丢失)
- 类成员变量与方法少用`public`，多用`private`
- 尽量不用硬编码(如 字符串放到 `res/string.xml`，SQL语句做一层基于业务的封装供上层使用)
- 使用设计模式，尽量让模块间的耦合关系保证在数据耦合或更弱

### 2. 原则汇总

| 原则  | 基本概念 | 解决问题 | 基本实现
| --- | --- | --- | ---
| 开闭原则 | 对扩展开发，对修改关闭 | 实现热拔插，解耦方式 | 接口、抽象
| 里氏代换原则 | 子类是父类的具体抽象，抽象并可代表父类(`Is-A`) | 解释抽象化的具体原则 | 继承，抽象
| 依赖倒转原则 | 针对接口编程，依赖于抽象不依赖于具体 | 易于拓展 | 接口编程时类型使用基类，而不使用具体实现的子类
| 接口隔离原则 | 使用多个隔离接口，比使用单个接口要好 | 降低耦合 | 封装接口的时候，尽量用不同接口解决不同问题，尽量不要合用一个接口
| 迪米特法则 | 以实体为单位，实体之间的相互作用尽量的少 | 降低耦合 | 写一个系统架构，或模块的时候，尽量少的对外依赖
| 合成复用原则 | 优先使用合成/聚合，而非继承 | 可以通过引入抽象类更加灵活，相互耦合变小，更加简单 | 尽量将已有对象纳入到新对象中，成为新对象的一部分，而不使用继承的方式进行复用，如 `ClassLoader` 中双亲委派架构


#### 使用组合而非继承的场景:

> 优先使用对象组合，而非继承

- `Has-A`的关系，而非`Is-A`的关系
- 子类的主要目的是拓展父类，而非`override`或`final`，如果存在大量这种情况，改用组合
- 引入工具类，而非继承自工具类
- 有可能或不确定 子类 有可能被替换为 另外一个类的子类的情况 ( 如果出现这种情况，就需要修改。因此还不如使用 组合，如果有类似需求，再 组合如新的对象，进行拓展即可)


#### 继承需要注意

> 当已经选择使用继承时，需要注意

- 实现抽象方法，拓展新的特性方法，尽量少的重载父类非抽象方法
- 重载父类非抽象方法时: 方法前置条件(方法形参)要比父类方法更宽松，方法后置条件(方法返回值)要比父类更严格

#### 类之间的关系与UML表示

![](/img/architecture-class-relate.png)

## II. 常见的模式

### 1. MVC 与 MVP

![](/img/architecutre-mvp-mvc.gif)
From http://msdn.microsoft.com/en-us/library/ff647859.aspx

> MVP(Model-View_Presenter)是MVC(Model-View_Controller)的一个子集。

- MVC中`Controller`控制全局事务，`View`将事件发送给`Controller`，`Controller`处理完事件同步给`Model`(数据库/数据模型)，`View`是通过所绑定的`Model`的改变来刷新自己。
- MVP中`Presenter`从`View`中获取数据，刷新`Model`，当`Model`中的数据发生改变后，`Presenter`读取`Model`并刷新`View`。

### 2. Flux

在MVC中由于`View`与`Model`存在双向通讯，当业务逐渐复杂后，MVC势必会出现大量的`View`与`Model`交错通信的情况，这种情况是非常危险的，如:

![](/img/architecutre-mvc-issue.png)

基于这个Facebook在2017提出了一个新的架构概念叫Flux，它在`Model`与`View`的通信中间加入了`Dispatcher`，通过`Dispatcher`统一处理`Mode`与`View`的通信处理，讲究单项数据流:

![](/img/architecture-flux.png)

### 3. MVVM

![](/img/architecture-mvvm.png)

> MVVM(View<->ViewModel->Model)

在Android中可以通过`DataBinding`，直接在`Layout`文件中绑定其`ViewModel`。

- `View`: 布局
- `ViewModel`: 负责显示数据(监听到`Model`中的数据变化进行显示)，以及处理用户交互(监听`View`布局中的用户Action)
- `Model`: 存储内容

### 4. MVVM-C

![](/img/architecture-mvvm-c.png)

> MVVM-C(View-ViewModel-Callback-Model)

- `View`: 布局
- `Callback`: 通常可以是`Fragment`或`Activity`，用于处理用户交互(监听`View`布局中的用户Action)
- `ViewModel`: 显示数据(监听`Model`中的数据变化进行显示)
- `Model`: 存储内容

#### 5. 指令分离

> 这样的好处很明显，当你调用一个`getUser`的时候，符合预期的就是获取当前的User，而数据不会被修改;
> 而当你执行`login`的时候，也就是登陆，而非为了返回数据;

- 执行命令型的方法返回`void`
- 查询的方法才有返回值
- 抛`Exception`而非返回错误的值

如:

```java
// 登陆就用于登陆
UserService.login(username, password);
// 获取登陆的用户用另外的方法
User u = UserService.getUser();
```

#### 6. 得墨忒耳定律

> 最少知识原则，尽可能少的获知有限的知识，这是一种松耦合的具体案例

- 每个单元对于其他的单元只能拥有有限的知识：只是与当前单元紧密联系的单元；
- 每个单元只能和它的朋友交谈：不能和陌生单元交谈；
- 只和自己直接的朋友交谈。

如:

```java
// 错误的方式，这种方式调用者就必须要知道ObjectB，ObjectC
objectA.getObjectB().getObjectC().doSomething();
// 正确的方式，这样调用者只需要知道ObjectA，以及其有doSomething()这个接口即可
ObjectA.doSomething()
```

#### 7. "死亡参数"

> 当方法的参数过多或者没有严格规范时，久而久之可读性就会非常差，并且容易出现问题

- 当方法的参数达到或超过3个时，就要停下来思考，如果这些参数真这么紧密，[为什么他们不是一个对象](https://www.refactoring.com/catalog/introduceParameterObject.html)
- 当参数很多时，特别在Java中是十分影响可读性，考虑使用Builder Pattern
- 参入参数能采用不可变就使用不可变
- 当传入参数有`Boolean`时，考虑拆成两个方法，因为这种时候通常都是处理两种情况，更易于维护
- 避免传入参数有`null`的可能，如果允许这种情况，拆成另外一个无需传入该参数的方法，如果不允许，使用`@NotNull`来注解。


## III. 设计模式

### 1. 工厂方法模式

![](/img/architecture-factor-method.png)

### 2. 单例模式

#### Initialization-on-demand holder idiom
> [Wiki](https://en.wikipedia.org/wiki/Initialization-on-demand_holder_idiom)

> 性能高，线程安全 基于JVM [Class Loader保证Class唯一性线程安全的模型](http://blog.dreamtobe.cn/2015/12/07/android_dynamic_dex/)

```
public class Something {
    private Something() {}

    private static class LazyHolder {
        private static final Something INSTANCE = new Something();
    }

    public static Something getInstance() {
        return LazyHolder.INSTANCE;
    }
}
```

### 3. 建造者模式

> 与工厂模式区别是: 工厂模式关注构建单个类型类型；建造者模式关注构建符合类型对象。

![](/img/architecture-builder-method.png)

### 4. 原型模式

> 当前对象对外提供拷贝方法

#### 浅拷贝

> 除了基本数据类型外，其他类型的对象都只持有当前对象的引用，而非重新创建拷贝

##### Java中的`Object#clone`

1. `Object#clone()`就已经提供了该对象的浅拷贝
2. 如果需要使用`Object#clone`,需要类实现`Clonable`这个接口，来申明该类对象支持拷贝，否则会抛`CloneNotSupportedException`, 如果对象中存在队列成员变量，队列也需要实现`Clonable`

#### 深拷贝

> 所有成员变量都将重新创建

##### 方式一:

直接序列化(Java中基于JVM层级最简单的让对象支持序列化的方式，实现`Serializable`），拷贝二进制流。

##### 方式二(推荐）：

基于`Object#clone()`将非基本数据类型以外的元素都实现深拷贝，挨个深拷贝返回。


### 5. 适配器模式

![](/img/architecture-adapter-method.png)

### 6. 装饰模式

![](/img/architecture-decorator-method.png)

### 7. 代理模式

![](/img/architecture-proxy-method.png)

### 8. 外观模式

![](/img/architecture-facade-method.png)

### 9. 桥接模式

![](/img/architecture-bridge-method.png)

### 10. 组合模式

![](/img/architecture-composite-method.png)

### 11. 享元模式

![](/img/architecture-flyweight-method.png)

### 12. 策略模式

![](/img/architecture-strategy-method.png)

### 13. 模板方法模式

![](/img/architecture-template-method.png)

### 14. 观察者模式

![](/img/architecture-observer-method.png)

TODO

---

- [Java之美[从菜鸟到高手演变]之设计模式](http://blog.csdn.net/zhangerqing/article/details/8194653)
- [软件设计原则----合成/聚合复用原则（CARP）](http://blog.csdn.net/beyondhaven/article/details/6906050)
- [【设计模式】之六大原则（二）](http://m.blog.csdn.net/article/details?id=48834109)
- [软件设计之——“高内聚低耦合”](http://blog.csdn.net/csh624366188/article/details/7183726)
- [UML中几种类间关系：继承、实现、依赖、关联、聚合、组合的联系与区别](http://blog.csdn.net/sfdev/article/details/3906243)
- [UML Class Diagrams](http://pages.cs.wisc.edu/~hasti/cs302/examples/UMLdiagram.html)
- [Java之美[从菜鸟到高手演变]之设计模式二](http://blog.csdn.net/zhangerqing/article/details/8239539)
- [Java之美[从菜鸟到高手演变]之设计模式三](http://blog.csdn.net/zhangerqing/article/details/8243942)
- [Difference between asp.net MVC and MVP? are they both same?](http://stackoverflow.com/questions/19996963/difference-between-asp-net-mvc-and-mvp-are-they-both-same)
- [Shades of MVVM](https://www.bignerdranch.com/blog/shades-of-mvvm/)
- [Object Oriented Tricks: #1 The Art of Command Query Separation](https://hackernoon.com/oo-tricks-the-art-of-command-query-separation-9343e50a3de0)
- [Design principal: Understand Law of Demeter](https://android.jlelse.eu/design-principal-understand-law-of-demeter-4a44ac18e923)
- [Object Oriented Tricks: #3 Death By Arguments](https://hackernoon.com/object-oriented-tricks-3-death-by-arguments-d070ac86d996)

---
