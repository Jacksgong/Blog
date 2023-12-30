title: 私有化GPT分析文档 -- LocalGPT
date: 2023-12-30 16:47:20
updated: 2023-12-30
categories:
- fun
tags:
- gpt
- localgpt
- private data

---

{% note info %} 今天主要是通过localGPT这个开源框架，使用我家闲置的Mac Mini使用LLAMA-CPP模型，私有化部署并分析本地文档。{% endnote %}

![](/img/local_gpt_deploy_66bb9541_0.png)

<!-- more -->

## 准备环境

### 1. 克隆项目

```bash
git clone https://github.com/PromtEngineer/localGPT.git
```

### 2. 安装conda来做虚拟环境管理
```bash
conda create -n localGPT python=3.10.0
```

### 4. 启动`localGPT`的虚拟环境

```bash
conda activate localGPT
```

![](/img/local_gpt_deploy_679eafd3_1.png)

### 5. 安装依赖
```bash
pip install -r requirements.txt
```

### 6. 安装`LLAMA-CPP`:

比如我是Mac Mini（M2芯片)
![](/img/local_gpt_deploy_e2d153ae_2.png)

```
CMAKE_ARGS="-DLLAMA_METAL=on"  FORCE_CMAKE=1 pip install llama-cpp-python==0.1.83 --no-cache-dir
```

至此已经安装完成。

## 配置与运行

### 1. 选择模型

如果你希望修改想要的模型，就可以打开`constants.py`文件:

![](/img/local_gpt_deploy_45d371d0_3.png)

比如我换了一个模型:

![](/img/local_gpt_deploy_84bfcefa_4.png)

### 2. 提取数据 

通过执行，以下代码来提取默认的`SOURCE_DOCUMENA`目录下的所有文件内容:

```bash
python ingest.py --device_type mps
```

![](/img/local_gpt_deploy_20279a10_5.png)

你可以将你想要提取的文件放在该目录下，然后重新提取。

### 3. 下载模型并且在命令行中执行

```bash
python run_localGPT.py --device_type mps
```

执行后就可以在Terminal中直接询问了:

![](/img/local_gpt_deploy_d7ae076a_6.png)

---

- [GitHub - PromtEngineer/localGPT: Chat with your documents on your local device using GPT models. No data leaves your device and 100% private.](https://github.com/PromtEngineer/localGPT?tab=readme-ov-file)
- [How to Install and Run Local GPT to Your System Mac OS | Offline ChaGPT in Your System 100% - YouTube](https://www.youtube.com/watch?v=UEt4ek2nwb4)