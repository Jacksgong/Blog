title: Kotlin
date: 2016-11-30 14:02:03
updated: 2017-05-25
permalink: 2016/11/30/kotlin
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483734&idx=1&sn=a9761881ebd6632fc7e1417988002339
wechatmptitle: 重谈Kotlin
sticky: 3
categories:
- 编程语言
tags:
- Kotlin
- Java
- Programing
- Effective Java

---

{% note info %} Kotlin被Google官方扶正了，现在是Android开发的正式开发语言之一。Kotlin是一门为JVM、Android、前端开发的一门静态语言，相比Java8，它有太多的前瞻性的功能并且非常极客。{% endnote %}

<!-- more -->


> 因为其标准库有100Kb左右，所以暂时没有考虑在生产环境用，前段时间, 刚好接了支付宝几个内部组件，因此都用Kotlin写了，整体感觉很不错。顺便也写了一个[kotlin的开源库](https://github.com/Jacksgong/grpc-android-kotlin)，其中覆盖了rxkotlin的使用、kotlin单元测试编写，整个代码架构是以MVP为主，是一个很好的kotlin入门案例。

## 前言

让我来描述下写Kotlin的感觉的话，是真的很爽，简洁，可读性强，而且很多优秀的设计规范被语言层面支持使得应用起来非常简单。比如单例就一个`object`就搞定了，data就一个`data class`搞定，默认的调用变量就是调用其`get`、`set`还支持`delegate`；创建变量的时候不用指明类型赋值什么就是什么；如builder pattern本身由于argument就支持指明是赋值给哪个默认就支持；编写的时候还可以更加健壮的思考清楚哪个参数可以为`null`，哪个参数不能为`null`，哪个参数在调用时才创建，哪个参数在访问之前肯定会在某处被创建；默认就是`final`提高稳定性与可维护性；`let`简化if；`when`支持区间"switch"；还有各类geek的`null`条件判断方式；类似groovy之类的字符串内用`$`带上变量组字符串；Lambda；Stream等等的特性支持，代码可以很简洁，可读性也很强。

这门语言已经被打磨了6、7年了，而且是Jetbrains团队打造的，Android这边很早就有很多大神在推。社区也在这半年火起来，官方也非常努力，包括自己的bbs，stackoverflow之类的，我之前在Stackoverflow提了一个issue，马上就有官方来回答，并且kotlin可以与java协同开发，而且java工程师转过去的曲线也很平滑，至少比学习rxjava的难度低很多。

唯两个点:

1. Kotlin调用Java确实100%协同，但是Java调用Kotlin就比较绕，因为Kotlin本身的封装实现
2. 目前版本1.1全量proguard后kotlin标准库大小大概是100kb左右，意味着包大小会增大小于100kb(如果有些kotlin标准库中方法没有调用到，在proguard时会被移除)

针对第二个问题，其实我有做过探究，Kotlin本身设计时是为了Jetbrain工程师更高效的开发稳定的桌面IDE用的，刚开始的时候肯定在大小这块考虑的比较少，不过目前已经发展了6、7年了，看官方的描述现在已经一直在做这块的优化了，其实吧，标准库带来的kotlin的大小是kotlin不得不面对的一个问题，并且由于编译后有很多的判空，类封装，可能编译为class的逻辑代码虽然编写起来简单了，但是应该不会小多少估计还有可能变得更大。

---

我自己也用自己之前写的小应用做了一个简单的对比:

本文样本是一个简单的Apk，拥有远程截图、远程获知手机live、远程定位情况等。对比部分基本包含方法260左右方法数，可能由于部分kotlin特性没有用上在proguard的时候对应的方法就被移除了，因此在标准库这块可能与大幅度使用时会有略微偏差，这里的偏差不超过100KB(官方数据这块标准库Proguard后小于100KB)。

#### 非Proguard包对比

![](/img/kotlin-no-proguard.png)

- Kotlin的包大了300+KB
- Kotlin的包使用Kotlin的代码逻辑部分多了41个方法数

#### Proguard包对比

![](/img/kotlin-proguard.png)

- Kotlin的包大了50+KB
- Kotlin的包使用Kotlin的代码逻辑部分多了31个方法数
- 由于很多Kotlin框架方法没有被调用到，因此这块标准库被Proguard移除了83%的方法数

#### 方法采样对比

![](/img/kotlin-class-compare.png)

可以很明显的看到，虽然我们编写代码的时候很简洁，但是编译为class以后，多出了很多判空。

---

至于未来是否Android Framework SDK带上，我本人是不看好的，估计应该长期需要带这个标准库，类似Appcompat，如果是官方的Android Framework SDK，会带来两个问题（类似OkHttp的场景):

