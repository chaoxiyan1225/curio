from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import UserUITool
import sys, platform, random

from SystemContrl import *
from UserControl import *
from VedioDownLoadProcesser import *

import Errors

class ShenQiWidget(QWidget): 

    def __init__(self, path):
        super(ShenQiWidget, self).__init__()          
        #self.setAutoFillBackground(True) 

        self.userCtrl = UserContrl()
        self.sysCtrl = SoftWareContrl()
        self.downloadP = VedioDownLoadProcesser()
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
            self.resize(1000,600)
            self.text = QTextEdit()
            self.text.setStyleSheet("QTextEdit{background-color:rgba(0,0,0,0); border:0px;}")

            urlsStr = ''
            urls, code = self.sysCtrl.getAllUrlsArray()
            if code != Errors.SUCCESS:  
                QMessageBox.question(self, "错误提示", "获取经典推荐信息错误", QMessageBox.StandardButton.Yes) 
                self.preCheckResult = False
                return

            for url in urls:
                id1=url.id.ljust(6, '_')
                name1=url.name.ljust(10, '_')
                des1=url.descript.ljust(16, '_')
                urlsStr =f'{urlsStr}<li>编号:<font color="blue">{id1}</font>| 名称:<font color="blue">{name1}</font> | 简介:<font color="blue">{des1}</font> | 网址:<font color="blue">{url.url}</font>\n'

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
        self.resize(1000,600)
        self.progressValue = 0

        self.email_label = QLabel("您的邮箱*:")
        self.email = QLineEdit("")
        self.email.resize(80, 40)
        self.email.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        
        self.tel_label = QLabel('您的手机号*:')
        self.tel = QLineEdit("")
        self.tel.resize(80, 40)
        self.tel.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")


        self.register_button = QPushButton("点我注册")
        self.register_button.resize(80, 40)
        
        splash_pix = QPixmap('./dq.png')

        splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
        splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        splash.setEnabled(False)
     

        layout1 = QHBoxLayout()
        layout1.addWidget(self.email_label)
        layout1.addWidget(self.email)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.tel_label)
        layout2.addWidget(self.tel)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addWidget(self.register_button)
        layout.addWidget(splash)

        self.setLayout(layout)
        self.register_button.clicked.connect(self.sendMsg4Register)


class BuyNow(ShenQiWidget):

    def initUI(self):

        self.setWindowTitle("当前位于续费界面")
        self.resize(1000,600)

        self.text = QTextEdit()

        self.text.setStyleSheet("QTextEdit{background-color:rgba(0,0,0,0); border:0px;}")

        str = '<html>\
        <head>\
        <title>当前位于续费页面</title>\
        </head>\
        <body>\
        <h1><font color="yellow">撸片神器使用须知</font></h1>\
        <ul>\
          <li>初次注册后可以免费使用1周,不限下载次数</li>\
          <li>软件仅支持一台电脑登陆使用</li>\
          <li>试用期过后半年49¥，全年89¥，不限下载次数</li>\
        </ul>\
        <h1><font color="yellow">付费通道</font></h1>\
          <div>\
            <font color="yellow">微信支付:请支付时务必备注您的</font><font color="red"><strong>VIP注册号</strong></font><br/>\
            <img src="./ld.png" width="160" height="160"/>\
            <br/>\
            <br>\
            <font color="yellow">支付宝支付:请支付时务必备注您的</font><font color="red"><strong>VIP注册号</strong></font><br/>\
            <img src="./ld.png" width="160" height="160"/>\
           </div>\
        </body>\
        </html>'

        self.text.setHtml(str)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.text)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        self.setLayout(layout)


class Download(ShenQiWidget):

    def CheckValid(self):
        
        if self.LoginValid == True and (timer.time() - self.lastValidTime)  < self.validPeriod:
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

        isValid = self.CheckValid()
        if isValid == False:
           return 
        
        self.preCheckResult = true
        self.downLoadind(url)

    def downLoadind(self, url):

        self.downloadP.downLoadStart(url)

        #设置初始进度条为0
        self.progerss_value = 0
        self.percent.setText('0/100')
        self.timer.start(150)

    def freshProgress(self):

        percent = self.downloadP.getPercent()
        if  percent >= 1:
            self.percent.setText('100/100') 
            self.timer.stop()
        else: 
            self.percent.setText(f'{percent}/100')   
            

    def initUI(self):

        self.setWindowTitle("当前位于下载界面")
        self.resize(1000,600)
        self.progressValue = 0

        self.file_label = QLabel("请输入下载URL")
        self.file_url = QLineEdit("")
        self.file_url.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.file_button = QPushButton("点我下载")

        pe = QPalette()
        pe.setColor(QPalette.ColorRole.WindowText,QColor("green"))#设置字体颜色
        self.file_label.setAutoFillBackground(True)#设置背景充满，为设置背景颜色的必要条件
        pe.setColor(QPalette.ColorRole.Window,QColor('grey'))#设置背景颜色
        #pe.setColor(QPalette.Background,Qt.blue)<span style="font-family: Arial, Helvetica, sans-serif;">#设置背景颜色，和上面一行的效果一样
        self.file_label.setPalette(pe)

        '''
        splash_pix = QPixmap('')
        splash_pix = splash_pix.scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        '''
   
        self.splash = QSplashScreen(QPixmap(''), Qt.WindowType.WindowStaysOnTopHint)
        self.splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.splash.setEnabled(False)
        self.progressBar = QProgressBar(self.splash)

        self.progressBar.setValue(0)

        self.progerss_value = 0 

        layout1 = QHBoxLayout()
        layout1.addWidget(self.file_label)
        layout1.addWidget(self.file_url)
        layout1.addWidget(self.file_button)

        self.progress_label = QLabel("【下载进度】")
        self.progress_label.setPalette(pe)

        self.percent = QLabel('0/100')
        layout2 = QHBoxLayout()
        layout2.addWidget(self.progress_label)
        layout2.addWidget(self.progressBar)
        layout2.addWidget(self.percent)

        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel(''))
        layout3.addWidget(self.splash)
        layout3.addLayout(layout2)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout3)

        self.timer = QTimer()
        self.setLayout(layout)
        self.file_button.clicked.connect(self.startDownLoad)
        self.timer.timeout.connect(self.freshProgress)


class MainWindow(QMainWindow):
    
   def __init__(self):
        super().__init__()

        self.setWindowTitle("撸片神器-V2.0.6.8")
        self.resize(800,  600)  

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)

        tabs.addTab(Download("./dl.png"), "点我撸片")
        tabs.addTab(AdviceUrls("./ld.png"), "经典推荐")
        tabs.addTab(BuyNow("./buy.png"), "续费入口")
        tabs.addTab(Register("./rg.png"), "一键注册")

        self.setCentralWidget(tabs)
        
def main():
    # 整个app的入口    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
   
if __name__ == "__main__":
    print ('开启撸片之旅')
    main()
    print('撸片之旅结束')
