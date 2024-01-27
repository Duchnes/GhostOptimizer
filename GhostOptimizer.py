from tkinter import *
from tkinter import messagebox
from ctypes import windll
import os
import shutil
import subprocess
import re
import platform
import wmi
import psutil
import GPUtil

################### title bar ###################

tk_title = "GhostOptimizer" # Put here your window title

root=Tk() # root (your app doesn't go in root, it goes in window)
root.title(tk_title) 
root.overrideredirect(True) # turns off title bar, geometry
root.geometry('900x600+75+75') # set new geometry the + 75 + 75 is where it starts on the screen
#root.iconbitmap("your_icon.ico") # to show your own icon 
root.minimized = False # only to know if root is minimized
root.maximized = False # only to know if root is maximized


LGRAY = '#3e4042' # button color effects in the title bar (Hex color)
DGRAY = '#25292e' # window background color               (Hex color)
RGRAY = '#10121f' # title bar color                       (Hex color)

root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)


def set_appwindow(mainWindow): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True
    # Some WindowsOS styles, required for task bar integration
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
    root.attributes("-alpha",0) # so you can't see the window when is minimized
    root.minimized = True       


def deminimize(event):

    root.focus() 
    root.attributes("-alpha",1) # so you can see the window when is not minimized
    if root.minimized == True:
        root.minimized = False                              
        

def maximize_me():

    if root.maximized == False: # if the window was not maximized
        root.normal_size = root.geometry()
        expand_button.config(text=" 🗗 ")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.maximized = not root.maximized 
        # now it's maximized
        
    else: # if the window was maximized
        expand_button.config(text=" 🗖 ")
        root.geometry(root.normal_size)
        root.maximized = not root.maximized
        # now it is not maximized

# put a close button on the title bar
close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)

# a frame for the main area of the window, this is where the actual app will go
window = Frame(root, bg=DGRAY,highlightthickness=0)

# pack the widgets
title_bar.pack(fill=X)
close_button.pack(side=RIGHT,ipadx=7,ipady=1)
expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
title_bar_title.pack(side=LEFT, padx=10)
window.pack(expand=1, fill=BOTH) # replace this with your main Canvas/Frame/etc.
#xwin=None
#ywin=None
# bind title bar motion to the move window function

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
    

def get_pos(event): # this is executed when the title bar is clicked to move the window
    if root.maximized == False:
 
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        
        def move_window(event): # runs when window is dragged
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


        def release_window(event): # runs when window is released
            root.config(cursor="arrow")
            
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
    else:
        expand_button.config(text=" 🗖 ")
        root.maximized = not root.maximized

title_bar.bind('<Button-1>', get_pos) # so you can drag the window from the title bar
title_bar_title.bind('<Button-1>', get_pos) # so you can drag the window from the title 

# button effects in the title bar when hovering over buttons
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
    
    if root.winfo_width() > 150 : # 150 is the minimum width for the window
        try:
            root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
        except:
            pass
    else:
        if difference > 0: # so the window can't be too small (150x150)
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

    if root.winfo_height() > 150: # 150 is the minimum height for the window
        try:
            root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
        except:
            pass
    else:
        if difference > 0: # so the window can't be too small (150x150)
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass

    resizex_widget.config(bg=DGRAY)

resizey_widget.bind("<B1-Motion>",resizey)

# some settings
root.bind("<FocusIn>",deminimize) # to view the window by clicking on the window icon on the taskbar
root.after(10, lambda: set_appwindow(root)) # to see the icon on the task bar


################### end of title bar ###################


# Nowy Frame na lewej stronie dla menu kategorii
category_menu_frame = Frame(window, bg=RGRAY, width=400)  # Zwiększam szerokość menu dwukrotnie do 400 pikseli
category_menu_frame.pack(side=LEFT, fill=Y)

