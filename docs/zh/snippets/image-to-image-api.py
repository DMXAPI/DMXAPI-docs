import http.client
import json
import base64

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXX" # API 密钥

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

def kling_generate_image():
    """调用 Kling AI 的图像生成API，提交一个图像生成任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有图像生成参数
    payload = json.dumps({
    "model_name": "kling-v1-5", # [必选]模型名称 可选择 kling-v1-5 或 kling-v1 或 kling-v2
    "prompt": "请生成这张照片的梵高风格", # [必选]文本提示词
    "image": get_image_base64("/Users/dmxapi/Desktop/dmx.png"), # [必选]参考图片，直接填 url 或者 base64 编码的形式
    "image_reference": "subject", # [必选，仅支持 kling-v1-5 模型]参考图片类型，可选值：subject（角色特征参考）, face（人物长相参考）
    # "image_fidelity": 0.5, # 参考图片强度，取值范围：[0,1]，数值越大参考强度越大
    # "human_fidelity": 0.5, # 面部参考强度，取值范围：[0,1]，数值越大参考强度越大
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
