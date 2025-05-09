import http.client
import json

# 配置全局变量
API_URL = "www.dmxapi.cn"  # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXX"  # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

def kling_video_extend():
    """调用 Kling AI 的视频延长API，提交一个视频延长任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有视频生成参数
    payload = json.dumps({
        "task_id": "CjhDaWgU7GAAAAAAAb1QfA",  # [必选]任务ID
        "video_id": "bc17f1e8-6c7b-440c-bd30-e47fb1c82932",  # [必选]要延长的视频ID
        "prompt": "继续展示动物的走动，保持相同的风格和氛围",  # 正向提示词
        # "negative_prompt": "突然的场景转换, 光线变化, 画面抖动",  # 负向提示词
        # "cfg_scale": 0.5,  # 提示词参考强度，设置较高以保持连贯性
        # "callback_url": "https://your-server.com/webhook/video-extend"  # 回调通知地址
    })
    
    # 构建请求头，包含认证信息和内容类型
    headers = {
        'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
        'Content-Type': 'application/json'  # 指定请求体格式为JSON
    }
    
    # 发送POST请求，路径为视频生成API端点
    conn.request("POST", "/kling/v1/videos/video-extend", payload, headers)
    
    # 获取API响应并解析JSON数据
    res = conn.getresponse()
    json_data = json.loads(res.read().decode("utf-8"))
    # print(json_data)
    
    if json_data['code'] == 0:
        # 成功则返回提交的任务 id
        return json_data['data']['task_id']
    else:
        # 失败则返回错误信息
        return json_data['message']

if __name__ == "__main__":
    # 提交视频延长任务
    print(kling_video_extend())