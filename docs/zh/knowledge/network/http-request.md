---
title: HTTP 请求
gitChangelog: false
---

# HTTP 请求

HTTP 协议是互联网的基石，它定义了客户端与服务器之间文本传输的规范。在 DMXAPI 的图像类型的 API 调用基本都是使用 HTTP 协议，因此了解 HTTP 协议对应用接入模型场景至关重要，下面详细介绍 HTTP 的请求方法、工作原理、消息结构以及状态码等方面。

## HTTP 请求方法

HTTP 协议定义了八种请求方法，用于指明对资源的不同操作方式：

| 方法 | 描述 |
| --- | --- |
| GET | 请求获取特定资源。不应用于产生"副作用"的操作（如修改数据）。 |
| POST | 向指定资源提交数据进行处理（如提交表单或上传文件），可能导致新资源的创建或已有资源的修改。 |
| HEAD | 与 GET 请求类似，但服务器只返回响应头，不返回响应体。用于获取资源的元信息。如文件的大小、修改时间等，而不需要获取整个资源内容，这样可以节省带宽和提高响应速度。 |
| PUT | 向指定资源位置替换其最新内容。如果资源不存在，则创建新资源。例如，通过 PUT 请求更新数据库中某条记录的信息。 |
| DELETE | 请求服务器删除指定的资源。 |
| OPTIONS | 返回服务器对特定资源支持的 HTTP 请求方法，也可用于测试服务器功能。例如客户端可以通过 OPTIONS 请求来了解服务器对特定资源支持哪些请求方法，以及是否需要进行身份验证等信息。 |
| TRACE | 回显服务器收到的请求，包括请求头、请求体等所有内容。这样客户端就可以查看在传输过程中请求是否被正确处理，以及是否有任何中间代理或服务器对请求进行了修改。主要用于测试或诊断。 |
| CONNECT | 预留给能够将连接改为隧道方式的服务器。 |

> 注意：HTTP/1.0 只定义了 GET、POST 和 HEAD 三种请求方法，其他五种是 HTTP/1.1 新增的。

## HTTP 工作原理

HTTP 协议采用请求/响应模型，工作流程如下：

1. **客户端连接到 Web 服务器**：浏览器与服务器的 HTTP 端口（默认 80）建立 TCP 连接
2. **发送 HTTP 请求**：客户端通过 TCP 套接字发送请求报文
3. **服务器接收请求并返回 HTTP 响应**：服务器解析请求，定位资源，将资源写入 TCP 套接字
4. **释放 TCP 连接**：根据 connection 模式（close 或 keepalive）决定是否保持连接
5. **客户端解析内容**：浏览器解析响应内容并显示

## HTTP 请求消息结构

HTTP 请求（Request）由四部分组成：

> [!TIP]
> 注意 URL 以及 URI 的区别
>
> - URI 是统一资源标识符（Uniform Resource Identifier）它是一种抽象概念，用于唯一地标识资源，只用来区分标识，不涉及资源的访问方式和位置等具体信息。
> - URL 是统一资源定位符（Uniform Resource Locator）它是一种具体的资源在互联网中的位置。
> 
> URL 是 URI 的子集，可以简单理解为 URL = base uri(BASE URL) + relative uri(PATH)


1. **请求行**：说明**请求方法、请求 URI 和 HTTP 协议版本**。例如下面样例中，`GET /index.html HTTP/1.1`，表示使用 GET 方法请求服务器上的/index.html资源，使用的 HTTP 协议版本是 1.1。
2. **请求头部**：说明服务器要使用的附加信息，例如客户端的信息、请求的内容类型、缓存策略等。包括不限于：
    - `Host`：请求的主机名，例如 `www.DMXAPI.com`。
    - `User-Agent`：客户端信息，例如浏览器类型、版本等。
    - `Accept`：客户端可接受的响应内容类型。
    - `Referer`：请求来源，例如 `www.DMXAPI.cn`。
    - `Accept-Encoding`：客户端可接受的编码方式。
    - `Accept-Language`：客户端可接受的语言。
    - `Connection`：连接方式，例如 `keep-alive` 表示保持连接，`close` 表示关闭连接。
    - `Authorization`：认证信息，例如 `Bearer token`。
    - `Cookie`：之前由服务器通过 Set-Cookie 发送的 HTTP cookie。
    - `Origin`：表示请求来自哪个站点（用于 CORS）
    - `Content-Type`：指定请求体的媒体类型，如 application/json
3. **空行**：请求头部后的空行（必须），它标志着请求头的结束和请求体的开始。
4. **请求数据**：请求的主体部分，可以为空。常见例如 POST 请求中提交的表单数据、上传的文件内容等。而 GET 请求一般没有请求体，因为 GET 请求的参数是通过 URL 传递的。

### GET 请求示例

```
GET /index.html HTTP/1.1
Host: www.DMXAPI.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36
Accept: image/webp,image/*,*/*;q=0.8
Referer: www.DMXAPI.cn
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8
```

GET 请求 API 实例可见：[query-api](../../models/kling/api/query-api.md)

