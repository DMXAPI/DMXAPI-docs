import http.client
import json
import time

class KlingVideoExtend:
    def __init__(self, api_token, api_url):
        """初始化 Kling 视频延长生成器
        
        参数:
            api_token: API 密钥
            api_url: API 节点地址
        """
        self.api_url = api_url
        self.api_token = api_token
        # 初始化 HTTP 连接
        self.conn = http.client.HTTPSConnection(self.api_url)
        self.endpoint = "/kling/v1/videos/video-extend"
        # 设置请求头
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def _kling_extend_video(self, task_id, video_id, prompt, negative_prompt="", cfg_scale=0.5, callback_url=""):
        """使用 kling 提交视频延长任务
        
        参数: 
            task_id: str, 任务ID
            video_id: str, 要延长的视频ID
            prompt: str, 文本提示词，指导延长方向
            negative_prompt: str, 负向文本提示词
            cfg_scale: float, 提示词参考强度
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
        返回:
            task_id: 生成任务的 id
        """
        # 构建请求体，请求的核心参数
        payload = {
            "task_id": task_id,
            "video_id": video_id,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "cfg_scale": cfg_scale,
            "callback_url": callback_url
        }
        
        # 发送 POST 请求，提交视频延长任务
        self.conn.request("POST", self.endpoint, json.dumps(payload), self.headers)
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
    
    def _query_video_extend_result(self, task_id):
        """使用查询接口获取视频延长结果
        
        参数:
            task_id: 生成任务的 id
        返回:
            video_url: 延长后的视频 url，任务未完成时返回 None
        """
        # 构建查询路径
        query_path = f"{self.endpoint}/{task_id}"

        # 发送 GET 请求，查询视频延长任务状态
        self.conn.request("GET", query_path, None, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        
        # 如果任务状态为成功，则返回视频 url
        if json_data['data']['task_status'] == "succeed":
            video_url = json_data['data']['task_result']['videos'][0]['url']
            video_id = json_data['data']['task_result']['videos'][0]['id']
            return video_url, video_id
        else: 
            return None
    
    def extend_video(self, task_id, video_id, prompt, negative_prompt="", cfg_scale=0.5, callback_url="", timeout=300):
        """实现功能，根据预设的参数延长视频并返回延长后的视频 url
        
        参数:
            task_id: str, 任务ID
            video_id: str, 要延长的视频ID
            prompt: str, 文本提示词，指导延长方向
            negative_prompt: str, 负向文本提示词
            cfg_scale: float, 提示词参考强度
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
            timeout: int, 超时时间（秒）
        返回:
            video_url: 延长后的视频 url
        """
        # 调用视频延长 API 提交任务，返回获取 task_id
        task_id = self._kling_extend_video(task_id, video_id, prompt, negative_prompt, cfg_scale, callback_url)
        
        start_time = time.time()
        
        # 轮询等待生成完成
        while True:
            # 根据 task_id 调用查询 API 查看任务是否完成
            video_url, video_id = self._query_video_extend_result(task_id)
            # 如果任务完成，则返回视频 url
            if video_url is not None:
                return video_url, video_id
            # 如果轮询超时，则返回 None
            if time.time() - start_time > timeout:
                print(f"请求达到 {timeout} 秒超时")
                return None
            # 轮询间隔 1 秒
            time.sleep(1)
            print(f"等待视频延长结果生成，{int(time.time() - start_time)} 秒", flush=True)


# 使用示例
if __name__ == "__main__":
    API_URL = "www.dmxapi.cn"  # API 节点地址
    DMX_API_TOKEN = "sk-XXXXXXXXXXXXXX"  # API 密钥
    
    # 创建视频延长生成器实例
    kling_video_extend = KlingVideoExtend(api_token=DMX_API_TOKEN, api_url=API_URL)
    
    # 延长视频
    video_url, video_id = kling_video_extend.extend_video(
        task_id="CjhDaWgU7GAAAAAAAb1QfA",  # [必选] 任务ID
        video_id="bc17f1e8-6c7b-440c-bd30-e47fb1c82932",  # [必选] 要延长的视频ID
        prompt="继续展示动物的走动，保持相同的风格和氛围",  # [必选] 文本提示词
        # negative_prompt="突然的场景转换, 光线变化, 画面抖动",  # 负向提示词
        # cfg_scale=0.5,  # 提示词参考强度，设置较高以保持连贯性
        # callback_url="",  # 回调地址
        # timeout=300  # 等待超时时间，视频处理通常需要更长时间
    )
    
    print(video_url)
    print(video_id)