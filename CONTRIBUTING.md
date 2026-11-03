# biliz 开发指南

感谢你对贡献biliz有所兴趣，在你开始之前可以阅读下面的一些提示。请注意，biliz正快速迭代，
如果你在阅读本文档时发现有些内容已经过时，请以master分支的代码为准。

# 开始之前

在一切开始之前，你需要先 **fork** 本仓库，然后clone你fork的仓库到你的本地：

```shell
git clone https://github.com/your_user_name/biliz
```

拉取至本地后，我**建议**你在独立的python环境中进行测试和开发，确认后进行本地源码可编辑安装：

```shell
pip install -e .
```

试试biliz命令能否正常执行。通过测试了？至此，你可以在本地开发biliz了🍻

# biliz 结构

在动手改动代码之前你需要对biliz的结构有一定的了解，下面是biliz的大致目录和各模块相应功能：

```text
biliz
├── __init__.py
├── __main__.py
├── _process.py  # 多进程相关
├── cli
│   ├── assign.py  # 分派哔哩哔哩任务
│   └── main.py    # 命令行入口
├── download
│   ├── base_downloader.py
│   ├── base_downloader_part.py  # 基础分段文件下载器
│   └── utils.py                 # 下载相关的一些工具函数
├── exception.py
├── log.py
├── progress
│   ├── abc.py            # 进度条抽象类
│   ├── cli_progress.py   # 命令行进度条
│   └── ws_progress.py
│   ├── __init__.py
├── sites     # 哔哩哔哩下载与 API
└── utils.py  # 通用工具函数
```

## 基础下载器

分段文件下载器为哔哩哔哩提供下载、限速和切片功能。CLI 由 `assign.py` 将请求分派给哔哩哔哩下载器或信息查询器。项目仅支持哔哩哔哩。
