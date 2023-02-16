from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import UserUITool
import sys, platform, random

from SystemContrl import *
from UserControl import *

import efinance as ef

import Errors

WIDTH = 1200
HEIGHT = 800

class BaseWidget(QWidget): 

    def __init__(self, path):
        super(BaseWidget, self).__init__()          
        #self.setAutoFillBackground(True) 

        self.userCtrl = UserContrl()
        self.sysCtrl = SoftWareContrl()
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

    def fillStocksBase(self, frame, type):
        strA = ''
        for c in frame.columns.values:
            strA =f'{strA}<th>{c}</th>\n'
      
        #是否按时间倒序排列
        if self.reverseSort:
           frame.sort_index(ascending=False,inplace=True)

        strB = ''
        count = 0;
        for index, row in frame.iterrows():
            strB = f'{strB}<tr>'
            count = count + 1
            if count >= self.showCnt:
                break

            for column in frame.columns:
                strB = f'{strB}<th>{frame[column].get(index)}</th>'
            strB = f'{strB}</tr>'

        print(f'当前显示条数：{count}, showCnt={self.showCnt}, 查询类型{type}')
         
        width = WIDTH - 100
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
        '''
        isValid = self.CheckValid()
        if isValid == False:
           return 
        '''
        self.preCheckResult = True
        type = self.cb.currentText()
        codes = list(map(int, codesInput.strip().split()))
        
        self.dispatchByType(codes, type)


    def refreshData(self):
        if not self.refreshButton.isChecked():
           return

        self.startQuery()

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


class BuyNow(BaseWidget):

    def initUI(self):

        self.setWindowTitle("当前位于续费界面")
        self.resize(WIDTH,HEIGHT)
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


class ShowStock(BaseWidget):

    def dispatchByType(self, codes, type):
        self.reverseSort = False
        if type == '股票信息':
           self.reverseSort = False
           frame = ef.stock.get_base_info(codes)
           self.fillStocksBase(frame , type)
        elif type == '1分钟K线':
           self.reverseSort = True
           frame = ef.stock.get_quote_history(codes, klt=1)[codes[0]]
           self.fillStocksBase(frame, type)        
        elif type == '5分钟K线':
           self.reverseSort = True
           frame = ef.stock.get_quote_history(codes, klt=5)[codes[0]]
           self.fillStocksBase(frame, type)       
        elif type == '历史K线':
           self.reverseSort = True
           frame = ef.stock.get_quote_history(codes)[codes[0]]
           self.fillStocksBase(frame, type)        
        elif type == '历史单子流入':
           self.reverseSort = True
           frame = ef.stock.get_history_bill(codes[0])
           self.fillStocksBase(frame, type)
        elif type == '最近一日单子流入':
           self.reverseSort = True
           frame = ef.stock.get_today_bill(codes[0])
           self.fillStocksBase(frame, type)
        elif type == '沪深市场A股近况':
           self.reverseSort = False
           frame = ef.stock.get_realtime_quotes()
           self.fillStocksBase(frame, type)
        elif type == '股票龙虎榜':
           self.reverseSort = False
           frame = ef.stock.get_daily_billboard()
           self.fillStocksBase(frame, type)

    def initUI(self):

        self.setWindowTitle("当前位于下载界面")
        self.resize(WIDTH,HEIGHT)
        self.progressValue = 0
        self.showCnt = 200

        self.stocks_label = QLabel("股票代码")
        self.stocks_code = QLineEdit("")
        self.stocks_code.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.cb=QComboBox()
        self.cb.addItem('股票信息')
        self.cb.addItem('1分钟K线')
        self.cb.addItem('5分钟K线')
        self.cb.addItem('历史K线')
        self.cb.addItem('历史单子流入')
        self.cb.addItem('最近一日单子流入')
        self.cb.addItem('沪深市场A股近况')
        self.cb.addItem('股票龙虎榜')
        #多个添加条目
        #当下拉索引发生改变时发射信号触发绑定的事件
        self.cb.currentIndexChanged.connect(self.startQuery)
        self.refreshButton=QRadioButton('自动5秒刷新')
        self.refreshButton.setChecked(False)

        self.queryButton = QPushButton("点我查询")

        self.layout = QVBoxLayout()
        self.queryButton.clicked.connect(self.startQuery)
        
        self.layout0 =  QHBoxLayout()
        self.layout0.addWidget(self.stocks_label)
        self.layout0.addWidget(self.stocks_code)
        self.layout0.addWidget(self.cb)
        self.layout0.addWidget(self.refreshButton)
        self.layout0.addWidget(self.queryButton)
        #self.layout0.addWidget(self.stopButton)

        self.layout.addLayout(self.layout0)

        self.text = QTextEdit()
        self.text.setStyleSheet("QTextEdit{background-color:rgba(0,0,0,0); border:0px;}")

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.text)
        self.layout.addLayout(self.layout1)

        self.setLayout(self.layout)
        self.timer = QTimer()
        self.timer.start(5000) 
        self.timer.timeout.connect(self.refreshData)

