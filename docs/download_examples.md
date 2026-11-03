# 下载案例

觉得命令行太麻烦，不够强大？biliz可做为python的库调用，并且接口设计易用，功能更强大，这给了你很大的扩展空间

## 从最简单的开始

```python
import asyncio
# 导入下载器，里面有很多方法，例如get_series, get_video, get_favour，get_dm等等
from biliz.sites.bilibili import DownloaderBilibili


async def main():
    # 你可以使用async with上下文管理器来开启和关闭一个下载器
    async with DownloaderBilibili() as d:
        # 然后用await异步等待下载完成
        await d.get_series("https://www.bilibili.com/video/BV1jK4y1N7ST?p=5")


if __name__ == '__main__':
    asyncio.run(main())

```

## 组合多种任务 / 控制并发量

你可以组合下载器返回的协程对象，利用gather并发执行他们，他们执行的并发度收到下载器对象的严格约束，因此不会对服务器造成意想不到的负担。

```python
import asyncio
from biliz.sites.bilibili import DownloaderBilibili


async def main():
    d = DownloaderBilibili(video_concurrency=5, part_concurrency=10)
    cor1 = d.get_series(
        'https://www.bilibili.com/bangumi/play/ss28277'
        , quality=999)
    cor2 = d.get_up(url_or_mid='436482484', quality=999)
    cor3 = d.get_video('https://www.bilibili.com/bangumi/play/ep477122', quality=999)
    await asyncio.gather(cor1, cor2, cor3)
    await d.aclose()


if __name__ == '__main__':
    asyncio.run(main())


```

## 下载切片

你可以只下视频的一小段

```python
import asyncio
from biliz.sites.bilibili import DownloaderBilibili


async def main():
    """download the 《嘉然我真的好喜欢你啊😭😭😭.mp4》 by timerange🤣"""
    async with DownloaderBilibili() as d:
        # time_range (start_time, end_time)
        await d.get_video('https://www.bilibili.com/video/BV1kK4y1A7tN', time_range=(0, 7))


if __name__ == '__main__':
    asyncio.run(main())

```

## 限制下载速度

创建下载器时设置 `speed_limit`，单位为字节/秒。以下示例限制为 1 MB/s。

```python
import asyncio
from biliz.sites.bilibili import DownloaderBilibili


async def main():
    async with DownloaderBilibili(speed_limit=1e6) as d:  # limit to 1MB/s
        await d.get_series("https://www.bilibili.com/video/BV1jK4y1N7ST?p=5")


if __name__ == "__main__":
    asyncio.run(main())
```

## 显示进度条

使用python模块时，进度条默认不显示，如需显示，可以

```python
from biliz.progress.cli_progress import CLIProgress

CLIProgress.start()
```

或者通过任意下载器内部的`progress`对象打开

```python
d.progress.start()
```
