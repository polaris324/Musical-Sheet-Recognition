# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:32:54 2021

@author: 易昶辰

"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import tkinterdnd2 as tkd # https://pythonguides.com/python-tkinter-drag-and-drop/ pip install tkinterdnd2

def drop(event):
    var.set(event.data)

def openByFilePath():
    print("Upload")# test
    file_location = e_box.get()
    # print(file_loc)# test
    
    showImage(file_location)
    # img = Image.open(file_loc)
    # canvas = tk.Canvas(ws, width=img.width // 5, height=img.height // 5, bg='gray')
    # img = img.resize( (img.width // 5, img.height // 5) )
    # image_file =  ImageTk.PhotoImage(img)
        
    # label = tk.Label(image = image_file)
    # label.grid(column=1, row=1 , padx=10, pady=10)
    #https://stackoverflow.com/questions/66159973/display-image-when-button-is-clicked-python-gui
    
    # return

def Upload():
    path = filedialog.askopenfilename()
    print(path)
    showImage(path)

def showImage(file_location):    
    image_width = Image.open(file_location).width
    image_height = Image.open(file_location).height
    if ( max(image_height, image_width) == image_height ):# vertical image
        resize_height = 600
        resize_width = 600/image_height*image_width
    else:# horizon image
        resize_height = 450/image_width*image_height
        resize_width = 450
    image_file = ImageTk.PhotoImage(Image.open(file_location).resize((int(resize_width), int(resize_height))))
    
    canvas.image = image_file
    canvas.create_image(225,300,anchor='center',image = image_file)

def showComboValueBySelect(event):
     #print("New Element Selected")# test
     print(combo.get())# test
     tempoText.set('Tempo of the sheet :' + combo.get())
     
def getComboValue():
     #print("New Element Selected")# test
     print(combo.get())# test
     tempoText.set('Tempo of the sheet :' + combo.get())
     #play_music(music_file)
#-----------------------------------------------------------------------------------------------
'''
import pygame

def play_music(midi_filename):
  #Stream music_file in a blocking manner
  clock = pygame.time.Clock()
  pygame.mixer.music.load(midi_filename)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    clock.tick(30) # check if playback has finished
    
midi_filename = 'Jenni Vartiainen - Ihmisten Edessa.mid'

# mixer config
freq = 44100  # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024   # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)

# listen for interruptions
try:
  # use the midi file you just saved
  play_music(midi_filename)
except KeyboardInterrupt:
  # if user hits Ctrl/C then exit
  # (works only in console mode)
  pygame.mixer.music.fadeout(1000)
  pygame.mixer.music.stop()
  raise SystemExit
'''
#-----------------------------------------------------------------------------------------------


# Initial window setting
ws = tkd.Tk()
ws.title("ProjectGUI")
ws.geometry("1115x750")
#ws.iconbitmap("Downloads\icon.ico")
ws.config(bg="lightgray")

# Create Frame for Canvas
frame = tk.Frame(ws)
canvas = tk.Canvas(frame, width=450, height=600)
canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

frame.grid(column=1, row=1, columnspan=3, rowspan=2)

# Drag and drop setting
var = tk.StringVar()
tk.Label(ws, text='Path of the Folder :',bg="lightgray").grid(column=0, row=0, padx=10, pady=10, sticky=tk.N)
# EnterBox
e_box = tk.Entry(ws, textvar=var, width=45)
e_box.grid(column=1, row=0 , padx=10, pady=10, sticky=tk.N)
e_box.drop_target_register(tkd.DND_FILES)
e_box.dnd_bind('<<Drop>>', drop)

# SendFilePath Button
btn_upload = tk.Button(ws, text='Send', command=openByFilePath)#https://stackoverflow.com/questions/13099908/python-tkinter-return-value-from-function-used-in-command
btn_upload.grid(column=2, row=0, padx=10, pady=5)

# Upload Button
btn_upload = tk.Button(ws, text='Upload', command=Upload)
btn_upload.grid(column=3, row=0, padx=10, pady=5)

