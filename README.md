# ![Owner avatar](https://avatars.githubusercontent.com/u/140964125?s=48&v=4)         **[CuckooIDE](https://github.com/Ashisheng2005/CuckooIDE)**  



该项目展示停止开发，原因是该项目采用的是python + tkiner,不只是性能上，UI界面和许多方面都具有很大限制，目前准备转为 **[electron](https://github.com/electron/electron)** + python  + Flask + [shadcn-ui](https://github.com/shadcn-ui/ui) 开发 ——  **[RIDE](https://github.com/Ashisheng2005/RIDE)**     ，所以此仓库作为tkinter学习使用，对于其中一些再封装的组件我将其另起一个项目：    **[ATK](https://github.com/Ashisheng2005/ATK)**     ，在这个项目中我会完善组件和编写完全的使用教程。

当前项目其实已经将ollama和Live2D的api封装好了，后续如果有机会，会给出一个流程闭环的成品。

此仓库内自带虚拟环境和第三方库，

git至本地后直接使用 \.venv\Scripts\python 中的编译器运行\UIFrame\windowFrame.py即可启动项目。

——2025.3.6



> :warning:该项目目前处于前期开发阶段，会包含功能不稳定、部分代码混乱、莫名bug等情况，但我们会在最大程度上保证您的代码和线程安全，我们设计了一套完整的保护机制以确保您的项目和线程的稳定。

> :warning:本项目包含Live2D服务和大模型接入等功能，但完全取决于您的意见。对于Live2D服务，我们不能完全保证相应支持的安全性，如果出现异常，请立即报告我们，我们会优先解决不安全的bug。对于侧端大模型，配置过程可能会少些复杂，但我们会给出相应的配置流程，相信这些会给您带来一些帮助。

> :warning:在后期的规划中，会融合STT和TTS技术以实现大模型的深度融合，这会使用到用户的麦克风权限。



### 这是什么项目？

是一个本地IDE，再插件存在的情况下允许运行任意语言的代码(包括汇编语言)， 同时，也支持Live2D和本地任何大模型的配合，也支持本地TTS选项（后续会支持更多的情况，例如在线LLM/ASR/TTS等）。我们尝试让大模型和本地项目深度融合，以实现更加灵活和智能的AI项目辅助。

我们会在后期计划尝试本地大模型的长期记忆，以实现永久聊天、无限上下文长度。

这个项目最初仅仅是为了突破个人能力所做的尝试。

目前支持Windows和Linux，MacOS不确定，但项目纯基于Python实现，所以大概率也是可行的。

项目支持全本地数据，只要您愿意，任何数据都不会离开本地，一切都在离线工作。



### 基础功能

> :white_check_mark:任意语言代码编辑
>
> :white_check_mark:基于插件提供的代码高亮
>
> :white_check_mark:插件管理
>
> :white_check_mark:库管理
>
> :white_check_mark:版本管理
>
> :white_check_mark:全真环境运行，不会存在任何IDE所导致代码偏差的可能
>
> :white_check_mark:Live2D 显示
>
> :white_check_mark:自选LLM后端
>
> ✅支持云端和侧端LLM
>
> 我们会在短时间内为您提供更多的功能。



### 目标平台

- macOS
- Linux
- Windows



### 当前支持的LLM后端

目前仅支持Ollama，但后期会支持任何与OpenAI API兼容的后端，如Groq、LM Studio、OpenAI 等



### 当前支持的文本转语音后端

这个是下一版本的更新内容哈

暂定支持：

- [py3-tts](https://github.com/thevickypedia/py3-tts)（本地，它是您系统的默认 TTS 引擎）
- [meloTTS](https://github.com/myshell-ai/MeloTTS)（本地，快速）
- [Coqui-TTS](https://github.com/idiap/coqui-ai-TTS) (本地，速度取决于您运行的模型。)
- [Azure 文本转语音](https://azure.microsoft.com/en-us/products/ai-services/text-to-speech) (在线，需要 API 密钥)



### LIve2D动画

您可以从本地存储在`live2d` 目录中的模型加载live2d模型。



### 安装和使用

#### 要求：

- Python >= 3.12 推荐3.12
- 已安装配置Ollama服务



您需要准备好并运行 [Ollama](https://github.com/jmorganca/ollama) ，准备您选择的LLM。在config.ini 中填写在 [model_name] 后面, 例如:

```ini
model_name = llama3.1:latest
```



建议使用conda或者venv等虚拟Python环境

在终端中运行以下命令以安装依赖项

```shell
pip install -r requirements.txt
```



如果您想使用live2d插件，请在设置中打开，如果您想修改模型，请在` config.ini `文件中修改一下内容：

```ini
[live2d]
path = 米塔\\3.model3.json 
```

注意路径填写方式