1. 只有某个版本后的Android支持，旧版本Android如何适配将成问题
2. 新版本的Kotlin特性无法全平台享用，也无法及时使用

而对于大多数同学关注的问题，其实[官方](http://kotlinlang.org/docs/reference/android-overview.html)已经说的很明白了:

- 兼容性: 兼容旧Android设备完全没问题
- 性能: 与Java一样快，并且由于支持inline、coroutine，甚至比java更快
- 协同: 与Kotlin 100%协同
- 大小: 如果全量带标准库，proguard后会大100kb左右
- 编译时间: 冷编译会慢些，但是由于增量编译，[非冷编译速度甚至比编译java还快](https://medium.com/keepsafe-engineering/kotlin-vs-java-compilation-speed-e6c174b39b5d)
- 学习曲线: java转过来很轻松(very easy)

## I. 相比Java优势:

- 增量编译，Kotlin更快些
- 代码更精准有效，更可读
- 完全支持与Java的协同工作
- 更加安全，更加稳定的编写方式

Kotlin语言是2010年Jetbrains团队为自己的团队打造的。宗旨是希望能够更简明并且消除一些Java的缺陷。由于Jetbrains团队原本打造的一系列的IDE都已经使用了Java，因此他们设计之初就考虑到Kotlin需要能够与Java协同工作，因此Kotlin是编译为Java字节码并且就考虑了如何才能让到Java工程师快速入门Kotlin。

### 根据《Effective Java》Kotlin的优化

#### 1. 不再需要builder:

在构造函数如果需要传入大量参数时，考虑到可读性，"Effective Java"在第二章中的谈到了[Builder Pattern](https://en.wikipedia.org/wiki/Builder_pattern)，以此构造与对象分离，达到更灵活、更可读。

在Kotlin中，由于它支持了为方法参数指定默认参数，以及支持在传入参数时，申明所赋值的参数名:

```kotlin
class KotlinNutritionFacts(
        private val servingSize: Int,
        private val servings: Int,
        private val calories: Int = 0,
        private val fat: Int = 0,
        private val sodium: Int = 0,
        private val carbohydrates: Int = 0)
```

```kotlin
val cocaCola = KotlinNutritionFacts(240,8,
                calories = 100,
                sodium = 35,
                carbohydrates = 27)
```

#### 2. 单例

在"Effective Java"的第三章中描述了单例，使得该对象在全局只有一个实例，十分的实用。

在Kotlin中，由于它支持了[Object declarations](https://kotlinlang.org/docs/reference/object-declarations.html#object-declarations)，因此可以非常简明的实现单例:

```kotlin
object KotlinElvis {

    fun leaveTheBuilding() {}
}
```

#### 3. 不用再主动编写`equals()`、`hashCode()`

在"Effective Java"的第十五章中建议到"除非有非常明确的理由，否则类都尽可能的定义为不可变"，在Java定义这么一个类是一件十分繁琐的事情，因为每一个对象都需要覆写他们的`equals()`与`hashCode()`，因此"Effective Java"在第8章与第9章通过了18页来篆述如何更好的完成这个。

在Kotlin中，由于它默认的[data classes](https://kotlinlang.org/docs/reference/data-classes.html)就已经默认实现了`equals()`、`hashCode()`等方法:

```kotlin
data class Person(val name: String, val age: Integer)
```

> P.S [AutoValue](https://github.com/google/auto/tree/master/value)为Java实现了类似的功能。


#### 4. 自动化`getter`与`setter`

在"Effective Java"的第十四章中建议到对于成员变量尽量使用方法可见(通常通过提供`getter`与`setter`实现)而非直接`public`。

在Kolin中，由于所有的成员变量，默认都是[property](https://kotlinlang.org/docs/reference/properties.html)，默认的对其的访问都是自动转为对其的`getter`与`setter`的访问，十分的简明:

```kotlin
class KotlinPerson {

    var name: String? = null

    var age: Int? = null
    set(value) {
        if (value in 0..120){
            field = value
        } else{
            throw IllegalArgumentException()
        }
    }
}

// 访问KotlinPerson

val person = KotlinPerson()
person.name = "Jacks"
person.age = 27
```

#### 5. `Overried`变为强制性注解

在Java 1.5中引入了`Overried`关键字，但这个关键字是`option`的，在"Effective Java"的第三十六章中说明了一定要加上这个注解一旦是覆写方法，否则在后期维护时很可能将覆写方法当做非覆写方法从而引来各种问题。

在Kotlin中，`override`变为了强制性的注解以避免类似的问题。


### 常用语法与特性

#### 1. 更加安全，更加稳定的编写方式

```kotlin
var a: String = “abc”; // 定义个一个非null的字符串变量a
a = null; // 编译直接失败

var b: String? = “abc”; // 定义一个可为null的字符串变量b
b = null; // 编译通过

val l = b.length; // 编译失败，因为b可能为null
l = b?.length ?: -1 // 如b为null，就返回-1
l = b?.length; // 如b为null，就返回null
l = b!!.length; // 如b为null，就会直接抛NPE错误
b?.let { println(b) } // 如b为null，就不执行let后面的代码块

val aInt: Int? = a as? Int // 如a不是Int类型，就回返回null

val nullableList: List<Int?> = listOf(1, 2, null, 4)
val intList: List<Int> = nullableList.filterNotNull() // 过滤出列表中所有不为null的数据，组成新的队列intList

// 可以通过lateinit var(不可为val)，定义一个无需在申明时初始化的non-nullable的参数，这个参数不允许被赋值为空，并且在调用时如果没有初始化会抛异常
lateinit var lateInitValue : String

// 通过by lazy { ... } 表达式，让所定义的参数在第一次访问(get)的时候执行{...}这段代码块，并赋值
val lazyValue: String by lazy {
  doAnything()
  "build lazy value"
}

// 通过by Delegates.observable("默认值")，在每次对该参数赋值的时候，都会回调回来
// vetoable是赋值前回调；observable是赋值后回调
var name: String by Delegates.observable("<no name>") {
    prop, old, new ->
    println("$old -> $new")
}

// 使用map来存储参数，通常是用于解析Json之类的键对数据结构
class User(val map: MutableMap<String, Any?>) {
        val name: String by map
        var age: Int     by map
}
val user = User(mapOf(
    "name" to "John Doe",
    "age"  to 25
))
println(user.name) // Prints "John Doe"

// 定义final的变量
val aFinalProperty : String = "final property"

// 定义final static的变量
class Values {
  companion object {
    val FINAL_STATIC_PROPERTY : String = "final static property"
  }
}
val something = Values.FINAL_STATIC_PROPERTY
```

#### 2. 代码更精准有效，更可读

```kotlin
// 智能cast
if (node is Leaf) {
    return node.symbol; //智能的将node转为Leaf类型，暴露Leaf的变量(symbol)
}

// 类似C++中的默认参数值
class Developer(val name: String,
 val age: Int,
 val someValue: Int = 0, // 当未传入someValue时，该参数将被赋值为0
 ) {
}
// 支持指明参数，可读性更强
val anand = Developer(name = “Anand Gaurav”, age = 20);

// 支持Java8的各项新特性
val numbers = arrayListOf(-42, 17, 13, -9, 12) //创建一个List，并给定值
val nonNegative = numbers.filter { it >= 0 } //从numbers中过滤出>=0的队列

// 下面这中Java8中的Stream特性，是不是特像RxJava
listOf(1, 2, 3, 4) // 列出 1, 2, 3, 4
.map { it * 10 } // 所有值乘以10 10, 20, 30, 40
.filter { it > 20 } // 过滤出>20的值 30, 40
.forEach { print(it) } // 打印出每个值 30, 40

// 通过as Button，进行转换，可读性更强
val button = findViewById(R.id.fab) as Button
button.setOnClickListener { view -> /* your code */} // lambda表达式

// 可以直接在赋值中使用表达式，甚至内嵌执行语句
val max = if (a > b) a else b
val max = if (a > b) {
    print("Choose a")
    a
} else {
    print("Choose b")
    b
}

// 支持when的表达式
println(when (language) {
    "EN" -> "Hello!"
    "FR" -> "Salut!"
    else -> "Sorry, I can't greet you in $language yet"
})

// 支持in，表达在一定的范围内作为条件
when (x) {
    in 1..10 -> print("x is in the range")
    in validNumberArray -> print("x is valid")
    else -> print("none of the above")
}

// 为Date类创建一个方法，方法名是isTuesday，执行内容是判断Date中的成员变量day是否等于2
fun Date.isTuesday() = day == 2

```

## II. Kotlin Unit-test

> 一般的单元测试是完全可以应付的，可以参考我写的[kotlin的开源库](https://github.com/Jacksgong/grpc-android-kotlin)，里面包含了一般的单元测试。

#### 1. 遇到的问题

对于编程设计来说，非常好的实践就是对拓展开放，对修改关闭的"开闭原则"，因为在Java中，我们对继承实在是太滥用了(可以参考[架构设计基础知识整理](https://blog.dreamtobe.cn/2016/10/25/oo_architecture/)中"使用组合而非继承")，也正是因为想要Kotlin中使这个情况得到好转，**因此Kotlin默认对所有Class与Method都是`final`的**， 除非使用`open`主动申明。

可是`final`的Class对于单元测试带来了一定的困难，因为我们在写Java的单元测试的时候，已经习惯了使用类似Mockito这样的库，去mock一些类，以达到纯粹的单元测试(参考[Android单元测试与模拟测试](https://blog.dreamtobe.cn/2016/10/28/android_test/))，正因为`final`类是不支持继承的，因此Mockito 2.1.0之前的版本对这样的类是无法mock的，虽然已经有了PowerMock，可以对静态方法进行mock，但是如果都使用PowerMock会显得很重，而且不灵活。

#### 2. 解决方法

##### 2.1 Javassist

> 实际测试kotlin-testrunner并不work，抽空的时候再研究研究，如果已经解决了欢迎评论指点

因为[Javassist](http://jboss-javassist.github.io/javassist/)这个开源库，支持在运行时修改Java字节码，因此刚好可以解决这个问题。dpreussler借助这个库写了一个[kotlin-testrunner](https://github.com/dpreussler/kotlin-testrunner)，创建一个ClassLoader，在加载指定类的时候将其`FINAL`的`modifiers`清除，并且通过`TestRunner`传入我们的ClassLoader，防止存在同一个Class在多个Loader中不唯一的问题(参考[Android 动态加载dex](https://blog.dreamtobe.cn/2015/12/07/android_dynamic_dex/))，以此解决该问题。

##### 2.2 Mockito 2.1.0 或更高版本

Mockito 2.1.0 及之后的版本原生支持了对`final`的method与class进行mock，使用方法与之前保持一致。 -- **实测是work的**。

**但是** 由于Mockito推出2.1.0时，对代码进行了大量的重构，虽然PowerMock已经在计划中通过2.0版本来对其进行适配，但是由于Mockito 2.1.0的重构，工作量还是比较大，因此还在[计划中](https://github.com/powermock/powermock/issues/706#issuecomment-264097614)。

#### 3. Kotlin单元测试总结

> 对于Kotlin Android项目的单元测试案例，可以参考[这里](https://github.com/Jacksgong/grpc-android-kotlin/tree/master/client-android/app/src/test/kotlin)

由于PowerMock还未适配Mockito v2.1.0，因此目前Kotlin中如果需要mock `static`的方法会麻烦些（可以使用通用方法: 封装一层`非static`的方法，在里面调用原本的`static`方法，然后对这个封装后的方法进行mock）。其他都比较流畅。

> 可以借助[nhaarman/mockito-kotlin](https://github.com/nhaarman/mockito-kotlin)使得更好的用Kotlin写单元测试。

## III. 实现写Java代码也能享受Kotlin的特性

> 无论是多出736KB的Kotlin基本库大小，还是公司不允许，**导致只能使用Java，但是又想使用一些Kotlin特性**。可以看看接下来提到的。

#### 1. Data classes

> Kotlin中`Data classes`特性，是在类前申明`data`，就会自动生成`equals()`、`hashCode()`、`toString()`、`copy()`方法。

Java中可以通过[Lombok - @Data](https://github.com/mplushnikov/lombok-intellij-plugin)实现这些特性。

#### 2. Lambda

> Kotlin支持绝大多数Java8的特性，但是Android目前还不支持Java8(虽然Jack&Jill编译器支持了，但是其在混淆等各方面的还不完善)。

Java7中的推荐使用[retrolambda](https://github.com/orfjackal/retrolambda)进行解决。

**需要特别注意的是**: Kotlin中采用`inline`Lambda是不会增加方法数的，但是使用Retrolambda/Jacks&Jill是会增加方法数的，可以参看下图([Jake Wharton在Exploring Java Hidden Costs演说](http://jakewharton.com/exploring-java-hidden-costs/)中提到的生成的方法数对比图):

![](/img/kotlin-1.png)

> P.S: Java对调用方法的开销可以参照: [Android优化 - 2.编码习惯](https://blog.dreamtobe.cn/2015/10/26/android_optimize/) 中的纂述。

#### 3. 数据控制与操作

> Kotlin中通过Streams(类似Java8的Streams)使得对数据的操作变得简单便捷，可读性高等特性。虽然Jack&Jill也提供了Streams的特性，但是要求最小sdk版本在24(`minSdkVersion = 24`)，不用考虑其他原因，就这一条目前就很难被接受。

Java7中推荐使用[Lightweight-Stream-API](https://github.com/aNNiMON/Lightweight-Stream-API)实现这些特性。

#### 4. 对类拓展函数

> Kotlin中支持在类外对某个已有类申明函数，十分的方便。

Java中可以通过[Lombok - @ExtensionMethod](https://github.com/mplushnikov/lombok-intellij-plugin)实现这些特性。

#### 5. 可读性折叠

> Kotlin中的各类更加可读的编写，使得代码看起来更加易懂简单，如(Kotlin: "My name is $name", Java: "My name is " + name)

Java7中可以通过Intelij的[Advanced Java Folding](https://plugins.jetbrains.com/plugin/9320-advanced-java-folding)插件实现这些特性，这个主要是通过Intelij IDEA的折叠代码的特性，使得代码折叠成类似Kotlin的更加可读的代码。

## IV. 为什么你可以开始使用Kotlin了

> 我们看了上面Kotlin这么多优势，那么我们是时候开始使用Kotlin了吗？答案是肯定的，现在是时候开始使用Kotlin了。

- Koltin非常容易入门: 相比于RxJava的学习曲线，Kotlin简单太多
- Google官方也在使用Kotlin: 如Android的[databinding compiler](https://android.googlesource.com/platform/frameworks/data-binding/+/master/compiler/src/main/kotlin/android/databinding/tool)
- Kotlin足够稳定可靠: Kotlin至今已经有7年的成长历史，最新版本是1.1，相比于你使用的其他开源库，Kotlin的稳定性更高
- Kotlin周边齐全: 由于是Jetbrains团队所开发的语言，而Android Studio又是基于Jetbrains开发的Intelij的，因此各类周边，包括Inspection等都是第一时间应用上的，包括各类社区、插件完全不用担心
- Kotlin兼容与Java协同开发: 正因为如此，我们可以使用所有的Java库的同时，也不必对已有的全局代码都进行修改，当然如果需要也可以通过Kotlin插件一键将Java代码转化为Kotlin代码

---

- [Why You Must Try Kotlin For Android Development?](https://medium.com/@amitshekhar/why-you-must-try-kotlin-for-android-development-e14d00c8084b#.i677kd5qs)
- [Null Safety](https://kotlinlang.org/docs/reference/null-safety.html)
- [Advancing Android Development with Kotlin](https://realm.io/news/oredev-jake-wharton-kotlin-advancing-android-dev/)
- [Classes and Inheritance](https://kotlinlang.org/docs/reference/classes.html)
- [Never say final: mocking Kotlin classes in unit tests](https://medium.com/@dpreussler/never-say-final-mocking-kotlin-classes-in-unit-tests-314d275b82b1#.665w1rs47)
- [Kotlin - lateinit VS Any? = null](http://stackoverflow.com/questions/35691123/kotlin-lateinit-vs-any-null)
- [Delegated Properties](https://kotlinlang.org/docs/reference/delegated-properties.html)
- [Kotlin - Property initialization using “by lazy” vs. “lateinit”](http://stackoverflow.com/questions/36623177/kotlin-property-initialization-using-by-lazy-vs-lateinit)
- [Static data in Kotlin](http://stackoverflow.com/questions/37482378/static-data-in-kotlin#)
- [Living(Android) without Kotlin](https://hackernoon.com/living-android-without-kotlin-db7391a2b170#.dcvfz0j06)
- [How “Effective Java” may have influenced the design of Kotlin — Part 1](https://medium.com/@lukleDev/how-effective-java-may-have-influenced-the-design-of-kotlin-part-1-45fd64c2f974#.r7qt7y819)
- [Android Testing with Kotlin](http://fernandocejas.com/2017/02/03/android-testing-with-kotlin/)
- [Kotlin in Production: Should you stay or should you go?](https://hackernoon.com/kotlin-in-production-should-you-stay-or-should-you-go-a3428b44b236)
- [Making Java Code Easier to Read (Without Changing it)](https://medium.com/@andrey_cheptsov/making-java-code-easier-to-read-without-changing-it-adeebd5c36de)

---
