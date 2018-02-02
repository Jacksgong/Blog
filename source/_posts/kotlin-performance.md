title: Kotlin运行时性能
date: 2017-07-12 00:47:03
updated: 2017-07-12
wechatmpurl: https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483756&idx=1&sn=4342775021bb9fa1b60ebc454293bd1e
wechatmptitle: Kotlin运行时性能
categories:
- 编程语言
tags:
- Kotlin
- Java
- Performance

---

{% note info %}Kotlin整体的性能相对于Java而言毫不逊色，甚至在一些方面优于Java，本文参考[这篇benchmark文章](https://sites.google.com/a/athaydes.com/renato-athaydes/posts/kotlinshiddencosts-benchmarks)进行Kotlin性能相关总结，关于Kotlin对包大小影响、使用、选择原因等请参考之前的一篇[Kotlin](https://blog.dreamtobe.cn/2016/11/30/kotlin/)的文章，如果对于Java运行时性能感兴趣可以参考[这篇文章](https://blog.dreamtobe.cn/2015/10/26/android_optimize/)。 {% endnote %}

<!-- more -->

## 前言

根据[benchmark文章](https://sites.google.com/a/athaydes.com/renato-athaydes/posts/kotlinshiddencosts-benchmarks )所有的所有测试均采样200次，使用单位ops/ms(执行次数/毫秒)(因此数值是越大越好)并且均在以下环境:

- Macbook Pro (2,5 GHz Intel Core i7, 16GB of RAM)
- Java HotSpot(TM) 64-Bit Server VM (build 25.131-b11, mixed mode)
- Kotlin version (1.1.3)
- JMH (0.5.6)

---

## 性能测试结果

### 1. 性能相比Java更差相关

- 对`varargs`参数展开，**Kotlin比Java慢1倍**，主要原因是在Kotlin在展开`varargs`前需要全量拷贝整个数组，这个是非常高的性能开销。
- 对`Delegated Properties`的应用，**Kotlin相比Java慢10%**。

### 2. 性能相比Java更优相关

- 对`Lambda`的使用，**Kotlin相比Java快30%**，而对用例中的`transaction`添加`inline`关键字配置内联后，发现其反而慢了一点点(约1.14%)。
- Kotlin对`companion object`的访问相比Java中的静态变量的访问，**Kotlin与Java差不多快或更快一点**。
- Kotlin对局部函数(`Local Functions`)的访问相比Java中的局部函数的访问，**Kotlin与Java差不多快或更快一点**。
- Kotlin的非空参数的使用相比没有使用空检查的Java，**Kotlin与Java差不多快或更快一点**。

### 3. Kotlin自身比较

- 对于基本类型范围的使用，无论是否使用`常量引用`还是`直接的范围`**速度都差不多**。
- 对于非基本类型范围的使用，`常量引用`相比`直接的范围`**会快3%左右**。
- 对于范围遍历方式中，`for`循环方式无论有没有使用`step`速度都差不多，但是如果对范围直接进行`.foreach`速度会比它们**慢3倍**，因此避免对范围直接使用`.foreach`。
- 在遍历中使用`lastIndex`会比使用`indices`**快2%左右**。

---

## 实验过程

### I. 性能相比Java更差相关

#### 1. `varargs`参数

测试发现: 对`varargs`参数展开，**Kotlin比Java慢1倍**，主要原因是在Kotlin在展开`varargs`前需要全量拷贝整个数组，这个是非常高的性能开销。

测试用例`Kotlin`代码:

```kotlin
fun runPrintDouble(blackHole: BlackHole, values: IntArray) {
    printDouble(blackHole, *values)
}

fun printDouble(blackHole: BlackHole, vararg values: Int) {
    for (value in values) {
        blackHole.consume(value)
    }
}
```

测试用例`Java`代码:

```java
public static void runPrintDouble( BlackHole blackHole, int[] values ) {
    printDouble( blackHole, values );
}

public static void printDouble( BlackHole blackHole, int... values ) {
    for (int value : values) {
        blackHole.consume( value );
    }
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `javaIntVarargs`  | 173265.270 | 260.837
| `kotlinIntVarargs` | 83621.509 | 990.854

![](/img/kotlin-performance-1.png)

#### 2. `Delegated Properties`

测试发现：对`Delegated Properties`的应用，**Kotlin相比Java慢10%**。

测试用例`Kotlin`代码:

```kotlin
class StringDelegate {
   private var cache: String? = null

   operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
       var result = cache
       if (result == null) {
           result = someOperation()
           cache = result
       }
       return result!!
   }

   operator fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
       cache = value
   }
}

class Example {
    var p: String by StringDelegate()
}

