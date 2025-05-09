import http.client
import json
import base64

# 配置全局变量
API_URL = "www.dmxapi.cn"  # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXX"  # API 密钥

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

def kling_video_effects_single():
    """调用 Kling AI 的视频特效API，提交一个视频特效任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有视频生成参数
    payload = json.dumps({
        "effect_scene": "expansion",  # 场景名称：bloombloom, dizzydizzy, fuzzyfuzzy, squish, expansion
        "input": {
            "model_name": "kling-v1-6",  # 模型名称
            "image": "https://p2-kling.klingai.com/bs2/upload-ylab-stunt/c54e463c95816d959602f1f2541c62b2.png?x-kcdn-pid=112452",  # 图片输入 base64 形式 get_image_base64("input.jpg") 或者图片 url，这里展示 url
            "duration": "5"  # 视频时长(秒)
        },
        
        # "callback_url": "https://your-server.com/webhook",  # 回调通知地址
        # "external_task_id": "custom_effect_001"  # 自定义任务ID
    })
    
    # 构建请求头，包含认证信息和内容类型
    headers = {
        'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
        'Content-Type': 'application/json'  # 指定请求体格式为JSON
    }
    
    # 发送POST请求，路径为视频生成API端点
    conn.request("POST", "/kling/v1/videos/effects", payload, headers)
    
    # 获取API响应并解析JSON数据
    res = conn.getresponse()
    json_data = json.loads(res.read().decode("utf-8"))
    print(json_data)
    
    # if json_data['code'] == 0:
    #     # 成功则返回提交的任务 id
    #     return json_data['data']['task_id']
    # else:
    #     # 失败则返回错误信息
    #     return json_data['message']

if __name__ == "__main__":
    # 提交视频特效任务
    print(kling_video_effects_single())