from tkinter import *
from tkinter import messagebox
from ctypes import windll
from licensing.models import *
from licensing.methods import Key, Helpers
from tkinter import font
from PIL import ImageTk, Image
import os
import shutil
import subprocess
import re
import platform
import wmi
import psutil
import GPUtil
import webbrowser
import pickle
import time
import winreg

# Loading window
loading_window = Tk()

width_of_window = 427
height_of_window = 250
screen_width = loading_window.winfo_screenwidth()
screen_height = loading_window.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
loading_window.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
loading_window.overrideredirect(1)  # for hiding titlebar
loading_window.iconbitmap("_internal/icon.ico")

Frame(loading_window, width=427, height=250, bg='#272727').place(x=0, y=0)
ghost_icon = PhotoImage(file='_internal/icon.png')
label1 = Label(loading_window, image=ghost_icon, bg='#272727')
label1.image = ghost_icon  # Reference to the image to prevent garbage collection
label1.place(x=165, y=35)

label2 = Label(loading_window, text='Loading...', fg='white', bg='#272727')  # decorate it 
label2.configure(font=("Calibri", 11))
label2.place(x=10, y=215)

image_a = ImageTk.PhotoImage(Image.open('_internal/c2.png'))
image_b = ImageTk.PhotoImage(Image.open('_internal/c1.png'))

