#coding=utf8
import base64
from operator import ne
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import utils.UserUITool, utils.CommonTool
from threading import Thread

from manager.SystemContrl import *
from manager.UserControl import *

import efinance as ef
import config.Errors, utils.logger
from pictures import *
from widgets.BaseWidget import *

class Register(BaseWidget):
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

class BuyNow(BaseWidget):

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


        l1 = QLabel("牛牛飞天软件使用须知:")
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

        '''
        l7 = QLabel("  2)支付宝:请支付时务必备注您的VIP注册号:")
        l7.setFont(font2)
        
        zhifubaoPng  = base64.b64decode(zhifubao_png)
        # pyqt页面  base64转化QPixmap
        zhifubaoIcon = QPixmap()
        zhifubaoIcon.loadFromData(zhifubaoPng)
        zhifubaoIcon.scaled(300, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation); 

        zfb = QLabel(self)
        zfb.setPixmap(zhifubaoIcon)  # 在label上显示图片
        zfb.setFixedSize(300, 400)
        '''
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
