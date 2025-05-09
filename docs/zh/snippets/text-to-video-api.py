import http.client
import json

# 配置全局变量
API_URL = "www.dmxapi.cn"  # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXXX"  # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

def kling_text_generate_video():
    """调用 Kling AI 的视频生成API，提交一个视频生成任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有视频生成参数
    payload = json.dumps({
        # 基础参数
        "model_name": "kling-v1-6",  # [可选] 模型名称，可选 kling-v1 或 kling-v1-6
        "prompt": "一只可爱的卡通海豚，在海中游泳",  # [必填] 正向文本提示词
        # "negative_prompt": "模糊, 扭曲",  # [可选] 负向文本提示词
        
        # 生成控制参数
        # "cfg_scale": 0.5,  # [可选] 生成视频的自由度，取值范围：[0, 1]
        # "mode": "std",  # [可选] 生成模式：std(标准模式) 或 pro(专家模式)
        # "aspect_ratio": "16:9",  # [可选] 视频比例：16:9, 9:16, 1:1
        # "duration": "5",  # [可选] 视频时长(秒)：5 或 10
        
        # 摄像机控制
        # "camera_control": {
            # "type": "forward_up",  # 预定义运镜类型
            # 如果使用 simple 类型，需要配置以下参数（六选一）
            # "config": {
            #     "horizontal": 0,  # 水平运镜 [-10, 10]
            #     "vertical": 0,    # 垂直运镜 [-10, 10]
            #     "pan": 5,         # 水平摇镜 [-10, 10]
            #     "tilt": 0,        # 垂直摇镜 [-10, 10]
            #     "roll": 0,        # 旋转运镜 [-10, 10]
            #     "zoom": 0         # 变焦 [-10, 10]
            # }
        # },
        
        # 任务控制参数
        # "callback_url": "",  # [可选] 回调地址
        # "external_task_id": ""  # [可选] 自定义任务ID
    })
    
    # 构建请求头，包含认证信息和内容类型
    headers = {
        'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
        'Content-Type': 'application/json'  # 指定请求体格式为JSON
    }
    
    # 发送POST请求，路径为视频生成API端点
    conn.request("POST", "/kling/v1/videos/text2video", payload, headers)
    
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
    # 提交视频生成任务
    print(kling_text_generate_video())