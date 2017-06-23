title: 训练识别数字图片的模型
date: 2017-03-24 01:57:03
updated: 2017-03-24 01:57:03
categories:
- AI 
tags:
- TensorFlow
- AI

---


{% note warning %} 本文根据官方教程，通过MNIST数据，使用Softmax Regressio算法训练一个输入784像素的图片，识别出其对应数字的模型 {% endnote %}

<!-- more -->

[前一篇文章](https://blog.dreamtobe.cn/tensorflow-sample/)中我们配置了TensorFlow并根据官方教程训练了一个简单的模型，今天我们继续训练另外一个简单的模型。

![](/img/tensorflow-mnist-1.png)

MNIST包含一个手写的数字，就好像:

![](/img/tensorflow-mnist-2.png)

#### 这个案例是为了解答:

1. TensorFlow是怎么工作的?
2. 机器学习的核心思想是什么?


#### 你可以学习到:

1. MNIST数据、Softmax Regression算法
2. 建立一个可以基于观察图片的每一个像素来识别数字的模型
3. 通过模型浏览上千个案例来训练模型识别数字
4. 通过测试数据，来验证模型的准确度

## I. MNIST数据

> 数据是在[Yann LeCun's website](http://yann.lecun.com/exdb/mnist/)这上面。

#### 该数据分为三部分

> 通过分离不同的数据，一部分用于训练，一部分用户测试，一部分用于学习，这样才能验证结果是训练的模型自己生成的。

1. mnist.train: 55_000个数据用于训练
2. mnist.test: 10_000个数据用于测试
3. minst.validation: 5_000个数据用于验证

#### 每个数据有两部分

1. 手写数字的图片(x)(`mnist.train.images`、`mnist.test.images`): 28px * 28px = 784px
2. 对应的标签(y)(`mnist.train.labels`、`mnist.test.labels`)

如数字`1`:

![](/img/tensorflow-mnist-3.png)

- `mnist.[train/test].images`是一个tensor，由55_000个由784个点的二维数组组成，数组中的每个值代表每个像素点，像素点有色的根据浅到深是0到1，无色为0，每个数组所呈现的数字对应一个label，我们表示为[55000,784]
![](/img/tensorflow-mnist-4.png)
- `minst.[train/test].labels`也是一个tensor，由55_000个由10个值的一维数组组成，数组中有且仅有一个为1，其余为0，数组的index表示标签所代表的数字，如3表示为[0,0,0,1,0,0,0,0,0,0]]，我们表示为[55000,10]
![](/img/tensorflow-mnist-5.png)

## II. Softmax Regression算法

> 我们算法要尽量准确的通过图片(784个像素点)所呈现的，让结果中正确的数字所占的比例尽量的高，如给出的图片对应的数字是9，模型运算结果可能是: 80%的概率是9，5%概率是8，15%的概率是其他。


**该算法使用场景:** 从不同的事件中为一个对象分配可能性，因为该算法给我们一个0到1的列表，并且加起来等于1

#### 大概步骤

1. 总结输入的数据在某些类中的证据(we add up the evidence of our input being in certain classes)
2. 将证据转化为具体的可能性

做像素强度(intensities)的加权值，当图片的强度(intentsity)与某个分类不一致，其权重为负数，当有强有力的证据证明是在那个分类，其权重为正数

#### 最终的模型权重

> 蓝色为正数权重，红色为负数

![](/img/tensorflow-mnist-6.png)

#### 大概算法

> 第i个类型、第j个像素、W为权重、x为输入的图片、b为偏移量

> 结果: $y = softmax(W_x$ + b)

![](/img/tensorflow-mnist-7.png)
![](/img/tensorflow-mnist-8.png)
![](/img/tensorflow-mnist-9.png)

## III. 通过Tensorflow实现

<script src="https://gist.dreamtobe.cn/Jacksgong/c90d3e0f6a877330c55daeeb7a021685.js"></script>

> 这边的正确率是92%，是由于我们的模型非常简单，最好的模型能够达到99.7%的正确率，可以看看网上的不同模型的[测试结果](http://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html)

---

- [MNIST For ML Beginners](https://www.tensorflow.org/get_started/mnist/beginners)

---
