import http.client
import json
import base64
import time

class KlingImageToVideo:
    def __init__(self, api_token, api_url):
        """初始化 Kling 图像生成视频转换器
        
        参数:
            api_token: API 密钥
            api_url: API 节点地址
        """
        self.api_url = api_url
        self.api_token = api_token
        # 初始化 HTTP 连接
        self.conn = http.client.HTTPSConnection(self.api_url)
        self.endpoint = "/kling/v1/videos/image2video"
        # 设置请求头
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    @staticmethod
    def get_image_base64(image_path):
        """将图片转换为 base64 编码形式
        
        参数:
            image_path: 图片路径
        返回:
            base64 编码后的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def _kling_generate_video(self, model_name, image, prompt, 
                             image_tail=None, negative_prompt="", 
                             cfg_scale=0.5, mode="std", duration="5",
                             camera_control=None, static_mask=None, dynamic_masks=None,
                             callback_url="", external_task_id=""):
        """使用 kling 进行图像转视频
        
        参数:
            model_name: str, 模型版本 kling-v1, kling-v1-5, kling-v1-6
            image: str, 起始图片，base64编码或URL
            prompt: str, 正向提示词
            image_tail: str, 结束图片，base64编码或URL
            negative_prompt: str, 负向提示词
            cfg_scale: float, 生成视频的自由度，取值范围：[0, 1]
            mode: str, 生成模式：std(标准模式) 或 pro(专家模式)
            duration: str, 视频时长(秒)：5 或 10
            camera_control: dict, 摄像机控制参数
            static_mask: str, 静态区域遮罩，base64编码或URL
            dynamic_masks: list, 动态区域遮罩列表
            callback_url: str, 回调地址
            external_task_id: str, 自定义任务ID
        返回:
            task_id: 生成任务的 id
        """
        # 构建请求体，请求的核心参数
        payload = {
            "model_name": model_name,
            "image": image,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "cfg_scale": cfg_scale,
            "mode": mode,
            "duration": duration,
            "callback_url": callback_url
        }
        
        # 如果提供了结束图片
        if image_tail:
            payload["image_tail"] = image_tail
            
        # 如果提供了摄像机控制参数
        if camera_control:
            payload["camera_control"] = camera_control
            
        # 如果提供了静态遮罩
        if static_mask:
            payload["static_mask"] = static_mask
            
        # 如果提供了动态遮罩
        if dynamic_masks:
            payload["dynamic_masks"] = dynamic_masks
            
        # 如果提供了自定义任务ID
        if external_task_id:
            payload["external_task_id"] = external_task_id
            
        # 发送 POST 请求，提交视频生成任务
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
    
    def _query_video_result(self, task_id):
        """使用查询接口获取生成视频结果
        
        参数:
            task_id: 生成任务的 id
        返回:
            video_url: 视频 url，任务未完成时返回 None
            video_id: 视频 id，任务未完成时返回 None
        """
        # 构建查询路径
        query_path = f"/kling/v1/videos/generations/{task_id}"

        # 发送 GET 请求，查询视频生成任务状态
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
    
    def generate_video(self, model_name, image, prompt, 
                      image_tail=None, negative_prompt="", 
                      cfg_scale=0.5, mode="std", duration="5",
                      camera_control=None, static_mask=None, dynamic_masks=None,
                      callback_url="", external_task_id="", timeout=600):
        """实现功能，根据图片生成视频并返回结果
        
        参数:
            model_name: str, 模型版本 kling-v1, kling-v1-5, kling-v1-6
            image: str, 起始图片URL或本地文件路径
            prompt: str, 正向提示词
            image_tail: str, 结束图片URL或本地文件路径
            negative_prompt: str, 负向提示词
            cfg_scale: float, 生成视频的自由度，取值范围：[0, 1]
            mode: str, 生成模式：std(标准模式) 或 pro(专家模式)
            duration: str, 视频时长(秒)：5 或 10
            camera_control: dict, 摄像机控制参数
            static_mask: str, 静态区域遮罩URL或本地文件路径
            dynamic_masks: list, 动态区域遮罩列表
            callback_url: str, 回调地址
            external_task_id: str, 自定义任务ID
            timeout: int, 超时时间（秒）
        返回:
            video_url: 视频URL
            video_id: 视频ID
        """
        # 处理起始图片输入
        if image.startswith(('http://', 'https://', 'ftp://')):
            # 如果是URL，直接使用
            image_data = image
        else:
            # 否则当作本地文件路径处理，转换为base64
            try:
                image_data = KlingImageToVideo.get_image_base64(image)
            except Exception as e:
                raise ValueError(f"无法读取起始图像文件: {str(e)}")
        
        # 处理结束图片输入(如果有)
        image_tail_data = None
        if image_tail:
            if image_tail.startswith(('http://', 'https://', 'ftp://')):
                # 如果是URL，直接使用
                image_tail_data = image_tail
            else:
                # 否则当作本地文件路径处理，转换为base64
                try:
                    image_tail_data = KlingImageToVideo.get_image_base64(image_tail)
                except Exception as e:
                    raise ValueError(f"无法读取结束图像文件: {str(e)}")
        
        # 处理静态遮罩(如果有)
        static_mask_data = None
        if static_mask:
            if static_mask.startswith(('http://', 'https://', 'ftp://')):
                # 如果是URL，直接使用
                static_mask_data = static_mask
            else:
                # 否则当作本地文件路径处理，转换为base64
                try:
                    static_mask_data = KlingImageToVideo.get_image_base64(static_mask)
                except Exception as e:
                    raise ValueError(f"无法读取静态遮罩文件: {str(e)}")
        
        # 处理动态遮罩(如果有)
        if dynamic_masks:
            processed_masks = []
            for mask_item in dynamic_masks:
                processed_item = mask_item.copy()
                
                # 处理遮罩图像
                if mask_item.get('mask'):
                    mask_image = mask_item['mask']
                    if mask_image.startswith(('http://', 'https://', 'ftp://')):
                        # 如果是URL，直接使用
                        processed_item['mask'] = mask_image
                    else:
                        # 否则当作本地文件路径处理，转换为base64
                        try:
                            processed_item['mask'] = KlingImageToVideo.get_image_base64(mask_image)
                        except Exception as e:
                            raise ValueError(f"无法读取动态遮罩文件: {str(e)}")
                
                processed_masks.append(processed_item)
            
            dynamic_masks = processed_masks
        
        # 调用生成视频 API 提交任务
        task_id = self._kling_generate_video(
            model_name, image_data, prompt, 
            image_tail_data, negative_prompt, 
            cfg_scale, mode, duration,
            camera_control, static_mask_data, dynamic_masks,
            callback_url, external_task_id
        )
        
        start_time = time.time()
        
        # 轮询等待生成完成
        while True:
            # 查询任务状态
            video_url, video_id = self._query_video_result(task_id)
            # 如果任务完成，返回结果
            if video_url is not None:
                return video_url, video_id
            # 如果超时，返回 None
            if time.time() - start_time > timeout:
                print(f"请求达到 {timeout} 秒超时")
                return None, None
            # 轮询间隔 3 秒
            time.sleep(3)
            print(f"等待视频生成，{int(time.time() - start_time)} 秒", flush=True)


# 使用示例
if __name__ == "__main__":
    API_URL = "www.dmxapi.cn"  # API 节点地址
    DMX_API_TOKEN = "sk-XXXXXXXXXXXXXX"  # API 密钥
    
    # 创建图像转视频生成器实例
    kling_image_to_video = KlingImageToVideo(api_token=DMX_API_TOKEN, api_url=API_URL)
    
    # 示例摄像机控制
    # camera_control = {
    #     "type": "forward_up",  # 预定义运镜类型 可选 “simple”, “down_back”, “forward_up”, “right_turn_forward”, “left_turn_forward”
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
    video_url, video_id = kling_image_to_video.generate_video(
        model_name="kling-v1-6",  # [必选] 模型版本 kling-v1, kling-v1-5, kling-v1-6
        image="/Users/dmxapi/Desktop/dmx.png",  # [必选] 起始图片，可以是 URL 或 本地文件 路径
        prompt="生成图中的几只动物走路的场景",  # [必选] 正向提示词
        # image_tail="end.jpg",  # 结束图片，可以是 URL 或 本地文件 路径
        # negative_prompt="模糊, 扭曲",  # 负向提示词
        # cfg_scale=0.5,  # 生成视频的自由度，取值范围：[0, 1]
        # mode="std",  # 生成模式：std(标准模式) 或 pro(专家模式)
        # duration="5",  # 视频时长(秒)：5 或 10
        # camera_control=camera_control,  # 摄像机控制参数
        # static_mask="mask.png",  # 静态区域遮罩，可以是URL或本地文件路径
        # dynamic_masks=[{  # 动态区域遮罩列表
        #     "mask": "mask.png",  # 动态区域遮罩，可以是URL或本地文件路径
        #     "trajectories": [
        #         {"x": 100, "y": 100},  # 起始点
        #         {"x": 150, "y": 200},  # 中间点
        #         {"x": 200, "y": 300}   # 结束点
        #     ]
        # }],
        # callback_url="",  # 回调地址
        # external_task_id="",  # 自定义任务ID
        # timeout=600  # 等待超时时间（秒）
    )
    
    print("生成的视频URL:", video_url)
    print("生成的视频ID:", video_id)