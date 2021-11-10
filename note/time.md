# datetime模块

datetime 模块是 Python 内置的功能模块，它可以实现对日期的算数运算，以指定的方式格式化日期。datetime 模块内含有一个同名的 datetime 类，该类中包含多个操作日期的函数，例如：datetime.now()、datetime.fromtimestamp()、datetime.timedelta()等，下面逐一举例说明。

## datetime()构造函数

datetime 类提供了一个now()的方法可以获取当前日期和时间，还提供了带参数的构造函数datetime()，可以通过传入特定的数字返回不同的datetime 对象。例如:

```python
import datetime
#当前日期和时间
print(datetime.datetime.now())
>>> 2019-09-30 22:19:37.582514
#获取指定时间
datetest = datetime.datetime(2019,9,30,22,22,0)
print(datetest)
>>> 2019-09-30 22:22:00
#获取日期的年月日时分秒
print(str(datetest.year)+"-"+str(datetest.month)+"-"+str(datetest.day)+" "+str(datetest.hour)+":"+str(datetest.minute)+":"+str(datetest.second))
>>> 2019-9-30 22:22:0
```

