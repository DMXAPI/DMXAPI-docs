---
title: 视频延长
gitChangelog: false
updatedAt: 2025-05-09
---


# 视频延长

> [!TIP]
> 由于任务是异步提交的，请在提交任务后，通过 [查询任务状态](/zh/models/kling/api/query-api.md) 接口查询任务状态及结果。
>
> 对于视频延长场景，生成时间可能较长，根据选择的参数而异，预计在 4 分钟内，请耐心等待。

## 接口描述

> [!WARNING]
> 暂不支持对V1.5模型生成的视频进行延长。
>
> 基于目前的清理策略、视频生成30天之后会被清理，则无法进行延长

视频延长是指对文生/图生视频结果进行时间上的延长，单次可延长4~5s，使用的模型和模式不可选择、与源视频相同。被延长后的视频可以再次延长，但总视频时长不能超过3min

## 请求

> [!WARNING]
> 为了让 DMXAPI 区分模型厂商，请在原 kling API 的 endpoint 基础上添加 `/kling` 路径，组合后的请求地址如下所示。

- 请求方式: POST

- 请求地址: `https://{api_url}/kling/v1/videos/video-extend`

## 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| task_id | string | 必须 | 无 | 任务ID |
| video_id | string | 必须 | 无 | 视频ID，支持通过文本、图片和视频延长生成的视频的ID（原视频不能超过3分钟） |
| prompt | string | 可选 | 无 | 正向文本提示词，不能超过2500个字符词 |
| negative_prompt | string | 可选 | 无 | 负向文本提示词，不能超过2500个字符词 |
| cfg_scale | float | 可选 | 0.5 | 提示词参考强度，取值范围：[0,1]，数值越大参考强度越大 |
| callback_url | string | 可选 | 无 | 本次任务结果回调通知地址 |

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。

<<< @/zh/snippets/video-extend-api.py{5-6,19-24}

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



