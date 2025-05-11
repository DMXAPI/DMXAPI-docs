import http.client
import json
import base64

# 配置全局变量
API_URL = "www.dmxapi.cn" # API 节点
DMX_API_TOKEN = "sk-XXXXXXXXXXXXX" # API 密钥

# 创建HTTP连接对象，用于后续所有API请求
conn = http.client.HTTPSConnection(API_URL)

# 将图片转换为 base64 编码形式
def get_image_base64(image_path):
    """将图片转换为 base64 编码形式
    输入参数:
        image_path: 图片路径
    返回参数:
        base64 编码后的图片字符串
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def kling_virtual_try_on():
   """调用 Kling AI 的虚拟试穿API，提交一个虚拟试穿任务
   
   返回值:
      task_id: 生成任务的唯一标识符，用于后续查询任务结果
   """
   # 构建API请求体，包含所有图像生成参数
   payload = json.dumps({
      "model_name": "kolors-virtual-try-on-v1-5", # 模型名称，可选值：基础版本 `kolors-virtual-try-on-v1` 或 v1-5 版本 `kolors-virtual-try-on-v1-5` 支持服装组合
      # 人物图片 也可以传入 base64 编码后的图片字符串 `get_image_base64("path/to/human_image.jpg")`
      "human_image": "https://assets.christiandior.com/is/image/diorprod/LOOK_F_25_1_LOOK_095_E04?$lookDefault_GH-GHC$&crop=568,0,1864,2000&bfc=on&qlt=85",
      # 服饰图片 也可以传入 base64 编码后的图片字符串 `get_image_base64("path/to/cloth_image.jpg")`
      "cloth_image": "https://assets.christiandior.com/is/image/diorprod/511R59A1166X3389_E01?$default_GHC$&crop=501,147,998,1572&bfc=on&qlt=85",
      # "callback_url": "https://www.dmxapi.cn/callback" # 回调地址，可以用于 webhook 等通知场景
   })
   
   # 构建请求头，包含认证信息和内容类型
   headers = {
   'Authorization': f'Bearer {DMX_API_TOKEN}',  # 使用Bearer令牌认证方式
   'Content-Type': 'application/json'  # 指定请求体格式为JSON
   }
   # 发送POST请求，路径为图像生成API端点
   conn.request("POST", "/kling/v1/images/kolors-virtual-try-on", payload, headers)
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
    print(kling_virtual_try_on())
