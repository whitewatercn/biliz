"""
你可以只下视频的一小段
You can download just a small clip of the video
"""
import asyncio

from biliz.sites.bilibili import DownloaderBilibili


async def main():
    """download the 《嘉然我真的好喜欢你啊😭😭😭.mp4》 by timerange🤣"""
    async with DownloaderBilibili() as d:
        # time_range (start_time, end_time)
        await d.get_video('https://www.bilibili.com/video/BV1kK4y1A7tN', time_range=(0, 7))


if __name__ == '__main__':
    asyncio.run(main())
