import json
import pickle
import random
import time
from abc import ABC, abstractmethod
from datetime import datetime
import sys

import requests
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Timer(object):
    def __init__(self, sleep_interval=0.5, buy_time='09:59:59.500', serverTimeUrl='https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5'):
        # '2018-09-28 22:45:50.000'
        # buy_time = 2020-12-22 09:59:59.500
        localtime = time.localtime(time.time())

        buy_time_config = datetime.strptime(
            localtime.tm_year.__str__() + '-' + localtime.tm_mon.__str__() + '-' + localtime.tm_mday.__str__() + ' ' + buy_time,
            "%Y-%m-%d %H:%M:%S.%f")
        if time.mktime(localtime) < time.mktime(buy_time_config.timetuple()):
            self.buy_time = buy_time_config
        else:
            self.buy_time = datetime.strptime(
                localtime.tm_year.__str__() + '-' + localtime.tm_mon.__str__() + '-' + (
                        localtime.tm_mday + 1).__str__() + ' ' + buy_time,
                "%Y-%m-%d %H:%M:%S.%f")
        print("3-预计购买时间：{}".format(self.buy_time))

        self.buy_time_ms = int(time.mktime(self.buy_time.timetuple()) * 1000.0 + self.buy_time.microsecond / 1000)
        self.sleep_interval = sleep_interval
        self.serverTimeUrl = serverTimeUrl

        self.diff_time = self.local_and_jd_time_diff()
        

    def jd_time(self):
        """
        从京东服务器获取时间毫秒
        :return:
        """
        #url = 'https://a.jd.com//ajax/queryServerData.html'

        headers={
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        url = 'https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5'
        
        ret = requests.get(url=url,headers=headers);

        if ret.status_code == 200:
           txt = ret.text
           js = json.loads(txt)
           return int(js["currentTime2"])

        """
         获取不到时间，则直接返回0
        """
        return 0

    def local_time(self):
        """
        获取本地毫秒时间
        :return:
        """
        return int(round(time.time() * 1000))

    def local_and_jd_time_diff(self):
        """
        计算本地服务器时间差
        :return:
        """

        # 如果从服务器获取时间失败了，则用默认本地跟京东无时间差
        if self.jd_time() == 0:
            return 0;


        return self.local_time() - self.jd_time()

    def start(self):
        print(f'4-正在等待抢购时间到达:{self.buy_time}')
        print(f'5-本地时间为{self.local_time()}, 服务器端时间为{self.jd_time()},'
              f' 误差为:{self.diff_time} 毫秒')
        while True:
            # 本地时间减去与京东的时间差，能够将时间误差提升到0.1秒附近
            # 具体精度依赖获取京东服务器时间的网络时间损耗
            if self.local_time() - self.diff_time >= self.buy_time_ms:
                print('6-时间到达，开始执行……')
                break
            else:
                print('........')
                time.sleep(self.sleep_interval)


class BaseSpider(ABC):

    def __init__(self, base_url: str, login_url: str, verify_url: str, sleep_time: int = 3):
        self.base_url = base_url
        self.login_url = login_url
        self.verify_url = verify_url
        self.driver = self.get_chrome_driver()
        self.wait = WebDriverWait(self.driver, 180, 0.05)
        self.is_login = False
        self.sleep_time = sleep_time
        self.data_list = []

    def start(self):
        self.login_by_cookies()
        self.driver.get(self.base_url)
        self.run()
        self.close()

    @abstractmethod
    def runForBuy(self):
        pass

    @abstractmethod
    def runForBook(self):
        pass

    def sleep(self):
        time.sleep(self.sleep_time)

    @staticmethod
    def get_chrome_driver() -> webdriver:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        # options.add_argument('--headless')  # 无头参数
        options.add_argument('--disable-gpu')
        # 关闭浏览器左上角通知提示
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        options.add_experimental_option('prefs', prefs)
        # 关闭'chrome目前受到自动测试软件控制'的提示
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver

    def login_by_cookies(self):
        if self.load_cookie():
            return self
        return self.login()

    def login(self):
        print('开始进行人工登录')
        driver = self.driver
        if not self.is_login:
            driver.get(self.login_url)
        self.verify_login()
        return self

    def verify_login(self):
        wait_time = 0
        while True and not self.is_login:
            print(f'登录中...等待时间为{wait_time}s')
            time.sleep(5)
            wait_time = wait_time + 5
            if self.verify_url in self.driver.current_url and not self.driver.current_url == self.login_url:
                print('登录成功')
                self.is_login = True
                break
            if wait_time >= 300:
                raise Exception('登录失败')
        self.save_cookie()
        return self.is_login

    def save_cookie(self):
        cookie = self.driver.get_cookies()
        with open(self.__class__.__name__, 'wb') as f:
            f.write(pickle.dumps(cookie))

    def load_cookie(self):
        print('1-开始加载cookies信息')
        try:
            with open(self.__class__.__name__, 'rb') as f:
                cookie = pickle.load(f)
                if not cookie:
                    return False
        except FileNotFoundError as e:
            return False
        for cookies in cookie:
            if 'expiry' in cookies:
                del cookies['expiry']
            if 'domain' in cookie:
                del cookies['domain']
        self.driver.get(self.base_url)
        #print(f'base_url:{self.base_url}, and cookies:{cookie}')
        for i in cookie:
            self.driver.add_cookie(i)
        print("2-cookies信息加载success！")
        self.driver.refresh()
        self.is_login = True
        return self

    def close(self):
        self.save_cookie()
        self.driver.close()
        self.driver.quit()
        self.is_login = False


class JdSpider(BaseSpider):

    def __init__(self, sleep_time: int = 3, item_id: int = 100012043978):
        super().__init__(base_url='http://suning.com/', login_url='https://passport.suning.com/ids/login?method=GET&loginTheme=b2c',
                         verify_url='https://www.suning.com/', sleep_time=sleep_time)
        self.item_id = item_id
        #self.item_url = f'https://item.jd.com/{item_id}.html'
        self.item_url = 'https://product.suning.com/0000000000/11001203841.html?safp=d488778a.13701.productWrap.14&safc=prd.0.0&safpn=10007.500394#unknown'
        self.serverTimeUrl = 'http://quan.suning.com/getSysTime.do'

    def runForBuy(self, buy_time):
        tag = 1
        self.driver.get(self.item_url)
        Timer(buy_time=buy_time, serverTimeUrl=self.serverTimeUrl).start()
        while True:
            self.driver.get(self.item_url)
            first_result = self.wait.until(presence_of_element_located((By.ID, "btn-reservation")))
            text_content = first_result.get_attribute("textContent")
            if text_content in ['等待抢购', '开始预购']:
                print('7-还没开始，等待抢购！{}'.format(tag))
            elif text_content == '立即抢购':
                try:
                    print('8-开始抢购.....')
                    first_result.click()
                    first_result = self.wait.until(presence_of_element_located((By.CLASS_NAME, "checkout-submit")))
                    first_result.click()
                    print("88-提交订单！")
                    time.sleep(30)
                    break
                except common.exceptions.TimeoutException as e:
                    print('9-抢购失败了！')
                    break
            time.sleep(random.randint(1, 3) * 0.1)
            tag += 1
            if tag > 300:
                break

    def runForBook(self, buy_time):
        bookSuccess = False
        tag = 1
        self.driver.get(self.item_url)
        Timer(buy_time=buy_time, serverTimeUrl=self.serverTimeUrl).start()
        while True:
            self.driver.get(self.item_url)
            first_result = self.wait.until(presence_of_element_located((By.ID, "addCart")))
            text_content = first_result.get_attribute("textContent")
            if text_content in ['等待预约']:
                print('7-还没开始，等待预约！{}'.format(tag))
            elif text_content == '立即预约':
                try:
                    print('8-开始预约.....')
                    first_result.click()
                    first_result = self.wait.until(presence_of_element_located((By.CLASS_NAME, "item_11001203841_gmq_yyljyy")))
                    first_result.click()
                    print("88-提交订单！")
                    time.sleep(30)
                    bookSuccess = True
                    break
                except common.exceptions.TimeoutException as e:
                    print('9-预约失败了！')
                    bookSuccess = False
                    break
            time.sleep(random.randint(1, 3) * 0.1)
            tag += 1
            if tag > 300:
                break

        return bookSuccess
        


if __name__ == '__main__':

    # https://item.jd.com/100012043978.html  茅台京东的网页
    dd = JdSpider().login_by_cookies()

    #京东跟苏宁的时间是不同的，下面的是苏宁的时间
    isSuccess = dd.runForBook(buy_time='16:16:20.500')
    
    if isSuccess == False:
       print('book failed,exit')
       dd.close()

    dd.runForBuy(buy_time='20:29:58.500')
    dd.close();

