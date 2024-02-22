# 一、 Python 打包工具—Pyinstaller
PyInstaller 是一个可以将 Python 程序打包成一个独立可执行文件的软件包。它通过读取已经编写好的 Python 脚本，分析代码执行需要的模块和库，然后将其依赖库一同打包转成可以直接脱离于python环境下独立运行的程序，目前已经支持 在Windows、Linux 和 Mac OS 上运行。简单的理解就是，通过对程序脚本的打包（尤其是带有操作界面的程序），可以获得一个完整的软件。

下载命令
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller

其中 Pyinstaller 命令的参数，其中

>-F 参数代表制作独立的可执行程序。
>-w 是指程序启动的时候不会打开命令行。如果不加 -w 的参数，就会有黑洞洞的控制台窗口出来。此外，-w 参数在 GUI 界面时非常有用。
>-i就是指设置自己的图标图案，因为默认打包图片如下图所示。这个参数也可以写成 --icon=aiyc.ico

从上图中，我们可以看到最后打包成功了，打包成功之后会在当前目录下生成两个文件夹，我们的EXE文件就在dist文件夹中。

已经生成了一个exe 应用程序，看来已经成功一半了。

（4）我们把这个get_shortest_distance.exe拖到和get_shortest_distance.py平级的目录，双击运行一下这个exe。

参考  [打包详解](https://www.cnblogs.com/qhu-hjx/p/13036551.html)

# 二、Python 打包可执行exe文件

下面的路径要换成mac下的路径,路径是ico文件的绝对位置，在我们的工程里面就是 img/favicon.ico文件的位置

pyinstaller -F -w -i g:\2345Downloads\logo.ico main.py          

如果报 pyinstaller 不是可识别的命令，则需要把  C:\Users\orange\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts  设置到系统的环境变量里面

解释：进入到cmd命令行中，然后cd到我们的项目代码所在的具体的目录，在项目代码所在的目录中，使用上述代码进行打包。

其中，

-F ：大写，  打包成一个exe文件；
-w：小写，取消控制台显示；
-i  ：小写，忽略打包过程中遇到的错误，就是遇到错误也继续执行；
从这个项目文件目录安排上可以看出，这里没有在项目里放置更多的文件夹，一些代码文件都是散放在主文件夹中，在 pyinstaller -F -w -i之后放的是我们需要最终显示的图标的绝对路径，之后的第一个Python文件就是这个项目的主文件，之后使用--hidden-import导入这个项目中的一些其他的Python文件。

# 三、ico 图片生成
自己做的软件都喜欢放上自己的图标，不过哪来那么多 ico 图片呢？一个是可以找专门的 ico 图片网站，不过都很小众，图片库也很小。另一个是可以自己生成，这里就给大家分享一个网站，可以把其他格式图片转成 ico 格式：在线图片转icon格式 – 图片转换成icon在线工具 – 迅捷PDF转换器在线免费版

# custumertkinter 打包

pyinstaller -F -w -i  /E/sourcecode/gitproject/curio/04-sourcecode/0-parser/vediodownloader/logo.ico  main_tkinter.py --collect-all customtkinter -p ./


#  四、把图片打包进  exe 
   https://blog.csdn.net/ziigea/article/details/112647727

  4.1 先把图片转为base64数据 放到 python文件里面

'''python

import base64

def pictopy(picture_names, py_name):
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    write_data = []
    for picture_name in picture_names:
        filename = picture_name.replace('.', '_')
        open_pic = open("%s" % picture_name, 'rb')
        b64str = base64.b64encode(open_pic.read())
        open_pic.close()
        # 注意这边b64str一定要加上.decode()
        write_data.append('%s = "%s"\n' % (filename, b64str.decode()))

    f = open('%s.py' % py_name, 'w+')
    for data in write_data:
        f.write(data)
    f.close()


if __name__ == '__main__':
    pics = ["logo_2.png", "logo.png"]
    pictopy(pics, 'memory_pic')  # 将pics里面的图片写到 memory_pic.py 中
    print("ok")

'''

最终生成的数据  类似

logo_2_png = "iVBORw0KGgoAAAANSUhEUgAAAXcAAABgCAIA...太长省略"
logo_png = "iVBORw0KGgoAAAANSUhEUgAAAX0AAAClCAYAAACwYy2nAAAAAXNSR...太长省略"

4.2 使用的时候通过引用该python文件

取base64图片
logo = base64.b64decode(logo_png)<br>
logo_2 = base64.b64decode(logo_2_png)<br>

pyqt页面  base64转化QPixmap<br>

icon = QPixmap() <br>
icon.loadFromData(logo_2)<br>
self.label_logo.setPixmap(icon)

https://p.vryunpan.cc/

# 打包提速 
https://zhuanlan.zhihu.com/p/133303836/
# 解决打包慢
https://blog.51cto.com/micai01/5890445

