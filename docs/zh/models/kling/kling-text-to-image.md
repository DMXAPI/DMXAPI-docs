---
title: 可灵 Kling 文生图
gitChangelog: false
updatedAt: 2025-05-08
---

# 可灵 Kling 文生图

这是一个文生图的示例，使用 kling 生成图像。

> [!TIP]
> 图像生成是计算密集型任务，特别是高质量、高分辨率图像可能需要数十秒甚至数分钟处理时间，为了让用户发送请求后可以立即收到响应（任务ID），而不必等待整个生成过程，因此用户可以同时提交多个生成任务，然后异步查询结果。
> 同时这样的队列系统允许服务提供商根据可用GPU/TPU资源智能调度任务。

通常来说，图像生成的常见流程是：

1. `POST`: 调用 `生成图像api` 提交图像生成任务，返回获取 `task_id`。
2. `GET`: 根据 `task_id` 调用 `查询图像api` 查看图像生成任务是否完成。

本示例实现了每隔一秒轮询任务状态，直到任务完成，然后返回图像 url。

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


::: code-group


<<< @/zh/snippets/kling-text-to-image.py{121-122,129-135}[标准类版本]



<<< @/zh/snippets/kling-text-to-image-function.py{6-7,20-26}[纯函数版本]



:::


## 返回结果

返回结果为图片的 url，每个 url 有效期一般为 3 天以内，尽快下载或者转存。

```
https://cdn.klingai.com/bs2/upload-kling-api/6567899185/image/CjikMGgHQaYAAAAAA1CAQw-0_raw_image_0.png
```

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-05-04-23-33-40.png)

## 函数流程图

```mermaid
flowchart TD
J[调用kling_generate_image获取task_id] --> K[开始轮询任务状态]
K --> L[调用query_kling_image_url]
L --> M{获取到图像URL?}
M -->|否| N{是否超时?}
N -->|否| O[等待1秒]
O --> L
N -->|是| P[返回超时错误]
M -->|是| Q[返回图像URL]
```