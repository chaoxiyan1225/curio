#coding=utf8
import base64
from operator import ne
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from manager.SystemContrl import *
from manager.UserControl import *
from widgets.BaseWidget import *

import efinance as ef
from pictures import *

# 600519 300750

# 一分钟K线：6 7 11

class ShowFund(BaseWidget):

    def filleFundBaseInfo(self, frames, type):
        tables = '';
        for frame in frames:
            strA = ''
            for c in frame.columns.values:
                strA =f'{strA}<th>{c}</th>\n'

            strB = ''
            for index, row in frame.iterrows():
                strB = f'{strB}<tr>'

                for column in frame.columns:
                    strB = f'{strB}<th>{frame[column].get(index)}</th>'
                strB = f'{strB}</tr>'

            width = WIDTH - 100
            height = HEIGHT - 500
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
        self.colorPos.clear()
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
           self.reverseSort = False
           self.colorPos.append(4) 
           frame = ef.fund.get_quote_history(codes[0])
           self.fillStocksBase(frame, type)          
        elif type == '全部公墓基金名单':
           self.reverseSort = False
           frame = ef.fund.get_fund_codes()
           self.fillStocksBase(frame, type)        
        elif type == '股票占比数据':
           self.reverseSort = False
           self.colorPos.append(5) 
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
        self.colorPos = []

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
