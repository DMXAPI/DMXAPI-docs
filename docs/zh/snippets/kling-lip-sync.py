import http.client
import json
import time
import base64

class KlingLipSync:
    def __init__(self, api_token, api_url):
        """初始化 Kling 口型同步生成器
        
        参数:
            api_token: API 密钥
            api_url: API 节点地址
        """
        self.api_url = api_url
        self.api_token = api_token
        # 初始化 HTTP 连接
        self.conn = http.client.HTTPSConnection(self.api_url)
        self.endpoint = "/kling/v1/videos/lip-sync"
        # 设置请求头
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    @staticmethod
    def get_audio_base64(audio_path):
        """将音频转换为 base64 编码形式
        
        参数:
            audio_path: 音频文件路径
        返回:
            base64 编码后的音频字符串
        """
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")

    def _kling_lip_sync(self, input_data):
        """提交口型同步任务
        
        参数: 
            input_data: dict, 包含所有口型同步所需的输入参数
        返回:
            task_id: 生成任务的 id
        """
        # 构建请求体
        payload = json.dumps({
            "input": input_data
        })
        
        # 发送 POST 请求，提交口型同步任务
        self.conn.request("POST", self.endpoint, payload, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        
        if 'code' in json_data and json_data['code'] == 0:
            # 成功则返回提交的任务 id
            return json_data['data']['task_id']
        else:
            # 失败则返回错误信息
            raise Exception(f"API调用失败：{json_data['message']}")
    
    def _query_lip_sync_result(self, task_id):
        """使用查询接口获取口型同步结果
        
        参数:
            task_id: 生成任务的 id
        返回:
            video_url: 结果视频 url，任务未完成时返回 None
            video_id: 结果视频 id，任务未完成时返回 None
        """
        # 构建查询路径
        query_path = f"{self.endpoint}/{task_id}"

        # 发送 GET 请求，查询任务状态
        self.conn.request("GET", query_path, None, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        
        # 检查响应是否成功
        if json_data['code'] == 0:
            # 如果任务状态为成功，则返回视频 url 和 id
            if json_data['data']['task_status'] == "succeed":
                video_url = json_data['data']['task_result']['videos'][0]['url']
                video_id = json_data['data']['task_result']['videos'][0]['id']
                return video_url, video_id
            else:
                return None, None
        else:
            # 如果查询失败，抛出异常
            raise Exception(f"查询失败: {json_data['message']}")
    
    def generate_text2video_lip_sync(self, video_source=None, video_id=None, task_id=None,
                                    text="", voice_id="", voice_language="zh", voice_speed=1.0,
                                    callback_url="", timeout=300):
        """文本转口型同步视频
        
        参数:
            video_source: str, 视频来源，可以是URL或任务ID (与task_id+video_id二选一)
            video_id: str, 现有视频的视频ID (与task_id一起使用)
            task_id: str, 现有视频的任务ID (与video_id一起使用)
            text: str, 要同步的文本内容
            voice_id: str, 音色ID
            voice_language: str, 音色语种，默认"zh"
            voice_speed: float, 语速，默认1.0
            callback_url: str, 回调地址
            timeout: int, 超时时间（秒）
        返回:
            video_url: 结果视频URL
            video_id: 结果视频ID
        """
        # 准备输入参数
        input_data = {
            "mode": "text2video",
            "text": text,
            "voice_id": voice_id,
            "voice_language": voice_language,
            "voice_speed": voice_speed
        }
        
        # 设置视频来源 - 自动识别和处理
        if video_source:
            if video_source.startswith(('http://', 'https://', 'ftp://')):
                # 如果是URL格式，作为视频URL处理
                input_data["video_url"] = video_source
            else:
                # 否则作为任务ID处理
                if not video_id:
                    raise ValueError("当提供任务ID时，必须同时提供视频ID")
                input_data["task_id"] = video_source
                input_data["video_id"] = video_id
        elif task_id and video_id:
            # 如果单独提供task_id和video_id，使用它们
            input_data["task_id"] = task_id
            input_data["video_id"] = video_id
        else:
            raise ValueError("必须提供视频来源(URL或任务ID)和视频ID")
        
        # 如果提供了回调地址，添加到请求中
        if callback_url:
            input_data["callback_url"] = callback_url
        
        # 调用 API 提交任务
        task_id = self._kling_lip_sync(input_data)
        
        start_time = time.time()
        
        # 轮询等待生成完成
        while True:
            # 查询任务状态
            video_url, video_id = self._query_lip_sync_result(task_id)
            # 如果任务完成，返回结果
            if video_url is not None:
                return video_url, video_id
            # 如果超时，返回 None
            if time.time() - start_time > timeout:
                print(f"请求达到 {timeout} 秒超时")
                return None, None
            # 轮询间隔 2 秒
            time.sleep(2)
            print(f"等待口型同步结果生成，{int(time.time() - start_time)} 秒", flush=True)
    
    def generate_audio2video_lip_sync(self, video_source=None, video_id=None, task_id=None,
                                     audio_source=None, callback_url="", timeout=300):
        """音频转口型同步视频
        
        参数:
            video_source: str, 视频来源，可以是URL或任务ID (与task_id+video_id二选一)
            video_id: str, 现有视频的视频ID (与task_id一起使用)
            task_id: str, 现有视频的任务ID (与video_id一起使用)
            audio_source: str, 音频来源，可以是URL或本地文件路径
            callback_url: str, 回调地址
            timeout: int, 超时时间（秒）
        返回:
            video_url: 结果视频URL
            video_id: 结果视频ID
        """
        # 准备输入参数
        input_data = {
            "mode": "audio2video"
        }
        
        # 设置视频来源 - 自动识别和处理
        if video_source:
            if video_source.startswith(('http://', 'https://', 'ftp://')):
                # 如果是URL格式，作为视频URL处理
                input_data["video_url"] = video_source
            else:
                # 否则作为任务ID处理
                if not video_id:
                    raise ValueError("当提供任务ID时，必须同时提供视频ID")
                input_data["task_id"] = video_source
                input_data["video_id"] = video_id
        elif task_id and video_id:
            # 如果单独提供task_id和video_id，使用它们
            input_data["task_id"] = task_id
            input_data["video_id"] = video_id
        else:
            raise ValueError("必须提供视频来源(URL或任务ID)和视频ID")
        
        # 设置音频来源 - 自动识别和处理
        if not audio_source:
            raise ValueError("必须提供音频来源(URL或本地文件路径)")
        
        if audio_source.startswith(('http://', 'https://', 'ftp://')):
            # 如果是URL格式，作为音频URL处理
            input_data["audio_type"] = "url"
            input_data["audio_url"] = audio_source
        else:
            # 否则作为本地文件路径处理
            try:
                input_data["audio_type"] = "file"
                input_data["audio_file"] = self.get_audio_base64(audio_source)
            except Exception as e:
                raise ValueError(f"无法读取音频文件: {str(e)}")
            
        # 如果提供了回调地址，添加到请求中
        if callback_url:
            input_data["callback_url"] = callback_url
        
        # 调用 API 提交任务
        task_id = self._kling_lip_sync(input_data)
        
        start_time = time.time()
        
        # 轮询等待生成完成
        while True:
            # 查询任务状态
            video_url, video_id = self._query_lip_sync_result(task_id)
            # 如果任务完成，返回结果
            if video_url is not None:
                return video_url, video_id
            # 如果超时，返回 None
            if time.time() - start_time > timeout:
                print(f"请求达到 {timeout} 秒超时")
                return None, None
            # 轮询间隔 2 秒
            time.sleep(2)
            print(f"等待口型同步结果生成，{int(time.time() - start_time)} 秒", flush=True)


# 使用示例
if __name__ == "__main__":
    API_URL = "www.dmxapi.cn"  # API 节点地址
    DMX_API_TOKEN = "sk-XXXXXXXXXXXXXX"  # API 密钥
    
    # 创建口型同步生成器实例
    kling_lip_sync = KlingLipSync(api_token=DMX_API_TOKEN, api_url=API_URL)
    
    # 示例1：文本转口型同步视频 - 使用任务ID和视频ID
    video_url, video_id = kling_lip_sync.generate_text2video_lip_sync(
        video_source="Cl6kH2gHPegAAAAABJAWDA",  # [必选] 视频来源(任务ID)
        video_id="aeba40f7-473a-47a3-ab85-02dba121970c",  # [必选] 视频ID
        text="欢迎大家使用 DMXAPI",  # [必选] 文本内容
        voice_id="girlfriend_1_speech02",  # [必选] 音色ID
        # voice_language="zh",  # 音色语种，默认"zh"
        # voice_speed=1.0,  # 语速，默认1.0
        # callback_url="",  # 回调地址
        # timeout=300  # 超时时间（秒）
    )
    
    print("文本生成的口型同步视频URL:", video_url)
    print("文本生成的口型同步视频ID:", video_id)
    
    # 示例2：文本转口型同步视频 - 使用视频URL
    # video_url, video_id = kling_lip_sync.generate_text2video_lip_sync(
    #     video_source="https://dmxapi.cn/video.mp4",  # [必选] 视频来源(URL)
    #     text="欢迎大家使用 DMXAPI",  # [必选] 文本内容
    #     voice_id="girlfriend_1_speech02",  # [必选] 音色ID
    # )
    
    # 示例3：音频转口型同步视频 - 使用URL
    # video_url, video_id = kling_lip_sync.generate_audio2video_lip_sync(
    #     video_source="https://dmxapi.cn/video.mp4",  # [必选] 视频来源(URL)
    #     audio_source="https://example.com/audio.mp3",  # [必选] 音频来源(URL)
    # )
    
    # 示例4：音频转口型同步视频 - 使用本地文件
    # video_url, video_id = kling_lip_sync.generate_audio2video_lip_sync(
    #     task_id="Cl6kH2gHPegAAAAABJAWDA",  # [必选] 任务ID
    #     video_id="aeba40f7-473a-47a3-ab85-02dba121970c",  # [必选] 视频ID
    #     audio_source="/path/to/local/audio.mp3",  # [必选] 音频来源(本地文件)
    # )