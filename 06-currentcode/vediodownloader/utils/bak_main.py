from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
import useruitool as UserUITool
import sys, platform, random

from service.systemcontrol import *
from service.usercontrol import *
from service.vediodownloadprocesser import *
from conf.pictures import *


import conf.errors as Errors

WIDTH = 800
HEIGHT = 600

def bytes_to_mb(bytes):  
     KB = 1024 # 1KB为1024字节  
     MB = KB * 1024 # 1MB是1024KB  
     return int(bytes/MB)

class ShenQiWidget(QWidget): 

    def __init__(self, path):
        super(ShenQiWidget, self).__init__()          
        #self.setAutoFillBackground(True) 

        self.userCtrl = UserContrl()
        self.sysCtrl = SoftWareContrl()
        self.downloadP = None
        self.validPeriod = 3600 
        self.lastValidTime = 0
        self.LoginValid = False

        background_color = QColor()
        background_color.setNamedColor('#282821')

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, background_color)
        self.setPalette(palette)
        self.path = path
        self.threadpool = QtCore.QThreadPool()
        self.initUI()

    def initUI(self):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.path)
        painter.drawPixmap(self.rect(), pixmap)

    def center(self):
        """居中显示"""
        self.win_rect = self.frameGeometry()     #获取窗口矩形
        self.screen_center = self.screen().availableGeometry().center()      #屏幕中心
        self.win_rect.moveCenter(self.screen_center)      # 移动窗口矩形到屏幕中心
        self.move(self.win_rect.center)         # 移动窗口与窗口矩形重合

#经典推荐入口
class AdviceUrls(ShenQiWidget):

    def initUI(self):

            self.setWindowTitle("当前位于经典推荐页面")
            self.resize(WIDTH,HEIGHT)
            self.text = QTextEdit()
            self.text.setStyleSheet("QTextEdit{background-color:rgba(0,0,0,0); border:0px;}")
            
            h = HEIGHT - 300
            w = WIDTH - 200
            urlsStr =   f'<table border="1" align="center" width={w} height={h}>\
                   <tr><th>编号</th><th>名称</th><th>简介</th><th>网址</th></tr><tr>'
            urls, code = self.sysCtrl.getAllUrlsArray()
            if code != Errors.SUCCESS:  
                QMessageBox.question(self, "错误提示", "获取经典推荐信息错误", QMessageBox.StandardButton.Yes) 
                self.preCheckResult = False
                return

            for url in urls:
         
                id1=url.id.ljust(6, '_')
                name1=url.name.ljust(10, '_')
                des1=url.descript.ljust(16, '_')
                urlsStr =f'{urlsStr}<tr><th>{id1}</th><th>{name1}</th><th>{des1}</th> <th>{url.url}</th></tr>\n' 
            
            urlsStr = f'{urlsStr}</table>'    

            str = f'<html>\
            <head>\
            <title>当前位于经典推荐页面</title>\
            </head>\
            <body>\
            <h1><font color="yellow">推荐资源列表</font></h1>\
            --------------------------------------------------------------------------------------------------\
            <ul>\
              {urlsStr}\
            </ul>\
            <br>\
            <br>\
            <h1><font color="yellow">版权声明:<font color="red"><strong>您必须是VIP注册用户</strong></font></font></h1>\
              <div>\
                <ul>\
                   <li>1.不得私自转售</li>\
                   <li>2.不得上传到其他平台</li>\
                </ul>\
                <br/>\
                <br>\
               </div>\
            </body>\
            </html>'

            self.text.setHtml(str)
            layout1 = QHBoxLayout()
            layout1.addWidget(self.text)

            layout = QVBoxLayout()
            layout.addLayout(layout1)
            self.setLayout(layout)


