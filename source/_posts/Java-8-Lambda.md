title: Java 8 Lambda
date: 2015-04-28 08:35:03
updated: 2015-04-28 08:35:03
permalink: 2015/04/28/Java-8-Lambda
categories:
- 编程语言
tags:
- java
- Lambda
- Android
- 优化

---

#### 发布时间
Java SE 8在2013年6月13的版本中已经完全了全部的功能

## I. Lambda表达式
> 函数式接口(functional interface): 只包含一个抽象方法的接口(如`Runnable`只有run()这么一个方法)



<!--more-->
#### 举例
`Runnable`:

```
new Thread(new Runnable() {
        public void run() {
            System.out.println("Run!");
        }
    }).start();
```

```
//由形式参数和方法体两部分组成，中间通过“->”分隔
new Thread(() -> {
        System.out.println("Run!");
    }).start();
```



使用: `java.util.function.Function`方式:

```
public class CollectionUtils {
    public static  List map(List input, Function processor) {
        ArrayList result = new ArrayList();
        for (T obj : input) {
            result.add(processor.apply(obj));
        }
        return result;
    }

    public static void main(String[] args) {
        List input = Arrays.asList(new String[] {"apple", "orange", "pear"});
        List lengths = CollectionUtils.map(input, (String v) -> v.length());
        List uppercases = CollectionUtils.map(input, (String v) -> v.toUpperCase());
    }
}
```

## II. 方法引用

> 可以在不调用某个方法的情况下引用一个方法

#### 举例

```
List input = Arrays.asList(new String[] {"apple", "orange", "pear"});

//Lambda表达式方式
input.forEach((v) -> System.out.println(v));

// 方法引用 方式
input.forEach(System.out::println);
```

## III. 构造方法引用

> 可以在不创建对象的情况下引用一个构造方法

#### 举例

```
List dateValues = Arrays.asList(new Long[] { 0L, 1000L});

List dates = CollectionUtils.map(dateValues, Date::new);
```

## IV. 接口默认方法

> 通过新的`default`关键词来修饰，为接口提供默认方法

#### 解决问题

1. **接口演化问题：** 通过新增默认接口方法来搞定新增的功能，而无需新增方法，在所有的实现类中改，当然，默认方法支持复写

2. **实现多继承的行为：** 一个类实现多个接口，就包含了默认方法的方法体

#### 举例

```
//一个简单的货币转换接口，假设需要调用的是第三方服务
public interface CurrencyConverter {
    BigDecimal convert(Currency from, Currency to, BigDecimal amount);
}
```

```
//当第三方提供了新的批量处理的功能，允许在一次请求中同事转换多个数值
//这里就可以直接通过 新增一个默认方法来解决
public interface CurrencyConverter {
    BigDecimal convert(Currency from, Currency to, BigDecimal amount);

    default List convert(Currency from, Currency to, List amounts) {
        List result = new ArrayList();
            for (BigDecimal amount : amounts) {
                result.add(convert(from, to, amount));
            }
            return result;
    }
}
```

## V. 推荐

Android开发中，推荐使用[retrolambda](https://github.com/evant/gradle-retrolambda)这个gradle插件。

----

> 整理自: [Java SE 8: Lambda表达式](http://www.infoq.com/cn/articles/Java-se-8-lambda)

---
