---
title: 文生视频
gitChangelog: false
updatedAt: 2025-05-09
---


# 文生视频

> [!TIP]
> 由于任务是异步提交的，请在提交任务后，通过 [查询任务状态](/zh/models/kling/api/query-api.md) 接口查询任务状态及结果。
>
> 对于文生视频场景，生成时间可能较长，根据选择的参数而异，预计在 5 分钟内，请耐心等待。

## 接口描述

提交文字生成视频任务。

## 请求

> [!WARNING]
> 为了让 DMXAPI 区分模型厂商，请在原 kling API 的 endpoint 基础上添加 `/kling` 路径，组合后的请求地址如下所示。

- 请求方式: POST

- 请求地址: `https://{api_url}/kling/v1/videos/text2video`

## 请求参数


| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| model_name | string | 可选 | kling-v1 | 模型名称，枚举值：kling-v1, kling-v1-6 |
| prompt | string | 必填 | 无 | 正向文本提示词，不能超过2500个字符 |
| negative_prompt | string | 可选 | 空 | 负向文本提示词，不能超过2500个字符 |
| cfg_scale | float | 可选 | 0.5 | 生成视频的自由度；值越大，模型自由度越小，与提示词相关性越强。取值范围：[0, 1] |
| mode | string | 可选 | std | 生成视频的模式。枚举值：<br>- `std`：标准模式，基础模式，性价比高<br>- `pro`：专家模式（高品质），高表现模式，生成视频质量更佳 |
| aspect_ratio | string | 可选 | 16:9 | 生成视频的画面纵横比（宽:高）。枚举值：16:9, 9:16, 1:1 |
| duration | string | 可选 | 5 | 生成视频时长，单位为秒。枚举值：5, 10 |
| callback_url | string | 可选 | 无 | 任务结果回调通知地址，服务器会在任务状态变更时主动通知 |
| external_task_id | string | 可选 | 无 | 自定义任务ID，不会覆盖系统生成的任务ID，但支持通过该ID查询任务，需保证单用户下唯一性 |

## 摄像机控制参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| camera_control | object | 可选 | 空 | 控制摄像机运动的协议（如未指定，模型将根据输入内容智能匹配） |
| camera_control.type | string | 可选 | 无 | 预定义的运镜类型，枚举值：<br>- `simple`：简单运镜，此类型下可在config中六选一进行运镜<br>- `down_back`：镜头下压并后退 ➡️ 下移拉远<br>- `forward_up`：镜头前进并上仰 ➡️ 推进上移<br>- `right_turn_forward`：先右旋转后前进 ➡️ 右旋推进<br>- `left_turn_forward`：先左旋并前进 ➡️ 左旋推进 |
| camera_control.config | object | 可选* | 无 | 包含六个字段的对象，用于指定摄像机在不同方向上的运动。当运镜类型为simple时必填 |
| camera_control.config.horizontal | float | 可选 | 无 | 水平运镜，控制摄像机在水平方向上的移动量。取值范围：[-10, 10]，负值表示向左，正值表示向右 |
| camera_control.config.vertical | float | 可选 | 无 | 垂直运镜，控制摄像机在垂直方向上的移动量。取值范围：[-10, 10]，负值表示向下，正值表示向上 |
| camera_control.config.pan | float | 可选 | 无 | 水平摇镜，控制摄像机在水平面上的旋转量。取值范围：[-10, 10]，负值表示向左旋转，正值表示向右旋转 |
| camera_control.config.tilt | float | 可选 | 无 | 垂直摇镜，控制摄像机在垂直面上的旋转量。取值范围：[-10, 10]，负值表示向下旋转，正值表示向上旋转 |
| camera_control.config.roll | float | 可选 | 无 | 旋转运镜，控制摄像机的滚动量。取值范围：[-10, 10]，负值表示逆时针旋转，正值表示顺时针旋转 |
| camera_control.config.zoom | float | 可选 | 无 | 变焦，控制摄像机的焦距变化。取值范围：[-10, 10]，负值表示焦距变长、视野变小，正值表示焦距变短、视野变大 |

> 注意：在 camera_control.config 中，六个参数只能择一使用，即只能有一个参数不为0，其余参数必须为0。


## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/text-to-video-api.py{5-6,19-46}

## 响应参数示例

> 业务码的含义请参考 [业务码](/zh/models/kling/api/business-code.md)。

```
{
	'code': 0, // 业务码 0 表示成功
	'message': 'SUCCEED', // 消息
	'request_id': 'Cl6kH2gHPegAAAAABJAWDA', // 请求ID
	'data': {
		'task_id': 'Cl6kH2gHPegAAAAABJAWDA', // 任务ID
		'task_status': 'submitted', // 任务状态
		'created_at': 1746768679809, // 创建时间
		'updated_at': 1746768679809 // 更新时间
	}
}
```



