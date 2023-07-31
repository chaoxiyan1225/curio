#coding=utf8
from operator import ne
from pickle import TRUE
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from manager.SystemContrl import *
from manager.UserControl import *
import time
from widgets.BaseWidget import *
import efinance as ef
import utils.logger
from pictures import *

# 600519 300750

# 一分钟K线：6 7 11

def needMonitor(map, k, period = PERIOD):
    if not map.get(k):
        map[k] = time.time()
        return True
    else:
        if time.time() > map[k] + period:
            return True
    return False

class ShowStock(BaseWidget):

   def dispatchByType(self, codes, type):
        self.reverseSort = False
        self.colorPos.clear()
        if type == '股票信息':
           logger.warning('get the stock info')
           self.reverseSort = False
           frame = ef.stock.get_base_info(codes)
           logger.warning('get the stock info end')
           self.fillStocksBase(frame , type)
        elif type == '1分钟K线':
           self.reverseSort = True
           self.colorPos.append(11)
           self.colorPos.append(12)
           frame = ef.stock.get_quote_history(codes, klt=1)[codes[0]]
           self.fillStocksBase(frame, type)        
        elif type == '5分钟K线':
           self.reverseSort = True
           self.colorPos.append(11)
           self.colorPos.append(12)
           frame = ef.stock.get_quote_history(codes, klt=5)[codes[0]]
           self.fillStocksBase(frame, type)       
        elif type == '历史K线':
           self.reverseSort = True
           self.colorPos.append(11)
           self.colorPos.append(12)
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
           self.colorPos.append(6)
           frame = ef.stock.get_daily_billboard()
           self.fillStocksBase(frame, type)

   def initUI(self):

        self.setWindowTitle("当前位于下载界面")
        self.resize(WIDTH,HEIGHT)
        self.progressValue = 0
        self.showCnt = 200
        self.colorPos = []
        self.stocks_label = QLabel("股票代码")
        self.stocks_code = QLineEdit("")
        self.stocks_code.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.cb=QComboBox()
        self.cb.addItem('股票信息')
        self.cb.addItem('1分钟K线')
        self.cb.addItem('5分钟K线')
        #self.cb.addItem('历史K线')
        self.cb.addItem('历史单子流入')
        self.cb.addItem('最近一日单子流入')
        #self.cb.addItem('沪深市场A股近况')
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

