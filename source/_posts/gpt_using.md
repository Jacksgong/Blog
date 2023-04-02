title: ChatGPT/OpenAI/NewBing的使用以及AI工具推荐
date: 2023-03-07 00:35:03
updated: 2023-04-02
categories:
- fun
tags:
- chatgpt
- openai
- new bing

---

{% note info %} 现在大多数内容都是记录在Obsidian上，想了下这块还是写成博客，这样可以帮助更多博友更快的体验类似颠覆的体验。{% endnote %}

<!-- more -->

> GPT使用需要翻墙，这里的翻墙机场推荐[xrelay](https://isseys.net/#/register?code=BjU5h6ev)，一个月15元，使用方法配套极其简单，还有实时客服聊天指导，注册后不用付款直接可以免费试用一天，即便付款后还支持30天无条件退款。

## I. ChatGPT 使用

这块网络上的教程非常多，我就不过多赘述了，需要特别留意的是，翻墙不用全局翻，就做以下配置就行:

1. 需要配置`openai.com`走代理
2. 需要开启UDP（至少是443与80端口）走代理，因为ChatGPT检测IP是通过UDP获取的


我问了下ChatGPT，居然让我用Visual Studio Code的插件来使用，具体建议网上查一查方法比较简单:

![](/img/gpt_using-b047afc0.png)

## II. OpenAI API 使用

这块网上也非常多教程，也不过多说明了几个需要注意的点:

1. 配置`openai.com`走代理
2. 使用[类似这个网站](https://sms-activate.org/getNumber)提供的号码，找个印度的或者美国的（推荐印度的便宜点），印度尼西亚的虽然便宜但是测试了，openai.com不认，另外没有收到验证码也不会扣钱，所以多试试没事
3. 进入到[Dashboard](https://platform.openai.com/onboarding)页面，`Personal -> View API key`, 创建一个key，保存下来

### 用python写一个机器人

顺便提下，这下面的代码是GPT自己写的，写的挺好的，能用(另外还是有点能扯):

![](/img/gpt_using-9d58700a.png)


```python
import openai

# Replace with your own API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Start a conversation with "Hello"
prompt = "Hello"

# Create a chatbot using ChatGPT engine
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=50,
    temperature=0.9
)

# Print out the chatbot's reply
print("Chatbot:", response["choices"][0]["text"])

# Loop until the user types "quit"
while True:
    # Get the user's input
    user_input = input("User: ")

    # Break the loop if the user types "quit"
    if user_input.lower() == "quit":
        break

    # Append the user's input to the prompt
    prompt += "\nUser: " + user_input

    # Create a new response using the updated prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=256,
        temperature=0.9
    )

    # Print out the chatbot's reply
    print(response["choices"][0]["text"])

    # Append the chatbot's reply to the prompt
    prompt += "\nChatbot: " + response["choices"][0]["text"]
```

## III. New Bing 使用

> 3.19更新，IP不能使用`4.2.2.2`，替换成`1.1.1.1`后可以正常使用

New Bing的使用也比较简单，不过有几点特别注意下:

1. 常规的需要在[这里](https://www.bing.com/new)申请加入白名单，然后等待微软的回邮件通知
2. 让 `bing.com` 走代理
3. 下载 Microsoft Edge Dev 版本（我之前一直在用Chrome，说实在的，这次为了New Bing我切成Edge以后，彻底不用Chrome了，主要还是真的好用）
4. 下载 [Header Editor](https://microsoftedge.microsoft.com/addons/detail/header-editor/afopnekiinpekooejpchnkgfffaeceko) 这个插件，然后配置请求头`X-Forwarded-For`: `1.1.1.1`，另外为了防止跳转到国内，也可以配置一个请求头。

| `x-forwarded-for` | `redirect` |
| --- | --- |
| ![](/img/gpt_using-ce86973c.png) | ![](/img/gpt_using-baa54a73.png) |

5. 配置Edge默认搜索不要跳转中国的bing，Edge -> 设置 -> 隐私、搜索和服务 -> 地址栏和搜索 -> 管理搜索引擎，添加一个搜索引擎，`https://global.bing.com/search?q=%s&mkt=en-US`，并将其设置为默认即可
![](/img/gpt_using-cfb0f842.png)


相比ChatGPT来说，New Bing的准确性是非常强的，并且有引用所有的判断来源:

![](/img/gpt_using-876e2cdc.png)

![](/img/gpt_using-1e90978a.png)

## IV. 好用的工具

### 1. Chrome/Firefox/Edge插件

#### 1.1 [ChatHub - All-in-one chatbot client](https://chrome.google.com/webstore/detail/chathub-all-in-one-chatbo/iaakpnchhognanibcahlpcplchdfmgma/related)

基于这个Chrome插件，可以同时使用ChatGPT与New Bing，甚至可以在上面直接使用Bard，非常方便。

![](/img/gpt_using-a976b067.png)

可以明显感受到，ChatGPT比较快，但是New Bing比较准确，算是可以相互互补。

需要留意的是，最好是使用`API Mode`，如果使用`Webapp Mode`通常不是很稳定

![](/img/gpt_using-50d1bbe5.png)

当然如果你有ChatGPT Plus，也可以配置使用GPT4的`API Model`。

### 1.2 [沉浸式双语网页翻译扩展](https://immersive-translate.owenyoung.com/)

这个扩展可以让你在浏览网页的时候，可以同时看到英文和中文，非常方便。支持OpenAI的GPT-3，也支持Google的翻译。

![](/img/gpt_using-4bf0cf9f.png)

并且支持快捷键，如默认支持的快捷键，超级方便:

```
Alt+A: 翻译/切换原文，按一下翻译，再按一下显示原文。

Alt+W: 翻译整个页面，而不是默认的智能翻译内容区域。
```

### 1.3  [OpenAI Translator](https://chrome.google.com/webstore/detail/openai-translator/)

已经有了沉浸式双语网页翻译扩展了，为啥我还推荐[OpenAI Translator](https://chrome.google.com/webstore/detail/openai-translator/)这个插件呢，原因很简单，就是他的能力绝不仅仅是`Translator`，他可以支持：

- 选择的文本的润色
- 选择的文本的总结
- 选择的内容的语法分析
- 选择的代码的解释

![](/img/gpt_using-108ff620.png)

### 2. 通过沟通控制软件系列

#### 2.1 Cursor/CodeX

这两个就不用多说了，[Cursor](https://www.cursor.so/)，通过沟通来编写代码，支持重构，写单测等等。

![](/img/gpt_using-19f078c2.png)

[CodeX](https://openai.com/blog/openai-codex)也是类似，还支持实时preview。

![](/img/gpt_using-7d965930.png)

#### 2.2 Unity AICommand

[AICommand](https://github.com/keijiro/AICommand) 可以支持通过和GPT聊天就能在Unity上创作作品，不过这个非官方，官方的还在迭代。

![](/img/gpt_using-f16d1b5e.png)

#### 2.3 [Shell GPT](https://github.com/TheR1D/shell_gpt) - 在已有的Terminal里面集成GPT

如果你仅仅只想要在terminal里面集成GPT，可以直接安装[Shell GPT](https://github.com/TheR1D/shell_gpt)来实现:

```bash
pip install shell-gpt
```

使用之前留意在环境变量中加上你的API Key，然后就可以愉快的玩耍了，赋值到这个`OPENAI_API_KEY`环境变量。

这个的用法也很简单:

![](/img/gpt_using-7451532a.png)

当然也有很多灵活的用法，比如：

```bash
sgpt "nginx default config file location"
# -> The default configuration file for Nginx is located at /etc/nginx/nginx.conf.

sgpt "mass of sun"
# -> = 1.99 × 10^30 kg

```

如果仅仅只是想要查询指令可以使用`--shell`或者`-s`:

```bash
sgpt --shell "make all files in current directory read only"
# -> chmod 444 *
# -> Execute shell command? [y/N]: y
# ...

ls
# -> 1.mp4 2.mp4 3.mp4
sgpt -s "using ffmpeg combine multiple videos into one without audio. Video file names: $(ls -m)"
# -> ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -filter_complex "[0:v] [1:v] [2:v] concat=n=3:v=1 [v]" -map "[v]" out.mp4
# -> Execute shell command? [y/N]: y
# ...
```

当然也包含基本的GPT的能力，如总结输入的内容之类的:

```bash
sgpt "Generate git commit message, my changes: $(git diff)"
# -> Commit message: Implement Model enum and get_edited_prompt() func, add temperature, top_p and editor args for OpenAI request.
```

甚至对出现的错误给出解决建议:

```bash
sgpt "check these logs, find errors, and explain what the error is about: ${docker logs -n 20 container_name}"
# ...
```

还可以生成代码，如下面生成一个代码片段，并直接写入到`fizz_buzz.py`:

```bash
sgpt --code "solve classic fizz buzz problem using Python" > fizz_buzz.py
```

### 3. [Warp](https://app.warp.dev/referral/Z99DVP) - 深度整合GPT的Terminal

我用了很多年的iTerm2+Tmux这样的组合，这是第一次让我有冲动尝试的全新的终端，你可以通过对话的方式，让[Warp](https://app.warp.dev/referral/Z99DVP)帮你完成一些操作，比如：

![](/img/gpt_using-ce940d1c.png)

当然Warp整体的UI以及交互也会更加友好，比如：

![](/img/gpt_using-ae14090e.png)

### 4. [Tome AI](https://tome.app/invite/jacks-gong-clfz87ouh6mrx429ic8d845nm) - 自动做PPT

通过这个网站可以快速的自动创建PPT，根据你的idea自动找图，生成动画，自动生成文案等，非常的自然好用。

![](/img/gpt_using-082f7446.png)

输入一个主题，立马全自动生成整个PPT，并且可以定制修改，支持中文，甚至支持做PPT演示录制。下面就是我输入了一个"如何迎接AGI时代的到来"，然后就自动生成了一个PPT。

![](/img/gpt_using-d5b1b23a.png)

不过需要留意的是，整体体验下来，整体模板样式目前还比较单一，另外就是会自动为PPT添加文本以及图片。

### 5. [Clipdrop](https://clipdrop.co/) - 图片移除背景，移除区域内容等图片处理

这个是一个非常有意思的网站，可以通过GPT来处理图片，能力非常的有用，比如：

![](/img/gpt_using-e08239b0.png)


---

- [New Bing 只是给我拉黑了？](https://www.v2ex.com/t/924296)
