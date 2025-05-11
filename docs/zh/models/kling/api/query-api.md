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

- 请求地址: `API对应请求接口/{task_id}`
- 例如针对 [生成图像 API](./generate-image.md)：
  - `https://{api_url}/kling/v1/images/generations/{task_id}`


## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| task_id | string | 是 | 任务ID |

## 响应参数示例

> 业务码的含义请参考 [业务码](/zh/models/kling/api/business-code.md)。

```
{
    'code': 0, // 业务码 0 表示成功
    'message': 'SUCCEED', // 消息
    'request_id': 'Cl58rmgHRLsAAAAABFV6lg', // 请求ID
    'data': {
        'task_id': 'Cl58rmgHRLsAAAAABFV6lg', // 任务ID
        'task_status': 'submitted', // 任务状态
        'created_at': 1746696422103, // 创建时间
        'updated_at': 1746696422103 // 更新时间
    }
}
```


## 代码示例

> 深色背景为可以修改的参数，非必选参数已经注释，可以按照自己的需求启用。


<<< @/zh/snippets/query-api.py{5-6,22,42}
