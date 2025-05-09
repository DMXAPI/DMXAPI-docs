---
title: 视频口型同步
gitChangelog: false
updatedAt: 2025-05-09
---


# 视频延长

> [!TIP]
> 由于任务是异步提交的，请在提交任务后，通过 [查询任务状态](/zh/models/kling/api/query-api.md) 接口查询任务状态及结果。
>
> 对于对口型场景，生成预计在 3 分钟左右，请耐心等待。

## 接口描述

> [!WARNING]
> 请确保使用的图片中有人像，否则会报错 `there is no human in the video`。

对口型是指根据文本生成视频，视频中的人物会根据文本内容进行对口型。

## 请求

> [!WARNING]
> 为了让 DMXAPI 区分模型厂商，请在原 kling API 的 endpoint 基础上添加 `/kling` 路径，组合后的请求地址如下所示。

- 请求方式: POST

- 请求地址: `https://{api_url}/kling/v1/videos/lip-sync`

## 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| input | object | 必须 | 空 | 包含多个字段，用于指定视频、口型对应内容等 |
| input.video_id | string | 必须* | 无 | 可灵AI生成的视频ID。与video_url二选一，仅支持30天内生成的5-10秒视频 |
| input.video_url | string | 必须* | 无 | 视频获取链接。支持mp4/mov格式，≤100MB，2-10秒，720p/1080p |
| input.mode | string | 必须 | 无 | 生成模式：`text2video`或`audio2video` |
| input.text | string | 可选† | 无 | 口型对应文本，mode为text2video时必填，**最大长度120字符** |
| input.voice_id | string | 可选† | 无 | 音色ID，mode为text2video时必填，[请查阅官方文档](https://docs.qingque.cn/s/home/eZQDvafJ4vXQkP8T9ZPvmye8S) |
| input.voice_language | string | 可选† | zh | 音色语种：`zh`(中文)或`en`(英文) |
| input.voice_speed | float | 可选† | 1.0 | 语速，范围[0.8-2.0]，精确到小数点后1位 |
| input.audio_type | string | 可选‡ | 无 | 音频传输方式：`file`或`url`，mode为audio2video时必填 |
| input.audio_file | string | 可选‡ | 无 | 音频文件Base64编码，audio_type为file时必填，支持mp3/wav/m4a/acc，≤5MB |
| input.audio_url | string | 可选‡ | 无 | 音频文件URL，audio_type为url时必填，格式要求同audio_file |
| callback_url | string | 可选 | 无 | 任务结果回调通知地址 |

注释说明：
- `*` 表示 video_id 和 video_url 必须二选一
- `†` 表示在 text2video 模式下必填
- `‡` 表示在 audio2video 模式下必填

### 视频要求

- 格式：`.mp4`或`.mov`
- 大小：≤100MB
- 时长：2-10秒
- 分辨率：720p或1080p
- 尺寸：边长在720px~1920px之间

### 音频要求

- 格式：`.mp3`、`.wav`、`.m4a`或`.acc`
- 大小：≤5MB
- Base64编码，格式不匹配或文件过大会返回错误码等信息
- 质量：系统会校验文本内容，如有问题会返回错误码等信息

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。

<<< @/zh/snippets/lip-sync.py{5-6,19-41}

## 响应参数示例

> 业务码的含义请参考 [业务码](/zh/models/kling/api/business-code.md)。

```
{
	'code': 0, // 业务码 0 表示成功
	'message': 'SUCCEED', // 消息
	'request_id': 'CjikY2gHPbcAAAAABI5n9g', // 请求ID
	'data': {
		'task_id': 'CjikY2gHPbcAAAAABI5n9g', // 任务ID
		'task_status': 'submitted', // 任务状态
		'created_at': 1746773850590, // 创建时间
		'updated_at': 1746773850590 // 更新时间
	}
}
```



