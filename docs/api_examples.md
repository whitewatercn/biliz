# API案例
biliz 提供哔哩哔哩的异步 API。
```python
import asyncio
from biliz.sites.bilibili import api
from httpx import AsyncClient


async def main():
    # 需要先实例化一个用来进行http请求的client
    client = AsyncClient(**api.dft_client_settings)
    data = await api.get_video_info(client, 'https://www.bilibili.com/bangumi/play/ep90849')
    print(data)


asyncio.run(main())

```
