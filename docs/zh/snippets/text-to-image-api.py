import http.client
import json

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXX" # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

def kling_generate_image():
    """调用 Kling AI 的图像生成API，提交一个图像生成任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有图像生成参数
    payload = json.dumps({
    "model_name": "kling-v1-5", # [必选]模型名称 可选择 kling-v1-5 或 kling-v1 或 kling-v2
    "prompt": "生成一张袋鼠的照片，手里拿着一个写着'DMXAPI'的牌子", # [必选]文本提示词
    # "negative_prompt": "", # 负向文本提示词
    # "output_format": "png", # 输出格式：png 或 jpg
    # "n": 1, # int, 生成数量 [1, 9]
    # "aspect_ratio": "16:9", # 输出图像比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
    # "callback_url": "url", # 回调地址，可以用于 webhook 等通知场景
    })
    
    # 构建请求头，包含认证信息和内容类型
    headers = {
    'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
    'Content-Type': 'application/json'  # 指定请求体格式为JSON
    }
    # 发送POST请求，路径为图像生成API端点
    conn.request("POST", "/kling/v1/images/generations", payload, headers)
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
    print(kling_generate_image())