### POST 请求示例

```
POST / HTTP1.1
Host: www.DMXAPI.com
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
Content-Type: application/x-www-form-urlencoded
Content-Length: 40
Connection: Keep-Alive

name=DMXAPI%20Ajax&publisher=DMXAPI
```

POST 请求 API 实例可见：[generate-image](../../models/kling/api/generate-image.md)

## HTTP 响应消息结构

HTTP 响应（Response）也由四部分组成：

1. **状态行**：包括 HTTP 协议版本、状态码和状态消息
2. **消息报头**：说明客户端要使用的附加信息等等，包括不限于：
   - `Content-Type`：响应内容的类型，例如 `text/html` 表示 HTML 页面，`image/jpeg` 表示图片等等。
   - `Content-Length`：响应体的长度，以字节为单位。
   - `Content-Encoding`：响应体的编码方式，如 gzip 等。
   - `Date`：响应的时间。
   - `Server`：服务器软件的名称和版本。
   - `Set-Cookie`：服务器通过 Set-Cookie 发送的 HTTP cookie。
   - `Access-Control-Allow-Origin`：指定允许哪些源可以访问资源（CORS）
3. **空行**：响应头和响应体之间由一个空行分隔，这个空行是必须的，它标志着响应头的结束和响应体的开始。
4. **响应正文**：服务器返回给客户端的文本信息，比如 HTML 页面内容、图片数据、JSON 格式的数据等。如果状态码表示请求失败，响应体中可能会包含错误信息。

### 响应示例

```
HTTP/1.1 200 OK
Date: Mon, 18 Dec 2023 14:32:47 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
Content-Length: 2048
Cache-Control: max-age=3600, public
Expires: Mon, 18 Dec 2023 15:32:47 GMT
Last-Modified: Mon, 18 Dec 2023 10:15:23 GMT
ETag: "a86-5f9c3e2ad83c0"
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Set-Cookie: session=u7y8i9o0p; Path=/; HttpOnly; Secure; SameSite=Strict


<html>
      <head>DMXAPI</head>
      <body>
            <!--body goes here-->
      </body>
</html>
```

## 常见 HTTP 状态码

> [!TIP]
> 有关于 DMXAPI 更详细的 API 状态码说明，请参考 [DMXAPI 返回状态码详解](./status-code.md)。

| 状态码 | 描述 | 类型 |
| --- | --- | --- |
| 200 | OK | 成功 - 操作将在响应正文中返回数据 |
| 204 | No Content | 成功 - 操作成功但不返回数据 |
| 301 | Moved Permanently | 重定向 - 资源已永久移动 |
| 302 | Found | 重定向 - 资源临时移动 |
| 304 | Not Modified | 重定向 - 资源未修改 |
| 400 | Bad Request | 客户端错误 - 参数无效 |
| 401 | Unauthorized | 客户端错误 - 未授权 |
| 403 | Forbidden | 客户端错误 - 禁止访问 |
| 404 | Not Found | 客户端错误 - 资源不存在 |
| 405 | Method Not Allowed | 客户端错误 - 方法不允许 |
| 413 | Payload Too Large | 客户端错误 - 请求长度过长 |
| 500 | Internal Server Error | 服务器错误 - 服务器内部错误 |
| 501 | Not Implemented | 服务器错误 - 未实施请求的操作 |
| 503 | Service Unavailable | 服务器错误 - 服务不可用 |

## 常用的 GET 与 POST 的对比

GET
  - 数据附加在 URL 上（如 `example.com?param1=value1&param2=value2`）参数直接暴露在 URL 中，不适合传输敏感信息
  - 受浏览器 URL 长度限制（一般为 2KB-8KB）。
  - 通常适合数据获取、搜索、简单表单，一般浏览器会缓存 GET 请求的结果，下次请求时直接从缓存中获取，提高性能。

POST：
  - 数据放在请求体中，不暴露在 URL 中，适合传输敏感信息，参数在请求体中，（HTTPS场景下）相对安全
  - 理论上无限制，但实际会受服务器配置限制
  - 适合文件上传以及包含敏感信息的表单

## HTTP 协议的主要特点

1. **无连接**：每次连接只处理一个请求，处理完即断开，这使得服务器可以同时处理多个请求，提高了服务器的资源利用效率和并发处理能力。
2. **无状态**：协议对事务处理没有记忆能力，不保存之前的信息，每个请求都是独立的，服务器只根据当前接收到的请求信息来处理请求，而不依赖于之前的请求状态。这样设计使得 HTTP 协议更加简单和高效，但在需要跟踪用户状态的应用中，就需要通过其他技术（如 Cookie、Session 等）来实现。
3. **简单快速**：客户端只需传送请求方法和路径
4. **灵活**：通过`Content-Type`等头部字段，HTTP 协议可以支持多种不同类型的数据传输，如 HTML、图片、音频、视频、JSON、XML 等。
5. **B/S 及 C/S 模式**：适用于浏览器/服务器和客户端/服务器架构。

