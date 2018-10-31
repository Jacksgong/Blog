title: Python爬虫验证码识别(使用Tesseract OCR识别)
date: 2018-10-31 22:41:03
updated: 2018-10-31
categories:
- Fun
tags:
- Python
- OCR
- Tesseract
- 爬虫

---

{% note info %}主要思路是根据[教程](https://github.com/tesseract-ocr/tesseract/wiki/Compiling#macos)使用源码安装完tesseract后，然后通过安装pillow与pytesseract打通python进行在python代码中引用使用。{% endnote %}

<!-- more -->

## I. 依赖安装

```
brew install automake autoconf libtool
brew install pkgconfig
brew install icu4c
brew install leptonica
brew install gcc
```

## II. Tesseract编译安装

```
git clone https://github.com/tesseract-ocr/tesseract/
cd tesseract
./autogen.sh
./configure CC=gcc-8 CXX=g++-8 CPPFLAGS=-I/usr/local/opt/icu4c/include LDFLAGS=-L/usr/local/opt/icu4c/lib
make -j
sudo make install  # if desired
```

## III. 语言配置

需要识别语言配置(参照[教程](https://github.com/tesseract-ocr/tesseract/wiki/Compiling#language-data)):

0. 前面安装完后，你会发现在`/usr/local/share/tessdata`会有默认的data，将`export TESSDATA_PREFIX='/usr/local/share/tessdata'`配置到系统环境中
1. 在[这里](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files)下载对应版本的语言包
2. 将下载的语言包直接放到这个`/usr/local/share/tessdata`

比如我这边是4.0版本，我需要的是对英文的ocr识别(识别英文的验证码)，我就直接下载4.00版本的`eng.traineddata`:

![](/img/python-verify-code-ocr1.png)

然后再将下载下来的`eng.traineddata`放到到`/usr/local/share/tessdata`中即可:

![](/img/python-verify-code-ocr2.png)

## IV. 打通Python

这边打通python直接通过[pytesseract](https://pypi.org/project/pytesseract/)，十分方便。

先安装pillow:

```
pip install pillow
```

再安装pytesseract:

```
pip install pytesseract
```

安装完成后就可以通过其在python中使用了，如:

```
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# Simple image to string
print(pytesseract.image_to_string(Image.open('test.png')))

# French text image to string
print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))
```

更多使用方法参照[官方](https://pypi.org/project/pytesseract/)的文档。