class Register(ShenQiWidget):
    def checkValid(self):
        email = self.email.text()        
        isValid = UserUITool.IsValidEmail(email)

        if isValid == False:
            QMessageBox.question(self, "错误提示", "输入的邮箱非法", QMessageBox.StandardButton.Yes) 
            self.preCheckResult = False
            return False

        tel = self.tel.text()        
        isValid = UserUITool.IsValidTel(tel)

        if isValid == False:
            QMessageBox.question(self, "错误提示", "输入的手机号非法", QMessageBox.StandardButton.Yes) 
            self.preCheckResult = False
            return False

        return True


    def sendMsg4Register(self):

        isValid = self.checkValid()
        if isValid == False:
            return

        #text, ok = QInputDialog.getText(self, '用户注册提示界面', '输入邮箱')

        isSend = self.userCtrl.clickToRegister(self.email.text(), self.tel.text())
        if isSend == Errors.SUCCESS:
           QMessageBox.question(self, "成功提示", "您的注册申请{成功}注意查收邮件", QMessageBox.StandardButton.Yes) 
           return True

        QMessageBox.question(self, "错误提示", "您的注册申请{失败}请稍后重试", QMessageBox.StandardButton.Yes) 
        return False


    def initUI(self):
        self.setWindowTitle("当前位于注册界面")
        self.resize(WIDTH,HEIGHT)
        self.progressValue = 0

        self.email_label = QLabel("您的邮箱*:")
        self.email = QLineEdit("")
        self.email.resize(80, 40)
        self.email.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        
        self.tel_label = QLabel('您的手机号*:')
        self.tel = QLineEdit("")
        self.tel.resize(80, 40)
        self.tel.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        self.name_label = QLabel('您的姓名:')
        self.name = QLineEdit("")
        self.name.resize(80, 40)
        self.name.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        self.msg = QLabel("【注意】上述的邮箱跟手机号都是必填项，请注意格式正确，否则无法提交。姓名不是必填项目")
        self.msg.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        p = QPalette()
        p.setColor(QPalette.ColorRole.WindowText, QColor('blue'))
        self.msg.setPalette(p)

        self.register_button = QPushButton("点我注册")
        self.register_button.resize(40, 20)
        self.register_button.setStyleSheet("QPushButton{font-family:'宋体';font-size:16px;color:rgb(0,0,0);}\
                               QPushButton{background-color:rgb(170,200,50)}\ QPushButton:hover{background-color:rgb(50, 170, 200)}")

        dq  = base64.b64decode(dq_png)
        # pyqt页面  base64转化QPixmap
        icon = QPixmap()
        icon.loadFromData(dq)
        icon.scaled(WIDTH, HEIGHT, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation); 

        splash = QSplashScreen(icon, Qt.WindowType.WindowStaysOnTopHint)
        splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        splash.setEnabled(False)
     
        layout1 = QHBoxLayout()
        layout1.addWidget(self.email_label)
        layout1.addWidget(self.email)
        layout1.addWidget(self.tel_label)
        layout1.addWidget(self.tel)
        layout1.addWidget(self.name_label)
        layout1.addWidget(self.name)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.msg)
        layout2.addWidget(self.register_button)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addWidget(splash)

        self.setLayout(layout)
        self.register_button.clicked.connect(self.sendMsg4Register)


class BuyNow(ShenQiWidget):

    def initUI(self):

        self.setWindowTitle("当前位于续费界面")
        self.resize(WIDTH,HEIGHT)

        font1 = QFont()
        font1.setPointSize(20) 
        p1 = QPalette()
        p1.setColor(QPalette.ColorRole.WindowText, QColor('red'))


        font2 = QFont()
        font2.setPointSize(16) 
        p2 = QPalette()
        p2.setColor(QPalette.ColorRole.WindowText, QColor('blue'))


        l1 = QLabel("撸片神器使用须知:")
        l1.setFont(font1)
        l1.setPalette(p1)

        l2 = QLabel("   1)初次注册后可以免费使用1周,不限下载次数")
        l3 = QLabel("   2)软件仅支持一台电脑登陆使用")
        l4 = QLabel("   3)试用期过后半年49¥，全年89¥，不限下载次数")
        l2.setFont(font2)
        l3.setFont(font2)
        l4.setFont(font2)

        l5 = QLabel("付费通道")
        l5.setFont(font1)
        l5.setPalette(p2)

        l6 = QLabel("  微信支付:请支付时务必备注您的VIP注册号:")
        l6.setFont(font2)

        weixinPng  = base64.b64decode(weixin_png)
        # pyqt页面  base64转化QPixmap
        weixinIcon = QPixmap()
        weixinIcon.loadFromData(weixinPng)
        weixinIcon.scaled(300, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation); 

        wx = QLabel(self)
        wx.setPixmap(weixinIcon)  # 在label上显示图片
        wx.setFixedSize(300, 350)
        layout = QVBoxLayout()
        layout.addWidget(l1)
        layout.addWidget(l2)
        layout.addWidget(l3)
        layout.addWidget(l4)
        layout.addWidget(l5)
        layout.addWidget(l6)
        layout.addWidget(wx)
        #layout.addWidget(l7)
        #layout.addWidget(zfb)
        self.setLayout(layout)



