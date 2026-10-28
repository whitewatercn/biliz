# biliz

[![GitHub license](https://img.shields.io/github/license/whitewatercn/biliz?style=flat-square)](https://github.com/whitewatercn/biliz/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/biliz?style=flat-square&color=blue)](https://pypi.org/project/biliz/)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/whitewatercn/biliz)](https://github.com/whitewatercn/biliz/commits/master/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/biliz?label=pypi%20downloads&style=flat-square)](https://pypi.org/project/biliz/)

⚡️Lightning-fast asynchronous download tool for bilibili and more

本项目 biliz 源自 [HFrost0/bilix](https://github.com/HFrost0/bilix)，在其基础上继续维护和改进，并以 `biliz` 发布到 PyPI。感谢原作者及贡献者的开源工作。本项目遵循 Apache 2.0 协议。

biliz is a fork of [HFrost0/bilix](https://github.com/HFrost0/bilix), published on PyPI as `biliz`.

[Documentation](https://whitewatercn.github.io/biliz/)

## Features

### ⚡️ Fast & Async

Asynchronous high concurrency support, controllable concurrency and speed settings.

### 😉 Lightweight & User-friendly

Lightweight user-friendly CLI with progress notification, focusing on core functionality.

### 📝 Fully-featured

Submissions, anime, TV Series, video clip, audio, favourite, danmaku ,cover...

### 🔨 Extensible

Extensible Python module suitable for more download scenarios.

## Install

```shell
uv tool install biliz
```

Alternatively, install with pip:

```shell
pip install biliz
```

## Usage Example

* If you prefer to use command line interface (cli)

```shell
biliz v 'url'
```

> `v` is a method short alias for `get_video`

* If you prefer to code with python

The Python import namespace is `biliz`.

```python
from biliz.sites.bilibili import DownloaderBilibili
import asyncio


async def main():
    async with DownloaderBilibili() as d:
        await d.get_video('url')


asyncio.run(main())
```

## Community

If you find bugs or have feature requests, feel free to raise an [Issue](https://github.com/whitewatercn/biliz/issues).

If you find this project helpful, you can support it with a [Star](https://github.com/whitewatercn/biliz/stargazers)🌟

## Contribute

❤️ Welcome! Details can be found in [Contributing](https://github.com/whitewatercn/biliz/blob/master/CONTRIBUTING_EN.md)