class SuggestStock(BaseWidget):

   def fillMatchStocks(self, frame):
          
        def needAdd(sList, target):
            if sList[0] <= -1:
               if sList[1] > -1:
                  return target <= sList[1]
               else:
                  return True
            else:
               if sList[1] > -1:
                  return target >= sList[0] and target <= sList[1]
               else:
                  return target >= sList[0]

        strA = ''
        for c in frame.columns.values:
            strA =f'{strA}<th>{c}</th>\n'
        
        strB = ''
        count = 0;
        for index, row in frame.iterrows():
            strTmp = f'<tr>'
            pos = 0
            isOK = True
            for column in frame.columns:
               pos = pos + 1
               v = frame[column].get(index)
               isDigital = isinstance(v, int) or isinstance(v, float)

               bc = ''
               isIn = pos in self.searchPos.keys()
               if isIn:
                  if isDigital == False:
                     isOK = False
                     break;
                  else:
                     if needAdd(self.searchPos.get(pos), float(v)) == False: 
                        isOK = False
                        break
                     else:  
                        bc = 'bgcolor="#FF0000"'
               
               strTmp = f'{strTmp}<th {bc}>{frame[column].get(index)}</th>'

            if isOK:  
               count = count + 1
               if count >= self.showCnt:
                  break 
               strTmp = f'{strTmp}</tr>'
               strB = f'{strB}{strTmp}'
        
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

   def checkQueryParams(self):
         self.needAlarm = False
         def isValidDigit(value):
           value =  value.replace('.', '')
           isValid = value.lstrip('-').isdigit()
           return isValid

         def setBackColor(lineE):
            if lineE.text() and not isValidDigit(lineE.text()):
               self.needAlarm = True
               lineE.setStyleSheet("QLineEdit{background-color:rgba(255,0,0,1); border:0px;}")
            else:
               lineE.setStyleSheet("QLineEdit{background-color:rgba(0,0,0,0.3); border:0px;}")
         
         # 涨幅

         self.searchPos[3] = [-1, -1]
         riseL = self.low.text()
         riseH = self.high.text()
         
         setBackColor(self.low)
         setBackColor(self.high)

         if riseL and isValidDigit(riseL):
            self.searchPos[3][0] = float(riseL)
         if riseH and isValidDigit(riseH):
            self.searchPos[3][1] = float(riseH)

         #换手率
         self.searchPos[9] = [-1, -1]
         lowC  = self.lowChange.text()
         highC = self.hignChange.text()

         setBackColor(self.lowChange)
         setBackColor(self.hignChange)

         if lowC and isValidDigit(lowC):
            self.searchPos[9][0] = float(lowC)
         if highC and isValidDigit(highC):
            self.searchPos[9][1] = float(highC)

         # 量比
         self.searchPos[10] = [-1, -1] 
         lowV  = self.lowVolume.text()
         highV = self.highVolume.text()

         setBackColor(self.lowVolume)
         setBackColor(self.highVolume)

         if lowV and isValidDigit(lowV):
            self.searchPos[10][0] = float(lowV)
         if highV and isValidDigit(highV):
            self.searchPos[10][1] = float(highV)

         # 动态市盈率
         self.searchPos[11] = [-1, -1]
         lowD = self.lowDynamicPE.text()
         highD = self.highDynamicPE.text()

         setBackColor(self.lowDynamicPE)
         setBackColor(self.highDynamicPE)

         if lowD and isValidDigit(lowD):
            self.searchPos[11][0] = float(lowD)
         if highD and isValidDigit(highD):
            self.searchPos[11][1] = float(highD)

         return self.needAlarm == False

   def querySuggestStock(self):
      self.searchPos.clear()

      if self.checkQueryParams() == True:
         frame = ef.stock.get_realtime_quotes()
         self.fillMatchStocks(frame)
      else:
         #print("need show box")
         QMessageBox.question(self, "错误提示", "参数错误已经红色标记出", QMessageBox.StandardButton.Yes) 
         return

   def initUI(self):
        p1 = QPalette()
        p1.setColor(QPalette.ColorRole.WindowText, QColor('black'))

        self.setWindowTitle("当前位于荐股界面")
        self.resize(WIDTH,HEIGHT)
        self.progressValue = 0
        self.showCnt = 20
        self.colorPos = []
        self.searchPos = {}
        self.needAlarm = False

        self.rise_label = QLabel("涨幅区间")
        self.rise_label.setPalette(p1)

        self.low = QLineEdit("")
        self.low.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.lowa = QLabel("%")

        self.rise_split = QLabel("-")

        self.high = QLineEdit("")
        self.high.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.higha = QLabel("%")

        self.change_label = QLabel("换手率区间")
        self.change_label.setPalette(p1)

        self.lowChange = QLineEdit("")
        self.lowChange.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.lowaChange = QLabel("%")

        self.change_split = QLabel("-")

        self.hignChange = QLineEdit("")
        self.hignChange.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.highaChange = QLabel("%")

        labelShu = QLabel("     |     ")
        labelShu.setPalette(p1)

        self.layout0 =  QHBoxLayout()
        self.layout0.addWidget(self.rise_label)
        self.layout0.addWidget(self.low)
        self.layout0.addWidget(self.lowa)
        self.layout0.addWidget(self.rise_split)
        self.layout0.addWidget(self.high)
        self.layout0.addWidget(self.higha)
        self.layout0.addWidget(labelShu)
        self.layout0.addWidget(self.change_label)
        self.layout0.addWidget(self.lowChange)
        self.layout0.addWidget(self.lowaChange)
        self.layout0.addWidget(self.change_split)
        self.layout0.addWidget(self.hignChange)
        self.layout0.addWidget(self.highaChange)

        self.volume_label = QLabel("量比区间")
        self.volume_label.setPalette(p1)

        self.lowVolume = QLineEdit("")
        self.lowVolume.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.volume_split = QLabel("-")

        self.highVolume = QLineEdit("")
        self.highVolume.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        self.dynamicPE_label = QLabel("动态市盈率")
        self.dynamicPE_label.setPalette(p1)

        self.lowDynamicPE = QLineEdit("")
        self.lowDynamicPE.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.dynamicPE_split = QLabel("-")

        self.highDynamicPE = QLineEdit("")
        self.highDynamicPE.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        labelShu1 = QLabel("     |     ")
        labelShu1.setPalette(p1)

        self.layout1 =  QHBoxLayout()
        self.layout1.addWidget(self.volume_label)
        self.layout1.addWidget(self.lowVolume)
        self.layout1.addWidget(self.volume_split)
        self.layout1.addWidget(self.highVolume)
        self.layout1.addWidget(labelShu1)
        self.layout1.addWidget(self.dynamicPE_label)
        self.layout1.addWidget(self.lowDynamicPE)
        self.layout1.addWidget(self.dynamicPE_split)
        self.layout1.addWidget(self.highDynamicPE)
        
        self.msg = QLabel("【注意】上述的条件都是区间的方式，如果右边为空则表示条件 >=左区间值， 如果左边为空则表示 <= 右区间值，每个条件可以不填表示没有该条件,但是都必须是数字可以带小数")
        self.msg.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        p2 = QPalette()
        p2.setColor(QPalette.ColorRole.WindowText, QColor('blue'))
        self.msg.setPalette(p2)

        self.queryButton = QPushButton("点我查询")
        self.queryButton.setStyleSheet("QPushButton{font-family:'宋体';font-size:16px;color:rgb(0,0,0);}\
                               QPushButton{background-color:rgb(170,200,50)}\ QPushButton:hover{background-color:rgb(50, 170, 200)}")

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.msg)
        self.layout2.addWidget(self.queryButton)
        self.queryButton.setMaximumSize(100, 40)

        self.text = QTextEdit()
        self.text.setStyleSheet("QTextEdit{background-color:rgba(0,0,0,0); border:0px;}")

        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.text)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout0)
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)

        self.queryButton.clicked.connect(self.querySuggestStock)
        self.setLayout(self.layout)

