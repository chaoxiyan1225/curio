#coding=utf8
import base64
from operator import ne
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

from manager.SystemContrl import *
from manager.UserControl import *
from widgets.FundWidget import *
from widgets.StockWidget import *
from widgets.OtherWidget import *

import time
import utils.logger
from pictures import *

# 600519 300750

# 一分钟K线：6 7 11

logger = utils.logger

class MainWindow(QMainWindow):
    
   def __init__(self):
        super().__init__()

        stock = base64.b64decode(stock_png)
        fund = base64.b64decode(fund_png)
        buy = base64.b64decode(buy_png)
        rg  = base64.b64decode(rg_png)
        icon  = base64.b64decode(icon_png)
        # pyqt页面  base64转化QPixmap
        iconStock = QPixmap()
        iconStock.loadFromData(stock)
        iconFund = QPixmap()
        iconFund.loadFromData(fund)
        iconBuy = QPixmap()
        iconBuy.loadFromData(buy)
        iconRg = QPixmap()
        iconRg.loadFromData(rg)
        iconIcon = QPixmap()
        iconIcon.loadFromData(icon)

        self.setWindowTitle("牛牛飞天-V2.0.7.8")
        self.setWindowIcon(QIcon(iconIcon))
        
        self.resize(WIDTH,HEIGHT) 

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)

        tabs.addTab(ShowStock(iconStock), "股票查询")
        #tabs.addTab(ShowFund(iconFund), "基金查询")
        tabs.addTab(SuggestStock(iconFund), "牛牛荐股")
        tabs.addTab(MonitorStock(iconBuy), "盯盘告警")
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
    logger.warning('starting...........')
    try:
       main()
    except Exception as e:
       logger.error(e)

    logger.warning('finishing.........')
