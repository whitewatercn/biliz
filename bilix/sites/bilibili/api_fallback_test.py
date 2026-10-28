"""Offline regression tests for BV pages without embedded playback data."""

import json
import unittest
from unittest.mock import AsyncMock, patch

import httpx

from bilix.exception import APIResourceError
from bilix.sites.bilibili import api


URL = 'https://www.bilibili.com/video/BV1Rg4y1K7BK/'


def video_html(playback=False, unavailable=False):
    state = {
        'error': {'code': -404} if unavailable else {},
        'bvid': 'BV1Rg4y1K7BK', 'aid': 1, 'tags': [],
        'cidMap': {'BV1Rg4y1K7BK': {'cids': {'1': 2}}},
        'videoData': {
            'title': 'Test video', 'desc': '',
            'stat': dict.fromkeys(
                ['view', 'danmaku', 'coin', 'like', 'reply', 'favorite', 'share'], 0),
            'pages': [{'part': 'Test video'}],
        },
    }
    html = '<script>window.__INITIAL_STATE__=' + json.dumps(state) + ';(function(){})()</script>'
    html += '<h1 title="Test video"></h1><meta property="og:image" content="https://example.com/cover.jpg">'
    if playback:
        html += '<script>window.__playinfo__={"data":{"durl":[]}}</script><script></script>'
    else:
        # The actual failing page references this variable without assigning it.
        html += '<script>if (window.__playinfo__) { use(window.__playinfo__); }</script>'
    return html


class PlaybackFallbackTests(unittest.IsolatedAsyncioTestCase):
    async def get_info(self, html):
        transport = httpx.MockTransport(lambda request: httpx.Response(200, text=html))
        async with httpx.AsyncClient(transport=transport) as client:
            return await api.get_video_info(client, URL)

    async def test_missing_playback_uses_api(self):
        expected = object()
        fallback = AsyncMock(return_value=expected)
        with patch.object(api, '_get_video_info_from_api', fallback):
            self.assertIs(await self.get_info(video_html()), expected)
        fallback.assert_awaited_once()
        self.assertEqual(fallback.await_args.args[1], URL)

    async def test_embedded_playback_keeps_html_path(self):
        with patch.object(api, '_get_video_info_from_api', AsyncMock()) as fallback:
            result = await self.get_info(video_html(playback=True))
        self.assertEqual(result.bvid, 'BV1Rg4y1K7BK')
        self.assertEqual(result.other, [])
        fallback.assert_not_awaited()

    async def test_unavailable_video_does_not_fallback(self):
        with patch.object(api, '_get_video_info_from_api', AsyncMock()) as fallback:
            with self.assertRaises(APIResourceError):
                await self.get_info(video_html(unavailable=True))
        fallback.assert_not_awaited()


if __name__ == '__main__':
    unittest.main()
