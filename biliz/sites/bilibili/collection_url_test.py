"""Offline tests for current Bilibili space collection URLs."""

import unittest
from unittest.mock import AsyncMock, patch

from biliz.sites.bilibili import DownloaderBilibili, api


class CollectionUrlTests(unittest.IsolatedAsyncioTestCase):
    async def test_modern_urls_route_to_collection_handler(self):
        for kind in ('season', 'series'):
            url = f'https://space.bilibili.com/307801268/lists/7727117?type={kind}'
            self.assertIs(DownloaderBilibili.parse_url(url), DownloaderBilibili.get_collect_or_list)

    async def test_modern_urls_use_existing_metadata_apis(self):
        for kind, method, legacy in (
            ('season', 'get_collect_info', 'collectiondetail'),
            ('series', 'get_list_info', 'seriesdetail'),
        ):
            with self.subTest(kind=kind):
                d = DownloaderBilibili(hierarchy=False)
                try:
                    with patch.object(api, method, AsyncMock(return_value=('Title', 'Author', ['BV123']))) as meta, \
                            patch.object(d, 'get_series', AsyncMock()) as download:
                        await d.get_collect_or_list(
                            f'https://space.bilibili.com/307801268/lists/7727117?foo=1&type={kind}')
                        self.assertEqual(meta.await_args.args[1],
                                         f'https://space.bilibili.com/307801268/channel/{legacy}?sid=7727117')
                        self.assertEqual(download.await_args.args[0], 'https://www.bilibili.com/video/BV123')
                finally:
                    await d.aclose()

    async def test_unknown_list_type_is_rejected(self):
        d = DownloaderBilibili(hierarchy=False)
        try:
            with self.assertRaises(ValueError):
                await d.get_collect_or_list('https://space.bilibili.com/307801268/lists/7727117?type=unknown')
        finally:
            await d.aclose()


if __name__ == '__main__':
    unittest.main()
