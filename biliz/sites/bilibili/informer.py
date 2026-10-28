import asyncio
from typing import Tuple
from rich.tree import Tree
from .downloader import DownloaderBilibili
from . import api
from biliz.log import logger
from rich import print as rprint
from biliz.utils import convert_size
from biliz.download.utils import req_retry
from biliz.cli.assign import kwargs_filter


class InformerBilibili(DownloaderBilibili):
    """A special downloader with functionality to log info of bilibili resources"""

    @classmethod
    def parse_url(cls, url: str):
        res = super().parse_url(url)
        func_name = res.__name__.replace("get_", "info_")
        return getattr(cls, func_name)

    async def info_key(self, key):
        await self.parse_url(key)(self, key)

    async def info_up(self, url: str):
        up_name, total_size, bvids = await api.get_up_video_info(self.client, url)
        rprint(up_name)

    async def info_favour(self, url: str):
        pass

    async def info_collect_or_list(self, url: str):
        pass

    async def info_video(self, url: str):
        video_info = await api.get_video_info(self.client, url)
        if video_info.dash is None and video_info.other is None:
            return logger.warning(f'{video_info.title} 需要大会员或该地区不支持')
        elif video_info.other and video_info.dash is None:
            return rprint(video_info.other)  # todo: beautify durl info

        async def ensure_size(m: api.Media):
            if m.size is None:
                res = await req_retry(self.client, m.base_url, method='GET', headers={'Range': 'bytes=0-1'})
                m.size = int(res.headers['Content-Range'].split('/')[-1])

        dash = video_info.dash
        cors = [ensure_size(m) for m in dash.videos] + [ensure_size(m) for m in dash.audios]
        await asyncio.gather(*cors)

        tree = Tree(
            f"[bold reverse] {video_info.title}-{video_info.pages[video_info.p].p_name} [/]"
            f" {video_info.status.view:,}👀 {video_info.status.like:,}👍 {video_info.status.coin:,}🪙",
            guide_style="bold cyan")
        video_tree = tree.add("[bold]画面 Video")
        audio_tree = tree.add("[bold]声音 Audio")
        leaf_fmt = "codec: {codec:32} size: {size}"
        # for video
        for quality in dash.video_formats:
            p_tree = video_tree.add(quality)
            for c in dash.video_formats[quality]:
                m = dash.video_formats[quality][c]
                p_tree.add(leaf_fmt.format(codec=m.codec, size=convert_size(m.size)))
            if len(p_tree.children) == 0:
                p_tree.style = "rgb(242,93,142)"
                p_tree.add("需要登录或大会员")
        # for audio
        name_map = {"default": "默认音质", "dolby": "杜比全景声 Dolby", "flac": "Hi-Res无损"}
        for k in dash.audio_formats:
            sub_tree = audio_tree.add(name_map[k])
            if m := dash.audio_formats[k]:
                sub_tree.add(leaf_fmt.format(codec=m.codec, size=convert_size(m.size)))
            else:
                sub_tree.style = "rgb(242,93,142)"
                sub_tree.add("需要登录或大会员")
        rprint(tree)

    @classmethod
    def handle(cls, method: str, keys: Tuple[str, ...], options: dict):
        if cls.pattern.match(keys[0]) and 'info' == method:
            informer = InformerBilibili(sess_data=options['cookie'], **kwargs_filter(cls, options))

            # in order to maintain order
            async def temp():
                for key in keys:
                    if len(keys) > 1:
                        logger.info(f"For {key}")
                    await informer.info_key(key)

            return informer, temp()
