---
title: 生成图像
gitChangelog: false
updatedAt: 2025-05-08
---


# 生成图像

> [!TIP]
> 由于任务是异步提交的，请在提交任务后，通过 [查询任务状态](/zh/models/kling/api/query-api.md) 接口查询任务状态及结果。
>
> 对于图像生成场景，Kling 的生成预计在 30 秒内，请耐心等待。

## 接口描述

提交生成图像任务。

## 请求

- 请求方式: POST

- 请求地址: `https://{api_url}/kling/v1/images/generations`

## 请求参数

### 文生图场景

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model_name | string | 是 | 模型名称，可选择 kling-v1-5 或 kling-v1 或 kling-v2|
| prompt | string | 是 | 文本提示词，描述想要生成的图像内容，不能超过2500个字符 |
| negative_prompt | string | 否 | 负向文本提示词，描述不希望在图像中出现的内容，不能超过2500个字符 |
| output_format | string | 否 | 输出格式，可选 png 或 jpg，默认为 png |
| n | int | 否 | 生成图像数量，范围 [1, 9]，默认为 1 |
| aspect_ratio | string | 否 | 输出图像比例，可选值：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3，默认为 1:1 |
| callback_url | string | 否 | 回调地址，可用于 webhook 等通知场景，任务完成后会向该地址发送请求 |

### 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/text-to-image-api.py{5-6,19-25}

### 图生图场景

> [!warning]
> 图像类型传参说明：
> - 支持Base64编码或图片URL。
> - 支持.jpg / .jpeg / .png格式，大小不能超过10MB，图片分辨率不小于300*300px。
> - 图片宽高比要在1:2.5 ~ 2.5:1之间。
> - Base64仅提供编码部分，data:image/png;base64,后面的部分，详细可以参考示例。
> 
> **在图生图的场景下（即image字段不为空时），不支持负向提示词**
> 

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model_name | string | 是 | 模型名称，可选择 kling-v1-5 或 kling-v1 或 kling-v2 |
| prompt | string | 是 | 文本提示词，描述想要生成的图像内容，不能超过2500个字符 |
| **image** | string | 是 | 参考图片，图片格式支持.jpg / .jpeg / .png |
| **image_reference** | string | 此参数仅支持 `kling-v1-5` 模型，必填。 | 参考图片类型，可选值：subject（角色特征参考）, face（人物长相参考），使用face（人物长相参考）时，上传图片需仅含1张人脸。 |
| **image_fidelity** | float | 否 | 参考图片强度，取值范围：[0,1]，数值越大参考强度越大。 |
| **human_fidelity** | float | 否 | 面部参考强度，即参考图中人物五官相似度，取值范围：[0,1]，数值越大参考强度越大。 |
| output_format | string | 否 | 输出格式，可选 png 或 jpg，默认为 png |
| n | int | 否 | 生成图像数量，范围 [1, 9]，默认为 1 |
| aspect_ratio | string | 否 | 输出图像比例，可选值：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3，默认为 1:1 |
| callback_url | string | 否 | 回调地址，可用于 webhook 等通知场景，任务完成后会向该地址发送请求 |

### 代码示例

<<< @/zh/snippets/image-to-image-api.py{6-7,31-40}  

## 响应参数示例

> 业务码的含义请参考 [业务码](/zh/models/kling/api/business-code.md)。

```
{
	'code': 0, // 业务码 0 表示成功
	'message': 'SUCCEED', // 消息
	'request_id': 'CjhDaWgU7GAAAAAAAZYRYA', // 请求ID
	'data': {
		'task_id': 'CjhDaWgU7GAAAAAAAZYRYA', // 任务ID
		'task_status': 'submitted', // 任务状态
		'created_at': 1746719586481, // 创建时间
		'updated_at': 1746719586481 // 更新时间
	}
}
```



