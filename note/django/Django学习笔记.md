# Django框架入门笔记

Django是一种重量级的python web框架。在学习过程中，最重要的笔记就是官方网站文档，而且支持了中文：[Django学习官网文档](https://docs.djangoproject.com/zh-hans/4.0/)

安装正式发行版本：

```shell
python -m pip install Django
```

在当前目录下创建项目：

```shell
django-admin startproject mysite
```

 这行代码将会在当前目录下创建一个 `mysite` 目录。 项目的结构如下：

```shell
mysite/					 # 项目根目录
	manage.py			 # 管理 Django 项目的命令行工具，直接编译可以看到所有命令
	mysite/				 # 项目包
		__init__.py		 # python包
		settings.py		 # 项目的配置文件
		urls.py			 # 项目路由配置文件
		asgi.py          # ASGI web服务网关配置文件
		wsgi.py			# web服务网关配置文件
```

切换到最外层的项目目录，执行以下命令就可以运行我们的项目了。

```shell
python manage.py runserver
python manage.py runserver 0.0.0.0 5000   # 修改服务器监听的IP
```

settings.py中常用配置

```python
# 项目的绝对路径
BASE_DIR = Path(__file__).resolve().parent.parent
# 启动模式：调试版本、release版本
# 调试模式：检测代码改动立刻重启；报错页面显示调试信息；
DEBUG = True
# 请求头过滤
ALLOWED_HOSTS = []
# 主路由地址
ROOT_URLCONF = 'mysite.urls'
# 模板
TEMPLATES
# 网关地址
WSGI_APPLICATION = 'mysite.wsgi.application'
# 数据库
DATABASES
# 静态URL地址
STATIC_URL
```

## URL和视图函数

URL（Uniform Resource Locator）即统一资源定位符，就是我们要访问网站的地址，用来表示互联网中某个资源的地址。

URL一般语法格式为：

```url
protocol://hostname[:port]/path[?query][#fragment]
```

-   协议（protocol）：http通过HTTP协议访问资源；https 通过安全的 STL+HTTP 协议访问资源；file资源为本地计算机上的文件。
-   主机名（hostname）：存放资源服务器的域名系统 DNS 主机名、域名或IP地址。
-   端口号（port）：http默认端口为80
-   路由地址（path）：由若干个“/”符号分隔的字符串，表示主机上的一个目录或文件地址，路由地址决定服务端如何处理该请求。
-   查询（query）：动态网页传递参数，可有多个参数，用“&”符号分隔，参数表示为 `key=value`。
-   信息片段（fragment）：指定网络资源中的片段，定位锚点。

Django处理URL请求过程：

```sequence
participant Django as django
participant settings.py as set
participant urls.py as url
participant views.py as view

django-->set:查找配置
set-->url:根据ROOT_URLCONF找到主路由文件
url-->url:加载urlpatterns匹配path
url-->view:调用对应视图函数处理请求
view-->django:返回响应
url-->django:如果没找到对应试图函数返回404
```

其中 `urlpatterns` 是一个数组，Django 在这个数组中逐个匹配请求的路由地址，如果没有匹配到返回 404 错误，如果匹配到就调用对用的视图函数处理请求。

**视图函数**是用于接受一个浏览器请求（HttpRequest对象）并通过 HttpResponse 对象返回响应的函数。

语法规则：

```python
from django.http import HttpResponse

def xxx_view(request[, args...]):
	return HttpResponse object
```

视图函数定义好之后要在 urls.py 文件中的 `urlpatterns` 中声明路由地址和视图函数的映射。

## 路由配置

配置路由函数在 `urls.py` 中的 `urlpatterns` 使用 `path()` 函数添加。

-   `path()` 函数
-   导入：`from django.url import path`
-   语法：`path(route, views, name=None)`
-   参数：
    -   route - 字符串类型，匹配的请求路径
    -   views：指定路径对应的视图处理函数名称
    -   name：为地址起别名，在模板中地址反解析时使用

使用 path 转换器可以匹配 url 中的变量。

-   语法：`<转换器类型:自定义名称>`
-   作用：若转换器类型匹配到对应类型的数据，则将数据按照关键字传参的方式传递给视图函数。
-   例如：`path('page/<int:page>', views.xxx)`

转换器类型包括：

| 类型 | 作用                                                    | 样例                                                  |
| :--: | :------------------------------------------------------ | ----------------------------------------------------- |
| str  | 匹配除了'/'之外的非空字符串                             | `"v1/user/<str:username>"` 匹配到 "v1/user/name"      |
| int  | 匹配0或任何整数，返回int                                | `"v1/user/<int:page>"` 匹配到 "v1/user/100"           |
| slug | 匹配任意由ASCII字母或数字以及连字符和下划线组成的短标签 | `"v1/user/<slug:sl>"` 匹配到 "v1/user/this-is-django" |
| path | 匹配非空字段，包括路径分隔符"/"                         | `"v1/user/<path:ph>"` 匹配到 "v1/user/a/b/c           |

正则精确匹配url：

-   `re_path()` 函数
-   在 url 匹配过程中使用正则表达式进行精确匹配
-   语法：
    -   `re_path(reg, view, name=xxx)`
    -   正则表达式为命名分组模式（`?P<name>pattern`）；匹配提取参数后用关键字传参方式传递给视图函数。
-   例如：`re_path(r'^(?P<x>\d{1,2})/(?P<op>\w+)/(?P<y>\d{1,2})$', views.cal_view)`

## 请求与响应

**请求**是指浏览器通过 HTTP 协议发送给服务器的数据；**响应**是指服务端接收到请求后做出相应的处理后在发送给浏览器的数据。

![](D:\study\python_Study\note\django\pics\cs.png)

请求样例：

```http
GET / HTTP/1.1
Host: www.baidu.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: https://www.baidu.com/s?wd=HTTP%20%E5%8D%8F%E8%AE%AE%E6%9C%89%E5%87%A0%E7%A7%8D%E5%92%8C.....
Accept-Encoding: gzip, deflate, sdch, br
Accept-Language: zh-CN,zh;q=0.8
Cookie: BIDUPSID=670A04B660AAF2716D3120BEAF946A11; BAIDUID=2454D4....
RA-Ver: 3.0.8
RA-Sid: CA623F7A-20150914-060054-2b9722-5fde41
```

第一行为**请求行**，包括请求方法，url 和 HTTP 版本，第二行开始到空行之间为**请求头**，剩余部分为**请求体**。

HTTP1.0定义了三种请求方法：GET、POST和HEAD方法，也是最常用的请求方法。HTTP1.1新增请求：OPTIONS、PUT、DELETE、TRACE和CONNECT方法。

Django中收到 HTTP 请求后，会根据请求的数据报文创建 `HttpRequest` 对象，通过属性描述了请求的所有相关信息，作为视图函数的第一个参数传递。

`HttpRequest` 对象属性包括：

-   `path_info`：URL字符串
-   `method`：字符串，表示HTTP请求方法
-   `GET`：QueryDict 查询字典对象，包含 GET 请求方式的所有数据
-   `POST`：QueryDict 查询字典对象，包含 POST 请求方式的所有数据
-   `FILE`：类似字典的对象，包含所有上传文件信息
-   `COOKIES`：字典，包含所有的cookies，键值都是字符串
-   `session`：类似字典的对象，表示当前会话
-   `body`：字符串，请求体的内容
-   `scheme`：请求协议（'http'/'https'）
-   `request.get_full_path()`：请求的完整路径
-   `request.META`：请求中的元数据（消息头）
    -   `request.META['REMOTE_ADDR']`：客户端IP地址

响应样例：

```http
HTTP/1.1 200 OK
Server: bfe/1.0.8.18
Date: Mon, 16 Jan 2017 06:35:24 GMT
Content-Type: text/html;charset=utf-8
Transfer-Encoding: chunked
Connection: keep-alive
Cache-Control: private
Expires: Mon, 16 Jan 2017 06:35:24 GMT
Content-Encoding: gzip
X-UA-Compatible: IE=Edge,chrome=1
Strict-Transport-Security: max-age=172800
BDPAGETYPE: 2
BDQID: 0xe0042a0200002ea3
BDUSERID: 252528851
Set-Cookie: BDSVRTM=104; path=/
Set-Cookie: BD_HOME=1; path=/
Set-Cookie: H_PS_PSSID=21767_1446_21111_18133_19898_20718; path=/; domain=.baidu.com
Set-Cookie: __bsi=17204004216256107848_00_0_I_R_105_0303_C02F_N_I_I_0; expires=Mon, 16-Jan-17 06:35:29 GMT; domain=www.baidu.com; path=/
```

第一行为**响应行**，包括HTTP版本，状态码和响应原因。

HTTP 状态码 HTTP Status Code：

-   200 - 请求成功
-   301 - 永久重定向-资源转移到其他URL
-   302 - 临时重定向
-   404 - 请求的资源不存在
-   500 - 服务器内部错误

Django中的响应对象由函数 `HttpResponse()` 构造。

-   语法：`HttpResponse(content=响应体, content_type=响应数据类型, status=状态码)`
-   作用：向客户端浏览器返回响应，同时携带响应体内容。

常用的content_type包括：

-   `text/html`：默认，html文件
-   `text/plain`：纯文本
-   `text/css`：css文件
-   `text/javascript`：js文件
-   `multipart/form-data`：文件提交
-   `application/json`：json传输
-   `application/xml`：xml文件

HTTP响应的其他子类：

```python
HttpResponseRediraect()		# 重定向 302
HttpResponseNotModified()	# 未修改 304
HttpResponseBadRequest()	# 请求错误 400
HttpResponseNitFound()		# 没有请求的资源 404
HttpResponseForbidden()		# 请求被禁止 403
HttpResponseServerError()	# 服务器错误 500
```

### GEST请求和POST请求

无论是GET请求还是POST请求，Django都是统一由视图函数处理请求，通过判断 request.method 区分请求动作。

```python
if request.method == 'GET':
    处理GET请求逻辑
elif request.method == 'POST':
    处理POST请求逻辑
else:
    其他请求逻辑
```

GET 请求动作一般用于向服务器获取数据：

-   浏览器地址栏输入URL回车
-    `a href="地址?参数=值&参数=值"`
-   form表单中的method为get

GET请求通过查询字符串传递数据给服务器。例如：`http://127.0.0.1:8000/page1?a=100&b=200`。GET处理查询字符串的方法有：

-   `request.GET['参数名']`
-   `request.GET.get('参数名', '默认值')`
-   `request.GET.getlist('参数名')`

POST 请求动作，一般用于向服务器提交大量/隐私数据，客户端通过表单等POST请求将数据传递给服务器。

-   `request.POST['参数名']`
-   `request.POST.get('参数名', '默认值')`
-   `request.POST.getlist('参数名')`

取消 csrf 验证，否则 Django 会拒绝客户端发来的POST请求，报403响应。禁止 `settings.py` 中 `MIDDLEWARE` 的中间件 `CsrfViewMiddleware`

## Django 设计模式

传统的 MVC 框架代表 Model-View-Controller （模型-视图-控制器）模式：

-   M 模型层，主要用于对数据库层的封装
-   V 视图层，用于向用户展示结果
-   C 控制层，用于请求处理、获取数据、返回结果

作用：降低模块间的耦合度。

Django的 MTV 模式代表 Model-Template-View（模型-模板-视图）模式：

-   M 模型层，负责与数据库交互
-   T 模板层，负责呈现内容到浏览器
-   V 视图层，核心，负责接收请求、获取数据、返回结果

### 模板层

模板是可以根据字典数据动态变化的html网页，可以根据视图层传输的数据动态生成对应的html网页。

在项目目录下创建模板目录为templates，在 settings.py 中 TEMPLATES 配置项：

-   BACKEND：指定模板的索引
-   DIRS：模板的搜索目录
-   APP_DIRS：是否在应用中的 templates 目录中搜索模板文件
-   OPTIONS：有关模板的选项

设置 `'DIRS': [os.path.join(BASE_DIR, 'templates')]`。

#### 模板的加载方式

通过 loader 方式加载，然后由 HttpResponse 进行响应。

```python
from django.template import loader
# 1. 通过 loader 加载模板
t = loader.get_template("模板文件名")
# 2. 将 t 转换为 HTML 字符串
html = t.render(字典数据)
# 3. 用响应对象将转换的字符串内容返回给浏览器
return HttpResponse(html)
```

使用 render 直接加载模板并响应模板。

```python
from django.shortcuts import render
return render(request, '模板文件名', 字典数据)
```

#### 视图层与模板层的交互

视图函数中可以将 Python 变量封装到**字典**中传递到模板：

```python
def xxx_view(request):
    dic = {
        "var1":"value1",
        "var2":"value2",
    }
    return render(request, 'xxx.html', dic)
```

在模板中，可以用 {{变量名}} 的语法调用视图函数传递进来的变量：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h3>我是模板层的测试页面</h3>
<h4>用户名：{{ username }} 权限等级：{{ privilage }}</h4>

</body>
</html>
```

能传递到模板的数据类型包括：str、int、list（数组）、tuple（元组）、dict（字典）、func（方法）、obj（类实例化对象）。

模板中使用的语法：`{{ 变量名 }}`、`{{ 变量名.index }}`、`{{ 变量名.key }}`、`{{ 对象.方法 }}`、`{{ 函数名 }}`。

#### 模板标签

将一些服务器的功能嵌入到模板中，例如流程控制等。

标签语法：

```html
{% 标签 %}
...
{% 结束标签 %}

# if标签
{% if expression1 %}
...
{% elif expression2 %}
...
{% else %}
...
{% endif %}
```

if 标签中使用实际括号是无效的语法，如果需要指示优先级，应该使用嵌套的 if 标签，具体参考官方文档：https://docs.djangoproject.com/zh-hans/4.0/ref/templates/builtins/#if

```html
{% for 变量 in 迭代对象 %}
...循环语句
{% empty %}
...迭代对象无数据填充时的语句
{% endfor %}
```

for 标签的内置变量 `forloop`

#### 过滤器和继承

过滤器用于变量输出时对变量的值进行处理，可以通过使用过滤器来该改变变量的输出显示。

语法：`{{ 变量 | 过滤器1:'参数值1' | 过滤器2:'参数值2' }}`

常用的过滤器：

-   lower：将字符串转换为小写
-   upper：将字符串转换为大写
-   safe：默认不对变量内的字符串进行html转义
-   add:"n"：将value的值增加n
-   truncatechars:'n'：如果字符串字符多于指定的字符数量，则会截断，可以用"..."结尾

Django为了预防 XSS 攻击，默认会将变量进行HTML转义，此时如果传入的变量为一串html代码，则会自动转义使变量作为字符串显示出来。

**模板继承**可以使用父模板的内容重用，子模版直接继承父模板的全部内容，并且可以覆盖父模板相应的块。

父模板语法：

-   定义父模板的块 block 标签
-   标识出哪些在子模版中是允许被修改的
-   block 标签：在父模板中定义，可以在子模版中覆盖

子模版语法：

-   继承模板 extends 标签（写在模板文件的第一行），例如 `{% extends 'base.html' %}`
-   子模版重写父模板中的内容块

```html
{% block block_name %}
子模版块用来覆盖父模板中 block_name 块的内容
{% endblock block_name %}
```

注意：模板继承无法继承服务器端的动态内容。

### url 反向解析

url可能出现的位置：

-   模板 html 中：
    -   `<a href='url'>超链接</a>` 点击后跳转到url
    -   `<form action='url' method='post'>` form 表单中的数据用 post 方法提交至 url
-   视图函数中：
    -   302 重定向，`HttpResponseRedirect('url')` 将用户地址栏中的地址跳转到 url

项目中 url 的规范：

-   绝对地址：`http://127.0.0.1:8000/page/1`
-   相对地址：`/page/1` 浏览器会将当前地址栏的协议、ip和端口加上该地址，作为最终访问地址；当相对地址为`page/1`时，浏览器会将当前的地址加上该相对地址，作为最终访问地址。

url反向解析是指在视图或模板中，用 path 定义的名称来**动态查找或计算出相应的路由**。

视图函数的语法：

```python
path(route, views, name='别名')
path('page', views.page_view, name='page_url')
```

在模板中，通过 url 标签实现地址的反向解析：

```html
{% url 'page_url' 'para1' 'para2' %}
```

在视图函数中，可以调用 Django 中的 `reverse` 方法进行反向解析：

```python
from django.urls import reverse
reverse('别名', args=[], kwargs={})

print(reverse('page', args=[100]))
print(reverse('page', kwargs={'name':'admin', 'age':18}))
```