# Przykładowe przyciski kategorii (możesz dostosować do własnych potrzeb)
category_button1 = Button(category_menu_frame, text='Home Page', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button2 = Button(category_menu_frame, text='Optimization', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button3 = Button(category_menu_frame, text='Pc Info', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)
category_button4 = Button(category_menu_frame, text='Credits', bg=RGRAY, padx=15, pady=5, bd=0, fg='white', font=("calibri", 10), highlightthickness=0)

# Przypnij przyciski do Frame
category_button1.pack(side=TOP, fill=X, pady=2)  # Dodaj trochę większy odstęp od góry i dołu
category_button2.pack(side=TOP, fill=X, pady=2)
category_button3.pack(side=TOP, fill=X, pady=2)
category_button4.pack(side=TOP, fill=X, pady=2)

# Efekty podświetlania przycisków po najechaniu myszką
def on_enter(event):
    event.widget['bg'] = LGRAY

def on_leave(event):
    event.widget['bg'] = RGRAY

# Przypnij efekty podświetlania przycisków
category_button1.bind('<Enter>', on_enter)
category_button1.bind('<Leave>', on_leave)
category_button2.bind('<Enter>', on_enter)
category_button2.bind('<Leave>', on_leave)
category_button3.bind('<Enter>', on_enter)
category_button3.bind('<Leave>', on_leave)
category_button4.bind('<Enter>', on_enter)
category_button4.bind('<Leave>', on_leave)

# Function to switch between categories
def switch_category(category_frame):
    # Destroy current category frame (if exists)
    if hasattr(root, 'current_category_frame'):
        root.current_category_frame.destroy()

    # Create new category frame based on the selected category
    root.current_category_frame = category_frame()
    root.current_category_frame.pack(side=LEFT, fill=BOTH, expand=True)











############ Category 1 ############
def display_category1():
    category_frame = Frame(window, bg=DGRAY)

    # Dodajemy zdjęcie
    image = PhotoImage(file="BigImage.png")
    image_label = Label(category_frame, image=image, bg=DGRAY)
    image_label.image = image  # Zapobiega usuwaniu obrazu przez garbage collector
    image_label.pack(pady=20)

    # Dodajemy etykietę tekstu
    label = Label(category_frame, text='Welcome!', font=("calibri", 22, "bold"), bg=DGRAY, fg='white')
    label.pack(pady=00)

    return category_frame



############ Category 2 ############
def show_notification(message):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Notification", message)
    root.destroy()

def clear_temp():
    try:
        # Ścieżka do folderu temp (dla systemu Windows)
        temp_folder_path = os.path.join(os.environ['TEMP'])
        
        # Pobierz listę plików w folderze temp
        files = os.listdir(temp_folder_path)

        # Usuń każdy plik w folderze temp
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
        # Ścieżka do folderu temp w katalogu Windows
        temp_folder_path = os.path.join(os.environ['SystemRoot'], 'Temp')
        
        # Pobierz listę plików w folderze temp
        files = os.listdir(temp_folder_path)

        # Usuń każdy plik w folderze temp
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
    # Run powercfg command to set the power plan to "Ultimate Performance"
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
    label3 = Label(category_frame, text='Add "Ultimate Performance" power plan', font=("calibri", 16), bg=DGRAY, fg='white')
    label3.grid(row=2, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button3 = Button(category_frame, text='PROCEED', command=ultimate_power, font=("calibri", 12),
                             bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button3.grid(row=2, column=2, pady=10, padx=20, sticky="e")
    proceed_button3.bind("<Enter>", on_enter)
    proceed_button3.bind("<Leave>", on_leave)

    # ITEM4
    label4 = Label(category_frame, text='Open power plan settings', font=("calibri", 16), bg=DGRAY, fg='white')
    label4.grid(row=3, column=0, pady=10, padx=(10, 10), sticky="w")

    proceed_button4 = Button(category_frame, text='PROCEED', command=open_power_settings, font=("calibri", 12),
                             bg=RGRAY, fg='white', borderwidth=3, relief="raised", padx=10, pady=5, bd=0, highlightthickness=0)
    proceed_button4.grid(row=3, column=2, pady=10, padx=20, sticky="e")
    proceed_button4.bind("<Enter>", on_enter)
    proceed_button4.bind("<Leave>", on_leave)

    return category_frame

############ Category 3 ############
def display_category3():
    category_frame = Frame(window, bg=DGRAY)
    pc = wmi.WMI()
    info = f"=========================== OS =========================== \n\n \
    Name: {platform.platform()}\n \
    Version: {platform.node()}\n \
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

############ Category 4 ############
def display_category4():
    category_frame = Frame(window, bg=DGRAY)
    label = Label(category_frame, text='\n\n\n\n\n\n\n\n\n\n\n\n\nGhostOptimizer\n\nDeveloped by Duchnes\nGitHub: https://github.com/Duchnes\nCountry: Poland\n\nSpecial thanks to the open-source community for their invaluable contributions.\n\n© 2024 GhostOptimizer - All rights reserved.', font=("calibri", 10, "bold"), bg=DGRAY, fg='white', anchor="w")
    label.pack(pady=20)
    label.pack(side='top', anchor=CENTER, pady=10)
    return category_frame









# Bind category buttons to switch_category function
category_button1.configure(command=lambda: switch_category(display_category1))
category_button2.configure(command=lambda: switch_category(display_category2))
category_button3.configure(command=lambda: switch_category(display_category3))
category_button4.configure(command=lambda: switch_category(display_category4))

# Display the initial category
switch_category(display_category1)














root.mainloop()