import http.client
import json
import time
import base64

class KlingVirtualTryOn:
    def __init__(self, api_token, api_url):
        """初始化 Kling 虚拟试穿生成器
        
        参数:
            api_token: API 密钥
            api_url: API 节点地址
        """
        self.api_url = api_url
        self.api_token = api_token
        # 初始化 HTTP 连接
        self.conn = http.client.HTTPSConnection(self.api_url)
        self.endpoint = "/kling/v1/images/kolors-virtual-try-on"
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

    def _kling_virtual_try_on(self, model_name, human_image, cloth_image, callback_url=""):
        """使用 kling 生成虚拟试穿图像
        
        参数: 
            model_name: str, 模型名称，可选值：基础版本 `kolors-virtual-try-on-v1` 或 v1-5 版本 `kolors-virtual-try-on-v1-5` 支持服装组合
            human_image: str, 人物图片（URL或base64编码）
            cloth_image: str, 服饰图片（URL或base64编码）
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
        返回:
            task_id: 生成任务的 id
        """
        # 构建请求体，请求的核心参数
        payload = {
            "model_name": model_name,
            "human_image": human_image,
            "cloth_image": cloth_image,
            "callback_url": callback_url
        }
        
        # 发送 POST 请求，提交虚拟试穿任务
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
    
    def _query_virtual_try_on_result(self, task_id):
        """使用查询接口获取虚拟试穿结果
        
        参数:
            task_id: 生成任务的 id
        返回:
            result_image: 虚拟试穿结果图像 url，任务未完成时返回 None
        """
        # 构建查询路径
        query_path = f"{self.endpoint}/{task_id}"

        # 发送 GET 请求，查询虚拟试穿任务状态
        self.conn.request("GET", query_path, None, self.headers)
        # 获取响应
        res = self.conn.getresponse()
        # 读取响应内容并解析为 JSON
        json_data = json.loads(res.read().decode("utf-8"))
        
        # 如果任务状态为成功，则返回结果图像 url
        if json_data['data']['task_status'] == "succeed":
            result_image = json_data['data']['task_result']['images'][0]['url']
            return result_image
        else: 
            return None
    
    def generate_try_on(self, model_name, human_image, cloth_image, callback_url="", timeout=120):
        """实现功能，根据人物图像和服饰图像生成虚拟试穿结果
        
        参数:
            model_name: str, 模型名称，可选值：基础版本 `kolors-virtual-try-on-v1` 或 v1-5 版本 `kolors-virtual-try-on-v1-5` 支持服装组合
            human_image: str, 人物图片路径或URL
            cloth_image: str, 服饰图片路径或URL
            callback_url: str, 回调地址，可以用于 webhook 等通知场景
            timeout: int, 超时时间（秒）
        返回:
            result_image: 虚拟试穿结果图像 url
        """
        # 处理人物图片输入
        if human_image.startswith(('http://', 'https://', 'ftp://')):
            # 如果是URL，直接使用
            human_data = human_image
        else:
            # 否则当作本地文件路径处理，转换为base64
            try:
                human_data = KlingVirtualTryOn.get_image_base64(human_image)
            except Exception as e:
                raise ValueError(f"无法读取人物图像文件: {str(e)}")
                
        # 处理服饰图片输入
        if cloth_image.startswith(('http://', 'https://', 'ftp://')):
            # 如果是URL，直接使用
            cloth_data = cloth_image
        else:
            # 否则当作本地文件路径处理，转换为base64
            try:
                cloth_data = KlingVirtualTryOn.get_image_base64(cloth_image)
            except Exception as e:
                raise ValueError(f"无法读取服饰图像文件: {str(e)}")
        
        # 调用虚拟试穿 API 提交任务，返回获取 task_id
        task_id = self._kling_virtual_try_on(model_name, human_data, cloth_data, callback_url)
        
        start_time = time.time()
        
        # 轮询等待生成完成
        while True:
            # 根据 task_id 调用查询 API 查看任务是否完成
            result_image = self._query_virtual_try_on_result(task_id)
            # 如果任务完成，则返回结果图像 url
            if result_image is not None:
                return result_image
            # 如果轮询超时，则返回 None
            if time.time() - start_time > timeout:
                print(f"请求达到 {timeout} 秒超时")
                return None
            # 轮询间隔 1 秒
            time.sleep(1)
            print(f"等待虚拟试穿结果生成，{int(time.time() - start_time)} 秒", flush=True)


# 使用示例
if __name__ == "__main__":
    API_URL = "www.dmxapi.cn"  # API 节点地址
    DMX_API_TOKEN = "sk-XXXXXXXXXXXXXX"  # API 密钥
    
    # 创建虚拟试穿生成器实例
    kling_virtual_try_on = KlingVirtualTryOn(api_token=DMX_API_TOKEN, api_url=API_URL)
    
    # 生成虚拟试穿结果
    result_url = kling_virtual_try_on.generate_try_on(
        model_name="kolors-virtual-try-on-v1-5",  # [必选] 模型名称 参数基础版本 `kolors-virtual-try-on-v1` 或 v1-5 版本 `kolors-virtual-try-on-v1-5` 支持服装组合
        human_image="https://assets.christiandior.com/is/image/diorprod/LOOK_F_25_1_LOOK_095_E04?$lookDefault_GH-GHC$&crop=568,0,1864,2000&bfc=on&qlt=85",  # [必选] 人物图片 参数可以是 图片的URL 或者 图片的本地路径 即可
        cloth_image="https://assets.christiandior.com/is/image/diorprod/511R59A1166X3389_E01?$default_GHC$&crop=501,147,998,1572&bfc=on&qlt=85",  # [必选] 服饰图片 参数可以是 图片的URL 或者 图片的本地路径 即可
        # callback_url="",  # 回调地址
        # timeout=120  # 等待超时时间 绘图任务推荐设置 30 秒以上
    )
    
    print(result_url)