class MonitorStock(BaseWidget):
    
   def checkBoxContent(self, cb, ql, type, needAlert = False):

        isValid = False
        if cb.isChecked():
           value = ql.text().replace('.', '')
           isValid = value.lstrip('-').isdigit()
           if isValid == False and needAlert:
              QMessageBox.question(self, "错误提示", "必须是数字", QMessageBox.StandardButton.Yes)

        cbValid = isValid

        if type == 'type1':
            self.cbValid1 = cbValid
        elif type == 'type2':
            self.cbValid2 = cbValid

   def monitor(self):

        if not self.monitor_1.isChecked() and not self.monitor_2.isChecked():
           return
        
        self.checkBoxContent(self.monitor_1, self.value_code_1, 'type1')
        self.checkBoxContent(self.monitor_2, self.value_code_2, 'type2')

        if not self.cbValid1 and not self.cbValid2:
            return

        self.reverseSort = True
        self.fillInfoAndMonitor()

   def getPosByType(self, type):
        pos = -1
        op = '>='
        if type == '选择监控类型':
            pos = -1
        elif type == '价格最高值':
            pos = 6
        elif type == '价格最低值':
            pos = 7
            op = '<='
        elif type == '涨幅最大%比':
            pos = 11
            op = '>='
        elif type == '跌幅最大%比':
            pos == 11 
            op = '<='
        
        return pos, op

   def needMonitor(self, threshold, value, op):
        if op == '>=':
            return value >= threshold
        elif op == '<=':
            return value <= threshold

   
   def fillInfoAndMonitor(self):

        def fillOneFrame(frame, pos, threshold, op):
            strA = ''
            for c in frame.columns.values:
                strA =f'{strA}<th>{c}</th>'

            strA = f'{strA}<th>盯盘告警</th>\n'
          
            #是否按时间倒序排列
            if self.reverseSort:
               frame.sort_index(ascending=False,inplace=True)

            strB = ''
            count = 0

            for index, row in frame.iterrows(): 
                count = count + 1
                if count > self.showCnt:
                    break
                strB = f'{strB}<tr>'
                tmpCnt = 0
                tmpValue = 0
                namePos = 0 
                stockName = ''
                for column in frame.columns:
                    tmpCnt = tmpCnt + 1
                    namePos = namePos + 1
                    if pos != -1 and tmpCnt == pos:
                       tmpValue = frame[column].get(index)

                    if namePos == 1:
                       stockName = frame[column].get(index)

                    strB = f'{strB}<th>{frame[column].get(index)}</th>'

                if threshold and threshold.strip() != '' and self.needMonitor(float(threshold), float(tmpValue), op):
                   strB = f'{strB}<th bgcolor="#FF0000">正在告警</th></tr>'
                   if needMonitor(self.monitorMap, stockName):
                      self.monitorMap[stockName] = time.time()
                      #ConsumerAndProducer.speak(f'{stockName}中了请处理')
                      
                   #CommonTool.sendMonitorMsg(self.userCtrl.userInfo.email, f'股票{stockName}达到设定值可以买卖', f'已经达到设定的阈值{threshold}，请进行买卖')
                else:
                   strB = f'{strB}<th>----</th></tr>'

            width = WIDTH
            height = HEIGHT - 500
            table = f'<table border="1" cellpadding = "10" width={width} height={height}>\
                        <tr>{strA}</tr>\
                            {strB}\
                      </table>'

            return table

        tables = '';
        isValid = False
        if self.monitor_1.isChecked():
            codeInput1 = self.stocks_code_1.text() 
            if codeInput1  and codeInput1.strip() != '':
               isValid = True

            if isValid == False:
               QMessageBox.question(self, "错误提示", "股票代码错误", QMessageBox.StandardButton.Yes) 
               self.preCheckResult = False
               return
             
            frame = ef.stock.get_quote_history(codeInput1, klt=1)
            pos, op = self.getPosByType(self.cb_1.currentText())
            table = fillOneFrame(frame, pos, self.value_code_1.text(), op)
            tables = f'{tables}{table}'
        
        isValid = False
        if self.monitor_2.isChecked():
            codeInput2 = self.stocks_code_2.text() 
            if codeInput2  and codeInput2.strip() != '':
               isValid = True

            if isValid == False:
               QMessageBox.question(self, "错误提示", "股票代码错误", QMessageBox.StandardButton.Yes) 
               self.preCheckResult = False
               return
            frame = ef.stock.get_quote_history(codeInput2, klt=1)
            pos, op = self.getPosByType(self.cb_2.currentText())
            table = fillOneFrame(frame, pos, self.value_code_2.text(), op)
            tables = f'{tables}{table}'

        strHtml = f'<html>\
                        <head>\
                        <title>{type}</title>\
                        </head>\
                        <body>\
                           {tables}\
                        </body>\
                    </html>'

        self.text.setHtml(strHtml)

   def initUI(self):

        self.setWindowTitle("当前位于盯盘界面")
        self.resize(WIDTH,HEIGHT)
        self.progressValue = 0
        self.showCnt = 1

        self.stocks_label_1 = QLabel("股票代码")
        self.stocks_code_1 = QLineEdit("")
        self.stocks_code_1.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.cb_1=QComboBox()
        self.cb_1.addItem('选择监控类型')
        self.cb_1.addItem('价格最高值')
        self.cb_1.addItem('价格最低值')
        self.cb_1.addItem('涨幅最大%比')
        self.cb_1.addItem('跌幅最大%比')

        self.value_label_1 = QLabel("输入数值")
        self.value_code_1 = QLineEdit("")
        self.value_code_1.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        self.monitor_1 = QCheckBox('开始盯盘')
        self.monitor_1.setChecked(False)
        self.cbValid1 = False
        self.monitor_1.stateChanged.connect(lambda:self.checkBoxContent(self.monitor_1, self.value_code_1, 'type1', needAlert = True))

        self.stocks_label_2 = QLabel("股票代码")
        self.stocks_code_2 = QLineEdit("")
        self.stocks_code_2.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")
        self.cb_2 = QComboBox()
        self.cb_2.addItem('选择监控类型')
        self.cb_2.addItem('价格最高值')
        self.cb_2.addItem('价格最低值')
        self.cb_2.addItem('涨幅最大%比')
        self.cb_2.addItem('跌幅最大%比')


        self.value_label_2 = QLabel("输入数值")
        self.value_code_2 = QLineEdit("")
        self.value_code_2.setStyleSheet("QLineEdit{background-color:rgba(100,100,100,100); border:0px;}")

        self.monitor_2 = QCheckBox('开始盯盘')
        self.monitor_2.setChecked(False)
        self.cbValid2 = False
        self.monitor_2.stateChanged.connect(lambda:self.checkBoxContent(self.monitor_2, self.value_code_2, 'type2', needAlert=True))

        self.layout0 =  QHBoxLayout()
        self.layout0.addWidget(self.stocks_label_1)
        self.layout0.addWidget(self.stocks_code_1)
        self.layout0.addWidget(self.cb_1)
        self.layout0.addWidget(self.value_label_1)
        self.layout0.addWidget(self.value_code_1)
        self.layout0.addWidget(self.monitor_1)

        self.layout1 =  QHBoxLayout()
        self.layout1.addWidget(self.stocks_label_2)
        self.layout1.addWidget(self.stocks_code_2)
        self.layout1.addWidget(self.cb_2)
        self.layout1.addWidget(self.value_label_2)
        self.layout1.addWidget(self.value_code_2)
        self.layout1.addWidget(self.monitor_2)

        self.text = QTextEdit()
        self.text.setStyleSheet("QTextEdit{background-color:rgba(0,0,0,0); border:0px;}")

        self.layoutV = QVBoxLayout()
        self.layoutV.addLayout(self.layout0)
        self.layoutV.addLayout(self.layout1)
        self.layoutV.addWidget(self.text)

        self.setLayout(self.layoutV)
        self.timer = QTimer()
        self.timer.start(5000) 
        self.timer.timeout.connect(self.monitor)
