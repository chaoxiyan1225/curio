# 简介
**什么是 mitmproxy？**
>mitm 为 Man-In-The-Middle attack；
>mitmproxy 即为 中间人攻击代理。
>为什么要用 mitmproxy？相比 Fiddler 和 Charles 它有什么优势？

mitmproxy 不仅可以截获请求帮助开发者查看、分析，更可以通过自定义脚本进行二次开发。举例来说，利用 Fiddler 可以过滤出浏览器对某个特定 url 的请求，并查看、分析其数据，但实现不了高度定制化的需求，类似于：“截获对浏览器对该 url 的请求，将返回内容置空，并将真实的返回内容存到某个数据库，出现异常时发出邮件通知”。而对于 mitmproxy，这样的需求可以通过载入自定义 python 脚本轻松实现。
特征

>1. 拦截 HTTP 和 HTTPS 请求和响应并即时修改它们
>2. 保存完整的 HTTP 对话以供以后重播和分析
>3. 重播 HTTP 对话的客户端
>4. 重播先前记录的服务器的 HTTP 响应
>5. 反向代理模式将流量转发到指定的服务器
>6. macOS 和 Linux 上的透明代理模式
>7. 使用 Python 对 HTTP 流量进行脚本化更改
>8. 实时生成用于拦截的 SSL / TLS 证书
>还有更多……

# 使用指南
[链接](https://www.cnblogs.com/hongdanni/p/13460698.html)

# 工具是开源
参考链接 [链接](https://docs.mitmproxy.org/stable/)
mitmproxy 是一组工具，为 HTTP/1、HTTP/2 和 WebSocket 提供交互式、支持 SSL/TLS 的拦截代理。

使用背景： 能通过代理，劫持所有的请求，且支持二次开发，支持解析请求以及修改响应等

# 使用场景
[jd商品抓取](https://testerhome.com/articles/31284?order_by=created_at&)

支持移动端，这个抢票是否是可能的。

在这个文档里面，阐述了如何通过

# 不同环境下证书问题
参考  [证书](https://earthly.dev/blog/mitmproxy/), 解决不同的证书问题

# 抓小程序 
https://www.cnblogs.com/hongdanni/p/13460698.html



