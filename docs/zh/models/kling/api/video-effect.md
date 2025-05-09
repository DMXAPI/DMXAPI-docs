---
title: 视频特效
gitChangelog: false
updatedAt: 2025-05-09
---


# 视频特效

> [!CAUTION]
> 对于视频特效处理场景的 API 待接入，暂时不可用。

## 接口描述

视频特效是指根据图片进行特效的添加或者重绘。目前支持单图以及双人图的特效处理。

- 单图特效：花花世界`bloombloom`、魔力转圈圈`dizzydizzy`、快来惹毛我`fuzzyfuzzy`、捏捏乐`squish`、万物膨胀`expansion`
- 双人互动特效： 3款，拥抱`hug`、亲吻`kiss`、比心`heart_gesture`

## 请求

> [!WARNING]
> 为了让 DMXAPI 区分模型厂商，请在原 kling API 的 endpoint 基础上添加 `/kling` 路径，组合后的请求地址如下所示。

- 请求方式: POST
- 请求地址: `https://{api_url}/kling/v1/videos/effects`

## 单图请求场景（待接入）

### 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| effect_scene | string | 必须 | 无 | 场景名称，枚举值：花花世界`bloombloom`、魔力转圈圈`dizzydizzy`、快来惹毛我`fuzzyfuzzy`、捏捏乐`squish`、万物膨胀`expansion` |
| input | object | 必须 | 无 | 支持不同任务输入的结构体，根据scene不同，结构体里传的字段不同，具体如「**input 场景参数**」所示 |
| callback_url | string | 可选 | 无 | 本次任务结果回调通知地址，如果配置，服务端会在任务状态发生变更时主动通知 |
| external_task_id | string | 可选 | 无 | 用户自定义任务ID，传入不会覆盖系统生成的任务ID，但支持通过该ID进行任务查询 |

### input 场景参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| input | object | 必须 | 空 | 支持不同任务输入的结构体，根据scene不同，结构体里传的字段不同 |
| input.model_name | string | 必须 | 无 | 模型名称 枚举值：`kling-v1-6` |
| input.image | string | 必须 | 无 | 图片url或者base64形式图片，图片文件大小不能超过10MB，图片分辨率不小于300*300px，图片宽高比要在1:2.5 ~ 2.5:1之间 |
| input.duration | string | 必须 | 无 | 视频时长秒，枚举值：5 |

### 代码示例

<<< @/zh/snippets/video-effects-single.py

## 两人互动场景（待接入）

### 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| effect_scene | string | 必须 | 无 | 场景名称，枚举值：拥抱`hug`、亲吻`kiss`、比心`heart_gesture` |
| input | object | 必须 | 无 | 支持不同任务输入的结构体，根据scene不同，结构体里传的字段不同，具体如「input 场景参数」所示 |
| callback_url | string | 可选 | 无 | 本次任务结果回调通知地址，如果配置，服务端会在任务状态发生变更时主动通知 |
| external_task_id | string | 可选 | 无 | 用户自定义任务ID，传入不会覆盖系统生成的任务ID，但支持通过该ID进行任务查询 |

### input 场景参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| input | object | 必须 | 空 | 支持不同任务输入的结构体，根据scene不同，结构体里传的字段不同 |
| input.model_name | string | 必须 | kling-v1 | 模型名称 枚举值：`kling-v1`, `kling-v1-5`, `kling-v1-6` |
| input.mode | string | 可选 | std | 模型模式 枚举值：`std`，`pro` |
| input.images | Array[string] | 必须 | 无 | 数组的长度必须是2，上传的第一张图在合照的左边，上传的第二张图在合照的右边（该服务包含合照功能），图片文件大小不能超过10MB，图片分辨率不小于300*300px，图片宽高比要在1:2.5 ~ 2.5:1之间 |
| input.duration | string | 必须 | 无 | 视频时长秒，枚举值：5，10 |

### 代码示例

<<< @/zh/snippets/video-effects-interaction.py

