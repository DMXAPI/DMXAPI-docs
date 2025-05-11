---
title: 可灵 Kling 虚拟试穿案例
gitChangelog: false
updatedAt: 2025-05-11
---

# 可灵 Kling 虚拟试穿

这是一个虚拟试穿的示例，使用 kling 生成虚拟试穿结果。

> [!TIP]
> 虚拟试穿是计算密集型任务，特别是高质量、高分辨率图像可能需要数十秒甚至数分钟处理时间，为了让用户发送请求后可以立即收到响应（任务ID），而不必等待整个生成过程，因此用户可以同时提交多个生成任务，然后异步查询结果。
> 同时这样的队列系统允许服务提供商根据可用GPU/TPU资源智能调度任务。

通常来说，虚拟试穿的常见流程是：

1. `POST`: 调用 `虚拟试穿api` 提交虚拟试穿任务，返回获取 `task_id`。
2. `GET`: 根据 `task_id` 调用 `查询虚拟试穿api` 查看虚拟试穿任务是否完成。

本示例实现了每隔一秒轮询任务状态，直到任务完成，然后返回图像 url 列表。

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/kling-virtual-try-on.py{152-153,160-164}


## 返回结果

返回结果为图片的 url ，每个 url 有效期一般为 30 天，推荐尽快下载或者转存。

```
https://cdn.klingai.com/bs2/upload-kling-api/0900730423/virtualTryOn/CjikMGgHQaYAAAAABUqu9w-0.png
```

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-05-11-22-15-55.png)

## 流程图

```mermaid
flowchart TD
    A[开始] --> B[初始化 KlingVirtualTryOn 实例]
    B --> C[调用 generate_try_on 方法]
    
    C --> D{检查人物图片类型}
    D -->|URL| E[直接使用URL]
    D -->|本地文件| F[转换为base64]
    
    C --> G{检查服饰图片类型}
    G -->|URL| H[直接使用URL]
    G -->|本地文件| I[转换为base64]
    
    E --> J[调用_kling_virtual_try_on提交任务]
    F --> J
    H --> J
    I --> J
    
    J --> K[获取task_id]
    K --> L[开始循环查询结果]
    
    L --> M[调用_query_virtual_try_on_result查询]
    M --> N{任务是否完成?}
    N -->|否| O{是否超时?}
    O -->|否| P[等待1秒]
    P --> M
    O -->|是| Q[返回超时信息]
    
    N -->|是| R[返回结果图像URL]
    
    Q --> S[结束]
    R --> S
```