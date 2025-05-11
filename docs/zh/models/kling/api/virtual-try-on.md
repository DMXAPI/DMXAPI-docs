---
title: 虚拟试穿
gitChangelog: false
updatedAt: 2025-05-09
---


# 虚拟试穿

> [!TIP]
> 由于任务是异步提交的，请在提交任务后，通过 [查询任务状态](/zh/models/kling/api/query-api.md) 接口查询任务状态及结果。
>
> 对于虚拟试穿场景，生成预计在 30 秒左右，请耐心等待。

## 接口描述

> [!WARNING]
> 请确保使用的图片中有人像，否则会报错 `there is no human in the video`。

虚拟试穿是指根据用户上传的衣物图片和用户图片，生成用户试穿衣物的效果图。

## 请求

> [!WARNING]
> 为了让 DMXAPI 区分模型厂商，请在原 kling API 的 endpoint 基础上添加 `/kling` 路径，组合后的请求地址如下所示。

- 请求方式: POST

- 请求地址: `https://{api_url}/kling/v1/images/kolors-virtual-try-on`

## 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| model_name | string | 可选 | kolors-virtual-try-on-v1 | 模型名称，可选值：基础版本 `kolors-virtual-try-on-v1` 或 v1-5 版本 `kolors-virtual-try-on-v1-5` 支持服装组合 |
| human_image | string | 必须 | 空 | 人物图片，支持Base64编码或URL 格式：jpg/jpeg/png 大小：≤10MB 分辨率：≥300*300px |
| cloth_image | string | 必须 | 空 | 服饰图片，支持商品图或白底图，支持上装(upper)、下装(lower)、连体装(dress) 格式：jpg/jpeg/png 大小：≤10MB 分辨率：≥300*300px |
| callback_url | string | 可选 | 无 | 任务结果回调通知地址 |

### 服装组合规则 (仅 v1-5 版本支持)

当使用 `kolors-virtual-try-on-v1-5` 模型时，可以将多个服装图片拼接在一张图上，支持以下服装组合规则：

| 输入组合 | 结果 |
|---------|------|
| 单个服饰（上装/下装/连体装） | ✅ 生成对应单品试穿图片 |
| 上装 + 下装 | ✅ 生成组合试穿图片 |
| 上装 + 上装 | ❌ 生成失败 |
| 下装 + 下装 | ❌ 生成失败 |
| 连体装 + 连体装 | ❌ 生成失败 |
| 上装 + 连体装 | ❌ 生成失败 |
| 下装 + 连体装 | ❌ 生成失败 |

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。

<<< @/zh/snippets/virtual-try-on.py{6-7,31-36}

## 生成响应参数

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

## 查询响应参数

```
{
  "code": 0, //错误码；具体定义见错误码
  "message": "string", //错误信息
  "request_id": "string", //请求ID，系统生成，用于跟踪请求、排查问题
  "data":{
  	"task_id": "string", //任务ID，系统生成
    "task_status": "string", //任务状态，枚举值：submitted（已提交）、processing（处理中）、succeed（成功）、failed（失败）
    "task_status_msg": "string", //任务状态信息，当任务失败时展示失败原因（如触发平台的内容风控等）
    "created_at": 1722769557708, //任务创建时间，Unix时间戳、单位ms
    "updated_at": 1722769557708, //任务更新时间，Unix时间戳、单位ms
    "task_result":{
      "images":[
        {
          "index": int, //图片编号
          "url": "string" //生成图片的URL，例如：https://h1.inkwai.com/bs2/upload-ylab-stunt/1fa0ac67d8ce6cd55b50d68b967b3a59.png（请注意，为保障信息安全，生成的图片/视频会在30天后被清理，请及时转存）
        }
      ]
    }
  }
}
```

