import http.client
import json

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXX" # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

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

    # 根据请求接口，构建完整的查询路径，包含task_id参数
    query_path = f"/kling/v1/{action}/{action2}/{task_id}"
    # 构建请求头，包含鉴权消息
    headers = {
    'Authorization': f'Bearer {DMX_API_TOKEN}'
    }
    # 发送GET请求查询任务状态
    conn.request("GET", query_path, None, headers)
    # 获取响应并解析JSON数据
    res = conn.getresponse()
    json_data = json.loads(res.read().decode("utf-8"))
    # print(json_data)
    # 检查任务状态，如果成功则返回第一张图像的URL，否则返回None
    if json_data['data']['task_status'] == "succeed":
        return json_data['data']['task_result']['images'][0]['url']
    else: 
        return None

# 使用示例
if __name__ == "__main__":
    task_id = "Cl58rmgHRLsAAAAABFV6lg"  # 替换为你的实际任务ID
    print(query_kling_image_url(task_id))