fun runStringDelegateExample(blackHole: BlackHole) {
    val example = Example()
    blackHole.consume(example.p)
    blackHole.consume(example.p)
}
```

测试用例`Java`代码:

```java
class DelegatePropertyTest {

   public static String stringValue = "hello";

   public static String someOperation() {
       return stringValue;
   }

}

class Example2 {
    public String p;

    public void initialize() {
        p = DelegatePropertyTest.someOperation();
    }
}

public static void runStringDelegateExample( BlackHole blackHole ) {
    Example2 example2 = new Example2();
    example2.initialize();
    blackHole.consume( example2.p );
    blackHole.consume( example2.p );
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `javaSimplyInitializedProperty`  | 274394.088 | 554.171
| `kotlinDelegateProperty` | 255899.824 | 910.112

![](/img/kotlin-performance-2.png)

### II. 性能相比Java更优相关

#### 1. Lambda

> 由于Lambda是在Java8中引入，所以对比的是Java8与Kotlin1.1.3

测试发现：对`Lambda`的使用，**Kotlin相比Java快30%**，而对用例中的`transaction`添加`inline`关键字配置内联后，发现其反而慢了一点点(约1.14%)。

测试用例`Kotlin`代码:

```kotlin
fun transaction(db: Database, body: (Database) -> Int): Int {
    db.beginTransaction()
    try {
        val result = body(db)
        db.setTransactionSuccessful()
        return result
    } finally {
        db.endTransaction()
    }
}

fun kotlinLambda() {
    val deletedRows = transaction(db) {
        it.delete("Customers", null, null)
    }
}
```

测试用例`Java`代码:

```java
public static int transaction( Database db, ToIntFunction<Database> body ) {
    db.beginTransaction();
    try {
        int result = body.applyAsInt( db );
        db.setTransactionSuccessful();
        return result;
    } finally {
        db.endTransaction();
    }
}

void javaLambda() {
    int deletedRows = transaction( db, ( database ) ->
           database.delete( "Customer", null, null ) );
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `javaLambda`  | 1024302.409 | 1851.789
| `kotlinInlinedFunction` | 1344885.445 | 2632.587
| `kotlinLambda` | 1362991.121 | 2824.862

![](/img/kotlin-performance-3.png)

#### 2. 静态(`Companion Objects`)变量访问

测试发现：Kotlin对`companion object`的访问相比Java中的静态变量的访问，**Kotlin与Java差不多快或更快一点**。

测试用例`Kotlin`代码:

```kotlin
class MyClass private constructor() {

    companion object {
        private val TAG = "TAG"

        fun newInstance() = MyClass()
    }

    fun helloWorld() = TAG
}

fun runCompanionObjectCallToPrivateConstructor(): String {
    val myClass = MyClass.newInstance()
    return myClass.helloWorld()
}
```

测试用例`Java`代码:

```java
class MyJavaClass {

    private static final String TAG = "TAG";

    private MyJavaClass() {
    }

    public static String helloWorld() {
        return TAG;
    }

    public static MyJavaClass newInstance() {
        return new MyJavaClass();
    }
}

public static String runPrivateConstructorFromStaticMethod() {
    MyJavaClass myJavaClass = newInstance();
    return myJavaClass.helloWorld();
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `javaPrivateConstructorCallFromStaticMethod`  | 398709.154 | 800.190
| `kotlinPrivateConstructorCallFromCompanionObject` | 404746.375 | 621.591

![](/img/kotlin-performance-4.png)

#### 3. 局部函数(`Local Functions`)访问

测试发现：Kotlin对局部函数的访问相比Java中的局部函数的访问，**Kotlin与Java差不多快或更快一点**。

测试用例`Kotlin`代码:

```kotlin
fun kotlinLocalFunctionCapturingLocalVariable(a: Int): Int {
    fun sumSquare(b: Int) = (a + b) * (a + b)

    return sumSquare(1) + sumSquare(2)
}

fun kotlinLocalFunctionWithoutCapturingLocalVariable(a: Int): Int {
    fun sumSquare(a: Int, b: Int) = (a + b) * (a + b)

    return sumSquare(a, 1) + sumSquare(a, 2)
}
```

测试用例`Java`代码:

```java
public static int javaLocalFunction( int a ) {
    IntUnaryOperator sumSquare = ( int b ) -> ( a + b ) * ( a + b );

    return sumSquare.applyAsInt( 1 ) + sumSquare.applyAsInt( 2 );
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `javaLocalFunction`  | 897015.956 | 1951.104
| `kotlinLocalFunctionCapturingLocalVariable` | 909087.356 | 1690.368
| `kotlinLocalFunctionWithoutCapturingLocalVariable` | 908852.870 | 1822.557

![](/img/kotlin-performance-5.png)

#### 4. 空检查(`Null safety`)

测试发现：Kotlin的非空参数的使用相比没有使用空检查的Java，**Kotlin与Java差不多快或更快一点**。

测试用例`Kotlin`代码:

```kotlin
fun sayHello(who: String, blackHole: BlackHole) = blackHole.consume("Hello $who")
```

测试用例`Java`代码:

```java
public static void sayHello( String who, BlackHole blackHole ) {
    blackHole.consume( "Hello " + who );
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `javaSayHello`  | 73353.725 | 155.551
| `kotlinSayHello` | 75637.556 | 162.963

![](/img/kotlin-performance-6.png)

### III. Kotlin自身比较

#### 1. 基本类型范围

测试发现: 对于基本类型范围的使用，无论是否使用`常量引用`还是`直接的范围`**速度都差不多**。

常量引用基本类型范围用例:

```kotlin
private val myRange get() = 1..10

fun isInOneToTenWithIndirectRange(i: Int) = i in myRange
```

直接引用基本类型范围的用例:

```kotlin
fun isInOneToTenWithLocalRange(i: Int) = i in 1..10
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `kotlinIndirectRange` | 1214464.562 | 2071.128
| `kotlinLocallyDeclaredRange`  | 1214883.411 | 1797.921

![](/img/kotlin-performance-7.png)

#### 2. 非基本类型范围

测试发现: 对于非基本类型范围的使用，`常量引用`相比`直接的范围`**会快3%左右**。

常量引用非基本类型范围用例:

```kotlin
private val NAMES = "Alfred".."Alicia"

fun isBetweenNamesWithConstantRange(name: String): Boolean {
    return name in NAMES
}
```

直接引用非基本类型范围的用例:

```kotlin
fun isBetweenNamesWithLocalRange(name: String): Boolean {
    return name in "Alfred".."Alicia"
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `kotlinStringRangeInclusionWithLocalRange` | 211468.439 | 483.879
| `kotlinStringRangeInclusionWithConstantRange` |  218073.886 | 412.408

![](/img/kotlin-performance-8.png)

#### 3. 范围遍历

测试发现: 对于范围遍历方式中，`for`循环方式无论有没有使用`step`速度都差不多，但是如果对范围直接进行`.foreach`速度会比它们**慢3倍**，因此避免对范围直接使用`.foreach`。

`for`循环的用例:

```kotlin
fun rangeForEachLoop(blackHole: BlackHole) {
    for (it in 1..10) {
        blackHole.consume(it)
    }
}
```


`for`循环并且加上`step`的用例:

```kotlin
fun rangeForEachLoopWithStep1(blackHole: BlackHole) {
    for (it in 1..10 step 1) {
        blackHole.consume(it)
    }
}
```

对范围直接进行`.foreach`的用例:

```kotlin
fun rangeForEachMethod(blackHole: BlackHole) {
    (1..10).forEach {
        blackHole.consume(it)
    }
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `kotlinRangeForEachFunction` | 108382.188 | 561.632
| `kotlinRangeForEachLoop` | 331558.172 | 494.281
| `kotlinRangeForEachLoopWithStep1` | 331250.339 | 545.200

![](/img/kotlin-performance-9.png)

#### 4. 对于`indices`对比

测试发现: 使用`lastIndex`会比使用`indices`**快2%左右**。

先创建一个`SparseArray`:

```kotlin
class SparseArray<out T>(val collection: List<T>) {
    fun size() = collection.size
    fun valueAt(index: Int) = collection[index]
}
```

使用`indices`的用例:

```kotlin
inline val SparseArray<*>.indices: IntRange
    get() = 0..size() - 1

fun printValuesUsingIndices(map: SparseArray<String>, blackHole: BlackHole) {
    for (i in map.indices) {
        blackHole.consume(map.valueAt(i))
    }
}
```

使用`lastIndex`的用例:

```kotlin
inline val SparseArray<*>.lastIndex: Int
    get() = size() - 1

fun printValuesUsingLastIndexRange(map: SparseArray<String>, blackHole: BlackHole) {
    for (i in 0..map.lastIndex) {
        blackHole.consume(map.valueAt(i))
    }
}
```

测试结果(每毫秒执行次数):

| Benchmark | 平均值 | 平均误差  
| --- | --- |  ---  
| `kotlinCustomIndicesIteration` | 79096.631 | 134.813
| `kotlinIterationUsingLastIndexRange` | 80811.554 | 122.462

![](/img/kotlin-performance-10.png)

---