# Fixed Image test
# img = Image.open(file_loc)
# img = Image.open("D:\Work\超越\OneDotIntro\icons\leaf.png")
# canvas = tk.Canvas(ws, width=img.width // 5, height=img.height // 5, bg='gray')
# canvas = tk.Canvas(ws, width = 45, height = 90, bg='white')
# img = img.resize( (img.width // 5, img.height // 5) )
# image_file =  ImageTk.PhotoImage(img)
# image = canvas.create_image(0, 0, anchor='nw', image=image_file)

# canvas.grid(column=1, row=1, rowspan=1,sticky='nswe')

#DirectEnter/SelectBox for Speed Selection
tempoText = tk.StringVar()
tempoText.set('Tempo of the sheet :')
# tk.Label(ws, text='Tempo of the sheet :',bg="lightgray").grid(column=4, row=0, padx=10, pady=10, sticky=tk.N)
tk.Label(ws, textvariable=tempoText,bg="lightgray", anchor=tk.W, width=32).grid(column=4, row=0, columnspan=3)
values=["Larghissimo -20",
        "Grave 20-40",
        "Langsam 40-45",
        "Largo 40-60",
        "Larghetto 60-66",
        "Adagio 66-76",
        "Andante 76-108",
        "Mäßig 108-120",
        "Allegro 120-168",
        "Vivace 138-168",
        "Presto 168-200",
        "Prestissimo 200-"]
combo = ttk.Combobox(ws,values = values)
combo.bind("<<ComboboxSelected>>", showComboValueBySelect)
combo.grid(column=4, row=1, pady=10, columnspan=3,sticky='NWE')
tk.Button(ws, text='Set Tempo', command=getComboValue).grid(column=7, row=1, padx=10, pady=10, sticky=tk.N)
#Exit Button
quit_buttom = tk.Button(ws, text="Exit Program", command=ws.destroy)
quit_buttom.grid(column=7, row=5, padx=10, pady=5)

#-----------------------------------------------------------------------------------------------
# Progress bar widget
progress = ttk.Progressbar(ws, orient = tk.HORIZONTAL,
              length = 100, mode = 'determinate')
  
# Function responsible for the updation
# of the progress bar value

cmd = False


def start():
    import time
    progress.start(1000)
    '''
    for per in range(100):
        progress['value'] = per
        ws.update_idletasks()
        ws.update()
        time.sleep(0.1)
        '''

def pause():
    progress.pause()

def stop():
    progress.stop()
    
    
progress.grid(column=4, row=1, columnspan=3, padx=10, pady=5,sticky='ews')

# This button will initialize
# the progress bar
tk.Button(ws, text = 'Start', command = start).grid(column=4, row=2, padx=10, pady=5, sticky='nwe')
tk.Button(ws, text = 'Pause', command = pause).grid(column=5, row=2, padx=10, pady=5, sticky='nwe')
tk.Button(ws, text = 'Stop', command = stop).grid(column=6, row=2, padx=10, pady=5, sticky='nwe')
#-----------------------------------------------------------------------------------------------



ws.mainloop()
# In[]

# 第1步，例項化object，建立視窗window
window = tk.Tk()

# 第2步，給視窗的視覺化起名字
window.title('Wellcome to Hongwei Website')

# 第3步，設定視窗的大小(長 * 寬)
window.geometry('400x300')  # 這裡的乘是小x

# 第4步，載入 wellcome image
canvas = tk.Canvas(window, width=400, height=135)#, bg='green
img = Image.open("ozono.png")
img = img.resize( (img.width // 10, img.height // 10) )
image_file =  ImageTk.PhotoImage(img)
image = canvas.create_image(200, 0, anchor='n', image=image_file)
canvas.pack(side='top')
tk.Label(window, text='Wellcome',font=('Arial', 16)).pack()

# 第5步，使用者資訊
tk.Label(window, text='User name:', font=('Arial', 14)).place(x=10, y=170)
tk.Label(window, text='Password:', font=('Arial', 14)).place(x=10, y=210)

# 第6步，使用者登入輸入框entry
# 使用者名稱
var_usr_name = tk.StringVar()
var_usr_name.set('example@python.com')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name, font=('Arial', 14))
entry_usr_name.place(x=120,y=175)
# 使用者密碼
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, font=('Arial', 14), show='*')
entry_usr_pwd.place(x=120,y=215)

