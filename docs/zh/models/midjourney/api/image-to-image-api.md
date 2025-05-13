---
title: 图生图 API
gitChangelog: false
updatedAt: 2025-05-08
---


# 图生图 API

## 接口描述

提交图生图任务。

## 请求

> [!TIP]
> `{api_url}` 为你实际使用的 API 节点，请根据实际情况填写。例如：
> - `www.dmxapi.cn`
> - `www.dmxapi.com`
> - `ssvip.dmxapi.com`


- 请求方式: POST

- 请求地址: `/mj/submit/imagine`

## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| mode | String | 否 | 生成模式，可选值："Turbo"、"Fast"（默认）、"Relax" |
| botType | String | 否 | 模型类型，可选值 "MID_JOURNEY"（默认） 或者 "NIJI_JOURNEY" |
| prompt | String | 是 | 提示词，描述希望生成的图片内容 |
| base64Array | Array | 否 | 包含图片 base64 数据的数组，格式为 "data:image/png;base64,<base64字符串>" |
| notifyHook | String | 否 | 回调通知的 URL，处理完成后会向该地址发送回调 |

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/midjourney/api/image-to-image-api.py{7-8,51-57,76-77}

## 响应参数示例

### 成功提交任务

```
{
    "code": 1, 
    "description": "提交成功", 
    "result": "1747141695143320", 
    "properties": {
        "discordInstanceId": "1371290282703978598", 
        "discordChannelId": "1371290282703978598"
    }
}
```

### 已提交到队列 等待启动

```
{
    "code": 1, 
    "description": "In queue, there are 67 tasks ahead", 
    "properties": None, 
    "result": "1747141540401979"
}
```