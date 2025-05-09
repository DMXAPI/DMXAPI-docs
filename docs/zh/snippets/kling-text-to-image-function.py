import http.client
import json
import time

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXX" # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

def kling_generate_image():
    """调用 Kling AI 的图像生成API，提交一个图像生成任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有图像生成参数
    payload = json.dumps({
    "model_name": "kling-v1-5", # [必选]模型名称 可选择 kling-v1-5 或 kling-v1
    "prompt": "生成一张袋鼠的照片，手里拿着一个写着'DMXAPI'的牌子", # [必选]文本提示词
    # "negative_prompt": "", # 负向文本提示词
    # "output_format": "png", # 输出格式：png 或 jpg
    # "n": 1, # int, 生成数量 [1, 9]
    # "aspect_ratio": "16:9", # 输出比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
    # "callback_url": "url", # 回调地址，可以用于 webhook 等通知场景
    })
    
    # 构建请求头，包含认证信息和内容类型
    headers = {
    'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
    'Content-Type': 'application/json'  # 指定请求体格式为JSON
    }
    # 发送POST请求，路径为图像生成API端点
    conn.request("POST", "/kling/v1/images/generations?=null", payload, headers)
    # 获取API响应并解析JSON数据
    res = conn.getresponse()
    json_data = json.loads(res.read().decode("utf-8"))
    print(json_data)
    return json_data['data']['task_id']

def query_kling_image_url(task_id):
    """查询已提交的图像生成任务的状态和结果
    
    参数:
        task_id: 图像生成任务的唯一标识符，由kling_generate_image()函数返回
        
    返回值:
        成功时: 返回生成图像的URL地址
        任务未完成或失败: 返回None
    """
    action = "images"
    action2 = "generations"

    # 构建完整的查询路径，包含task_id参数
    query_path = f"/kling/v1/{action}/{action2}/{task_id}"
    # 构建请求头，仅包含认证信息
    headers = {
    'Authorization': f'Bearer {DMX_API_TOKEN}'
    }
    # 发送GET请求查询任务状态
    conn.request("GET", query_path, None, headers)
    # 获取响应并解析JSON数据
    res = conn.getresponse()
    json_data = json.loads(res.read().decode("utf-8"))
    # 检查任务状态，如果成功则返回第一张图像的URL，否则返回None
    if json_data['data']['task_status'] == "succeed":
        return json_data['data']['task_result']['images'][0]['url']
    else: 
        return None

def generate_image():
    """完整的图像生成流程，包括提交任务和轮询等待结果

    返回值:
        成功时: 返回生成图像的URL
        失败或超时: 返回None
    """
    # 调用生成图像API提交任务，获取task_id
    task_id = kling_generate_image() 
    # 记录开始时间，用于计算等待时长和判断超时
    start_time = time.time()
    timeout = 60  # 设置最大等待时间为60秒
    
    # 循环查询任务状态，直到成功或超时
    while True:
        # 调用查询API检查任务状态
        image_url = query_kling_image_url(task_id) 
        # 如果获取到URL，说明任务成功完成，返回URL
        if image_url is not None:
            return image_url
        # 检查是否超时
        if time.time() - start_time > timeout:
            print(f"请求达到 {timeout} 秒超时")
            return None
        # 等待1秒后再次查询，避免过于频繁的API调用
        time.sleep(1)
        # 打印等待时间，flush=True确保实时输出
        print(f"等待图像生成，{int(time.time() - start_time)} 秒", flush=True)

if __name__ == "__main__":
    print(generate_image())