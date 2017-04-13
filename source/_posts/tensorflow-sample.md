title: 敲开TensorFlow的大门
date: 2017-03-17 23:58:03
categories:
- 编程语言
tags:
- TensorFlow
- AI

---

{% note warning %} 目前的AI还处在比较低级的阶段，但是像TensorFlow的出现，极大的推进了AI的进程，使得各类应用可以以最低的成本最快的的时间接入AI，今天我们就通过一个简单的模型训练来敲开TensorFlow的大门。

AI的模型训练其实就是: 对模型变量的值进行不断调整，直到训练模型对所有可能的变量求出的结果都无限接近目标值，而我们要做的工作就是给足够的数据进行训练，以及不断优化训练算法 {% endnote %}

<!-- more -->

## I. macOS Sierra中配置运行环境

> 官方教程地址: https://www.tensorflow.org/install/install_mac#installing_with_virtualenv

一共有四种方式，根据官方推荐，我采用的是virtualenv

> 由于我的MBP没有NVIDIA CUDA GPU，因此这里我没有配GPU

<script src="https://gist.dreamtobe.cn/Jacksgong/2f1f2779f08aa88342940a46540e6ea9.js"></script>

![](/img/tensorflow-sample-1.png)

<script src="https://gist.dreamtobe.cn/Jacksgong/21f03952c3f8214cdda4c2b3c97e786b.js"></script>

![](/img/tensorflow-sample-2.png)

<script src="https://gist.dreamtobe.cn/Jacksgong/734e15c59e02decc025246e75c06971f.js"></script>

![](/img/tensorflow-sample-3.png)

由于我的Python是2.7.10版本，并且没有支持GPU，因此执行:

<script src="https://gist.dreamtobe.cn/Jacksgong/a0d758b72f6b50c49646920bee6347e9.js"></script>

> 如果是其他情况的请参照[官方教程](https://www.tensorflow.org/install/install_mac#installing_with_virtualenv)

![](/img/tensorflow-sample-4.png)

#### 验证安装

> 官方地址: https://www.tensorflow.org/install/install_mac#ValidateYourInstallation

![](/img/tensorflow-sample-5.png)

## II. 训练模型案例

> 该案例来自[官方的入门案例](https://www.tensorflow.org/get_started/get_started)

<script src="https://gist.dreamtobe.cn/Jacksgong/03258a8e0f536ea8d01f64210a8a839d.js"></script>

![](/img/tensorflow-sample-6.png)

该次模型训练的性能决定因素是: 优化器选择、精度选择、训练数据

#### 通过高级的接口快速的实现上面的模型训练

<script src="https://gist.dreamtobe.cn/Jacksgong/1d9fc40f9affe4478c06cb71004f957a.js"></script>

当然我们也可以通过`tf.contrib.learn.Estimator`这个高级接口，再使用低级接口来定制Linear Regressor算法模型(实际上内置的`tf.contrib.learn.LinearRegressor`也是继承自`tf.contrib.learn.Estimator`的)。当然我们不是通过继承，是通过提供`model_fn`来告诉他训练的步骤、如果评估等:

<script src="https://gist.dreamtobe.cn/Jacksgong/355d0129457eec50ffe2dcbd15763352.js"></script>

## III. 常见的API

> 具体API可以参看[官网文档](https://www.tensorflow.org/api_docs/)

![](/img/tensorflow-sample-7.jpg)

- 定义常量: `tf.constant(value, type)`，如`tf.constant(3.0, tf.float32)`，当type没有给定的时候，会根据所给value定义
- 定义变量: `tf.placeholder(type)`, 如`tf.placeholder(tf.float32)`
- 定义训练模型: `tf.Variable([value], type]`, 如`tf.Variable([.3], tf.float32)`
- 计算结果: 通过`tf.Session()`的`run`去计算
- 初始化训练模型: `tf.global_variables_initializer()`，对其进行复位运行起对象即可，如Session对象是`sees`，初始化模型对象是`init`时: `sess.run(init)`
- 对模型重新赋值: 如对`W`模型重新赋值: `fixW = tf.assign(W, [-1.])`
- 求平方: `tf.square(value)`
- 求和: `tf.reduce_sum(value)`

---

> 欢迎阅读另一篇文章[训练识别数字图片的模型](/tensorflow-mnist/)，进一步的了解TensorFlow的使用。

---

[本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/tensorflow-sample.md)。

---

本文已经发布到JackBlog公众号: [敲开TensorFlow的大门 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483719&idx=1&sn=7f70a02d7d6ec49ab55354d9fa26768e)

---

- [Api Doc](https://www.tensorflow.org/api_docs/)
- [Getting Started With TensorFlow](https://www.tensorflow.org/get_started/get_started)

---
