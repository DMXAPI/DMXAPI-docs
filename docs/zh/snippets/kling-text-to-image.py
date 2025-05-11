import http.client
import json
import time

class KlingTextToImage:
    def __init__(self, api_token, api_url):
        """初始化 Kling 图像生成器
        
        参数:
            api_token: API 密钥
            api_url: API 节点地址
        """
        self.api_url = api_url
        self.api_token = api_token
        # 初始化 HTTP 连接
        self.conn = http.client.HTTPSConnection(self.api_url)
        # 设置请求头
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def _kling_generate_image(self, model_name, prompt, negative_prompt, output_format, n, aspect_ratio, callback_url):
        """使用 kling 生成图像
        
        参数: 
            model_name: str, 模型名称 可选择 kling-v1-5 或 kling-v1
            prompt: str, 文本提示词
            negative_prompt: str, 负向文本提示词
            output_format: str, 输出格式：png 或 jpg
            n: int, 生成数量 [1, 9]
            aspect_ratio: str, 输出比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
        返回参数:
            task_id: 生成任务的 id
        """
        # 构建请求体，请求的核心参数
        payload = json.dumps({
        "model_name": model_name,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "output_format": output_format,
        "n": n,
        "aspect_ratio": aspect_ratio,
        "callback_url": callback_url,
        })
        
        # 发送 POST 请求，提交图像生成任务
        self.conn.request("POST", "/kling/v1/images/generations?=null", payload, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        # print(json_data)
        # 从 json 文件中返回任务 ID
        return json_data['data']['task_id']
    
    def _query_kling_image_url(self, task_id):
        """使用查询接口获取生成图像 url
        
        输入参数:
            task_id: 生成任务的 id
        输出参数:
            image_url: 图像 url
        """
        # 构建查询路径
        action = "images"
        action2 = "generations"

        query_path = f"/kling/v1/{action}/{action2}/{task_id}"

        # 发送 GET 请求，查询图像生成任务状态
        self.conn.request("GET", query_path, None, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        # 如果任务状态为成功，则返回图像 url
        if json_data['data']['task_status'] == "succeed":
            image_urls = [image['url'] for image in json_data['data']['task_result']['images']]
            return image_urls
        else: 
            return None
    
    def generate_image(self, model_name, prompt, negative_prompt="", output_format="png", n=1, aspect_ratio="16:9", callback_url="", timeout=60):
        """实现功能，直接根据预设的参数返回生成图像的 url
        
        参数:
            model_name: str, 模型名称 可选择 kling-v1-5 或 kling-v1
            prompt: str, 文本提示词
            negative_prompt: str, 负向文本提示词
            output_format: str, 输出格式：png 或 jpg
            n: int, 生成数量 [1, 9]
            aspect_ratio: str, 输出比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
        返回参数:
            image_url: 图像 url
        """
        # 调用生成图像 api 提交图像生成任务，返回获取 task_id。
        task_id = self._kling_generate_image(model_name, prompt, negative_prompt, output_format, n, aspect_ratio, callback_url) 
        start_time = time.time()
        # 轮询等待生成完成
        while True:
            # 根据 task_id 调用查询图像api 查看图像生成任务是否完成。
            image_url = self._query_kling_image_url(task_id) 
            # 如果图像生成任务完成，则返回图像 url
            if image_url is not None:
                return image_url
            # 如果轮询超时，则返回 None
            if time.time() - start_time > timeout:
                print(f"请求达到 {timeout} 秒超时")
                return None
            # 轮询间隔 1 秒
            time.sleep(1)
            print(f"等待图像生成，{int(time.time() - start_time)} 秒", flush=True)


# 使用示例
if __name__ == "__main__":
    API_URL="www.dmxapi.cn" # API 节点地址
    DMX_API_TOKEN = "sk-XXXXXXXXXXXXXX"  # API 密钥
    
    # 创建图像生成器实例
    kling_text_to_image = KlingTextToImage(api_token=DMX_API_TOKEN, api_url=API_URL)
    
    # 生成图像
    image_url = kling_text_to_image.generate_image(
        model_name="kling-v1-5", # [必选]模型名称 可选择 kling-v1-5 或 kling-v1
        prompt="生成一张袋鼠的照片，手里拿着一个写着'DMXAPI'的牌子", # [必选]文本提示词
        # negative_prompt="", # 负向文本提示词
        # output_format="png", # 输出格式：png 或 jpg
        # n=1, # int, 生成数量 [1, 9]
        # aspect_ratio="16:9", # 输出比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
        # callback_url="", # 回调地址，可以用于 webhook 等通知场景
        # timeout=120 # 队列等待超时时间
    )
    
    print(image_url)