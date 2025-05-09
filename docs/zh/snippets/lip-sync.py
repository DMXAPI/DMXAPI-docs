import http.client
import json

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXX" # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

def kling_lip_sync():
    """调用 Kling AI 的口型同步API，提交一个口型同步任务
    
    返回值:
        task_id: 生成任务的唯一标识符，用于后续查询任务结果
    """
    # 构建API请求体，包含所有图像生成参数
    payload = json.dumps({
    "input": {
        # kling 生成的视频
        "task_id": "Cl6kH2gHPegAAAAABJAWDA", # 任务ID
        "video_id": "aeba40f7-473a-47a3-ab85-02dba121970c", # 视频ID

        # 提交视频url
        # "video_url": "https://dmxapi.cn/video.mp4",

        # 文本生成模式
        "mode": "text2video", 
        "text": "欢迎大家使用 DMXAPI", # 文本内容最大长度120
        "voice_id": "girlfriend_1_speech02", # 音色ID 可见 https://docs.qingque.cn/s/home/eZQDvafJ4vXQkP8T9ZPvmye8S
        "voice_language": "zh", # 音色语种
        "voice_speed": 1.0 # 语速

        # 音频生成模式
        # "mode": "audio2video", # 音频生成模式
        # "audio_type": "file",  # 或 "url"
        # # 使用文件时：
        # "audio_file": "base64_encoded_audio",
        # # 或使用URL时：
        # "audio_url": "https://example.com/audio.mp3"
    }
    })
    
    # 构建请求头，包含认证信息和内容类型
    headers = {
    'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
    'Content-Type': 'application/json'  # 指定请求体格式为JSON
    }
    # 发送POST请求，路径为图像生成API端点
    conn.request("POST", "/kling/v1/videos/lip-sync", payload, headers)
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
    print(kling_lip_sync())