class ShowFund(BaseWidget):
   
    def filleFundBaseInfo(self, frames, type):

        tables = '';
        for frame in frames:
            strA = ''
            for c in frame.columns.values:
                strA =f'{strA}<th>{c}</th>\n'
          
            #是否按时间倒序排列
            if self.reverseSort:
               frame.sort_index(ascending=False,inplace=True)

            strB = ''
            count = 0;
            for index, row in frame.iterrows():
                strB = f'{strB}<tr>'
                count = count + 1
                if count >= self.showCnt:
                    break

                for column in frame.columns:
                    strB = f'{strB}<th>{frame[column].get(index)}</th>'
                strB = f'{strB}</tr>'

            width = WIDTH - 100
            height = HEIGHT - 700
            table = f'<table border="1" cellpadding = "10" width={width} height={height}>\
                        <tr>{strA}</tr>\
                            {strB}\
                      </table>'
            tables = f'{tables}{table}<br><br>'

        strHtml = f'<html>\
                        <head>\
                        <title>{type}</title>\
                        </head>\
                        <body>\
                           {tables}\
                        </body>\
                    </html>'

        self.text.setHtml(strHtml)


    def dispatchByType(self, codes, type):
        self.reverseSort = False
        if type == '基金信息':
           self.reverseSort = False
           frame1 = ef.fund.get_base_info(codes)
           frame2 = ef.fund.get_realtime_increase_rate(f'{codes[0]}')
           frame3 = ef.fund.get_types_percentage(codes[0])

           frames = []
           frames.append(frame1)
           frames.append(frame2)
           frames.append(frame3)
           self.filleFundBaseInfo(frames, type)     
        elif type == '历史净值信息':
           self.reverseSort = True
           frame = ef.fund.get_quote_history(codes[0])
           self.fillStocksBase(frame, type)       
        elif type == '全部公墓基金名单':
           self.reverseSort = False
           frame = ef.fund.get_fund_codes()
           self.fillStocksBase(frame, type)        
        elif type == '股票占比数据':
           self.reverseSort = False
           frame = ef.fund.get_invest_position(codes[0])
           self.fillStocksBase(frame, type)
        elif type == '阶段涨跌幅度':
           self.reverseSort = True
           frame = ef.fund.get_period_change(codes[0])
           self.fillStocksBase(frame, type)

    def initUI(self):

        self.setWindowTitle("当前位于基金界面")
        self.resize(WIDTH,HEIGHT)
        self.progressValue = 0
        self.showCnt = 200

        self.stocks_label = QLabel("基金代码")
        self.stocks_code = QLineEdit("")
        self.stocks_code.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.cb=QComboBox()
        self.cb.addItem('基金信息')
        self.cb.addItem('历史净值信息')
        self.cb.addItem('全部公墓基金名单')
        self.cb.addItem('股票占比数据')
        self.cb.addItem('阶段涨跌幅度')
        #多个添加条目
        #当下拉索引发生改变时发射信号触发绑定的事件
        self.cb.currentIndexChanged.connect(self.startQuery)
        self.refreshButton=QRadioButton('自动5秒刷新')
        self.refreshButton.setChecked(False)

        self.queryButton = QPushButton("点我查询")

        self.layout = QVBoxLayout()
        self.queryButton.clicked.connect(self.startQuery)
        
        self.layout0 =  QHBoxLayout()
        self.layout0.addWidget(self.stocks_label)
        self.layout0.addWidget(self.stocks_code)
        self.layout0.addWidget(self.cb)
        self.layout0.addWidget(self.refreshButton)
        self.layout0.addWidget(self.queryButton)
        #self.layout0.addWidget(self.stopButton)

        self.layout.addLayout(self.layout0)

        self.text = QTextEdit()
        self.text.setStyleSheet("QTextEdit{background-color:rgba(0,0,0,0); border:0px;}")

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.text)
        self.layout.addLayout(self.layout1)

        self.setLayout(self.layout)
        self.timer = QTimer()
        self.timer.start(5000) 
        self.timer.timeout.connect(self.refreshData)


class MainWindow(QMainWindow):
    
   def __init__(self):
        super().__init__()

        self.setWindowTitle("牛牛飞天-V2.0.6.8")
        self.resize(WIDTH,HEIGHT) 

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)

        tabs.addTab(ShowStock("./stock.png"), "股票操作")
        tabs.addTab(ShowFund("./fund.png"), "基金操作")
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
    print ('开始发财')
    main()
    print('财已到手')
