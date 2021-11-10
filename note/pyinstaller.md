# 将python打包成exe可执行文件

## 安装pyinstall

python 上常见的打包方式目是通过 pyinstaller 来实现的。

```shell
pip install pyinstaller
# 清华源
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 详细步骤

pyinstaller 是一个命令行工具，下面是详细步骤

1. cmd 切换到 python 文件的目录。

2. 执行命令 `pyinstaller -F -w -i python.ico watermark.py`
    
    执行完毕会发现生成了 3 个文件夹：

```shell
    ├── pyinstall
    │   ├── __pycache__
    │   ├── build
    │   └── dist
```

其中 dist 文件夹就有我们已经打包完成的 exe 文件。

## 详细参数

在上面的打包命令中，用到了好几个参数：-F，-W，-i，这些参数的含义如下面的表格：

|  参数   | 用法  |
|  ----  | ----  |
| -F  | 生成结果是一个 exe 文件，所有的第三方依赖、资源和代码均被打包进该 exe 内 |
| -D  | 生成结果是一个目录，各种第三方依赖、资源和 exe 同时存储在该目录（默认） |
| -a  | 不包含unicode支持 |
| -d  | 执行生成的 exe 时，会输出一些log，有助于查错 |
| -w  | 不显示命令行窗口 |
| -c  | 显示命令行窗口（默认） |
| -p  | 指定额外的 import 路径，类似于使用 python path |
| -i  | 指定图标 |
| -v  | 显示版本号 |
| -n  | 生成的 .exe 的文件名 |

`pyinstaller -F -w -i python.ico watermark.py` 就表示 -F，打包只生成一个 exe 文件，-w，在运行程序的时候不打打开命令行的窗口，-i 就是打包带有自己设置的 ico 图标。