for i in range(5):  # 5 loops
    l1 = Label(loading_window, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
    l2 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
    l3 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
    l4 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
    loading_window.update_idletasks()
    time.sleep(0.5)

    l1 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
    l2 = Label(loading_window, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
    l3 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
    l4 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
    loading_window.update_idletasks()
    time.sleep(0.5)

    l1 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
    l2 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
    l3 = Label(loading_window, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
    l4 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
    loading_window.update_idletasks()
    time.sleep(0.5)

    l1 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
    l2 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
    l3 = Label(loading_window, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
    l4 = Label(loading_window, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
    loading_window.update_idletasks()
    time.sleep(0.5)

loading_window.destroy()



# Create the main window
################### title bar ###################

tk_title = "GhostOptimizer" 

root=Tk()
root.title(tk_title) 
root.overrideredirect(True) # Turn off Windows Title Bar
root.geometry('900x600+75+75')
root.minimized = False
root.maximized = False
root.iconbitmap("_internal/icon.ico")


LGRAY = '#3e4042' # button color effects
DGRAY = '#25292e' # window background color
RGRAY = '#10121f' # title bar color

root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)


def set_appwindow(mainWindow):

    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())
    

def minimize_me():
    root.attributes("-alpha",0)
    root.minimized = True       


def deminimize(event):

    root.focus() 
    root.attributes("-alpha",1)
    if root.minimized == True:
        root.minimized = False                              
        

def maximize_me():

    if root.maximized == False:
        root.normal_size = root.geometry()
        expand_button.config(text=" 🗗 ")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.maximized = not root.maximized 
        
    else:
        expand_button.config(text=" 🗖 ")
        root.geometry(root.normal_size)
        root.maximized = not root.maximized


close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)


window = Frame(root, bg=DGRAY,highlightthickness=0)


title_bar.pack(fill=X)
close_button.pack(side=RIGHT,ipadx=7,ipady=1)
expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
title_bar_title.pack(side=LEFT, padx=10)
window.pack(expand=1, fill=BOTH)


def changex_on_hovering(event):
    global close_button
    close_button['bg']='red'
    
    
def returnx_to_normalstate(event):
    global close_button
    close_button['bg']=RGRAY
    

def change_size_on_hovering(event):
    global expand_button
    expand_button['bg']=LGRAY
    
    
def return_size_on_hovering(event):
    global expand_button
    expand_button['bg']=RGRAY
    

def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=LGRAY
    
    
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=RGRAY
    

def get_pos(event):
    if root.maximized == False:
 
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        
        def move_window(event): 
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


        def release_window(event):
            root.config(cursor="arrow")
            
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
    else:
        expand_button.config(text=" 🗖 ")
        root.maximized = not root.maximized

title_bar.bind('<Button-1>', get_pos) 
title_bar_title.bind('<Button-1>', get_pos) 

close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
expand_button.bind('<Enter>', change_size_on_hovering)
expand_button.bind('<Leave>', return_size_on_hovering)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)

# resize the window width
resizex_widget = Frame(window,bg=DGRAY,cursor='sb_h_double_arrow')
resizex_widget.pack(side=RIGHT,ipadx=2,fill=Y)


def resizex(event):
    xwin = root.winfo_x()
    difference = (event.x_root - xwin) - root.winfo_width()
    
    if root.winfo_width() > 150 :
        try:
            root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
        except:
            pass
    else:
        if difference > 0: 
            try:
                root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
            except:
                pass
              
    resizex_widget.config(bg=DGRAY)

resizex_widget.bind("<B1-Motion>",resizex)

# resize the window height
resizey_widget = Frame(window,bg=DGRAY,cursor='sb_v_double_arrow')
resizey_widget.pack(side=BOTTOM,ipadx=2,fill=X)

def resizey(event):
    ywin = root.winfo_y()
    difference = (event.y_root - ywin) - root.winfo_height()

    if root.winfo_height() > 150: 
        try:
            root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
        except:
            pass
    else:
        if difference > 0: 
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass

    resizex_widget.config(bg=DGRAY)

resizey_widget.bind("<B1-Motion>",resizey)


root.bind("<FocusIn>",deminimize)
root.after(10, lambda: set_appwindow(root)) 


################### end of title bar ###################




# Left side frame
category_menu_frame = Frame(window, bg=RGRAY, width=400) 
category_menu_frame.pack(side=LEFT, fill=Y)

# Buttons
category_button1 = Button(category_menu_frame, text='Home Page', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button2 = Button(category_menu_frame, text='Optimization', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button3 = Button(category_menu_frame, text='Optimization [PRO]', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button4 = Button(category_menu_frame, text='Registry Options', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button5 = Button(category_menu_frame, text='Pc Info', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button6 = Button(category_menu_frame, text='Credits', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)

# Add Buttons to frame
category_button1.pack(side=TOP, fill=X, pady=2) 
category_button2.pack(side=TOP, fill=X, pady=2)
category_button3.pack(side=TOP, fill=X, pady=2)
category_button4.pack(side=TOP, fill=X, pady=2)
category_button5.pack(side=TOP, fill=X, pady=2)
category_button6.pack(side=TOP, fill=X, pady=2)


# Light up buttons
def on_enter(event):
    event.widget['bg'] = LGRAY

def on_leave(event):
    event.widget['bg'] = RGRAY

category_button1.bind('<Enter>', on_enter)
category_button1.bind('<Leave>', on_leave)
category_button2.bind('<Enter>', on_enter)
category_button2.bind('<Leave>', on_leave)
category_button3.bind('<Enter>', on_enter)
category_button3.bind('<Leave>', on_leave)
category_button4.bind('<Enter>', on_enter)
category_button4.bind('<Leave>', on_leave)
category_button5.bind('<Enter>', on_enter)
category_button5.bind('<Leave>', on_leave)
category_button6.bind('<Enter>', on_enter)
category_button6.bind('<Leave>', on_leave)


# Switch categories
def switch_category(category_frame):
    if hasattr(root, 'current_category_frame'):
        root.current_category_frame.destroy()

    root.current_category_frame = category_frame()
    root.current_category_frame.pack(side=LEFT, fill=BOTH, expand=True)










def show_notification(message):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Notification", message)
    root.destroy()

############ Category 1 ############
def callback(url):
    webbrowser.open_new(url)

def create_restore_point():
    try:
        # Tworzenie punktu przywracania o nazwie "GhostOptimizer"
        subprocess.run(['powershell', '-Command', 'Checkpoint-Computer -Description "GhostOptimizer" -RestorePointType "MODIFY_SETTINGS"'])
        print("Restore point 'GhostOptimizer' created successfully.")
        show_notification(f"Restore point created successfully.")
    except Exception as e:
        print(f"Error creating restore point: {e}")


def display_category1():
    category_frame = Frame(window, bg=DGRAY)

    image = PhotoImage(file="_internal/BigImage.png")
    image_label = Label(category_frame, image=image, bg=DGRAY)
    image_label.image = image
    image_label.pack(pady=20)

    label = Label(category_frame, text='Welcome!', font=("calibri", 25, "bold"), bg=DGRAY, fg='white')
    label.pack(pady=00)

    # ITEM1
    proceed_button = Button(category_frame, text='Create Restore Point', command=create_restore_point, font=("calibri", 12),
                            bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button.bind("<Enter>", on_enter)
    proceed_button.bind("<Leave>", on_leave)
    proceed_button.pack(pady=100)

    return category_frame


############ Category 2 ############
def clear_temp():
    try:
        temp_folder_path = os.path.join(os.environ['TEMP'])
        
        files = os.listdir(temp_folder_path)

        for file in files:
            file_path = os.path.join(temp_folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Nie udało się usunąć pliku/folderu: {e}")

        show_notification(f"Folder {temp_folder_path} has been cleared successfully.")
    except Exception as e:
        print(f"Błąd podczas czyszczenia folderu temp: {e}")

def clear_temp2():
    try:
        temp_folder_path = os.path.join(os.environ['SystemRoot'], 'Temp')
        
        files = os.listdir(temp_folder_path)

        for file in files:
            file_path = os.path.join(temp_folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Nie udało się usunąć pliku/folderu: {e}")

        show_notification(f"Folder {temp_folder_path} has been cleared successfully.")
    except Exception as e:
        print(f"Błąd podczas czyszczenia folderu temp w katalogu Windows: {e}")

def ultimate_power():
    command = "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"
    try:
        subprocess.run(command, shell=True, check=True)
        show_notification(f'Power plan "Ultimate Performance" added successfully')
    except subprocess.CalledProcessError as e:
        print(f"Error setting power plan to Ultimate Performance: {e}")

def open_power_settings():
    try:
        subprocess.run(["control", "powercfg.cpl"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def clear_prefetch():
    try:
        prefetch_folder_path = os.path.join(os.environ['SystemRoot'], 'Prefetch')
        
        files = os.listdir(prefetch_folder_path)

        for file in files:
            file_path = os.path.join(prefetch_folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Nie udało się usunąć pliku/folderu: {e}")

        show_notification(f"Folder {prefetch_folder_path} has been cleared successfully.")
    except Exception as e:
        print(f"Błąd podczas czyszczenia folderu prefetch w katalogu Windows: {e}")




def display_category2():
    category_frame = Frame(window, bg=DGRAY)
    category_frame.pack()

    # ITEM1
    label = Label(category_frame, text='Clean the APPDATA TEMP folder', font=("calibri", 16), bg=DGRAY, fg='white')
    label.grid(row=0, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button = Button(category_frame, text='PROCEED', command=clear_temp, font=("calibri", 12),
                            bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button.grid(row=0, column=2, pady=10, padx=20, sticky="e")
    proceed_button.bind("<Enter>", on_enter)
    proceed_button.bind("<Leave>", on_leave)

    # ITEM2
    label2 = Label(category_frame, text='Clean the TEMP folder', font=("calibri", 16), bg=DGRAY, fg='white')
    label2.grid(row=1, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button2 = Button(category_frame, text='PROCEED', command=clear_temp2, font=("calibri", 12),
                             bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button2.grid(row=1, column=2, pady=10, padx=20, sticky="e")
    proceed_button2.bind("<Enter>", on_enter)
    proceed_button2.bind("<Leave>", on_leave)

    # ITEM3
    label3 = Label(category_frame, text='Clean the PREFETCH folder', font=("calibri", 16), bg=DGRAY, fg='white')
    label3.grid(row=2, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button3 = Button(category_frame, text='PROCEED', command=clear_prefetch, font=("calibri", 12),
                             bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button3.grid(row=2, column=2, pady=10, padx=20, sticky="e")
    proceed_button3.bind("<Enter>", on_enter)
    proceed_button3.bind("<Leave>", on_leave)

    # ITEM4
    label4 = Label(category_frame, text='Add "Ultimate Performance" power plan', font=("calibri", 16), bg=DGRAY, fg='white')
    label4.grid(row=3, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button4 = Button(category_frame, text='PROCEED', command=ultimate_power, font=("calibri", 12),
                             bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button4.grid(row=3, column=2, pady=10, padx=20, sticky="e")
    proceed_button4.bind("<Enter>", on_enter)
    proceed_button4.bind("<Leave>", on_leave)

    # ITEM5
    label5 = Label(category_frame, text='Open power plan settings', font=("calibri", 16), bg=DGRAY, fg='white')
    label5.grid(row=4, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button5 = Button(category_frame, text='PROCEED', command=open_power_settings, font=("calibri", 12),
                             bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button5.grid(row=4, column=2, pady=10, padx=20, sticky="e")
    proceed_button5.bind("<Enter>", on_enter)
    proceed_button5.bind("<Leave>", on_leave)

    return category_frame


############ Category 3 ############
def telemetry_off():
    commands = [
        "sc delete DiagTrack",
        "sc delete dmwappushservice",
        "sc delete WerSvc",
        "sc delete OneSyncSvc",
        "sc delete MessagingService",
        "sc delete wercplsupport",
        "sc delete PcaSvc",
        "sc config wlidsvc start=demand",
        "sc delete wisvc",
        "sc delete RetailDemo",
        "sc delete diagsvc",
        "sc delete shpamsvc",
        "sc delete TermService",
        "sc delete UmRdpService",
        "sc delete SessionEnv",
        "sc delete TroubleshootingSvc",
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "wscsvc" ^| find /i "wscsvc"\') do (reg delete %I /f)',
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "OneSyncSvc" ^| find /i "OneSyncSvc"\') do (reg delete %I /f)',
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "MessagingService" ^| find /i "MessagingService"\') do (reg delete %I /f)',
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "PimIndexMaintenanceSvc" ^| find /i "PimIndexMaintenanceSvc"\') do (reg delete %I /f)',
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "UserDataSvc" ^| find /i "UserDataSvc"\') do (reg delete %I /f)',
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "UnistoreSvc" ^| find /i "UnistoreSvc"\') do (reg delete %I /f)',
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "BcastDVRUserService" ^| find /i "BcastDVRUserService"\') do (reg delete %I /f)',
        'for /f "tokens=1" %I in (\'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Services" /k /f "Sgrmbroker" ^| find /i "Sgrmbroker"\') do (reg delete %I /f)',
        "sc delete diagnosticshub.standardcollector.service",
        'reg add "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Siuf\\Rules" /v "NumberOfSIUFInPeriod" /t REG_DWORD /d 0 /f',
        'reg delete "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Siuf\\Rules" /v "PeriodInNanoSeconds" /f',
        'reg add "HKLM\\SYSTEM\\ControlSet001\\Control\\WMI\\AutoLogger\\AutoLogger-Diagtrack-Listener" /v Start /t REG_DWORD /d 0 /f',
        'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v AITEnable /t REG_DWORD /d 0 /f',
        'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v DisableInventory /t REG_DWORD /d 1 /f',
        'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v DisablePCA /t REG_DWORD /d 1 /f',
        'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat" /v DisableUAR /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\MicrosoftEdge\\PhishingFilter" /v "EnabledV9" /t REG_DWORD /d 0 /f',
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "EnableSmartScreen" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Microsoft\\Internet Explorer\\PhishingFilter" /v "EnabledV9" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v "NoRecentDocsHistory" /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\CompatTelRunner.exe" /v Debugger /t REG_SZ /d "%windir%\\System32\\taskkill.exe" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\DeviceCensus.exe" /v Debugger /t REG_SZ /d "%windir%\\System32\\taskkill.exe" /f'
    ]

    for command in commands:
        subprocess.run(command, shell=True)      
    show_notification(f'Telemetry has been disabled successfully')  

def windows_hello():
    commands = [
        'schtasks /Change /TN "\Microsoft\Windows\HelloFace\FODCleanupTask" /Disable'
    ]

    for command in commands:
        subprocess.run(command, shell=True)
    show_notification(f'Windows Hello has been disabled successfully')          
    
def disable_maps_tasks():
    commands = [
        'sc delete MapsBroker',
        'sc delete lfsvc',
        'schtasks /Change /TN "\\Microsoft\\Windows\\Maps\\MapsUpdateTask" /disable',
        'schtasks /Change /TN "\\Microsoft\\Windows\\Maps\\MapsToastTask" /disable'
    ]

    for command in commands:
        subprocess.run(command, shell=True)
    show_notification(f'Maps has been removed successfully')  

def uninstall_onedrive():
    commands = [
        r'%SystemRoot%\SysWOW64\OneDriveSetup.exe /uninstall',
        rf'rd "{os.path.expanduser("~")}\\OneDrive" /s /q',
        rf'rd "{os.environ["LocalAppData"]}\\Microsoft\\OneDrive" /s /q',
        rf'rd "{os.environ["ProgramData"]}\\Microsoft OneDrive" /s /q',
        r'rd "C:\OneDriveTemp" /s /q',
        rf'del "{os.path.expanduser("~")}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\OneDrive.lnk" /s /f /q'
    ]

    for command in commands:
        subprocess.run(command, shell=True)
    show_notification(f'OneDrive has been uninstalled successfully')  

def disable_cortana_and_bing_search():
    commands = [
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy\\FirewallRules" /v "{2765E0F4-2918-4A46-B9C9-43CDD8FCBA2B}" /t REG_SZ /d "BlockCortana|Action=Block|Active=TRUE|Dir=Out|App=C:\\windows\\systemapps\\microsoft.windows.cortana_cw5n1h2txyewy\\searchui.exe|Name=Search and Cortana application|AppPkgId=S-1-15-2-1861897761-1695161497-2927542615-642690995-327840285-2659745135-2630312742|" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" /v BingSearchEnabled /t REG_DWORD /d 0 /f'
    ]

    for command in commands:
        subprocess.run(command, shell=True)

def disable_windows_error_reporting():
    commands = [
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f'
    ]

    for command in commands:
        subprocess.run(command, shell=True)

def disable_setting_sync():
    commands = [
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\SettingSync" /v DisableSettingSync /t REG_DWORD /d 2 /f',
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\SettingSync" /v DisableSettingSyncUserOverride /t REG_DWORD /d 1 /f'
    ]

    for command in commands:
        subprocess.run(command, shell=True)

def install_wim_tweak2_command():
    command = 'install_wim_tweak.exe /o /c Microsoft-Windows-ContactSupport /r'
    subprocess.run(command, shell=True)

def remove_3d_edit_associations():
    commands = [
        'for /f "tokens=1* delims=" %I in (\'reg query "HKEY_CLASSES_ROOT\\SystemFileAssociations" /s /k /f "3D Edit" ^| find /i "3D Edit"\') do (reg delete "%I" /f)',
        'for /f "tokens=1* delims=" %I in (\'reg query "HKEY_CLASSES_ROOT\\SystemFileAssociations" /s /k /f "3D Print" ^| find /i "3D Print"\') do (reg delete "%I" /f)'
    ]

    for command in commands:
        subprocess.run(command, shell=True)

def install_wim_tweak3_command():
    command = 'install_wim_tweak.exe /o /c Microsoft-PPIProjection-Package /r'
    subprocess.run(command, shell=True)


def display_category3():
    category_frame = Frame(window, bg=DGRAY)
    category_frame.pack()

    # ITEM1
    label1 = Label(category_frame, text='Disable Telemetry', font=("calibri", 16), bg=DGRAY, fg='white')
    label1.grid(row=0, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button1 = Button(category_frame, text='PROCEED', command=telemetry_off, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button1.grid(row=0, column=2, pady=10, padx=20, sticky="e")
    proceed_button1.bind("<Enter>", on_enter)
    proceed_button1.bind("<Leave>", on_leave)

    # ITEM2
    label2 = Label(category_frame, text='Disable "Windows Hello"', font=("calibri", 16), bg=DGRAY, fg='white')
    label2.grid(row=1, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button2 = Button(category_frame, text='PROCEED', command=windows_hello, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button2.grid(row=1, column=2, pady=10, padx=20, sticky="e")
    proceed_button2.bind("<Enter>", on_enter)
    proceed_button2.bind("<Leave>", on_leave)

    # ITEM3
    label3 = Label(category_frame, text='Remove Maps', font=("calibri", 16), bg=DGRAY, fg='white')
    label3.grid(row=2, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button3 = Button(category_frame, text='PROCEED', command=disable_maps_tasks, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button3.grid(row=2, column=2, pady=10, padx=20, sticky="e")
    proceed_button3.bind("<Enter>", on_enter)
    proceed_button3.bind("<Leave>", on_leave)

    # ITEM4
    label4 = Label(category_frame, text='Remove OneDrive', font=("calibri", 16), bg=DGRAY, fg='white')
    label4.grid(row=3, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button4 = Button(category_frame, text='PROCEED', command=uninstall_onedrive, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button4.grid(row=3, column=2, pady=10, padx=20, sticky="e")
    proceed_button4.bind("<Enter>", on_enter)
    proceed_button4.bind("<Leave>", on_leave)

    # ITEM5
    label5 = Label(category_frame, text='Disable Cortana', font=("calibri", 16), bg=DGRAY, fg='white')
    label5.grid(row=4, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button5 = Button(category_frame, text='PROCEED', command=disable_cortana_and_bing_search, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button5.grid(row=4, column=2, pady=10, padx=20, sticky="e")
    proceed_button5.bind("<Enter>", on_enter)
    proceed_button5.bind("<Leave>", on_leave)

    # ITEM6
    label6 = Label(category_frame, text='Disable Windows Error Reporting', font=("calibri", 16), bg=DGRAY, fg='white')
    label6.grid(row=5, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button6 = Button(category_frame, text='PROCEED', command=disable_windows_error_reporting, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button6.grid(row=5, column=2, pady=10, padx=20, sticky="e")
    proceed_button6.bind("<Enter>", on_enter)
    proceed_button6.bind("<Leave>", on_leave)

    # ITEM7
    label7 = Label(category_frame, text='Disable Settings Sync', font=("calibri", 16), bg=DGRAY, fg='white')
    label7.grid(row=6, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button7 = Button(category_frame, text='PROCEED', command=disable_setting_sync, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button7.grid(row=6, column=2, pady=10, padx=20, sticky="e")
    proceed_button7.bind("<Enter>", on_enter)
    proceed_button7.bind("<Leave>", on_leave)

    # ITEM8
    label8 = Label(category_frame, text='Disable Windows Get Help', font=("calibri", 16), bg=DGRAY, fg='white')
    label8.grid(row=7, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button8 = Button(category_frame, text='PROCEED', command=install_wim_tweak2_command, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button8.grid(row=7, column=2, pady=10, padx=20, sticky="e")
    proceed_button8.bind("<Enter>", on_enter)
    proceed_button8.bind("<Leave>", on_leave)

    # ITEM9
    label9 = Label(category_frame, text='Disable Microsoft-PPIProjection-Package', font=("calibri", 16), bg=DGRAY, fg='white')
    label9.grid(row=8, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button9 = Button(category_frame, text='PROCEED', command=install_wim_tweak3_command, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button9.grid(row=8, column=2, pady=10, padx=20, sticky="e")
    proceed_button9.bind("<Enter>", on_enter)
    proceed_button9.bind("<Leave>", on_leave)

    # ITEM10
    label10 = Label(category_frame, text='Disable Paint 3D Print', font=("calibri", 16), bg=DGRAY, fg='white')
    label10.grid(row=9, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button10 = Button(category_frame, text='PROCEED', command=remove_3d_edit_associations, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button10.grid(row=9, column=2, pady=10, padx=20, sticky="e")
    proceed_button10.bind("<Enter>", on_enter)
    proceed_button10.bind("<Leave>", on_leave)

    return category_frame


############ Category 4 ############
def powerlimit_off():
    try:

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling", 0, winreg.KEY_SET_VALUE)

        winreg.SetValueEx(key, "PowerThrottlingOff", 0, winreg.REG_DWORD, 1)

        winreg.CloseKey(key)
        
        show_notification("Power limits disabled successfully.")
    except Exception as e:
        print("An error occurred:", e)

def networklimit_off():
    try:

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", 0, winreg.KEY_SET_VALUE)

        winreg.SetValueEx(key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 0xffffffff)
        winreg.SetValueEx(key, "SystemResponsiveness", 0, winreg.REG_DWORD, 0x0)

        winreg.CloseKey(key)
        
        show_notification("Network limits disabled successfully.")
    except Exception as e:
        print("An error occurred:", e)

def hibernation_off():
    try:

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", 0, winreg.KEY_SET_VALUE)

        winreg.SetValueEx(key, "HibernateEnabled", 0, winreg.REG_DWORD, 0x0)

        winreg.CloseKey(key)
        
        show_notification("Hibernation disabled successfully.")
    except Exception as e:
        print("An error occurred:", e)
        
def display_category4():
    category_frame = Frame(window, bg=DGRAY)
    category_frame.pack()

    # ITEM1
    label1 = Label(category_frame, text='Disable Power Limits', font=("calibri", 16), bg=DGRAY, fg='white')
    label1.grid(row=0, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button1 = Button(category_frame, text='PROCEED', command=powerlimit_off, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button1.grid(row=0, column=2, pady=10, padx=20, sticky="e")
    proceed_button1.bind("<Enter>", on_enter)
    proceed_button1.bind("<Leave>", on_leave)

    # ITEM2
    label2 = Label(category_frame, text='Disable Network Limits', font=("calibri", 16), bg=DGRAY, fg='white')
    label2.grid(row=1, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button2 = Button(category_frame, text='PROCEED', command=networklimit_off, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button2.grid(row=1, column=2, pady=10, padx=20, sticky="e")
    proceed_button2.bind("<Enter>", on_enter)
    proceed_button2.bind("<Leave>", on_leave)

    # ITEM3
    label3 = Label(category_frame, text='Disable Hibernation', font=("calibri", 16), bg=DGRAY, fg='white')
    label3.grid(row=2, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button3 = Button(category_frame, text='PROCEED', command=hibernation_off, font=("calibri", 12), bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button3.grid(row=2, column=2, pady=10, padx=20, sticky="e")
    proceed_button3.bind("<Enter>", on_enter)
    proceed_button3.bind("<Leave>", on_leave)

    return category_frame

############ Category 5 ############
def display_category5():
    category_frame = Frame(window, bg=DGRAY)
    pc = wmi.WMI()
    info = f"=========================== OS =========================== \n\n \
    Name: {platform.platform()}\n \
    Version: {platform.version()}\n \
    User Name: {platform.node()}\n\n \
    =========================== CPU =========================== \n\n \
    Name: {pc.Win32_Processor()[0].name}\n \
    Psyhical Cores: {psutil.cpu_count(logical=False)}\n \
    Total Cores: {psutil.cpu_count(logical=True)}\n\n \
    =========================== GPU =========================== \n\n \
    Name: {pc.Win32_VideoController()[0].name}\n\n \
    =========================== MEMORY =========================== \n\n \
    Total: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.2f} GB\n \
    Used: {psutil.virtual_memory().used / 1024 / 1024 / 1024:.2f} GB\n \
    Avaiable: {psutil.virtual_memory().available / 1024 / 1024 / 1024:.2f} GB\n \
    "
    label1 = Label(category_frame, text="Your PC", font=("comfortaa", 40, "bold"), bg=DGRAY, fg='white', anchor="w")
    label = Label(category_frame, text=info, font=("calibri", 13, "bold"), bg=DGRAY, fg='white', anchor="w")
    label.pack(pady=20)
    label1.pack(side='top', anchor=CENTER, pady=10)
    label.pack(side='bottom', anchor=CENTER, pady=10)
    return category_frame


############ Category 6 ############
def display_category6():
    category_frame = Frame(window, bg=DGRAY)
    label = Label(category_frame, text='\n\n\n\n\n\n\n\n\n\n\n\nGhostOptimizer\n\nDeveloped by Duchnes\nGitHub: https://github.com/Duchnes\nCountry: Poland\n\nSpecial thanks to the open-source community for their invaluable contributions.\n\n© 2024 GhostOptimizer - All rights reserved.', font=("calibri", 10, "bold"), bg=DGRAY, fg='white', anchor="w")
    label.pack(pady=20)
    label.pack(side='top', anchor=CENTER, pady=10)
    link1 = Label(category_frame, text="Github", font=("calibri", 10, "bold"), bg=DGRAY, fg="blue", cursor="hand2")
    link1.pack(side="top", anchor=CENTER)
    link1.bind("<Button-1>", lambda e: callback("https://github.com/Duchnes/GhostOptimizer"))
    return category_frame










# Bind category buttons to switch_category function
category_button1.configure(command=lambda: switch_category(display_category1))
category_button2.configure(command=lambda: switch_category(display_category2))
category_button3.configure(command=lambda: switch_category(display_category3))
category_button4.configure(command=lambda: switch_category(display_category4))
category_button5.configure(command=lambda: switch_category(display_category5))

# Display the initial category
switch_category(display_category1)


# Schedule the main_content function to be called after 3 seconds

root.mainloop()
