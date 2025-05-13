import http.client
import json
import requests
import base64

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXX" # API 密钥

# 获取图片的base64编码
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 从URL获取图片并转换为base64格式
def url_image_to_base64(image_url):
    """
    从URL获取图片并转换为base64格式
    
    参数:
        image_url (str): 图片的URL地址
        
    返回:
        str: base64编码的图片字符串
    """
    try:
        # 发送GET请求获取图片
        response = requests.get(image_url)
        
        # 将图片内容编码为base64
        image_binary = response.content
        base64_encoded = base64.b64encode(image_binary).decode('utf-8')
        
        return base64_encoded
    
    except Exception as e:
        print(f"获取图片失败: {str(e)}")
        return None

# 提交图生图任务
def midjourney_generate_image(image_path):

    # 获取图片的base64编码
    if image_path.startswith('https://') or image_path.startswith('http://'):
        base64_string = url_image_to_base64(image_path)
    else:
        base64_string = get_image_base64(image_path)

    conn = http.client.HTTPSConnection(API_URL)
    payload = json.dumps({
       "mode": "RELAX", # 模式 可选值："Turbo"、"Fast"（默认）、"Relax"
       "botType": "NIJI_JOURNEY", # 模型类型，可选值 "MID_JOURNEY"（默认） 或者 "NIJI_JOURNEY"
       "prompt": "这是一个视频截图，请生成对应的吉卜力风格的图片", # 提示词，描述希望生成的图片内容
       "base64Array": [
          "data:image/png;base64," + base64_string # 包含图片 base64 数据的数组，格式为 "data:image/png;base64,<base64字符串>"
       ],
       "notifyHook": "string" # 回调通知的 URL，处理完成后会向该地址发送回调
    })

    # 设置请求头，包含认证信息和内容类型
    headers = {
       'Authorization': f'Bearer {DMX_API_TOKEN}',
       'Content-Type': 'application/json'
    }
    # 发送POST请求到/mj/submit/imagine接口
    conn.request("POST", "/mj/submit/imagine", payload, headers)
    # 获取响应
    res = conn.getresponse()
    data_json = json.loads(res.read().decode("utf-8"))
    # print(data_json)
    print(data_json["description"])
    task_id = data_json["result"]
    return task_id

if __name__ == "__main__":
    # image_path = "/Users/dmxapi/Desktop/dxmapi.jpg" # 本地图片方式生成
    image_url = "https://cdn.klingai.com/bs2/upload-kling-api/8089468206/image/Cl6kH2gHPegAAAAABUwweg-0_raw_image_0.png" # url 图片方式生成
    print(midjourney_generate_image(image_url))