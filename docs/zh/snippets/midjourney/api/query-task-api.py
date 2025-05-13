import http.client
import json

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXX" # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

def query_midjourney_task_api(task_id):
    # 设置 Request headers
    headers = {
        'Authorization': f'Bearer {DMX_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    # 根据请求接口，构建完整的查询路径，包含task_id参数
    query_path = f"/mj/task/{task_id}/fetch"

    try:
        # request 请求规范：方法, URL, body, headers
        conn.request("GET", query_path, None, headers)
        # 获取响应并解析JSON数据
        res = conn.getresponse()
        json_data = json.loads(res.read().decode("utf-8"))
        return json_data

    except Exception as e:
        print(f"query midjourney task api error: {e}")

if __name__ == "__main__":
    task_id = "1747132423020537"  # 替换为你的实际任务ID
    print(query_midjourney_task_api(task_id))
