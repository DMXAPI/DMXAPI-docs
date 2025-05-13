---
title: 查询任务
gitChangelog: false
updatedAt: 2025-05-08
---


# 查询任务

## 接口描述

查询已提交的任务的状态和结果。

## 请求

> [!TIP]
> `{api_url}` 为你实际使用的 API 节点，请根据实际情况填写。例如：
> - `www.dmxapi.cn`
> - `www.dmxapi.com`
> - `ssvip.dmxapi.com`


- 请求方式: GET

- 请求地址: `/mj/task/{task_id}/fetch`
- 例如针对 [提交任务 API]()：
  - `https://{api_url}/mj/task/{task_id}/fetch`


## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 是 | 任务ID |

## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/midjourney/api/query-task-api.py{5-6,32}

## 响应参数示例

```
{
    "id": "1747132423020537", 
    "action": "IMAGINE", 
    "customId": "", 
    "botType": "", 
    "prompt": "这是一个视频截图，请生成对应的吉卜力风格的图片", 
    "promptEn": "http://upload.mjdjourney.top/fileSystem/mj/133/2025/05/13/1747132422998780679_3218.png This is a video screenshot, please generate the corresponding Ghibli style image", 
    "description": "提交成功", 
    "state": "", 
    "mode": "", 
    "proxy": "", 
    "submitTime": 1747132423020, 
    "startTime": 1747132424482, 
    "finishTime": 1747132463701, 
    "imageUrl": "https://cdn.gptbest.vip/mj/attachments/1371679336578420847/1371797719932469310/bodnarovataisiia_This_is_a_video_screenshot_please_generate_the_6dc7beb8-8310-4fd4-b46c-716b422ddffc.png?ex=682471af&is=6823202f&hm=f7bcaa9bf369b81525fda9c1320bd98633c20e21bbbf7c003dbc99911a317f2c&", 
    "imageHeight": 0, 
    "imageWidth": 0, 
    "status": "SUCCESS", 
    "progress": "100%", 
    "failReason": "", 
    "buttons": [
        {
            "customId": "MJ::JOB::upsample::1::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "U1", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::upsample::2::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "U2", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::upsample::3::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "U3", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::upsample::4::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "U4", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::reroll::0::6dc7beb8-8310-4fd4-b46c-716b422ddffc::SOLO", 
            "emoji": "🔄", 
            "label": "", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::variation::1::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "V1", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::variation::2::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "V2", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::variation::3::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "V3", 
            "type": 2, 
            "style": 2
        }, 
        {
            "customId": "MJ::JOB::variation::4::6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
            "emoji": "", 
            "label": "V4", 
            "type": 2, 
            "style": 2
        }
    ], 
    "maskBase64": "", 
    "properties": {
        "notifyHook": "string", 
        "flags": 0, 
        "messageId": "1371797720431464448", 
        "messageHash": "6dc7beb8-8310-4fd4-b46c-716b422ddffc", 
        "nonce": "1922238820857864192", 
        "customId": "", 
        "finalPrompt": "<https://s.mj.run/RdNm0xs6fRI> This is a video screenshot, please generate the corresponding Ghibli style image --fast", 
        "progressMessageId": "1371797720431464448", 
        "messageContent": "**<https://s.mj.run/RdNm0xs6fRI> This is a video screenshot, please generate the corresponding Ghibli style image --fast** - <@1364921896055083058> (fast)", 
        "discordInstanceId": "1371679336578420847", 
        "discordChannelId": "1371679336578420847"
    }
}
```