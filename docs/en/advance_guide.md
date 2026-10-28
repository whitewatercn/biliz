# Advance Guide
Please use `biliz -h` for more help，including method short alias，video quality selection，concurrency control，
download speed control，download directory...

## Method short alias

Method names like `get_series` and `get_video` are too cumbersome to write? Agreed! You can use their
short alias for faster access:

```shell
biliz s 'url'
biliz v 'url'
...
```
please check `biliz -h` for all short alias

## Login

there are two ways to login

* cookie option

  By adding the `SESSDATA` cookie from your browser's cache in the `--cookie` option, you can download videos that require a premium membership.

* load cookies from browser

  After logging in through the browser, use the `-fb --from-browser` option to read cookies from the browser,
  such as `-fb chrome`. Using this method may require authorization. The method that `biliz` uses to read browser
  cookies is the open-source project [browser_cookie3](https://github.com/borisbabic/browser_cookie3).

:::tip
If you want to keep logged in, you can use `alias biliz=biliz --cookie xxxxxx` or `alias biliz=biliz -fb chrome`
to create an alias for the `biliz` command
:::

## Video and audio quality, codec selection

You can use `--quality -q`option to choose video resolution，biliz supports two different selection ways：

* relatively choose (default)

  By default, biliz will select the accessible highest quality for you (that is, `-q 0`), for the second, use `-q 1` to specify, the larger number the lower resolution.
  When the number out of index, the lowest quality will be is selected. For example, you can always select the lowest quality by `-q 999`.
* absolute choose

  You can use`-q 1080P` to specific a resolution, the string is a substring of the resolution name on bilibili.

For more advanced users who may need to specify a particular video codec for download, the encodings supported by Bilibili are not visible on the website or in the app. For this purpose, biliz has designed the `info` method. By using it, you can fully understand all the information about the video:

```text
biliz info 'https://www.bilibili.com/video/BV1kG411t72J' --cookie 'xxxxx'

 【4K·HDR·Hi-Res】群青 - YOASOBI  33,899👀 1,098👍 201🪙
┣━━ 画面 Video
┃   ┣━━ HDR 真彩
┃   ┃   ┗━━ codec: hev1.2.4.L153.90                 total: 149.86MB
┃   ┣━━ 4K 超清
┃   ┃   ┣━━ codec: avc1.640034                      total: 320.78MB
┃   ┃   ┗━━ codec: hev1.1.6.L153.90                 total: 106.54MB
┃   ┣━━ 1080P 60帧
┃   ┃   ┣━━ codec: avc1.640032                      total: 171.91MB
┃   ┃   ┗━━ codec: hev1.1.6.L150.90                 total: 24.66MB
┃   ┣━━ 1080P 高清
┃   ┃   ┣━━ codec: avc1.640032                      total: 86.01MB
┃   ┃   ┗━━ codec: hev1.1.6.L150.90                 total: 24.18MB
┃   ┣━━ 720P 高清
┃   ┃   ┣━━ codec: avc1.640028                      total: 57.39MB
┃   ┃   ┗━━ codec: hev1.1.6.L120.90                 total: 11.53MB
┃   ┣━━ 480P 清晰
┃   ┃   ┣━━ codec: avc1.64001F                      total: 25.87MB
┃   ┃   ┗━━ codec: hev1.1.6.L120.90                 total: 7.61MB
┃   ┗━━ 360P 流畅
┃       ┣━━ codec: hev1.1.6.L120.90                 total: 5.24MB
┃       ┗━━ codec: avc1.64001E                      total: 11.59MB
┗━━ 声音 Audio
    ┣━━ 默认音质
    ┃   ┗━━ codec: mp4a.40.2                        total: 10.78MB
    ┗━━ Hi-Res无损
        ┗━━ codec: fLaC                             total: 94.55MB
```

looks good😇，so how can I download the video with the specified codec?

biliz provides another option `--codec`. For example, you can use a combination like `-q 480P --codec hev1.1.6.L120.90`
to specify downloading the 7.61MB one. The `--codec` option is similar to the `-q` option which supports substring specification,
for example using `--codec hev` to make all videos choose codec that start with hev.

For audio quality, some videos may contain Dolby and Hi-Res audio. You can use the `--codec` option to specify these
audio formats, for example:

```shell
biliz v 'https://www.bilibili.com/video/BV1kG411t72J' --cookie 'xxxxx' --codec hev:fLaC
```

in `--codec hev:fLaC`, use`:` to split video and audio codec, if you just want to specify audio codec，you can use`--codec :fLaC`

## Resuming Interrupted Downloads

Users can interrupt tasks by pressing `Ctrl+C`. For unfinished files, re-executing the command will resume the download
based on the previous progress, and completed files will be skipped. However, for unfinished files, it is recommended
to clear the temporary files of the unfinished tasks before executing the command again in the following situations,
otherwise some temporary files may remain:

* Changing the video quality `-q` or `--codec` after interruption
* Changing the `--part-con` after interruption
* Changing the `--time-range` after interruption

## Provide multiple urls at once
All methods of biliz support providing multiple `url`
```shell
biliz v 'url1' 'url2' 'url3'
biliz up 'up_url1' 'up_url2'
```
Concurrency, speed control also works fine when you provide multiple `url` of course


## Support for More Sites

biliz also supports some other websites, but their availability may vary as the author is currently busy.
For further information, please refer to the following [discussion](https://github.com/HFrost0/bilix/discussions/39).

## Basic Download method
For some basic download scenarios
* You can directly download a file through the file url
  ```shell
  biliz f 'https://xxxx.com/xxxx.mp4'
  ```
* you can directly download m3u8 video by url
  ```shell
  biliz m3u8 'https:/xxxx.com/xxxx.m3u8'
  ```

## Proxy
biliz will use system proxy by default