class Download(ShenQiWidget):
    progressChanged = QtCore.pyqtSignal(int)

    def CheckValid(self):
        
        if self.LoginValid == True and (timer.time() - self.lastValidTime)  < self.validPeriod:
            return True
            
            
        result = self.sysCtrl.clientValid()
        logger.warn(f'the client valid check {result.toString()}')
        if result == Errors.S_Forbidden:
           QMessageBox.question(self, "错误提示", "该版本的客户端已经禁止使用", QMessageBox.StandardButton.Yes)
           self.preCheckResult = False
           return False
           
        elif result == Errors.S_ClientFreeUse:
           self.preCheckResult = True
           return True

        result = self.userCtrl.LoginCheck()
        if result == Errors.C_InvalidUser:
           QMessageBox.question(self, "错误提示", "您还未注册，请点击右上角一键注册", QMessageBox.StandardButton.Yes) 
           self.preCheckResult = False
           return False

        elif result == Errors.C_Arrearage:
           QMessageBox.question(self, "错误提示", "您已欠费请续费", QMessageBox.StandardButton.Yes)
           self.preCheckResult = False
           return
        elif result != Errors.SUCCESS:
           QMessageBox.question(self, "错误提示", "发生了未知错误请稍后重试", QMessageBox.StandardButton.Yes)
           self.preCheckResult = False
           return False

        result = self.sysCtrl.clientValid()

        if result == Errors.S_Forbidden:
           QMessageBox.question(self, "错误提示", "该版本的客户端已经禁止使用", QMessageBox.StandardButton.Yes)
           self.preCheckResult = False
           return False

        elif result  != Errors.SUCCESS: 
           QMessageBox.question(self, "错误提示", "发生了未知错误请稍后重试", QMessageBox.StandardButton.Yes)
           self.preCheckResult = False 
           return False

        self.LoginValid = True
        self.lastValidTime = time.time()
        return True


    def startDownLoad(self):
        url = self.file_url.text()        
        isValid = UserUITool.IsValidUrl(url)

        if isValid == False:
           QMessageBox.question(self, "错误提示", "下载地址不正确请重新输入", QMessageBox.StandardButton.Yes) 
           self.preCheckResult = False
           return

        #isValid = self.CheckValid()
        #if isValid == False:
        #   return 
        
        name = self.name.text()
        self.preCheckResult = True
        
        logger.warn(f'后台线程去执行下载')
        self.downloadP = VedioDownLoadProcesser()
        t = threading.Thread(target=self.downLoading, args=(url, name))
        t.start()
        t2 = threading.Thread(target=self.inside_thread)
        t2.start()
        
            
    def downLoading(self, url, name):
    
        try:
           self.downloadP.downLoadStart(url, name)
 
        except  BaseException as e1:
           logger.error(f"the input url:{url} not valid, and error msg: {str(e1)}")
           QMessageBox.question(self, "错误提示", "输入的影片网址不对请重新输入", QMessageBox.StandardButton.Yes)
           return
        except Exception as ex:
           logger.error(f"the input url:{url} download error, and error msg: {str(ex)}")         
           QMessageBox.question(self, "错误提示", "下载出现问题请稍后重试", QMessageBox.StandardButton.Yes)
           return

        #设置初始进度条为0
        self.progerss_value = 1
        
    def inside_thread(self):
        percent = 1
        while percent < 100:
            percent = 1 if self.downloadP.getPercent() == 0 else self.downloadP.getPercent()
            self.progressChanged.emit(percent)
            time.sleep(5)
        
        if percent == 100:
           self.progressChanged.emit(100)
                  
    def setPercentV(self):
        percent = 1 if self.downloadP.getPercent() == 0 else self.downloadP.getPercent()
        
        logger.warn(f'当前进度{percent}')
        if  percent >= 0:
            #self.percent.setText(f'{percent}/100')
            self.progressBar.setValue(percent)
            #self.timer.stop()

    def initUI(self):

        self.setWindowTitle("当前位于下载界面")
        self.resize(WIDTH,HEIGHT)
        self.progressValue = 0

        self.file_label = QLabel("请输入下载URL")
        self.file_url = QLineEdit("")
        self.file_url.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        
        self.name_label = QLabel("输入影片名")
        self.name = QLineEdit("")
        self.name.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.file_button = QPushButton("点我下载")
        
        self.speedLable = QLabel("【当前网络情况】")
        #speed_test = Speedtest() 
 
        #download_speed = bytes_to_mb(speed_test.download())
        
        result = f'当前的下载速度是11MB/s'
        
        self.speedLine = QLineEdit(result)
        self.speedLine.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
 
 
     

        pe = QPalette()
        pe.setColor(QPalette.ColorRole.WindowText,QColor("green"))#设置字体颜色
        self.file_label.setAutoFillBackground(True)#设置背景充满，为设置背景颜色的必要条件
        pe.setColor(QPalette.ColorRole.Window,QColor('grey'))#设置背景颜色
        #pe.setColor(QPalette.Background,Qt.blue)<span style="font-family: Arial, Helvetica, sans-serif;">#设置背景颜色，和上面一行的效果一样
        self.file_label.setPalette(pe)
        
        self.name_label.setAutoFillBackground(True)#设置背景充满，为设置背景颜色的必要条件
        self.name_label.setPalette(pe)
        

        '''
        splash_pix = QPixmap('')
        splash_pix = splash_pix.scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        '''
        
        ab  = base64.b64decode(dq_png)
        # pyqt页面  base64转化QPixmap
        icon = QPixmap()
        icon.loadFromData(ab)
        icon.scaled(WIDTH, HEIGHT, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation); 
        
        self.splash = QSplashScreen(icon, Qt.WindowType.WindowStaysOnTopHint)
        self.splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.splash.setEnabled(False)
   
        self.progressBar = QProgressBar(self.splash)

        self.progressBar.setValue(0)
        self.progressChanged.connect(self.progressBar.setValue)

        self.progerss_value = 0 

        layout1 = QHBoxLayout()
        layout1.addWidget(self.file_label)
        layout1.addWidget(self.file_url)
        layout1.addWidget(QLabel('  |  '))
        layout1.addWidget(self.name_label)
        layout1.addWidget(self.name)
        layout1.addWidget(self.file_button)


        self.progress_label = QLabel("【下载进度】")
        self.progress_label.setPalette(pe)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.progress_label)
        layout2.addWidget(self.progressBar)
        #layout2.addWidget(self.percent)
        
        layout2_1 = QHBoxLayout()
        layout2_1.addWidget(self.speedLable)
        layout2_1.addWidget(self.speedLine)
        #layout2.addWidget(self.percent)

        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel(''))
        layout3.addWidget(self.splash)
        layout3.addLayout(layout2)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2_1)
        layout.addLayout(layout3)

        #self.timer = QTimer()
        self.setLayout(layout)
        self.file_button.clicked.connect(self.startDownLoad)
        #self.timer.timeout.connect(self.freshProgress)
        self.progressChanged.connect(self.setPercentV)


