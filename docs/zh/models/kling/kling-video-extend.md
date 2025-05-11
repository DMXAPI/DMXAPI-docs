---
title: 可灵 Kling 视频延长案例
gitChangelog: false
updatedAt: 2025-05-11
---

# 可灵 Kling 视频延长

这是一个视频延长的示例，使用 kling 延长视频。

> [!TIP]
> 视频延长是计算密集型任务，特别是高质量、高分辨率视频可能需要数十秒甚至数分钟处理时间，为了让用户发送请求后可以立即收到响应（任务ID），而不必等待整个生成过程，因此用户可以同时提交多个生成任务，然后异步查询结果。
> 同时这样的队列系统允许服务提供商根据可用GPU/TPU资源智能调度任务。

通常来说，视频延长的常见流程是：

1. `POST`: 调用 `视频延长api` 提交视频延长任务，返回获取 `task_id`。
2. `GET`: 根据 `task_id` 调用 `查询视频api` 查看视频延长任务是否完成。

本示例实现了每隔一秒轮询任务状态，直到任务完成，然后返回视频 url 和 id。

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/kling-video-extend.py{124-125,132-138}


## 返回结果

返回结果为视频的 url 和 id，视频的有效期一般为 30 天，推荐尽快下载或者转存。

```

```

## 流程图

```mermaid
flowchart TD
    A[开始] --> B[初始化 KlingVideoExtend 实例]
    B --> C[调用 extend_video 方法]
    
    C --> D[准备参数: task_id, video_id, prompt等]
    D --> E[调用 _kling_extend_video 提交任务]
    E --> F[获取task_id]
    
    F --> G[开始循环查询结果]
    G --> H[调用 _query_video_extend_result 查询]
    
    H --> I{任务是否完成?}
    I -->|否| J{是否超时?}
    J -->|否| K[等待1秒]
    K --> H
    J -->|是| L[返回超时信息]
    
    I -->|是| M[获取结果: video_url, video_id]
    M --> N[返回视频URL和视频ID]
    
    L --> O[结束]
    N --> O
```