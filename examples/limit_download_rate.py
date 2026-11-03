import asyncio
from biliz.sites.bilibili import DownloaderBilibili


async def main():
    async with DownloaderBilibili(speed_limit=1e6) as d:  # limit to 1MB/s
        await d.get_series("https://www.bilibili.com/video/BV1jK4y1N7ST?p=5")


if __name__ == "__main__":
    asyncio.run(main())
