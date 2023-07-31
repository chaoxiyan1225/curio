参考链接https://blog.csdn.net/cui_yonghua/article/details/107498535

# 一、loguru模块的基础使用
如果想更简洁，可用loguru库，python3安装：pip3 install loguru。

loguru默认的输出格式是上面的内容，有时间、级别、模块名、行号以及日志信息，不需要手动创建 logger，直接使用即可，另外其输出还是彩色的，看起来会更加友好。


from loguru import logger

logger.debug('this is a debug message')
logger.info('this is another debug message')
logger.warning('this is another debug message')
logger.error('this is another debug message')
logger.info('this is another debug message')
logger.success('this is success message!')
logger.critical('this is critical message!')

# 二、不需要配置什么东西，直接引入一个 logger，然后调用其 debug 方法即可。

如果想要输出到文件，只需要：
from loguru import logger
logger.add('my_log.log')
logger.debug('this is a debug')

# 三. logurr详细使用
比如支持输出到多个文件，分级别分别输出，过大创建新文件，过久自动删除等等。

## 3.1 add 方法的定义
def add(
        self,
        sink,
        *,
        level=_defaults.LOGURU_LEVEL,
        format=_defaults.LOGURU_FORMAT,
        filter=_defaults.LOGURU_FILTER,
        colorize=_defaults.LOGURU_COLORIZE,
        serialize=_defaults.LOGURU_SERIALIZE,
        backtrace=_defaults.LOGURU_BACKTRACE,
        diagnose=_defaults.LOGURU_DIAGNOSE,
        enqueue=_defaults.LOGURU_ENQUEUE,
        catch=_defaults.LOGURU_CATCH,
        **kwargs
    ):
    pass

看看它的源代码，它支持这么多的参数，如 level、format、filter、color 等等，另外我们还注意到它有个非常重要的参数 sink，我们看看官方文档：，可以了解到通过 sink 我们可以传入多种不同的数据结构，汇总如下：

sink 可以传入一个 file 对象，例如 sys.stderr 或者 open(‘file.log’, ‘w’) 都可以。
sink 可以直接传入一个 str 字符串或者 pathlib.Path 对象，其实就是代表文件路径的，如果识别到是这种类型，它会自动创建对应路径的日志文件并将日志输出进去。
sink 可以是一个方法，可以自行定义输出实现。
sink 可以是一个 logging 模块的 Handler，比如 FileHandler、StreamHandler 等等。
sink 还可以是一个自定义的类，具体的实现规范可以参见官方文档https://loguru.readthedocs.io/en/stable/api/logger.html#sink。
所以说，刚才我们所演示的输出到文件，仅仅给它传了一个 str 字符串路径，他就给我们创建了一个日志文件，就是这个原理。

## 3.2 基本参数
下面我们再了解下它的其他参数，例如 format、filter、level 等等。

其实它们的概念和格式和 logging 模块都是基本一样的了，例如这里使用 format、filter、level 来规定输出的格式：

logger.add('runtime.log', format="{time} {level} {message}", filter="my_module", level="INFO")
1
## 3.3 删除 sink
另外添加 sink 之后我们也可以对其进行删除，相当于重新刷新并写入新的内容。

删除的时候根据刚刚 add 方法返回的 id 进行删除即可，看下面的例子：

from loguru import logger

trace = logger.add('my_log.log')
logger.debug('this is a debug message')
logger.remove(trace)
logger.debug('this is another debug message')

看这里，我们首先 add 了一个 sink，然后获取它的返回值，赋值为 trace。随后输出了一条日志，然后将 trace 变量传给 remove 方法，再次输出一条日志，看看结果是怎样的。

控制台输出如下：

# 自带 logging

Python内置了日志模块，在默认情况下输出的日志是不带文件名和函数名的，这样在排查问题时，遇到相似的日志就变得容易混淆，可以通过设置将输出的日志中带有文件名和函数名。参考了stackoverflow的回答，详细代码如下。

import logging      
log = logging.getLogger('root')     
LOG_FORMAT = "%(filename)s:%(lineno)s %(funcName)s() %(message)s"    
logging.basicConfig(format=LOG_FORMAT)       
log.setLevel(logging.DEBUG)       
        
def InitLogger(logFile, logLevel):    
    logger = logging.getLogger()      
    fileHandler = logging.FileHandler(logFile)        
    formatter = logging.Formatter(        
        "[%(asctime)s] [%(levelname)s]  %(message)s", "%Y-%m-%d %H:%M:%S"           
    )           
    fileHandler.setFormatter(formatter)        
    logger.addHandler(fileHandler)         
    logger.setLevel(logLevel)        
    return logger       
        
        
logger = InitLogger(       
    "nsmu_%s_%s_%s.log"         
    % (        
        datetime.datetime.now().year,          
        datetime.datetime.now().month,           
        datetime.datetime.now().day,          
    ),          
    logging.INFO,      
)        
        

