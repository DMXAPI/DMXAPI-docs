import http.client
import json
import base64
import time

class KlingImageToImage:
    def __init__(self, api_token, api_url):
        """初始化 Kling 图生图转换器
        
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
    
    def _kling_generate_image(self, model_name, prompt, image, image_reference, 
                             image_fidelity=0.5, human_fidelity=0.5, 
                             output_format="png", n=1, aspect_ratio="16:9", callback_url=""):
        """使用 kling 进行图生图
        
        参数:
            model_name: str, 模型名称，可选择 kling-v1-5 或 kling-v1
            prompt: str, 文本提示词
            image: str, 参考图片，base64编码或URL
            image_reference: str, 参考图片类型，可选值：subject（角色特征参考）, face（人物长相参考）
            image_fidelity: float, 参考图片强度，取值范围：[0,1]，数值越大参考强度越大
            human_fidelity: float, 面部参考强度，取值范围：[0,1]，数值越大参考强度越大
            output_format: str, 输出格式：png 或 jpg
            n: int, 生成数量 [1, 9]
            aspect_ratio: str, 输出比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
        返回:
            task_id: 生成任务的 id
        """
        # 构建请求体，请求的核心参数
        payload = {
            "model_name": model_name,
            "prompt": prompt,
            "image": image,
            "image_reference": image_reference,
            "image_fidelity": image_fidelity,
            "human_fidelity": human_fidelity,
            "output_format": output_format,
            "n": n,
            "aspect_ratio": aspect_ratio,
            "callback_url": callback_url
        }
            
        # 发送 POST 请求，提交图像生成任务
        self.conn.request("POST", "/kling/v1/images/generations", json.dumps(payload), self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        # print(json_data)
        if 'code' in json_data and json_data['code'] == 0:
            # 成功则返回提交的任务 id
            return json_data['data']['task_id']
        else:
            # 失败则返回错误信息
            raise Exception(f"API调用失败：{json_data['message']}")
    
    def _query_kling_image_url(self, task_id):
        """使用查询接口获取生成图像 url
        
        参数:
            task_id: 生成任务的 id
        返回:
            image_url: 图像 url，任务未完成时返回 None
        """
        # 构建查询路径
        query_path = f"/kling/v1/images/generations/{task_id}"

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
    
    def generate_image(self, model_name, prompt, image, 
                      image_reference="subject", image_fidelity=0.5, human_fidelity=0.5, 
                      output_format="png", n=1, aspect_ratio="16:9", callback_url="", timeout=120):
        """实现功能，直接根据预设的参数返回生成图像的 url
        
        参数:
            model_name: str, 模型名称，可选择 kling-v1-5 或 kling-v1
            prompt: str, 文本提示词
            image: str, 参考图片的URL或本地文件路径
            image_reference: str, 参考图片类型，可选值：subject（角色特征参考）, face（人物长相参考）
            image_fidelity: float, 参考图片强度，取值范围：[0,1]，数值越大参考强度越大
            human_fidelity: float, 面部参考强度，取值范围：[0,1]，数值越大参考强度越大
            output_format: str, 输出格式：png 或 jpg
            n: int, 生成数量 [1, 9]
            aspect_ratio: str, 输出比例：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
            timeout: int, 等待生成完成的超时时间（秒）
        返回:
            image_url: 图像 url
        """
        # 处理图像输入 - 自动判断是URL还是本地文件路径
        if image.startswith(('http://', 'https://', 'ftp://')):
            # 如果是URL，直接使用
            image_data = image
        else:
            # 否则当作本地文件路径处理，转换为base64
            try:
                image_data = KlingImageToImage.get_image_base64(image)
            except Exception as e:
                raise ValueError(f"无法读取图像文件: {str(e)}")
        
        # 调用生成图像 api 提交图像生成任务，返回获取 task_id
        task_id = self._kling_generate_image(
            model_name, prompt, image_data, image_reference, 
            image_fidelity, human_fidelity, output_format, n, aspect_ratio, callback_url
        )
        
        start_time = time.time()
        
        # 轮询等待生成完成
        while True:
            # 根据 task_id 调用查询图像api 查看图像生成任务是否完成
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
    API_URL = "www.dmxapi.cn"  # API 节点地址
    DMX_API_TOKEN = "sk-XXXXXXXXXXXXXX"  # API 密钥
    
    # 创建图生图转换器实例
    kling_image_to_image = KlingImageToImage(api_token=DMX_API_TOKEN, api_url=API_URL)
    
    # 生成图像
    image_urls = kling_image_to_image.generate_image(
        model_name="kling-v1-5",  # [必选]模型名称 参数 kling-v1 或者 kling-v1-5 （注意 v2 没有图生图能力）
        prompt="请生成这张照片的梵高风格迁移后的图像",  # [必选]文本提示词 
        image="/Users/dmxapi/Desktop/dmxapi.png",  # [必选]参考图片路径 参数可以是 图片的URL https://image.jpg 或者 图片的本地路径 即可
        image_reference="subject",  # [必选]参考图片类型，可选值：subject（角色特征参考）, face（人物长相参考）
        # image_fidelity=0.5,  # 参考图片强度 参数范围 0-1 默认 0.5 
        # human_fidelity=0.5,  # 面部参考强度 参数范围 0-1 默认 0.5 
        # output_format="png",  # 输出格式 参数范围 png 或者 jpg
        # n=1,  # 生成数量 参数范围 1-9 默认 1
        # aspect_ratio="16:9",  # 输出比例 参数范围 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3 默认 16:9
        # callback_url="",  # 回调地址
        # timeout=120 # 等待超时时间
    )
    
    print(image_urls)