import customtkinter
import os
from PIL import Image
import webbrowser
import time
import threading
from tkinter import messagebox
import utils.useruitool as UserUITool
import utils.commontool as CommonTool
from service.system_control import *
from service.user_control import *
from service.downloader_control import *
from conf.pictures import *
from tkinter import filedialog
import utils.logger as logger
import conf.errors as Errors
from io import BytesIO
from conf.pictures_v3 import *

PIC_SIZE = 30
FRAME_NAMES = ["", "", ""]
PROGRESS_INFO = "【下载详情】共UU个链接,正在下载第:CC个链接,本链接共有:TT个视频,已下载成功:SS个,失败:FF,是否下载完成:YY  "

STATUS_INFO = "【NOTES】:您当前处于:cc, ss!"

class App(customtkinter.CTk):

    def __initImg__(self):
       # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

        self.logo_image = customtkinter.CTkImage(Image.open(BytesIO(logo_png)), size=(26, 26))
        self.image_icon_light = customtkinter.CTkImage(Image.open(BytesIO(aboutus_png)), size=(712, 362))
        self.download_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(download_png)),dark_image=Image.open(BytesIO(download_png)), size=(PIC_SIZE, PIC_SIZE))
        self.shares_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(share_png)),dark_image=Image.open(BytesIO(share_png)), size=(PIC_SIZE, PIC_SIZE))
        self.aboutus_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(aboutus_png)),dark_image=Image.open(BytesIO(aboutus_png)), size=(PIC_SIZE, PIC_SIZE))
        self.search_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(search_png)),dark_image=Image.open(BytesIO(search_png)), size=(PIC_SIZE, PIC_SIZE))
        self.download_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(download_png)),dark_image=Image.open(BytesIO(download_png)), size=(PIC_SIZE, PIC_SIZE))
        self.more_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(more_png)),dark_image=Image.open(BytesIO(more_png)), size=(PIC_SIZE, PIC_SIZE))
        self.language_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(language_png)),dark_image=Image.open(BytesIO(language_png)), size=(PIC_SIZE, PIC_SIZE))
        self.register_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(register_png)),dark_image=Image.open(BytesIO(register_png)), size=(PIC_SIZE, PIC_SIZE))
        self.confirm_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(confirm_png)),dark_image=Image.open(BytesIO(confirm_png)), size=(PIC_SIZE, PIC_SIZE))                                         
        self.back_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(back_png)),dark_image=Image.open(BytesIO(back_png)), size=(PIC_SIZE, PIC_SIZE))
        self.open_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(open_png)),dark_image=Image.open(BytesIO(open_png)), size=(PIC_SIZE, PIC_SIZE))
        self.add_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(add_png)),dark_image=Image.open(BytesIO(add_png)), size=(PIC_SIZE, PIC_SIZE))
        self.cha_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(cha_png)),dark_image=Image.open(BytesIO(cha_png)), size=(PIC_SIZE, PIC_SIZE))

        self.bg1_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(bg1_png)),dark_image=Image.open(BytesIO(bg1_png)), size=(712,  322))
        self.bg2_img = customtkinter.CTkImage(light_image=Image.open(BytesIO(bg2_png)),dark_image=Image.open(BytesIO(bg2_png)), size=(712,  322))                                    
                                             
    def __init__(self):
        super().__init__()

        self.title("Octopus Brother")

        self.geometry(f"{1000}x{560}")
        self.iconbitmap('logo.ico') 

        # set grid layout 1x2
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.userCtrl = UserContrl()
        self.sysCtrl = SoftWareContrl()
         
        # init images
        self.__initImg__()
      
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" BestVedioDownloader", image=self.logo_image,  compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.download_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="DownLoad", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.download_img, anchor="w", command=self.download_button_event)
        self.download_button.grid(row=1, column=0, sticky="ew")
        self.register_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Register", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.register_img, anchor="w", command=self.register_button_event)
        self.register_button.grid(row=3, column=0, sticky="ew")
        self.aboutus_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="AboutUs", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.aboutus_img, anchor="w", command=self.aboutus_button_event)
        self.aboutus_button.grid(row=4, column=0, sticky="ew")
        self.language_label =  customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=30, border_spacing=10, text="Language Select:", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.language_label.grid(row=7, column=0, padx=20, pady=(10, 0) )
        self.language_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["中文", "English", "Spnish"], command=self.change_language_event)
        
        self.language_optionemenu.grid(row=8, column=0, padx=(0,20), pady=(0, 10))

        # download frame
        self.download_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        #self.download_frame.grid(row=0, column=1,  sticky="nsew")
        self.download_frame.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)
        self.download_frame.grid_rowconfigure((0,1,3,4,5,6,7,8,9), weight=1)

        self.info_label =  customtkinter.CTkLabel(self.download_frame,corner_radius=0, height=15,  text="视频网址:",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                      anchor="w")
        self.info_label.grid(row=1, column=0, padx=(20,0), pady=(0,0))

        self.shares_button = customtkinter.CTkButton(self.download_frame, corner_radius=0, height=40, border_spacing=10, text="获取网址", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.shares_img, anchor="w", command=self.shares_button_event)
        self.shares_button.grid(row=1, column=15, columnspan = 1)
    
        self.add_button =  customtkinter.CTkButton(self.download_frame, corner_radius=0, width=15,text="", fg_color="transparent",hover_color=("gray70", "gray30"), image=self.add_img, command=self.add_new)
        self.add_button.grid(row=2, column=0,padx=(0,0), columnspan=1, pady=(0, 0))

        self.url_entry = customtkinter.CTkEntry(self.download_frame, width = 380, placeholder_text="请粘贴视频网址")
        self.url_entry.grid(row=2, column=1, padx=(10,10), columnspan=14, pady=(0, 0),sticky="ew")
        
        self.start_down_button = customtkinter.CTkButton(self.download_frame, text="download", command=self.start_downLoad)
        self.start_down_button.grid(row=2, column=15, columnspan=1, padx=(0,10), pady=(0,0))
        
        self.current_row = 2
       
        self.save_entry = customtkinter.CTkEntry(self.download_frame, width = 420,  placeholder_text="请选择路径")
        self.save_entry.grid(row=11, column=0, padx=(20,0), columnspan=15, pady=0, sticky="ew")
        
        self.buttonOpen = customtkinter.CTkButton(self.download_frame, corner_radius=0, width=10, fg_color="transparent", text = " ", hover_color=("gray70", "gray30"), image=self.open_img, command=self.select_path)
        self.buttonOpen.grid(row=11, column=15, columnspan=1, padx=(0,0), pady=0)

        self.progress_label =  customtkinter.CTkLabel(self.download_frame, corner_radius=0, height=30,  text=f"{PROGRESS_INFO}", fg_color="transparent", text_color=("gray10", "gray90"), anchor="w")
        self.progress_label.grid(row=12, column=0, columnspan=16, padx=(20,0), pady=(0, 0), sticky="nsew")
        self.progressbar = customtkinter.CTkProgressBar(self.download_frame, height= 30)
        self.progressbar.grid(row=13, column=0, columnspan=16, padx=(20,10), pady=(0, 10), sticky="nsew")
        self.progressbar.set(0.01)

        # # create shares frame
        self.shares_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.shares_frame.grid_columnconfigure((1), weight=1)
        self.shares_frame.grid_rowconfigure((1), weight=0)

        # create register frame
        self.register_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.register_frame.grid_columnconfigure((1), weight=1)
        self.register_frame.grid_rowconfigure((1), weight=0)


        rowNum = 1
        self.status_label =  customtkinter.CTkLabel(self.register_frame, corner_radius=0, height=30,  text=f"{STATUS_INFO}", fg_color="transparent", text_color=("gray10", "gray90"), anchor="w")
        self.status_label.grid(row=rowNum, column=0, columnspan=5, padx=(40,0), pady=(10, 0), sticky="nsew")

        self.tel_label = customtkinter.CTkLabel(self.register_frame, text="TelNum:", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.tel_label.grid(row=rowNum+1, column=0, padx=(0,0), pady=(20,10))
        self.tel_entry = customtkinter.CTkEntry(self.register_frame, width = 50, placeholder_text="please input telNum")
        self.tel_entry.grid(row=rowNum+1, column=1, columnspan=4,sticky="nsew", padx=(5,5), pady=(20,10))
        self.tel_info_label = customtkinter.CTkLabel(self.register_frame, text="* Give me your tel exactly", compound="left", font=customtkinter.CTkFont(size=15))
        self.tel_info_label.grid(row=rowNum+1, column=5, padx=(0,20), pady=(20,10))
        self.email_label = customtkinter.CTkLabel(self.register_frame, text="Email:", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.email_label.grid(row=rowNum+2, column=0, padx=(0,0), pady=10)
        self.email_entry = customtkinter.CTkEntry(self.register_frame, width =50, placeholder_text="please input email")
        self.email_entry.grid(row=rowNum+2, column=1, columnspan=4,sticky="nsew", padx=(0,5), pady=10)
        self.email_info_label = customtkinter.CTkLabel(self.register_frame, text="* Give me your Email exactly", compound="left", font=customtkinter.CTkFont(size=15))
        self.email_info_label.grid(row=rowNum+2, column=5, padx=(0,20), pady=10)
        
        self.submit_button = customtkinter.CTkButton(self.register_frame, text="submit", command=self.register_submit_event, image=self.confirm_img)
        self.submit_button.grid(row=rowNum+3, column=0, columnspan=1, padx=(60,0), pady=20)
        self.VIP_button = customtkinter.CTkButton(self.register_frame, text="BeVIP", command=self.vip_button_event, image=self.more_img)
        self.VIP_button.grid(row=rowNum+3, column=5, columnspan=1, padx=(0,20), pady=20)

        #create textbox
        self.register_box = customtkinter.CTkTextbox(self.register_frame, width=600)
        self.register_box.grid(row=rowNum+5, column=0, columnspan=10, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.register_box.insert("0.0", "NOTES!!!\n\n" + "You need to register, if you want to use this software  unt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 10)

        # create about us frame
        self.aboutus_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.aboutus_frame.grid_columnconfigure(1, weight=1)
        self.aboutus_frame.grid_rowconfigure(0, weight=1)

        self.textbox3 = customtkinter.CTkTextbox(self.aboutus_frame, width=300, bg_color="blue")
        self.textbox3.grid(row=0, column=0, columnspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox3.insert("0.0", "Welcome!!!\n\n" + "please see go the page to known everything about us.\n\n\n"
                                    "You can also visit  https://chaoxiyan1225.github.io/aboutme")
    
        self.back_button = customtkinter.CTkButton(self.aboutus_frame, corner_radius=0, height=40, border_spacing=10, text="Back",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.back_img, anchor="w", command=self.download_button_event)
        self.back_button.grid(row=1, column = 0, padx=(20, 0), pady=(0, 20))
        
        self.is_need_stop = False

        # select default frame
        self.select_frame_by_name("download")
        self.change_appearance_mode_event("light")

        t = threading.Thread(target=self.async_load_urls)
        t.start()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.download_button.configure(fg_color=("gray75", "gray25") if name == "download" else "transparent")
        self.register_button.configure(fg_color=("gray75", "gray25") if name == "register" else "transparent")
        self.aboutus_button.configure(fg_color=("gray75", "gray25") if name == "aboutus" else "transparent")
        self.shares_button.configure(fg_color=("gray75", "gray25") if name == "shares" else "transparent")

        # show selected frame
        if name == "download":
            self.download_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.download_frame.grid_forget()
            
        if name == "register":
            self.register_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.register_frame.grid_forget()
        if name == "aboutus":
            self.aboutus_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.aboutus_frame.grid_forget()
        if name == "shares":
            self.shares_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.shares_frame.grid_forget()

    def change_language_event(self):
        return

    def download_button_event(self):
        self.select_frame_by_name("download")

    def shares_button_event(self):
        self.select_frame_by_name("shares")

    def register_button_event(self):
        self.select_frame_by_name("register")

    # to aboutus page view 
    def aboutus_button_event(self):
        self.select_frame_by_name("aboutus")
        webbrowser.open('https://chaoxiyan1225.github.io/aboutme')

    # to aboutus page view 
    def shares_button_event(self):
        webbrowser.open('https://chaoxiyan1225.github.io/shareurls')

    # to aboutus page view 
    def vip_button_event(self):
        webbrowser.open('https://chaoxiyan1225.github.io/business')

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def open_path(self):
        path = self.save_entry.get().replace("/", "\\")
        directory = f'{path}'
        os.system("explorer.exe %s" % directory)
        
    def add_new(self):
        self.current_row = self.current_row + 1
 
        if self.current_row > 4:
           self.current_row = self.current_row - 1
           messagebox.showinfo(title="警告", message="只能支持同时下载三个视频链接") 
           return
           
        url_entry = customtkinter.CTkEntry(self.download_frame, width = 380, placeholder_text="请粘贴视频网址")
        url_entry.grid(row=self.current_row, column=1, padx=(10,10), columnspan=14, pady=(0, 0),sticky="ew")
        
        cha_button = customtkinter.CTkButton(self.download_frame, corner_radius=0, height=40, border_spacing=10, text=" ",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.cha_img, anchor="w", command=lambda: self.forget_row(cha_button))
                                                      
        cha_button.grid(row=self.current_row, column=15, columnspan=1, padx=(0,10), pady=(0,0))
    
    def forget_row(self, chaButton):  
        buttonRow = int(chaButton.grid_info()["row"])    
        self.current_row = self.current_row - 1

        for entry in self.download_frame.grid_slaves():
            if int(entry.grid_info()["row"]) == buttonRow:
                columnN = int(entry.grid_info()["column"])
                entry.grid_forget()
                
        for entry in self.download_frame.grid_slaves():       
            currentR = int(entry.grid_info()["row"])
            if currentR > buttonRow and currentR < 11: 
                if int(entry.grid_info()["column"] == 1):
                    entry.grid(row=currentR-1, column=1, padx=(10,10), columnspan=13, pady=(0, 0),sticky="ew")  
                if int(entry.grid_info()["column"] == 15):
                    entry.grid(row=currentR-1, column=15, columnspan=1, padx=(0,20), pady=(0,0), sticky="ew")

                    
    def async_load_urls(self):
        table = []
        row = []  #row里面加满一行的就添加到上面的table里，使table成为一个二维列表。
        for r in range(4):
            for c in range(4):
                widget = customtkinter.CTkButton(self.shares_frame, corner_radius=0, height=60, border_spacing=10, text="Language Select:",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w")
                widget.grid(row=r,column=c, padx=20, pady=20, sticky="nsew")
                row.append(widget)    #把每次创建的Entry对象添加到row列表里
            table.append(row)       #把row列表添加到table列表里，使table成为一个二维列表。
        
        ##加个表头试一下
        field = ['url','suggest','website', 'suggest']
        for t in field:
            table[0][field.index(t)].configure(
                            textvariable=customtkinter.StringVar(value=t)
                            )
            
    def check_register_valid(self):
        tel = self.tel_entry.get()        
        isValid = UserUITool.IsValidTel(tel)

        if isValid == False:
            messagebox.showinfo(title="错误提示", message="输入的手机号非法")
            self.tel_entry.configure(fg_color="red")
            return False

        email = self.email_entry.get()        
        isValid = UserUITool.IsValidEmail(email)

        if isValid == False:
            messagebox.showinfo(title="错误提示", message="输入的邮箱非法") 
            self.tel_entry.configure(fg_color="white") 
            self.email_entry.configure(fg_color="red")
            return False

        return True


    def register_submit_event(self):

        isValid = self.check_register_valid()
        if isValid == False:
            return
        
        self.email_entry.configure(fg_color="white") 
        self.tel_entry.configure(fg_color="white")

        #text, ok = QInputDialog.getText(self, '用户注册提示界面', '输入邮箱')
        isSend = self.userCtrl.clickToRegister(self.email_entry.get(), self.tel_entry.get())
        if isSend == Errors.SUCCESS:
           messagebox.showinfo(self, "成功提示", "您的注册申请{成功}注意查收邮件") 
           return True

        messagebox.showinfo(self, "错误提示", "您的注册申请{失败}请稍后重试") 
        return False

    def check_login_valid(self):
        
        if self.LoginValid == True and (threading.Timer.time() - self.lastValidTime)  < self.validPeriod:
            return True
            
        result = self.sysCtrl.clientValid()
        logger.warn(f'the client valid check {result.toString()}')
        if result == Errors.S_Forbidden:
           messagebox.showinfo(title="错误提示", message="该版本的客户端已经禁止使用")
           return False
           
        elif result == Errors.S_ClientFreeUse:
           return True

        result = self.userCtrl.LoginCheck()
        if result == Errors.C_InvalidUser:
           messagebox.showinfo(title="错误提示", message="您还未注册，请点击右上角一键注册") 
           return False

        elif result == Errors.C_Arrearage:
           messagebox.showinfo(title="错误提示", message="您已欠费请续费")
           return
        elif result != Errors.SUCCESS:
           messagebox.showinfo(title="错误提示", message="发生了未知错误请稍后重试")
           return False

        result = self.sysCtrl.clientValid()

        if result == Errors.S_Forbidden:
           messagebox.showinfo(title="错误提示", message="该版本的客户端已经禁止使用")
           self.preCheckResult = False
           return False

        elif result  != Errors.SUCCESS: 
           messagebox.showinfo(title="错误提示", message="发生了未知错误请稍后重试")
           self.preCheckResult = False 
           return False

        self.LoginValid = True
        self.lastValidTime = time.time()
        return True

    def select_path(self):
        filePath = filedialog.askdirectory()
        self.save_entry.insert(0,filePath)
        
    
    def parse_allUrls(self):
       urls = []
       for entry in self.download_frame.grid_slaves():       
           currentR = int(entry.grid_info()["row"])
           if currentR >= 2 and currentR < 11: 
              if int(entry.grid_info()["column"] == 1):
                 url = entry.get()
                 if url != None and url.strip() != "":
                    urls.append(url)
       return urls

    def start_downLoad(self):
        urls = self.parse_allUrls()
        if len(urls) == 0:
           messagebox.showinfo(title="严重", message="必须输入一个网址！") 
           return
        
        for url in urls:
            isValid = UserUITool.IsValidUrl(url)
            if isValid == False:
               messagebox.showinfo(title="严重", message="输入url不合法！") 
               self.is_need_stop = True
               return

        #isValid = self.CheckValid()
        #if isValid == False:
        #   return        
        
        savePath = self.save_entry.get() 
        if savePath == None or savePath.strip() == '':
           self.save_entry.configure(fg_color="red")
           messagebox.showinfo(title="严重", message="您必须选择一个保存路径！") 
           return 
        else:
           self.save_entry.configure(fg_color="white")
           
        if not os.path.exists(savePath):
           self.save_entry.configure(fg_color="red")
           messagebox.showinfo(title="严重", message="您选择的路径不存在！") 
           return 
        
        logger.warn(f'excute the downloader backgroud!')
        
        self.is_need_stop = False
        self.downloadCtrl = DownloadControl()

        t = threading.Thread(target=self.downLoading, args=(urls, savePath))
        t2 = threading.Thread(target=self.inside_thread)
        t2.start()
        t.start()
            
    def downLoading(self, urls, savePath):
        try:
            self.downloadCtrl.downLoad_start(urls, savePath)
        except Exception as e1:
            logger.error(f"the input url:{urls} download fail, and error msg: {str(e1)}")
            messagebox.showinfo(title="严重", message="下载出现问题请稍后重试") 
            #self.is_need_stop = True
            logger.exception(e1)
            self.downloadCtrl.clear()
        
    def inside_thread(self):
        while True:
            metricInfo = self.downloadCtrl.get_total_metrics()
            if metricInfo == None:
               time.sleep(5)
               continue
            
            self.set_frame_view(metricInfo)

            if metricInfo.totalVedioCnt > 0 and metricInfo.totalFailCnt + metricInfo.totalSuccessCnt >= metricInfo.totalVedioCnt:
               logger.warn(f"have  down load finish, {metricInfo.to_string()}")
               self.is_need_stop = True
               break
               
            if not self.downloadCtrl.downloading:
               logger.warn(f'the downloader finish')
               break
          
            time.sleep(10)
                    
    def set_frame_view(self, metricInfo:TotalMetricInfo):
        currMetric = metricInfo.currentMetricInfo
        percent = currMetric.percentCurrent

        logger.warn(f'currentProgress:{percent}')
        self.progressbar.set(percent/100)
        
        inP = "Yes"
        if currMetric.totalVedioCnt == 0:
           inP = "Yes"
        else:
           inP = "No" if currMetric.successVedioCnt + currMetric.failVedioCnt < currMetric.totalVedioCnt else "Yes"

        info = PROGRESS_INFO.replace("UU", str(metricInfo.totalUrlCnt)).replace("CC", str(metricInfo.currentUrl))
        info = info.replace("TT", str(currMetric.totalVedioCnt)).replace("SS", str(currMetric.successVedioCnt)).replace("FF", str(currMetric.failVedioCnt)).replace("YY", inP)
        
        self.progress_label.configure(text=info)
       
if __name__ == "__main__":
    app = App()
    app.mainloop()
    #CommonTool.convert_pathPic_pyFile("imgs", "pictures_v3")
