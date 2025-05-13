---
title: 图片常见的输入方式
category: 迁移
gitChangelog: false
---

# 图片常见的输入方式

通常对于图像生成或推理大模型，图片的输入方式主要有以下两种：

1. 图片的 url 传入
2. 图片的 base64 编码传入

## 方式1-图片 url 传入

> [!WARNING]
> **请确保该图片的链接访问权限是公开的**。

常见模型均支持以图片 url 传入，可以通过将图片上传到图床等方式获取图片 url 链接，以字符串的方式传入，模型侧会访问该 url 并下载图片分析。


## 方式2-图片 base64 编码传入

> [!TIP]
> Base64 编码常用于本地上传图片的场景。

`Base64` 编码是将数据用 64 个可打印的字符进行编码的方式，任何数据底层实现都是二进制，因此都可以使用 `Base64` 编码，在网络数据传输过程中图片通常使用 `Base64` 编码。`Base64` 编码可用于在HTTP环境下传递较长的标识信息。

### 常用函数

```python[python]
import base64

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

# base64 编码后的图片字符串
base64array = get_image_base64("/Users/your_image.png") # 修改为你的图片绝对路径
print(base64array)
```

## 方式3-将 url 图片获取为 base64 编码

> [!TIP]
> 需要确保访问的图片链接是公开的并且**没有网络代理方面的问题**。

可以通过网络请求直接读取图片内容并且转换为 base64 编码，以下为示例代码：

### 常用函数

```python[python]
import requests
import base64

def url_image_to_base64(image_url):
    """
    从URL获取图片并转换为base64格式
    
    参数:
        image_url (str): 图片的URL地址
        
    返回:
        str: base64编码的图片字符串
    """
    try:
        # 发送GET请求获取图片
        response = requests.get(image_url)
        
        # 检查请求是否成功
        response.raise_for_status()
        
        # 将图片内容编码为base64
        image_binary = response.content
        base64_encoded = base64.b64encode(image_binary).decode('utf-8')
        
        return base64_encoded
    
    except Exception as e:
        print(f"获取图片失败: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    url = "https://cdn.klingai.com/bs2/upload-kling-api/8089468206/image/Cl6kH2gHPegAAAAABUwweg-0_raw_image_0.png"
    base64_string = url_image_to_base64(url)
    print(base64_string)
```