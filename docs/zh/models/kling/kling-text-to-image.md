---
title: 可灵 Kling 文生图案例
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


<<< @/zh/snippets/kling-text-to-image.py{122-123,130-137}


## 返回结果

返回结果为图片的 url 列表，这里使用参数 `n=2` 生成两张图片，每个 url kling 官方保证有效期为 30 天，尽快下载或者转存。

```
['https://cdn.klingai.com/bs2/upload-kling-api/8089468206/image/Cl6kH2gHPegAAAAABUwweg-0_raw_image_0.png', 'https://cdn.klingai.com/bs2/upload-kling-api/8089468206/image/Cl6kH2gHPegAAAAABUwweg-1_raw_image_0.png']
```

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-05-11-20-50-49.png)

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-05-11-20-51-02.png)

## 函数流程图

```mermaid
graph TD
    A[初始化 KlingTextToImage] -->|提供 API 凭证| B[调用 generate_image 方法]
    B -->|传入提示词和参数| C[_kling_generate_image 方法]
    C -->|构建请求体| D[发送 POST 请求到 API]
    D -->|返回 task_id| E[开始轮询任务状态]
    
    E -->|调用| F[_query_kling_image_url 方法]
    F -->|发送 GET 请求| G[检查任务状态]
    
    G -->|任务状态?| H{任务完成?}
    H -->|是| I[提取并返回图像 URL]
    H -->|否| J{是否超时?}
    
    J -->|是| K[返回 None]
    J -->|否| L[等待 1 秒]
    L --> F
    
    I -->|返回图像 URL 列表| M[结束流程]
    K -->|返回超时信息| M
```