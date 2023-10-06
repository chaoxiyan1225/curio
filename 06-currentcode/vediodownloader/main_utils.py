import customtkinter
import os
from PIL import Image
import webbrowser
import time
import threading
from tkinter import messagebox
import tkinter as tk
import utils.useruitool as UserUITool
import utils.commontool as CommonTool
from service.system_control import *
from service.user_control import *
from service.downloader_control import *
from conf.systemconf import *
from conf.pictures import *
from tkinter import filedialog
from utils.logger import *
import conf.errors as Errors
from io import BytesIO
from conf.pictures_v4 import *
import requests

PIC_SIZE = 30
FRAME_NAMES = ["", "", ""]
PROGRESS_INFO = "Total UU urls, now the CC url is downloading and there is TT vedio in the url,success SS,and FF failed,is finished?YY  "

STATUS_INFO = "【WARNING】your information:cc, ss!"

def open_path(app):
   path = app.save_entry.get().replace("/", "\\")
   directory = f'{path}'
   os.system("explorer.exe %s" % directory)
   
def add_new(app):
   app.current_row = app.current_row + 1

   if app.current_row > 4:
      app.current_row = app.current_row - 1
      messagebox.showinfo(title="WARNING", message="You can download 3 vedio one time!") 
      return
      
   url_entry = customtkinter.CTkEntry(app.download_frame, width = 380, placeholder_text="Paste you vedio url")
   url_entry.grid(row=app.current_row, column=1, padx=(10,10), columnspan=14, pady=(0, 0),sticky="ew")
   
   cha_button = customtkinter.CTkButton(app.download_frame, corner_radius=0, height=40, border_spacing=10, text=" ",
                                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=app.cha_img, anchor="w", command=lambda: app.forget_row(cha_button))
                                                
   cha_button.grid(row=app.current_row, column=15, columnspan=1, padx=(0,10), pady=(0,0))

def forget_row(app, chaButton):  
   buttonRow = int(chaButton.grid_info()["row"])    
   app.current_row = app.current_row - 1

   for entry in app.download_frame.grid_slaves():
      if int(entry.grid_info()["row"]) == buttonRow:
         columnN = int(entry.grid_info()["column"])
         entry.grid_forget()
         
   for entry in app.download_frame.grid_slaves():       
      currentR = int(entry.grid_info()["row"])
      if currentR > buttonRow and currentR < 11: 
         if int(entry.grid_info()["column"] == 1):
               entry.grid(row=currentR-1, column=1, padx=(10,10), columnspan=13, pady=(0, 0),sticky="ew")  
         if int(entry.grid_info()["column"] == 15):
               entry.grid(row=currentR-1, column=15, columnspan=1, padx=(0,20), pady=(0,0), sticky="ew")

def check_register_valid(app):
   tel = app.tel_entry.get()        
   isValid = UserUITool.IsValidTel(tel)

   if isValid == False:
      messagebox.showinfo(title="WARNING", message="the telNum invalid!")
      app.tel_entry.configure(fg_color="red")
      return False

   email = app.email_entry.get()        
   isValid = UserUITool.IsValidEmail(email)

   if isValid == False:
      messagebox.showinfo(title="WARNING", message="the email invalid!!") 
      app.tel_entry.configure(fg_color="white") 
      app.email_entry.configure(fg_color="red")
      return False

   return True

def register_submit_event(app):

   isValid = check_register_valid(app)
   if isValid == False:
      return
   
   app.email_entry.configure(fg_color="white") 
   app.tel_entry.configure(fg_color="white")

   isSend = app.userCtrl.clickToRegister(app.email_entry.get(), app.tel_entry.get())
   if isSend == Errors.SUCCESS:
      messagebox.showinfo(app, "SUCCESS", "please check message from your email!") 
      return True

   messagebox.showinfo(app, "ERROR", "register error, please try later!") 
   return False

def check_login_valid(app):
    
   if app.LoginValid == True and (threading.Timer.time() - app.lastValidTime)  < app.validPeriod:
      return True
      
   result = app.sysCtrl.clientValid()
   logger.warning(f'the client valid check {result.toString()}')
   if result == Errors.S_Forbidden:
      messagebox.showinfo(title="WARNING", message="this client is forbidden!")
      return False
      
   elif result == Errors.S_ClientFreeUse:
      return True

   result = app.userCtrl.LoginCheck()
   if result == Errors.C_InvalidUser:
      messagebox.showinfo(title="WARNING", message="please register first!") 
      return False

   elif result == Errors.C_Arrearage:
      messagebox.showinfo(title="WARNING", message="you are incharge!")
      return
   elif result != Errors.SUCCESS:
      messagebox.showinfo(title="WARNING", message="some unknown error happens!")
      return False

   result = app.sysCtrl.clientValid()

   if result == Errors.S_Forbidden:
      messagebox.showinfo(title="WARNING", message="this client is forbidden")
      app.preCheckResult = False
      return False

   elif result  != Errors.SUCCESS: 
      messagebox.showinfo(title="WARNING", message="some unknown error happens, please try later!")
      app.preCheckResult = False 
      return False

   app.LoginValid = True
   app.lastValidTime = time.time()
   return True

