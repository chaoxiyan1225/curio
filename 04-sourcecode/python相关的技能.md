# 实现一个进度条功能且带颜色

```python
import time

def progress_bar(total):
    if total <= 0:
        raise ValueError("Wrong total number ...")
    # step = (100 // total if total <= 100 else total // 100)

    for i in range(0, total):
        time.sleep(0.05)
        step = int(100 / total * (i + 1))
        str1 = '\r[%3d%%] %s' % (step, '>' * step)
        print(('\033[32m%s\033[0m' % str1), end='', flush=True)

progress_bar(20)
print()
progress_bar(110)
print()

````

# pyQT学习地址 
https://maicss.gitbook.io/pyqt-chinese-tutoral/pyqt5/index

# 如何打包python到exe

参考知乎网址 https://zhuanlan.zhihu.com/p/162237978 

也许我们不一定是专业的程序员，但是我们仍然可以通过代码提高我们的效率，尽量少加班，多陪陪媳妇。再不行，让代码替我们干着重复的工作，我们有节省出来的时间打游戏不好嘛，是吧，哈哈哈。

如果对于Python感兴趣，那么除了网上的一些教程之外，Python书籍也是不可缺少的，个人觉得《Python编程从入门到精通》是非常适合零基础入门的，这本书可以让初学者打好Python基础。未来不管是从事Python的哪个方向，掌握这些基础知识都是必不可少的！

Python编程从入门到精通 零基础学python数据分析教程

但是呢，我们开发的脚本一般都会用到一些第三方包，可能别人也需要用到我们的脚本，如果我们将我们的xx.py文件发给他，的，他还需要安装python解释器，甚至还要安装我们用的那些第三方包，是不是有点小麻烦？但是我们都知道，PC是可以直接运行exe文件的，这就为我们提供了一个便捷的方式。所以，从看了这个教程以后，这都将成为过去式，打成exe之后，分享即可用。

PS: 如果打包为exe的话，版本尽量选择python3.6+32位版本，因为win64位系统向下兼容32位程序，但是如果不考虑32位系统的话无所谓，直接python64位版本直接打包就可以，只是只能在win64位系统上跑。

安装pyinstaller
首先安装pyinstaller，使用安装命令：pip3 install pyinstaller，如下图所示。

pyinstaller打包机制
我们写的python脚本是不能脱离python解释器单独运行的，所以在打包的时候，至少会将python解释器和脚本一起打包，同样，为了打包的exe能正常运行，会把我们所有安装的第三方包一并打包到exe。

即使我们的项目只使用的一个requests包，但是可能我们还安装了其他n个包，但是他不管，因为包和包只有依赖关系的。比如我们只装了一个requests包，但是requests包会顺带装了一些其他依赖的小包，所以为了安全，只能将所有第三方包+python解释器一起打包。如下图所示。

蓝色表示是安装requests依赖的包，看到了吧！

Pyinstaller打包exe
这里呢，我就拿刚给同事写办公自动化脚本示例一下。源码示例效果，如下图所示。

动图封面
1、我们来将这个.py的文件打包成一个exe，我们直接cmd切换到这个脚本的目录，执行命令：pyinstaller-F setup.py，如下图所示。


ps: -F参数表示覆盖打包，这样在打包时，不管我们打包几次，都是最新的，这个记住就行，固定命令。

2、执行完毕之后，会生成几个文件夹，如下图所示。


3、在dist里面呢，就有了一个exe程序，这个就是可执行的exe程序，如下图所示。


4、我们把这个setup.exe拖到和setup.py平级的目录，我们来运行一下这个，效果图如下图所示。

动图封面
5、这样，我们就完成了一个打包工作，如果别人需要，即使没有python环境，他依然可以运行。

6、接下来我们再来打包一个带界面的，这里我用pyqt5写了一个最简单的框架，看一下打包成exe是否能运行成功，效果图如下图所示。

动图封面
我们可以看到，后面有一个黑洞洞的窗口，这就有点尴尬了，所以，我们的打包命令也要变一下。

7、执行 pyinstaller -F -wsetup.py 多加-w以后，就不会显示黑洞洞的控制台了，这里就不做演示啦！

8、但是我们打包的exe，我们的图标呀，实在是有点丑陋，默认的，没有一点自己的风格，那么，我们应该怎么改一下呢？

执行命令:pyinstaller -F -w-i wind.ico setup.py，如下图所示。


9、默认打包图片，如下图所示。


10、加上 -i 参数之后，如下图所示，会形成一个类似风力发电机的logo图案。


ps:程序路径最好全部都是英文，否则肯能会出现莫名其妙的问题

11、到此，我们能用到的pyton打包成exe命令都总结完了

总结命令
Pyinstaller -F setup.py 打包exe

Pyinstaller -F -w setup.py 不带控制台的打包

Pyinstaller -F -i xx.ico setup.py 打包指定exe图标打包

平常我们只需要这三个就好了，足够满足所有需求了。

如果对于Python感兴趣，那么除了网上的一些教程之外，Python书籍也是不可缺少的，个人觉得《Python编程从入门到精通》是非常适合零基础入门的，这本书可以让初学者打好Python基础。未来不管是从事Python的哪个方向，掌握这些基础知识都是必不可少的！

# pyQT 实现进度条
https://blog.51cto.com/u_15872074/5846693
