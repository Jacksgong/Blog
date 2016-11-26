title: Kotlin
date: 2016-11-17 00:36:03
tags:
- Kotlin
- Java
- Programing

---

> 最近入职支付宝性能架构组，本想沉下心来，做前沿技术研究以及做架构、性能优化等事宜，于是乎在上家公司离职前，为最后造的打点轮子(Stamper)全面覆盖了Unit-test，打算进入支付宝后，所有的经我手的项目都有一定的单元测试保障，并且由于近三个月陆陆续续受到Realm News、Android Weekly、Jake Wharton等对新语言Kotlin的灌溉，打算在接下来一些新组件开发中采用Kotlin进行编写，却没曾想刚进支付宝，就赶上组内要出团队组件的demo、文档，并且已经被评估好时间，略有无奈与失望。今天偷偷早点回来(虽然到家已经不早了)，做点Kotlin的总结，保持学习吧。

Kotlin是一门为JVM、Android、前端开发的一门静态语言，相比Java8，它有太多的前瞻性的功能并且非常极客。

<!-- more -->

## I. 相比Java优势:

- 增量编译，Kotlin更快些
- 代码更精准有效，更可读
- 完全支持与Java的协同工作
- 更加安全，更加稳定的编写方式

#### 更加安全，更加稳定的编写方式

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
```

#### 代码更精准有效，更可读

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

## Kotlin使用

> 小技巧: 如果是不知道各类Kotlin特性，可以写出对应的Java代码，再通过Kotlin的Idea插件，直接将其转为Kotlin，从中学习。

---

TODO

---

- [Why You Must Try Kotlin For Android Development?](https://medium.com/@amitshekhar/why-you-must-try-kotlin-for-android-development-e14d00c8084b#.i677kd5qs)
- [Null Safety](https://kotlinlang.org/docs/reference/null-safety.html)
- [Advancing Android Development with Kotlin](https://realm.io/news/oredev-jake-wharton-kotlin-advancing-android-dev/)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
