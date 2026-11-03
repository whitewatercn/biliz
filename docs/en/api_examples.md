# API Examples
biliz provides asynchronous APIs for Bilibili.
```python
import asyncio
from biliz.sites.bilibili import api
from httpx import AsyncClient


async def main():
    # instantiate a httpx client for making http requests
    client = AsyncClient(**api.dft_client_settings)
    data = await api.get_video_info(client, 'https://www.bilibili.com/bangumi/play/ep90849')
    print(data)


asyncio.run(main())

```
