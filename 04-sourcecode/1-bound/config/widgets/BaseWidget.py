#coding=utf8
import base64
from operator import ne
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from manager.SystemContrl import *
from manager.UserControl import *
import time

import efinance as ef
import config.Errors, utils.logger
from pictures import *

WIDTH = 1000
HEIGHT = 600
PERIOD = 5  #默认5s一个检测周期

# 600519 300750

# 一分钟K线：6 7 11

class BaseWidget(QWidget): 

    def __init__(self, path):
        super(BaseWidget, self).__init__()          
        #self.setAutoFillBackground(True) 
        self.userCtrl = UserContrl()
        self.sysCtrl = SoftWareContrl()
        self.validPeriod = 3600 
        self.lastValidTime = 0
        self.LoginValid = False
        self.monitorMap = {}

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

    def fillStocksBase(self, frame, type, isMonitor = False):
        strA = ''
        for c in frame.columns.values:
            strA =f'{strA}<th>{c}</th>\n'
            
        logger.warning('fill the stock info')

        #是否按时间倒序排列
        if self.reverseSort:
           frame.sort_index(ascending=False,inplace=True)
           
        #print(self.colorPos)

        strB = ''
        count = 0;
        for index, row in frame.iterrows():
            strB = f'{strB}<tr>'
            count = count + 1
            if count >= self.showCnt:
                break

            count1 = 0
            for column in frame.columns:
                count1 = count1 + 1
                bc = ''
                v = frame[column].get(index)
                isDigital = isinstance(v, int) or isinstance(v, float)
                if count1 in self.colorPos and isDigital and v < 0:
                   bc = 'bgcolor="#00FF00"'
                elif count1 in self.colorPos and isDigital and v > 0:
                   bc = 'bgcolor="#FF0000"'

                strB = f'{strB}<th {bc}>{frame[column].get(index)}</th>'
            strB = f'{strB}</tr>'
        
        width = WIDTH
        strHtml = f'<html>\
        <head>\
        <title>{type}</title>\
        </head>\
        <body>\
         <table border="1" align="center" width={width} height={HEIGHT}>\
           <tr>{strA}</tr>\
           {strB}\
        </table>\
        </body>\
        </html>'

        self.text.setHtml(strHtml)

    def CheckValid(self):
        
        result = self.sysCtrl.clientValid()
        logger.warning(f'the client valid check {result.toString()}')
        if result == Errors.S_Forbidden:
           QMessageBox.question(self, "错误提示", "该版本的客户端已经禁止使用", QMessageBox.StandardButton.Yes)
           self.preCheckResult = False
           return False
           
        elif result == Errors.S_ClientFreeUse:
           self.preCheckResult = True
           return True

        elif result  != Errors.SUCCESS: 
           QMessageBox.question(self, "错误提示", "发生了未知错误请稍后重试", QMessageBox.StandardButton.Yes)
           self.preCheckResult = False 
           return False

        
        if self.LoginValid == True and (time.time() - self.lastValidTime)  < self.validPeriod:
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

        logger.warning(f'the user login success')
        self.LoginValid = True
        self.lastValidTime = time.time()
        return True

    def dispatchByType(self, codes, type):
        pass

    def startQuery(self):
        codesInput = self.stocks_code.text() 
        isValid = True
        if  not codesInput or codesInput.strip() == '':
            isValid = False

        if isValid == False:
           QMessageBox.question(self, "错误提示", "股票代码错误", QMessageBox.StandardButton.Yes) 
           self.preCheckResult = False
           return

        # 600519 300750
        
        isValid = self.CheckValid()
        if isValid == False:
            return
              
        logger.warning(f'start query the  code:{codesInput}.........')
        self.preCheckResult = True
        type = self.cb.currentText()
        codes = list(map(int, codesInput.strip().split()))
        self.dispatchByType(codes, type)
        
        logger.warning(f'query end  code: {codesInput}........')


    def refreshData(self):
        if not self.refreshButton.isChecked():
           return

        self.startQuery()
