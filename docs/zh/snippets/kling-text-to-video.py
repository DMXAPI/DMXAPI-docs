import http.client
import json
import time

class KlingTextToVideo:
    def __init__(self, api_token, api_url):
        """初始化 Kling 视频生成器
        
        参数:
            api_token: API 密钥
            api_url: API 节点地址
        """
        self.api_url = api_url
        self.api_token = api_token
        # 初始化 HTTP 连接
        self.conn = http.client.HTTPSConnection(self.api_url)
        self.endpoint = "/kling/v1/videos/text2video"
        # 设置请求头
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def _kling_generate_video(self, model_name, prompt, negative_prompt="", cfg_scale=0.5, 
                             mode="std", aspect_ratio="16:9", duration="5", 
                             camera_control=None, callback_url="", external_task_id=""):
        """使用 kling 生成视频
        
        参数: 
            model_name: str, 模型名称 可选择 kling-v1-6 或 kling-v1
            prompt: str, 文本提示词
            negative_prompt: str, 负向文本提示词
            cfg_scale: float, 生成视频的自由度，取值范围：[0, 1]
            mode: str, 生成模式：std(标准模式) 或 pro(专家模式)
            aspect_ratio: str, 视频比例：16:9, 9:16, 1:1
            duration: str, 视频时长(秒)：5 或 10
            camera_control: dict, 摄像机控制参数
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
            external_task_id: str, 自定义任务ID
        返回参数:
            task_id: 生成任务的 id
        """
        # 构建请求体，请求的核心参数
        payload_dict = {
            "model_name": model_name,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "cfg_scale": cfg_scale,
            "mode": mode,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "callback_url": callback_url,
            "external_task_id": external_task_id
        }
        
        # 如果提供了摄像机控制参数，添加到请求体中
        if camera_control:
            payload_dict["camera_control"] = camera_control
            
        payload = json.dumps(payload_dict)
        
        # 发送 POST 请求，提交视频生成任务
        self.conn.request("POST", self.endpoint, payload, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        # print(json_data)
        # 检查响应是否成功
        if 'code' in json_data and json_data['code'] == 0:
            # 成功则返回提交的任务 id
            return json_data['data']['task_id']
        else:
            # 失败则返回错误信息
            raise Exception(f"API调用失败：{json_data['message']}")
    
    def _query_kling_video_url(self, task_id):
        """使用查询接口获取生成视频 url
        
        输入参数:
            task_id: 生成任务的 id
        输出参数:
            video_url: 视频 url
        """
        # 构建查询路径
        query_path = f"{self.endpoint}/{task_id}"

        # 发送 GET 请求，查询视频生成任务状态
        self.conn.request("GET", query_path, None, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))

        # 检查响应是否成功
        if json_data['code'] == 0:
            # 如果任务状态为成功，则返回视频 url
            if json_data['data']['task_status'] == "succeed":
                video_url = json_data['data']['task_result']['videos'][0]['url']
                video_id = json_data['data']['task_result']['videos'][0]['id']
                return video_url, video_id
            else:
                return None
        else:
            # 如果查询失败，抛出异常
            raise Exception(f"视频状态查询失败: {json_data['message']}")
    
    def generate_video(self, model_name, prompt, negative_prompt="", cfg_scale=0.5, 
                      mode="std", aspect_ratio="16:9", duration="5", 
                      camera_control=None, callback_url="", external_task_id="", timeout=600):
        """实现功能，直接根据预设的参数返回生成视频的 url
        
        参数:
            model_name: str, 模型名称 可选择 kling-v1-6 或 kling-v1
            prompt: str, 文本提示词
            negative_prompt: str, 负向文本提示词
            cfg_scale: float, 生成视频的自由度，取值范围：[0, 1]
            mode: str, 生成模式：std(标准模式) 或 pro(专家模式)
            aspect_ratio: str, 视频比例：16:9, 9:16, 1:1
            duration: str, 视频时长(秒)：5 或 10
            camera_control: dict, 摄像机控制参数
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
            external_task_id: str, 自定义任务ID
            timeout: int, 超时时间（秒）
        返回参数:
            video_url: 视频 url
        """
        # 调用生成视频 api 提交视频生成任务，返回获取 task_id
        task_id = self._kling_generate_video(
            model_name, prompt, negative_prompt, cfg_scale, 
            mode, aspect_ratio, duration, camera_control, 
            callback_url, external_task_id
        )
        
        start_time = time.time()
        # 轮询等待生成完成
        while True:
            # 根据 task_id 调用查询视频 api 查看视频生成任务是否完成
            video_url, video_id = self._query_kling_video_url(task_id)
            # 如果视频生成任务完成，则返回视频 url
            if video_url is not None:
                return video_url, video_id
            # 如果轮询超时，则返回 None
            if time.time() - start_time > timeout:
                print(f"请求达到 {timeout} 秒超时")
                return None
            # 轮询间隔 3 秒（视频生成通常需要更长时间）
            time.sleep(3)
            print(f"等待视频生成，{int(time.time() - start_time)} 秒", flush=True)


# 使用示例
if __name__ == "__main__":
    API_URL = "www.dmxapi.cn"  # API 节点地址
    DMX_API_TOKEN = "sk-XXXXXXXXXXXXX"  # API 密钥
    
    # 创建视频生成器实例
    kling_text_to_video = KlingTextToVideo(api_token=DMX_API_TOKEN, api_url=API_URL)
    
    # 示例摄像机控制
    # camera_control = {
    #     "type": "down_back",  # 预定义运镜类型 可选 “simple”, “down_back”, “forward_up”, “right_turn_forward”, “left_turn_forward”
    #     # 如果使用 simple 类型，需要配置以下参数（六选一）
    #     # "config": {
    #     #     "horizontal": 0,  # 水平运镜 [-10, 10]
    #     #     "vertical": 0,    # 垂直运镜 [-10, 10]
    #     #     "pan": 5,         # 水平摇镜 [-10, 10]
    #     #     "tilt": 0,        # 垂直摇镜 [-10, 10]
    #     #     "roll": 0,        # 旋转运镜 [-10, 10]
    #     #     "zoom": 0         # 变焦 [-10, 10]
    #     # }
    # }
    
    # 生成视频
    video_url, video_id = kling_text_to_video.generate_video(
        model_name="kling-v1",  # [必选]模型名称 可选择 kling-v1-6 或 kling-v1
        prompt="一只可爱的卡通袋鼠，举起了一个写着 DMXAPI 的牌子",  # [必选]文本提示词
        # negative_prompt="模糊, 扭曲",  # 负向文本提示词
        # cfg_scale=0.5,  # 生成视频的自由度 可选 [0,1]
        # mode="std",  # 生成模式 可选 std(标准模式) 或 pro(专家模式)
        # aspect_ratio="16:9",  # 视频比例 可选 16:9, 9:16, 1:1
        # duration="5",  # 视频时长(秒) 可选 5 或 10
        # camera_control=camera_control,  # 摄像机控制 配置见上
        # callback_url="",  # 回调地址
        # external_task_id="",  # 自定义任务ID
        # timeout=600  # 轮询等待超时时间（秒）
    )
    
    print(video_url)
    print(video_id)
