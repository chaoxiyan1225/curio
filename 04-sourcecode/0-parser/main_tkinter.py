import customtkinter
import os
from PIL import Image
import webbrowser
import time
import asyncio

PIC_SIZE = 30
FRAME_NAMES = ["", "", ""]

class App(customtkinter.CTk):

    def __initImg__(self):
       # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
        #self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(PIC_SIZE, PIC_SIZE))
        self.download_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "download.png")),dark_image=Image.open(os.path.join(image_path, "download.png")), size=(PIC_SIZE, PIC_SIZE))
        self.shares_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "share.png")),dark_image=Image.open(os.path.join(image_path, "share.png")), size=(PIC_SIZE, PIC_SIZE))
        self.aboutus_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "aboutus.png")),dark_image=Image.open(os.path.join(image_path, "aboutus.png")), size=(PIC_SIZE, PIC_SIZE))
        self.search_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "search.png")),dark_image=Image.open(os.path.join(image_path, "search.png")), size=(PIC_SIZE, PIC_SIZE))
        self.download_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "download.png")),dark_image=Image.open(os.path.join(image_path, "download.png")), size=(PIC_SIZE, PIC_SIZE))
        self.more_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "more.png")),dark_image=Image.open(os.path.join(image_path, "more.png")), size=(PIC_SIZE, PIC_SIZE))
        self.language_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "language.png")),dark_image=Image.open(os.path.join(image_path, "language.png")), size=(PIC_SIZE, PIC_SIZE))
        self.register_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "register.png")),dark_image=Image.open(os.path.join(image_path, "register.png")), size=(PIC_SIZE, PIC_SIZE))
        self.confirm_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "confirm.png")),dark_image=Image.open(os.path.join(image_path, "confirm.png")), size=(PIC_SIZE, PIC_SIZE))                                         
        self.back_img = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "back.png")),dark_image=Image.open(os.path.join(image_path, "back.png")), size=(PIC_SIZE, PIC_SIZE))
                                             
    def __init__(self):
        super().__init__()

        self.title("Octopus Brother")

        self.geometry(f"{1000}x{580}")

        # set grid layout 1x2
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure(1, weight=1)
         
        # init images
        self.__initImg__()
      
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" BestVedioDownloader", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.download_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="DownLoad",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.download_img, anchor="w", command=self.download_button_event)
        self.download_button.grid(row=1, column=0, sticky="ew")

        self.shares_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Shares",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.shares_img, anchor="w", command=self.shares_button_event)
        self.shares_button.grid(row=2, column=0, sticky="ew")

        self.register_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Register",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.register_img, anchor="w", command=self.register_button_event)
        self.register_button.grid(row=3, column=0, sticky="ew")

        self.aboutus_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="AboutUs",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.aboutus_img, anchor="w", command=self.aboutus_button_event)
        self.aboutus_button.grid(row=4, column=0, sticky="ew")

        self.language_label =  customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=30, border_spacing=10, text="Language Select:",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w")
        self.language_label.grid(row=7, column=0, padx=20, pady=(10, 0) )

        self.language_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame,  values=["中文", "English", "Spnish"], 
                                                                       command=self.change_language_event)
        self.language_optionemenu.grid(row=8, column=0, padx=(0,20), pady=(0, 10))

        # create download frame
        self.download_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.download_frame.grid(row=3, column=10,  sticky="nsew")
        self.download_frame.grid_rowconfigure((1), weight=1)
        self.download_frame.grid_columnconfigure((0,10), weight=1)
       
        self.button = customtkinter.CTkButton(self.download_frame, text="Start", command=None, image=self.search_img)
        self.button.grid(row=0, column=0, columnspan=1, padx=(0,0), pady=20)

        self.entry = customtkinter.CTkEntry(self.download_frame, width = 400, placeholder_text="请输入网址")
        self.entry.grid(row=0, column=1, padx=(0,10), columnspan=11, pady=20, sticky="nsew")
        
        self.save_entry = customtkinter.CTkEntry(self.download_frame, width = 50, placeholder_text="输入影片名")
        self.save_entry.grid(row=0, column=12, padx=(0,10), pady=20, sticky="nsew")


        # create textbox
        self.textbox = customtkinter.CTkTextbox(self.download_frame, width=300)
        self.textbox.grid(row=1, column=0, columnspan=13, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
     
        # loadButton = customtkinter.CTkButton(self.download_frame, text="Bars", image=self.download_img)
        # loadButton.grid(row=5, column=0, columnspan=1, padx=(0,20), pady=20)

        progressbar = customtkinter.CTkProgressBar(self.download_frame)
        progressbar.grid(row=5, column=0, columnspan=12, padx=20, pady=20, sticky="nsew")
        progressbar.set(0.01)

        buttonOpen = customtkinter.CTkButton(self.download_frame, text="Open", image=self.more_img)
        buttonOpen.grid(row=5, column=12, columnspan=1, padx=(20,10), pady=20)

        # create shares frame
        self.shares_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.shares_frame.grid_columnconfigure((1), weight=1)
        self.shares_frame.grid_rowconfigure((1), weight=0)


        # create register frame
        self.register_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.register_frame.grid_columnconfigure((1), weight=1)
        self.register_frame.grid_rowconfigure((1), weight=0)


        self.tel_label = customtkinter.CTkLabel(self.register_frame, text="TelNum:", 
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.tel_label.grid(row=0, column=0, padx=(10,0), pady=(20,10))
        self.tel_entry = customtkinter.CTkEntry(self.register_frame, width = 50, placeholder_text="please input telNum")
        self.tel_entry.grid(row=0, column=1, columnspan=2,sticky="nsew", padx=(5,5), pady=(20,10))
        
        self.tel_info_label = customtkinter.CTkLabel(self.register_frame, text="* You must give me your tel exactly",
                                                compound="left", font=customtkinter.CTkFont(size=15))
        self.tel_info_label.grid(row=0, column=3, padx=(0,20), pady=(20,10))


        self.email_label = customtkinter.CTkLabel(self.register_frame, text="Email:", 
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.email_label.grid(row=1, column=0, padx=(10,0), pady=10)
        self.email_entry = customtkinter.CTkEntry(self.register_frame, width =50, placeholder_text="please input email")
        self.email_entry.grid(row=1, column=1, columnspan=2,sticky="nsew", padx=(0,5), pady=10)

        self.email_info_label = customtkinter.CTkLabel(self.register_frame, text="* You must give me your Email exactly",
                                                compound="left", font=customtkinter.CTkFont(size=15))
        self.email_info_label.grid(row=1, column=3, padx=(0,20), pady=10)


        self.submit_button = customtkinter.CTkButton(self.register_frame, text="submit", command=None, image=self.confirm_img)
        self.submit_button.grid(row=2, column=1, columnspan=1, padx=(0,0), pady=20)

        #create textbox
        self.register_box = customtkinter.CTkTextbox(self.register_frame, width=280)
        self.register_box.grid(row=3, column=0, columnspan=10, padx=(20, 0), pady=(20, 0), sticky="nsew")
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

        # select default frame
        self.select_frame_by_name("download")
        self.change_appearance_mode_event("light")

        self.after(1000, self.async_load_urls)

        print("start end ")

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

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def async_load_urls(self):
        print("start ---")
        time.sleep(5)
        table = []
        row = []  #row里面加满一行的就添加到上面的table里，使table成为一个二维列表。
        print("start fill table")
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
