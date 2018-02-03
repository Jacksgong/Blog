title: 通过Scikit-learn编写一个HelloWorld
date: 2017-06-23 23:08:03
updated: 2017-06-23
categories:
- AI
tags:
- Scikit-learn
- TensorFlow
- AI

---

{% note warning %} [上一篇文章](https://blog.dreamtobe.cn/tensorflow-mnist/)中我们介绍了如何通过TensorFlow去训练一个识别数字图片模型，其中涉及了算法推演到最后的输出结果，其实可以借助Scikit-learn来简化。{% endnote %}

<!-- more -->

> 参考视频: https://youtu.be/cKxRvEZd3Mw


## I. 前言

一个简单的AI目的，如: 输入一个照片识别出是什么水果。

传统的做法我们需要写大量的代码来区分不同水果的特征，如形状、颜色等，但是AI可以通过训练Classifier来自动辨别而不需要我们编写。

## II. 方案

通过[scikit-learn](http://scikit-learn.org/stable/install.html)这个库，可以采用[Anaconda](https://www.continuum.io/downloads)来一键安装所有scikit-learn的依赖（而且支持Windows、macOS、Linux等)。

大概的步骤: 收集训练的数据 -> 训练Classifier -> 结果验证

## III. 编写helloword

安装完Anaconda之后，可以简单的编写python通过`import sklearn`然后执行下，验证下是否已经可以正常import。

### 1. 训练数据(表)

![](/img/scikit-learn-hello-world.png)

我们可以看到训练数据Orange比较粗糙也比较重，这里训练的维度就参考`重量`与`纹理情况`。

### 2. 代码

在编写时，将输入的训练数据`1`定义为`smooth`，将`0`定义为`bumpy`；将输出数据`1`定义为`Orange`，将`1`定义为`Apple`。

最后验证时，我们验证了[重量为150kg，比较粗糙的]，输出的是`1`，是比较符合预期的。

```python
from sklearn import tree
# 1. collect tranining data
# input: [weight, 1-> smooth | 0 -> bumpy]
features = [[140, 1], [130, 1], [150, 0], [170, 0]]
# output: apple -> 0 | orange -> 1
labels = [0, 0, 1, 1]

# 2. train claasifier
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)

# 3. make predict
# 150kg, bumpy
print clf.predict([[150, 0]])
```

---
