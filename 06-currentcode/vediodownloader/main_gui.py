import customtkinter
import os
from PIL import Image
import webbrowser
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
from main_utils import *

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

        #self.iconbitmap('logo.ico')
        #tmp.ico
        tmp = open('tmp.ico', 'wb+')
        tmp.write(logo_ico)
        tmp.close()
        self.iconbitmap('tmp.ico')
        os.remove('tmp.ico')

        # set grid layout 1x2
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.userCtrl = UserContrl()
        self.sysCtrl = SoftWareContrl()
        self.LoginValid = False
         
        # init images
        self.__initImg__()
      
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" BestVedioDownloader", image=self.logo_image,  compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        #download 
        tmpR = 1
        self.download_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="DownLoad", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.download_img, anchor="w", command=self.download_button_event)
        self.download_button.grid(row=tmpR, column=0, sticky="ew")
        #getlatest version
        self.latest_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="GetLatest", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.more_img, anchor="w", command=self.latest_button_event)
        self.latest_button.grid(row=tmpR+1, column=0, sticky = "ew")
        #shares website
        self.shares_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Shares", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.shares_img, anchor="w", command=self.shares_button_event)
        self.shares_button.grid(row=tmpR+2, column=0, sticky = "ew")
        #register frame
        self.register_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Register", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.register_img, anchor="w", command=self.register_button_event)
        self.register_button.grid(row=tmpR+3, column=0, sticky="ew")
        #aboutus  
        self.aboutus_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="AboutUs", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.aboutus_img, anchor="w", command=self.aboutus_button_event)
        self.aboutus_button.grid(row=tmpR+4, column=0, sticky="ew")
        #language frame
        self.language_label =  customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=30, border_spacing=10, text="Language Select:", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.language_label.grid(row=7, column=0, padx=20, pady=(10, 0) )
        self.language_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["中文", "English", "Spnish"], command=self.change_language_event)
        self.language_optionemenu.grid(row=8, column=0, padx=(0,20), pady=(0, 10))

        # download frame
        self.download_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        #self.download_frame.grid(row=0, column=1,  sticky="nsew")
        self.download_frame.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)
        self.download_frame.grid_rowconfigure((0,1,3,4,5,6,7,8,9), weight=1)
        self.info_label =  customtkinter.CTkLabel(self.download_frame,corner_radius=0, height=15,  text="website url:",fg_color="transparent", text_color=("gray10", "gray90"),anchor="w")
        self.info_label.grid(row=1, column=0, padx=(20,0), pady=(0,0))
        self.more_button = customtkinter.CTkButton(self.download_frame, corner_radius=0, height=40, border_spacing=10, text="More vedio website", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.shares_img, anchor="w", command=self.more_button_event)
        self.more_button.grid(row=1, column=15, columnspan = 1)
        self.add_button =  customtkinter.CTkButton(self.download_frame, corner_radius=0, width=15,text="", fg_color="transparent",hover_color=("gray70", "gray30"), image=self.add_img, command= lambda: add_new(app))
        self.add_button.grid(row=2, column=0,padx=(0,0), columnspan=1, pady=(0, 0))
        self.url_entry = customtkinter.CTkEntry(self.download_frame, width = 380, placeholder_text="Paste the vedio url")
        self.url_entry.grid(row=2, column=1, padx=(10,10), columnspan=14, pady=(0, 0),sticky="ew")
        self.start_down_button = customtkinter.CTkButton(self.download_frame, text="download", command=lambda: start_downLoad(app))
        self.start_down_button.grid(row=2, column=15, columnspan=1, padx=(0,10), pady=(0,0))

        self.current_row = 2
        tmpR = 10
        self.progressbar = customtkinter.CTkProgressBar(self.download_frame, height= 30)
        self.progressbar.grid(row=tmpR, column=0, columnspan=14, padx=(20,10), pady=(0, 10), sticky="nsew")
        self.progressbar.set(0.01)
        self.current_label =  customtkinter.CTkLabel(self.download_frame, corner_radius=0, height=30,  text=f"  ", fg_color="transparent", text_color=("gray10", "gray90"), anchor="w", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.current_label.grid(row=tmpR, column=14, columnspan=3, padx=(20,0), pady=(0, 0), sticky="nsew")
        self.progress_label =  customtkinter.CTkLabel(self.download_frame, corner_radius=0, height=30,  text=f"{PROGRESS_INFO}", fg_color="transparent", text_color=("gray10", "gray90"), anchor="w")
        self.progress_label.grid(row=tmpR + 1, column=0, columnspan=16, padx=(20,0), pady=(0, 0), sticky="nsew")
        self.buttonOpen = customtkinter.CTkButton(self.download_frame, corner_radius=0, width=10, fg_color="transparent", text = " ", hover_color=("gray70", "gray30"), image=self.open_img, command=lambda: select_path(app))
        self.buttonOpen.grid(row=tmpR + 2, column=15, columnspan=1, padx=(0,0), pady=0)
        self.save_entry = customtkinter.CTkEntry(self.download_frame, width = 420,  placeholder_text="Select the path to save vedio")
        self.save_entry.grid(row=tmpR + 2, column=0, padx=(20,0), columnspan=15, pady=0, sticky="ew")
        self.tmp_label =  customtkinter.CTkLabel(self.download_frame, corner_radius=0, height=30,  text=f"", fg_color="transparent", text_color=("gray10", "gray90"), anchor="w")
        self.tmp_label.grid(row=tmpR + 3, column=0, columnspan=3, padx=(20,0), pady=(0, 0), sticky="nsew")
        
        #getLatest frame 
        self.latest_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.latest_frame.grid_columnconfigure((1), weight=1)
        self.latest_frame.grid_rowconfigure((1), weight=0)

        self.textbox_latest = customtkinter.CTkTextbox(self.latest_frame, width=260, bg_color="blue")
        self.textbox_latest.grid(row=0, column=0, columnspan=10, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox_latest.insert("0.0", "Welcome!!!\n\n" + f"Your software version is:V_{clientVersion}.\n\n\n")
        self.checkLatest_button = customtkinter.CTkButton(self.latest_frame, corner_radius=0, height=40, border_spacing=10, text="CheckLatest",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=self.back_img, anchor="w", command=self.checkLatest_button_event)
        self.checkLatest_button.grid(row=1, column = 0, padx=(20, 0), pady=(0, 20))
        self.is_need_stop = False

        #create shares frame
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
        self.tel_label = customtkinter.CTkLabel(self.register_frame, text="Your Telnum", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.tel_label.grid(row=rowNum+1, column=0, padx=(0,0), pady=(20,10))
        self.tel_entry = customtkinter.CTkEntry(self.register_frame, width = 50, placeholder_text="please input telNum")
        self.tel_entry.grid(row=rowNum+1, column=1, columnspan=10, padx=(0,300), pady=(20,10),sticky="nsew")
        self.email_label = customtkinter.CTkLabel(self.register_frame, text="Your  Email", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.email_label.grid(row=rowNum+2, column=0, padx=(0,0), pady=10)
        self.email_entry = customtkinter.CTkEntry(self.register_frame, width =50, placeholder_text="please input email")
        self.email_entry.grid(row=rowNum+2, column=1, columnspan=10, padx=(0,300), pady=10,sticky="nsew")
        self.submit_button = customtkinter.CTkButton(self.register_frame, text="register", command=lambda: register_submit_event(self), image=self.confirm_img)
        self.submit_button.grid(row=rowNum+3, column=0, columnspan=1, padx=(20,0), pady=20)
        self.step1_label = customtkinter.CTkLabel(self.register_frame, corner_radius=0, height=30, text="STEP-1", fg_color='transparent', text_color=("gray10", "gray90"), anchor='w')
        self.step1_label.grid(row=rowNum+3, column=1, columnspan=3, padx=(0, 400), pady=20)
        self.register_box = customtkinter.CTkTextbox(self.register_frame, width=400)
        self.register_box.grid(row=rowNum+5, column=0, columnspan=10, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.register_box.insert("0.0", "WARNING!!!\n\n" + "You need to register, if you want to use this software.You may pay little money for more "
                                 "comfirtable feels.\n\n First give me your email and telNum, and register for a free license code. \n\nSecond with the license code from step1 , by Paypall,VISA card or Wechat or Zhifubao to buy a high!")
        
        self.paypal_button = customtkinter.CTkButton(self.register_frame, text="paypal", command=lambda: openForPay(SystemConf.PAYPAL_URL), image=self.confirm_img)
        self.paypal_button.grid(row=rowNum+6, column=0, columnspan=1, padx=(20,30), pady=20)
        self.cbibank_button = customtkinter.CTkButton(self.register_frame, text="CBibank", command=lambda: openForPay(SystemConf.VISA_URL), image=self.confirm_img)
        self.cbibank_button.grid(row=rowNum+6, column=1, columnspan=1, padx=(20,30), pady=20)
        self.umpay_button = customtkinter.CTkButton(self.register_frame, text="Umpay", command=lambda: openForPay(SystemConf.CBIBANK_URL), image=self.confirm_img)
        self.umpay_button.grid(row=rowNum+6, column=2, columnspan=1, padx=(20,30), pady=20)

        self.step2_label = customtkinter.CTkLabel(self.register_frame, corner_radius=0, height=30, text="STEP-2", fg_color='transparent', text_color=("gray10", "gray90"), anchor='w')
        self.step2_label.grid(row=rowNum+6, column=3, columnspan=2, padx=(0, 100), pady=20)

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

        # select default frame
        self.select_frame_by_name("download")
        self.change_appearance_mode_event("light")

        t = threading.Thread(target=lambda: async_load_urls(self))
        t.start()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.download_button.configure(fg_color=("gray75", "gray25") if name == "download" else "transparent")
        self.register_button.configure(fg_color=("gray75", "gray25") if name == "register" else "transparent")
        self.aboutus_button.configure(fg_color=("gray75", "gray25") if name == "aboutus" else "transparent")   
        self.shares_button.configure(fg_color=("gray75", "gray25") if name == "shares" else "transparent")
        self.latest_button.configure(fg_color=("gray75", "gray25") if name == "latest" else "transparent")

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
        if name == "latest":
            self.latest_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.latest_frame.grid_forget()    
            

    def change_language_event(self):
        return

    def download_button_event(self):
        self.select_frame_by_name("download")

    def shares_button_event(self):
        self.select_frame_by_name("shares")
    
    def latest_button_event(self):
        self.select_frame_by_name("latest")

    def register_button_event(self):
        self.select_frame_by_name("register")
        
    def checkLatest_button_event(self):
        versionSLatest = self.sysCtrl.getLatestVersionFromS()
        self.textbox_latest.delete("0.0", tk.END)

        if SystemConf.clientVersion not in versionSLatest:
           #messagebox.showinfo(title="WARNING", message="Your version is old, there is newer version!")
           self.textbox_latest.insert('0.0', "Welcome!!!\n\n" + f"Your software version is:V_{clientVersion}.  The newest version is V_{versionSLatest}. \n\n Please click the GetLatest button for it!!")
           self.getLatest_button = customtkinter.CTkButton(self.latest_frame, corner_radius=0, height=40, border_spacing=10, text="GetLatest",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=self.confirm_img, anchor="w", command=self.getLatest_button_event)
           self.getLatest_button.grid(row=1, column = 1, padx=(20, 0), pady=(0, 20))
        else:
           self.textbox_latest.insert('0.0', "Welcome!!!\n\n" + f"Your software version is:V_{clientVersion}.\n\nYou are in the newest version!")
           messagebox.showinfo(title="WARNING", message="Your version is the latest version!") 

    # to aboutus page view 
    def aboutus_button_event(self):
        self.select_frame_by_name("aboutus")
        webbrowser.open('https://chaoxiyan1225.github.io/aboutme')

    # to getLatest sofeware view
    def getLatest_button_event(self):
        webbrowser.open('https://chaoxiyan1225.github.io/shareurls')

    # to aboutus page view 
    def more_button_event(self):
        webbrowser.open('https://chaoxiyan1225.github.io/shareurls')

    # to aboutus page view 
    def vip_button_event(self):
        webbrowser.open('https://chaoxiyan1225.github.io/business')

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
                  
if __name__ == "__main__":
    app = App()
    app.mainloop()