class MainWindow(QMainWindow):
    
   def __init__(self):
        super().__init__()

        self.setWindowTitle("撸片神器-V2.0.6.8")
        self.resize(WIDTH,HEIGHT) 

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)
        
        
        stock = base64.b64decode(stock_png)
        fund = base64.b64decode(fund_png)
        buy = base64.b64decode(buy_png)
        rg  = base64.b64decode(rg_png)
        icon  = base64.b64decode(icon_png)
        
        iconDL = QPixmap()
        iconDL.loadFromData(stock)
        
        iconSuggest = QPixmap()
        iconSuggest.loadFromData(fund)
        iconBuy = QPixmap()
        iconBuy.loadFromData(buy)
        
        iconRg = QPixmap()
        iconRg.loadFromData(rg)
        iconIcon = QPixmap()
        iconIcon.loadFromData(icon)
        
        self.setWindowIcon(QIcon(iconIcon))
        tabs.addTab(Download(iconDL), "点我撸片")
        tabs.addTab(AdviceUrls(iconSuggest), "经典推荐")
        tabs.addTab(BuyNow(iconBuy), "续费入口")
        tabs.addTab(Register(iconRg), "一键注册")

        self.setCentralWidget(tabs)
        
def main():
    # 整个app的入口    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
   
if __name__ == "__main__":
    logger.warning ('开启撸片之旅')
    try:
      main()
    except Exception as e:
      logger.error(f'the error happens: {str(e)}')
    
    logger.warn('撸片之旅结束')
