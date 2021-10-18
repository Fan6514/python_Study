# 解析命令行参数选项

使用optparse模块中的OptionParser注册命令行选项，可以优雅地解析命令行参数。使用该模块通过调用 `add_option` 方法即可添加选项，更具有拓展性。调用 `parse_args`方法可以获得输入选项参数。

示例：

```python
class Run(object):
    "Run system"

    def __init__(self):
        "Init."
        self.options = None
        self.args = None

    def parseArgs(self):
        desc = ("This is a test for cmd args input.")
        usage = ('%prog [options]\n'
                 '(type %prog -h for details)')
        version = ("0.0.1")

        opts = OptionParser(description=desc, usage=usage, version=version)
        opts.add_option('-c', '--config', action='store',
                        default=False, help='write config to FILE')
        opts.add_option('-v', '--verbosity', type='choice',
                        choices=list(LEVELS.keys()), default = 'warn',
                        help='|'.join(LEVELS.keys()))
        
        self.options, self.args = opts.parse_args()
```