def select_path(app):
   filePath = filedialog.askdirectory()
   app.save_entry.delete(0, 10000)
   app.save_entry.insert(0,filePath)
   app.save_entry.configure(fg_color="white") 

def parse_allUrls(app):
   urls = []
   for entry in app.download_frame.grid_slaves():       
       currentR = int(entry.grid_info()["row"])
       if currentR >= 2 and currentR < 11: 
          if int(entry.grid_info()["column"] == 1):
             url = entry.get()
             if url != None and url.strip() != "":
                urls.append(url)
   return urls

def start_downLoad(app):
   app.progressbar.set(0.01)
   app.current_label.configure(text=" ")
   
   urls = parse_allUrls(app)
   if len(urls) == 0:
      messagebox.showinfo(title="WARNING", message="you must input one website at least!") 
      return
   
   for url in urls:
      isValid = UserUITool.IsValidUrl(url)
      if isValid == False:
         messagebox.showinfo(title="WARNING", message="the url input invalid!") 
         app.is_need_stop = True
         return

   if check_login_valid(app) == False:
      return        
   
   savePath = app.save_entry.get() 
   if savePath == None or savePath.strip() == '':
      app.save_entry.configure(fg_color="red")
      messagebox.showinfo(title="WARNING", message="you should chose a path to save vedio!") 
      return 
   else:
      app.save_entry.configure(fg_color="white")
      
   if not os.path.exists(savePath):
      app.save_entry.configure(fg_color="red")
      messagebox.showinfo(title="WARNING", message="the path is not exist") 
      return 
   
   logger.warning(f'excute the downloader backgroud!')
   
   app.is_need_stop = False
   app.downloadCtrl = DownloadControl()

   t = threading.Thread(target=downLoading, args=(app, urls, savePath))
   t2 = threading.Thread(target=inside_thread, args=(app))
   t2.start()
   t.start()
        
def downLoading(app, urls, savePath):
   try:
      app.downloadCtrl.downLoad_start(urls, savePath)
   except Exception as e1:
      logger.error(f"the input url:{urls} download fail, and error msg: {str(e1)}")
      messagebox.showinfo(title="WARNING", message="some error happens when downloading!") 
      #app.is_need_stop = True
      logging.exception(e1)
      app.downloadCtrl.clear()
    
def inside_thread(app):
   while True:
      metricInfo = app.downloadCtrl.get_total_metrics()
      if metricInfo == None:
         time.sleep(5)
         continue
      
      app.set_frame_view(metricInfo)

      if metricInfo.totalVedioCnt > 0 and metricInfo.totalFailCnt + metricInfo.totalSuccessCnt >= metricInfo.totalVedioCnt:
         logger.warning(f"have  down load finish, {metricInfo.to_string()}")
         app.is_need_stop = True
         break
         
      if not app.downloadCtrl.downloading:
         logger.warning(f'the downloader finish')
         break
   
      time.sleep(10)

# open paypal or other pay platform
def openForPay(url):
   logger.info(f'the input: {url}, and to pay for')
   webbrowser.open(url)
                
def set_frame_view(app, metricInfo:TotalMetricInfo):
   currMetric = metricInfo.currentMetricInfo
   percent = currMetric.percentCurrent

   logger.warning(f'currentProgress:{percent}')
   app.progressbar.set(percent/100)
   info = f' {percent}%'
   app.current_label.configure(text=info)
   
   inP = "Yes"
   if currMetric.totalVedioCnt == 0:
      inP = "Yes"
   else:
      inP = "No" if currMetric.successVedioCnt + currMetric.failVedioCnt < currMetric.totalVedioCnt else "Yes"

   info = PROGRESS_INFO.replace("UU", str(metricInfo.totalUrlCnt)).replace("CC", str(metricInfo.currentUrl))
   info = info.replace("TT", str(currMetric.totalVedioCnt)).replace("SS", str(currMetric.successVedioCnt)).replace("FF", str(currMetric.failVedioCnt)).replace("YY", inP)
   
   app.progress_label.configure(text=info)
    

def async_load_urls(app):
   table = []
   row = [] 
   
   remoteUrls = app.sysCtrl.getAllUrlsArray()
   urls = remoteUrls if remoteUrls and len(remoteUrls) > 0 else SystemConf.default_urls
   field = []
   rNum = 0

   for r in range(len(urls)):
      urlInfo = urls[r]
      res=requests.get(urlInfo.logo)
      with open("tmplogo" ,'wb') as f:
         f.write(res.content)
         
      tmp_img = customtkinter.CTkImage(light_image=Image.open("tmplogo"),dark_image=Image.open("tmplogo"), size=(PIC_SIZE, PIC_SIZE))    
      tmp_button = customtkinter.CTkButton(app.shares_frame, corner_radius=0, height=40, border_spacing=10, text=urlInfo.name, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=tmp_img, anchor="w", command=lambda: webbrowser.open(urlInfo.url))
      tmp_button.grid(row=rNum,column=r%3, padx=20, pady=20) 
      row.append(tmp_button)
         
      if r % 3 ==0 and r > 0:
         table.append(row)
         rNum = rNum + 1
