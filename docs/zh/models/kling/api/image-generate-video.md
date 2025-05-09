---
title: 图生视频
gitChangelog: false
updatedAt: 2025-05-09
---


# 图生视频

> [!TIP]
> 由于任务是异步提交的，请在提交任务后，通过 [查询任务状态](/zh/models/kling/api/query-api.md) 接口查询任务状态及结果。
>
> 对于图生视频场景，生成时间可能较长，根据选择的参数而异，预计在 4 分钟内，请耐心等待。

## 接口描述

提交图片生成视频任务。

## 请求

> [!WARNING]
> 为了让 DMXAPI 区分模型厂商，请在原 kling API 的 endpoint 基础上添加 `/kling` 路径，组合后的请求地址如下所示。

- 请求方式: POST

- 请求地址: `https://{api_url}/kling/v1/videos/image2video`

## 请求参数

> [!TIP]
> 通过合理使用尾帧控制，可以创建更有预见性和控制力的视频生成效果，特别适合需要明确起止状态的视频动画制作。

| 字段 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| model_name | string | 可选 | kling-v1 | 模型名称。枚举值：kling-v1, kling-v1-5, kling-v1-6 |
| image | string | 必须 | 空 | 参考图像。支持图片Base64编码或URL，格式支持.jpg/.jpeg/.png，文件大小≤10MB，分辨率≥300*300px，宽高比在1:2.5~2.5:1之间 |
| image_tail | string | 可选 | 空 | 参考图像尾帧控制。格式要求同image。与image至少二选一 |
| prompt | string | 可选 | 无 | 正向文本提示词。不超过2500个字符 |
| negative_prompt | string | 可选 | 空 | 负向文本提示词。不超过2500个字符 |
| cfg_scale | float | 可选 | 0.5 | 生成视频的自由度。取值范围[0, 1]，值越大与提示词相关性越强 |
| mode | string | 可选 | std | 生成视频模式。枚举值：std(标准模式)，pro(专家模式) |
| static_mask | string | 可选 | 无 | 静态笔刷涂抹区域。格式要求同image，长宽比须与输入图片相同 |
| dynamic_masks | array | 可选 | 无 | 动态笔刷配置列表。最多6组 |
| dynamic_masks.mask | string | 可选 | 无 | 动态笔刷涂抹区域。格式要求同image，长宽比须与输入图片相同 |
| dynamic_masks.trajectories | array | 可选 | 无 | 运动轨迹坐标序列。5s视频坐标数范围[2,77] |
| dynamic_masks.trajectories.x | int | 可选 | 无 | 轨迹点横坐标（以图片左下角为原点） |
| dynamic_masks.trajectories.y | int | 可选 | 无 | 轨迹点纵坐标（以图片左下角为原点） |
| camera_control | object | 可选 | 空 | 控制摄像机运动的协议 |
| camera_control.type | string | 可选 | 无 | 预定义运镜类型。枚举值：simple, down_back, forward_up, right_turn_forward, left_turn_forward |
| camera_control.config | object | 可选 | 无 | 摄像机运动配置。type为simple时必填 |
| camera_control.config.horizontal | float | 可选 | 无 | 水平运镜。范围[-10,10]，负左正右 |
| camera_control.config.vertical | float | 可选 | 无 | 垂直运镜。范围[-10,10]，负下正上 |
| camera_control.config.pan | float | 可选 | 无 | 水平摇镜。范围[-10,10]，负左正右 |
| camera_control.config.tilt | float | 可选 | 无 | 垂直摇镜。范围[-10,10]，负下正上 |
| camera_control.config.roll | float | 可选 | 无 | 旋转运镜。范围[-10,10]，负逆时针正顺时针 |
| camera_control.config.zoom | float | 可选 | 无 | 变焦。范围[-10,10]，负拉远正拉近 |
| duration | string | 可选 | 5 | 生成视频时长(秒)。枚举值：5，10 |
| callback_url | string | 可选 | 无 | 任务结果回调通知地址 |
| external_task_id | string | 可选 | 无 | 自定义任务ID。单用户下需唯一 |

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/image-to-video-api.py{6-7,31-72}

## 响应参数示例

> 业务码的含义请参考 [业务码](/zh/models/kling/api/business-code.md)。

```
{
	'code': 0, // 业务码 0 表示成功
	'message': 'SUCCEED', // 消息
	'request_id': 'CjhDaWgU7GAAAAAAAb1QfA', // 请求ID
	'data': {
		'task_id': 'CjhDaWgU7GAAAAAAAb1QfA', // 任务ID
		'task_status': 'submitted', // 任务状态
		'created_at': 1746771840640, // 创建时间
		'updated_at': 1746771840640 // 更新时间
	}
}
```


