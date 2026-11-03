# 进阶使用
请使用`biliz -h`查看更多参数提示，包括方法名简写，视频画面质量选择，并发量控制，下载速度限制，下载目录等。

## 方法名简写

觉得`get_series`，`get_video`这些方法名写起来太麻烦了？同感！你可以使用他们的简写，这样快多了：

```shell
biliz s 'url'
biliz v 'url'
...
```
更多简写请查看`biliz -h`

## 登录

你是大会员？🥸，两种方式登录

* 直接填写cookie

  在`--cookie`参数中填写浏览器缓存的`SESSDATA`cookie，填写后可以下载需要大会员的视频

* 从浏览器载入cookie

  在浏览器中登录之后，使用`-fb --from-browser`参数从浏览器中读取cookie，例如`-fb chrome`，使用这种方法可能需要授权，biliz读取浏览器cookie的
  方式为开源项目[browser_cookie3](https://github.com/borisbabic/browser_cookie3)。
:::tip
::: tip macOS 27 浏览器凭证授权
使用 `-fb edge` 或 `-fb chrome` 导入登录凭证时，biliz 需要读取浏览器的本地 Cookie 数据库。请在 **系统设置 → 隐私与安全性 → 完全磁盘访问权限** 中，为实际运行 biliz 的应用（例如 Terminal.app）手动授权。授权后完全退出并重新打开该应用，再重试命令。

未授权时，导入浏览器凭证可能报错 `browser_cookie3.BrowserCookieError: Unable to read database file`。可以按上面的步骤授权后重试，或者去掉 `-fb` 参数，以匿名方式下载公开视频。

如果已授权仍出现 `Unable to read database file`，请确认命令确实在已授权的应用中运行，并尝试完全退出浏览器后重试。

[Apple 完全磁盘访问权限说明](https://developer.apple.com/documentation/security/accessing-files-from-the-macos-app-sandbox#Request-full-disk-access-to-use-all-files-on-a-Mac)
:::

如果你总是需要保持登录，在linux和mac系统中你可以使用`alias biliz=biliz --cookie xxxxxx`或`alias biliz=biliz -fb chrome`来为`biliz`命令创建别名
:::

## 画质，音质和编码选择

你可以使用`--quality`即`-q`参数选择画面分辨率，biliz支持两种不同的选择方式：

* 相对选择（默认）

  biliz在默认情况下会为你选择可选的最高画质进行下载（即`-q 0`），如果你想下载第二清晰的可使用`-q 1`进行指定，以此类推，指定序号越大画质越低，
  当超过可选择范围时，默认选择到最低画质，例如你总是可以通过`-q 999`来选择到最低画质。
* 绝对选择

  在某些时候，你只希望下载720P的视频，但是720P在相对选择中并不总是处于固定的位置，这在下载收藏夹，合集等等场景中经常出现。
  另外有可能你就是喜欢通过`-q 1080P`这样的方式来指定画质。
  没问题，biliz同时也支持通过`-q 4K` `-q '1080P 高码率'`等字符串的形式来直接指定画质，字符串为b站显示的画质名称的子串即可。

在更加专业用户的需求中，可能需要指定特定的视频编码进行下载，而b站支持的编码在网页或app中是不可见的，biliz为此设计了方法`info`
， 通过它你可以完全了解该视频的所有信息：

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

看上去不错😇，那么我要怎么才能下到指定编码的视频呢？

biliz提供了另一个参数`--codec`来指定编码格式，例如你可以通过组合`-q 480P --codec hev1.1.6.L120.90`来指定下载7.61MB的那个。
`--codec`参数与`-q`参数类似，也支持子串指定，例如你可以通过`--codec hev`来使得所有视频都选择`hev`开头的编码。

对于音质，部分视频会含有大会员专享的杜比全景声和Hi-Res无损音质，利用`--codec`参数可以指定这些音频，例如

```shell
biliz v 'https://www.bilibili.com/video/BV1kG411t72J' --cookie 'xxxxx' --codec hev:fLaC
```

`--codec hev:fLaC`中使用`:`将画质编码和音频编码隔开，如只指定音频编码，可使用`--codec :fLaC`

## 关于断点重连

用户可以通过Ctrl+C中断任务，对于未完成的文件，重新执行命令会在之前的进度基础上下载，已完成的文件会进行跳过。
但是对于未完成的文件，以下情况建议清除未完成任务的临时文件再执行命令，否则可能残留部分临时文件。

- 中断后改变画面质量`-q`或编码`--codec`
- 中断后改变分段并发数`--part-con`
- 中断后改变时间范围`--time-range`

## 一次提供多个url
biliz的所有方法都支持提供多个`url`
```shell
biliz v 'url1' 'url2' 'url3'
biliz up 'up_url1' 'up_url2'
```
当你提供多个`url`时，并发控制当然也正常工作


## 支持范围

biliz 仅支持哔哩哔哩（含 b23.tv 短链接）。其他网站以及通用文件、M3U8 链接下载已停止支持。

## 代理
biliz默认使用系统代理
