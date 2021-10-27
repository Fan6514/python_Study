# 输出日志 logging 模块

## 日志级别

logging输出日志级别包括：CRITICAL、ERROR、WARNING、INFO、DEBUG

- debug：通常用于调试和诊断时打印一些较详细的内容
- info：打印程序运行时按照预期出现的内容
- warning：可能会出现某些错误，但目前程序仍可正常运行，提醒程序员要注意这部分内容
- error：程序无法执行的内容
- critical：程序发生严重的问题，无法继续执行

## 构建自定义记录器类

logging模块包括Logger记录器、Handler处理器、Filter过滤器和Formatter格式化器。在构建一个记录器类之前，需要导入logging模块。此外，操作日志文件需要导入time模块获取当前时间来为日志文件命名，导入os模块来操作日志文件。

```python
import logging
from logging import Logger
import time
import os
```

接下来定义输出日志的格式：

```python
LOGMSGFORMAT = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
```

顺便定义日志的级别和设置的默认级别：

```python
# log level names
LEVELS = { 'debug': logging.DEBUG,
           'info': logging.INFO,
           'warning': logging.WARNING,
           'warn': logging.WARNING,
           'error': logging.ERROR,
           'critical': logging.CRITICAL }
# change this to logging.INFO to get printouts
LOGLEVELDEFAULT = logging.WARNING
```

定义Logger类：

```python 
class SysLogger(Logger, object):
    """My system logger
        Enable each sys .py file to with one import
        from log import [lg, info, error, warn, ...]"""

    def __init__(self, name="system"):

        Logger.__init__(self, name)

        # create console handler for write log file
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_path = os.path.join(os.getcwd(), 'logs')
        logfile = os.path.join(log_path, '%s.log' % rq)
        ch = logging.FileHandler(logfile, mode='a', encoding='UTF-8')
        # create formatter
        formatter = logging.Formatter(LOGMSGFORMAT)
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to lg and initilize log level
        self.addHandler(ch)
        self.ch = ch
        self.setLogLevel()

    def setLogLevel(self, levelname=None):
        """Setup log level.
            level name from LEVELS"""
        if levelname and levelname not in LEVELS:
            print(LEVELS)
            raise Exception( 'setLogLevel: unknown levelname %s' % levelname )
        level = LEVELS.get(levelname, LOGLEVELDEFAULT)
        self.setLevel(level)
        self.ch.setLevel(level)
```

## 适配多个参数的日志打印函数

```python
# Make things a bit more convenient by adding aliases
# (info, warn, error, debug) and allowing info( 'this', 'is', 'OK' )
def makeListCompatible(fn):
    """Return a new function allowing fn( 'a 1 b' ) to be called as
       newfn( 'a', 1, 'b' )"""
    def newfn( *args ):
        "Generated function. Closure-ish."
        if len( args ) == 1:
            return fn( *args )
        args = ' '.join( str( arg ) for arg in args )
        return fn( args )

    # Fix newfn's name and docstring
    setattr( newfn, '__name__', fn.__name__ )
    setattr( newfn, '__doc__', fn.__doc__ )
    return newfn
```

## 日志输出

```python
# Initialize logger and logging functions
logging.setLoggerClass(SysLogger)
lg = logging.getLogger("system")
_loggers = lg.info, lg.warning, lg.error, lg.debug
_loggers = tuple(makeListCompatible(logger) for logger in _loggers)
lg.info, lg.warning, lg.error, lg.debug = _loggers
info, warning, error, debug = _loggers
warn = warning  # alternate/old name
setLogLevel = lg.setLogLevel
```