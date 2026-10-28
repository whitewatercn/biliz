"""Offline coverage for UP listing errors and WBI query encoding."""
import hashlib
import unittest
from unittest.mock import AsyncMock, patch
from urllib.parse import urlencode

import httpx

from biliz.exception import APIInvalidError
from biliz.sites.bilibili import api


class UpVideoInfoTests(unittest.IsolatedAsyncioTestCase):
    async def fetch(self, payload, status=200):
        self.requests = []
        def respond(request):
            self.requests.append(request)
            return httpx.Response(status, json=payload)
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            with patch.object(api, '_add_sign', AsyncMock()):
                return await api.get_up_video_info(client, '161418029')

    async def test_risk_response_reports_business_error(self):
        with self.assertRaisesRegex(APIInvalidError, '-352.*风控校验失败'):
            await self.fetch({'code': -352, 'message': '风控校验失败', 'data': {'v_voucher': 'test'}})

    async def test_http_412_does_not_repeat_blocked_request(self):
        with self.assertRaisesRegex(APIInvalidError, 'HTTP 412'):
            await self.fetch({}, status=412)
        self.assertEqual(len(self.requests), 1)

    async def test_empty_page_is_valid(self):
        self.assertEqual(await self.fetch({'code': 0, 'data': {
            'list': {'vlist': []}, 'page': {'count': 0}}}), ('161418029', 0, []))

    async def test_normal_page(self):
        self.assertEqual(await self.fetch({'code': 0, 'data': {
            'list': {'vlist': [{'author': 'Test UP', 'bvid': 'BV123'}]},
            'page': {'count': 1}}}), ('Test UP', 1, ['BV123']))

    async def test_malformed_success_response(self):
        with self.assertRaisesRegex(APIInvalidError, '未返回有效列表'):
            await self.fetch({'code': 0, 'data': {}})

    async def test_wbi_encoding_matches_transmitted_query(self):
        # Public WBI example keys and their known mixin key.
        payload = {'data': {'wbi_img': {
            'img_url': 'https://example.com/7cd084941338484aae1ad9425b84077c.png',
            'sub_url': 'https://example.com/4932caff0ff746eab6f01bf08b70ac45.png'}}}
        async with httpx.AsyncClient(transport=httpx.MockTransport(
                lambda request: httpx.Response(200, json=payload))) as client:
            params = {'keyword': "中文 &空格!'()*", 'mid': '161418029', 'w_rid': 'stale'}
            with patch.object(api.time, 'time', return_value=1702204169):
                await api._add_sign(client, params)
        self.assertEqual(params['keyword'], '中文 &空格')
        query = urlencode(sorted((k, v) for k, v in params.items() if k != 'w_rid'))
        expected = hashlib.md5((query + 'ea1db124af3c7062474693fa704f4ff8').encode()).hexdigest()
        self.assertEqual(params['w_rid'], expected)
        self.assertEqual(str(httpx.QueryParams({k: v for k, v in params.items() if k != 'w_rid'})),
                         urlencode({k: v for k, v in params.items() if k != 'w_rid'}))
