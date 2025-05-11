---
title: 可灵 Kling 视频口型同步案例
gitChangelog: false
updatedAt: 2025-05-11
---

# 可灵 Kling 视频口型同步

这是一个视频口型同步的示例，使用 kling 口型同步视频。

> [!TIP]
> 视频口型同步是计算密集型任务，特别是高质量、高分辨率视频可能需要数十秒甚至数分钟处理时间，为了让用户发送请求后可以立即收到响应（任务ID），而不必等待整个生成过程，因此用户可以同时提交多个生成任务，然后异步查询结果。
> 同时这样的队列系统允许服务提供商根据可用GPU/TPU资源智能调度任务。

通常来说，视频口型同步的常见流程是：

1. `POST`: 调用 `视频口型同步api` 提交视频口型同步任务，返回获取 `task_id`。
2. `GET`: 根据 `task_id` 调用 `查询视频api` 查看视频口型同步任务是否完成。

本示例实现了每隔一秒轮询任务状态，直到任务完成，然后返回视频 url 和 id。

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/kling-lip-sync.py{247-248,255-262,270-272,277-278,283-285}


## 返回结果

返回结果为视频的 url 和 id，视频的有效期一般为 30 天，推荐尽快下载或者转存。

```

```

## 流程图

```mermaid
flowchart TD
    A[开始] --> B[初始化 KlingLipSync 实例]
    
    %% 文本转视频口型同步路径
    B --> C1[调用 generate_text2video_lip_sync]
    C1 --> D1[准备输入参数]
    D1 --> E1{检查视频来源}
    
    E1 -->|URL格式| F1[设置为video_url]
    E1 -->|任务ID格式| G1[设置为task_id和video_id]
    E1 -->|使用task_id和video_id| H1[直接使用提供的参数]
    
    F1 --> I1[设置文本和语音参数]
    G1 --> I1
    H1 --> I1
    
    %% 音频转视频口型同步路径
    B --> C2[调用 generate_audio2video_lip_sync]
    C2 --> D2[准备输入参数]
    D2 --> E2{检查视频来源}
    
    E2 -->|URL格式| F2[设置为video_url]
    E2 -->|任务ID格式| G2[设置为task_id和video_id]
    E2 -->|使用task_id和video_id| H2[直接使用提供的参数]
    
    F2 --> I2{检查音频来源}
    G2 --> I2
    H2 --> I2
    
    I2 -->|URL格式| J2[设置为audio_url]
    I2 -->|本地文件| K2[转换为base64并设置]
    
    %% 共同的API调用和结果处理部分
    I1 --> L[调用_kling_lip_sync提交任务]
    J2 --> L
    K2 --> L
    
    L --> M[获取task_id]
    M --> N[开始轮询任务结果]
    
    N --> O[调用_query_lip_sync_result]
    O --> P{任务是否完成?}
    
    P -->|否| Q{是否超时?}
    Q -->|否| R[等待2秒]
    R --> O
    Q -->|是| S[返回超时信息]
    
    P -->|是| T[获取video_url和video_id]
    T --> U[返回结果]
    
    S --> V[结束]
    U --> V
```