# 第8步，定義使用者登入功能
def usr_login():
    # 這兩行程式碼就是獲取使用者輸入的usr_name和usr_pwd
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    # 這裡設定異常捕獲，當我們第一次訪問使用者資訊檔案時是不存在的，所以這裡設定異常捕獲。
    # 中間的兩行就是我們的匹配，即程式將輸入的資訊和檔案中的資訊匹配。
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        # 這裡就是我們在沒有讀取到`usr_file`的時候，程式會建立一個`usr_file`這個檔案，並將管理員
        # 的使用者和密碼寫入，即使用者名稱為`admin`密碼為`admin`。
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
            usr_file.close()    # 必須先關閉，否則pickle.load()會出現EOFError: Ran out of input

    # 如果使用者名稱和密碼與檔案中的匹配成功，則會登入成功，並跳出彈窗how are you? 加上你的使用者名稱。
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tkinter.messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
        # 如果使用者名稱匹配成功，而密碼輸入錯誤，則會彈出'Error, your password is wrong, try again.'
        else:
            tkinter.messagebox.showerror(message='Error, your password is wrong, try again.')
    else:  # 如果發現使用者名稱不存在
        is_sign_up = tkinter.messagebox.askyesno('Welcome！ ', 'You have not sign up yet. Sign up now?')
        # 提示需不需要註冊新使用者
        if is_sign_up:
            usr_sign_up()

# 第9步，定義使用者註冊功能
def usr_sign_up():
    def sign_to_Hongwei_Website():
        # 以下三行就是獲取我們註冊時所輸入的資訊
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        # 這裡是開啟我們記錄資料的檔案，將註冊資訊讀出
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        # 這裡就是判斷，如果兩次密碼輸入不一致，則提示Error, Password and confirm password must be the same!
        if np != npf:
            tkinter.messagebox.showerror('Error', 'Password and confirm password must be the same!')

        # 如果使用者名稱已經在我們的資料檔案中，則提示Error, The user has already signed up!
        elif nn in exist_usr_info:
            tkinter.messagebox.showerror('Error', 'The user has already signed up!')

        # 最後如果輸入無以上錯誤，則將註冊輸入的資訊記錄到檔案當中，並提示註冊成功Welcome！,You have successfully signed up!，然後銷燬視窗。
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tkinter.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            # 然後銷燬視窗。
            window_sign_up.destroy()

    # 定義長在視窗上的視窗
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('300x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()  # 將輸入的註冊名賦值給變數
    new_name.set('example@python.com')  # 將最初顯示定為'example@python.com'
    tk.Label(window_sign_up, text='User name: ').place(x=10, y=10)  # 將`User name:`放置在座標（10,10）。
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)  # 建立一個註冊名的`entry`，變數為`new_name`
    entry_new_name.place(x=130, y=10)  # `entry`放置在座標（150,10）.

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=130, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=130, y=90)

    # 下面的 sign_to_Hongwei_Website
    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_Hongwei_Website)
    btn_comfirm_sign_up.place(x=180, y=120)
# 第7步，login and sign up 按鈕
btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=120, y=240)
btn_sign_up = tk.Button(window, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=200, y=240)

# 第10步，主視窗迴圈顯示
window.mainloop()
# In[]
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


root = Tk()

#setting up a tkinter canvas with scrollbars
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# xscroll = Scrollbar(frame, orient=HORIZONTAL)
# xscroll.grid(row=1, column=0, sticky=E+W)
# yscroll = Scrollbar(frame)
# yscroll.grid(row=0, column=1, sticky=N+S)

# canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas = Canvas(frame)
canvas.grid(row=0, column=0, sticky=N+S+E+W)

# xscroll.config(command=canvas.xview)
# yscroll.config(command=canvas.yview)

frame.pack(fill=BOTH,expand=1)


#function to be called when mouse is clicked
def printcoords():
    File = filedialog.askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    filename = ImageTk.PhotoImage(Image.open(File))
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(0,0,anchor='nw',image=filename)

Button(root,text='choose',command=printcoords).pack()
root.mainloop()
'''