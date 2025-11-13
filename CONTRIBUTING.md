# 贡献指南

NOTE: 如果只是有文档希望被采纳，请直接发送邮件给 `fycbot@163.com`，标明少学组和文件相关信息即可。

## 安装依赖

使用 `mkdocs` 构建文档需要依赖，所有需要的依赖都写在 `requirements.txt` 中，只需要执行 `pip install -r requirements.txt` 即可安装所有依赖。

## `autogen.py` 的使用

在大多数 markdown 文件中，你都可以看到类似于以下形式的代码：

```markdown
<!-- AUTOGEN CONFIG START -->
<!-- LIST: [中国民族器乐.pptx] -->
<!-- LIST: [音乐课ppt乐理部分.pdf] -->
<!-- AUTOGEN CONFIG END -->

<!-- AUTOGEN CONTENT START -->
<!-- AUTOGEN CONTENT END -->
```

这是用来自动生成目录的，`<!-- AUTOGEN CONFIG START -->` 和 `<!-- AUTOGEN CONFIG END -->` 之间的内容是用来配置生成内容的。其中有多个形如 `<!-- OPERATION: [PARAMATER] -->` 的注释，`autogen.py` 会根据每个注释的内容 *依次生成* 对应的 markdown，填充到 `<!-- AUTOGEN CONTENT START -->` 和 `<!-- AUTOGEN CONTENT END -->` 之间。不同 OPERATION 的含义：

- `LIST`: 声明当前目录下存在文件名为参数的文件，并生成显示该文件的组件。
- `IGNORE`: 声明当前目录下存在文件名为参数的文件，但是不显示该文件。
- `HEADER`：生成一个二级标题用于把文件分组。

每次运行 `python autogen.py` 时，都会读取通过 `LIST` 和 `IGNORE` 声明的文件，并与该目录下未声明的文件会自动添加到配置中，默认使用的 OPERATION 是 `LIST`。

但是使用 Git 追踪自动生成的文件并无意义，同时在合并时会产生大量冲突，因此要求在提交之前删除所有自动生成的内容。这可以通过 `python autogen.py remove` 实现。

## 构建文档

在安装完成所有依赖的情况下只需要直接运行 `mkdocs build` 即可。
