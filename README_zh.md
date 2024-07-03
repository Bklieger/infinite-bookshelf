![License](https://img.shields.io/badge/license-MIT-green)

<p align="center">
    【<a href="README.md">English </a> | 简体中文】
</p>

# Groqbook: 使用 Groq 和 Llama3 在几秒钟内生成整本书籍

Groqbook 是一个 streamlit 应用程序，它使用 Groq 上的 Llama3 从一句话的提示中构建书籍的创建。它在非小说书籍上效果很好，并在几秒钟内生成每一章。该应用程序混合使用 Llama3-8b 和 Llama3-70b，利用较大的模型生成结构，较小的模型生成内容。目前，模型仅使用章节标题的上下文生成章节内容。未来，这将扩展到整本书的完整上下文，以便 groqbook 生成高质量的小说书籍。

[Groqbook 演示](https://github.com/Bklieger/groqbook/assets/62450410/3adb11cd-8264-4289-a28a-49dc5b3cf453)
> Groqbook 快速生成书籍内容的演示

---

[第二部分的 Groqbook 演示](https://github.com/Bklieger/groqbook/assets/62450410/5b0147fb-90f3-4584-8572-fa452545d833)
> Groqbook 下载 markdown 风格书籍的演示

---

### 特点

- 📖 有策略地在 Llama3-70b 和 Llama3-8b 之间切换以平衡速度和质量的引导提示
- 🖊️ 使用 markdown 样式在 streamlit 应用程序上创建美观的书籍，包括表格和代码
- 📂 允许用户下载包含整本书内容的文本文件

### 示例生成的书籍:

| 示例                                      | 提示                                                                                                                                |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| [LLM 基础](Example_1.md)             |  大型语言模型的基础                                       |
| [数据结构和算法](Example_2.md) | Java 中的数据结构和算法                                            |

---

## 快速开始

> [!重要]
> 要使用 Groqbook，您可以使用托管版本 [groqbook.streamlit.app](https://groqbook.streamlit.app)
> 或者，您可以按照快速入门说明在本地运行 groqbook。

### 托管在 Streamlit 上:

要使用 Groqbook，您可以使用托管版本 [groqbook.streamlit.app](https://groqbook.streamlit.app)

### 本地运行:

或者，您可以在本地使用 streamlit 运行 groqbook。

#### 第一步
首先，您可以在环境变量中设置 Groq API 密钥:

~~~
export $GROQ_API_KEY = gsk_yA...
~~~

这是一个可选步骤，允许您跳过稍后在 streamlit 应用程序中设置 Groq API 密钥。

#### 第二步
接下来，您可以设置虚拟环境并安装依赖项。

~~~
python3 -m venv venv
~~~

~~~
source venv/bin/activate # Bash

venv\Scripts\activate.bat # Windows
~~~

~~~
pip3 install -r requirements.txt
~~~

#### 第三步 (仅限 Windows)
对于 Windows 用户，可能需要安装 gtk3。

~~~
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer?tab=readme-ov-file
~~~

#### 第四步
最后，您可以运行 streamlit 应用程序。

~~~
python3 -m streamlit run main.py
~~~

## 详细信息

### 技术

- Streamlit
- Llama3 在 Groq 云上

### 限制

Groqbook 可能生成不准确的信息或占位内容。它应该仅用于生成娱乐目的的书籍。

## 贡献

欢迎通过 PR 提出改进！

## 更新日志

### v0.2.0
2024 年 5 月 29 日:

[Groqbook 统计演示](https://github.com/Bklieger/groqbook/assets/62450410/b7af2fd5-f587-44ae-bc6d-40c1233c8b7e)
> Groqbook 生成统计的演示

### v0.3.0
2024 年 6 月 8 日:

![新 PDF 下载选项的图片](assets/imgs/release_note_jun_8th.png)
> 下载样式化的 PDF 书籍

### 未来功能:
- 能够命名书籍并在下载时显示
- 能够将书籍保存到 Google Drive
- 可选的种子内容字段以输入现有笔记
