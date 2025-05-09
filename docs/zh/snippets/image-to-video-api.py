import http.client
import json
import base64

# 配置全局变量
API_URL = "www.dmxapi.cn"  # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXX"  # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

# 将图片转换为 base64 编码形式
def get_image_base64(image_path):
    """将图片转换为 base64 编码形式
    输入参数:
        image_path: 图片路径
    返回参数:
        base64 编码后的图片字符串
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def kling_image_generate_video():
    """调用 Kling AI 的视频生成API，提交一个视频生成任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有视频生成参数
    payload = json.dumps({
        # 基础参数
        "model_name": "kling-v1-6",  # 模型版本 kling-v1, kling-v1-5, kling-v1-6
        "image": get_image_base64("/Users/dmxapi/Desktop/dmx.png"),  # 起始图片
        # "image_tail": get_image_base64("end.jpg"),  # 结束图片
        "prompt": "生成图中的几只动物走路的场景",  # 正向提示词
        # "negative_prompt": "模糊, 扭曲",  # 负向提示词
        
        # 生成控制参数
        # "cfg_scale": 0.5,  # [可选] 生成视频的自由度，取值范围：[0, 1]
        # "mode": "std",  # [可选] 生成模式：std(标准模式) 或 pro(专家模式)
        # "duration": "5",  # [可选] 视频时长(秒)：5 或 10
        
        # 摄像机运动控制
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
        
        # # 静态笔刷示例
        # "static_mask": get_image_base64("mask.png"),  # 静态区域遮罩
        
        # # 动态笔刷示例
        # "dynamic_masks": [{
        #     "mask": get_image_base64("mask.png"),  # 动态区域遮罩
        #     "trajectories": [
        #         {"x": 100, "y": 100},  # 起始点
        #         {"x": 150, "y": 200},  # 中间点
        #         {"x": 200, "y": 300}   # 结束点
        #     ]
        # }],
        
        # # 任务控制
        # "callback_url": "https://your-server.com/webhook",  # 回调地址
        # "external_task_id": "custom_task_001"  # 自定义任务ID
    })
    
    # 构建请求头，包含认证信息和内容类型
    headers = {
        'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
        'Content-Type': 'application/json'  # 指定请求体格式为JSON
    }
    
    # 发送POST请求，路径为视频生成API端点
    conn.request("POST", "/kling/v1/videos/image2video", payload, headers)
    
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
    print(kling_image_generate_video())