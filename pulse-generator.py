import tkinter as tk
from tkinter import ttk
import numpy as np
import serial
w = 50
h = 4

DELAY_MULT = 1
SERIAL_PORT = "/dev/ttyACM1"

current_widget = None
description_array = [[0 for x in range(w)] for y in range(h)]
lock_column = -1
only_on = 1
index_label_list = []
e4 = None
entry_nbr_repet = None
ser = None

class TagCanvas(tk.Canvas):
    def __init__(self, master, col, row, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.master = master
        self.col = col
        self.row = row
        self.configure(bg='white')


    def toggle_onoff(self):
        global only_on
        global description_array
        if (description_array[self.row][self.col] == 1):
            if (only_on == 0):
                description_array[self.row][self.col] = 0
                self.configure(bg='white')
                generateCommandLine(description_array)

        else:
            if (only_on == 1):
                description_array[self.row][self.col] = 1
                self.configure(bg=getChanelColor(self.row))
                generateCommandLine(description_array)
        
def generateInnerCommandLine(value_array):
    changeArray = getChangeArray(value_array)
    changeArray = np.transpose(changeArray)
    changeArray = changeArray[:-1]
    innerCommand = ""
    delay_accu = 0
    for col in changeArray:
        isChangeOnThisTime = not all([ v == 0 for v in col ])
        if (isChangeOnThisTime):
            if (delay_accu != 0):
                try:
                    innerCommand = innerCommand + "d" + str(delay_accu*int(entry_square_time.get())) + ","
                except:
                    innerCommand = innerCommand + "d" + str(delay_accu*int(1)) + ","
                delay_accu = 0
            k = 0
            for ro in col:
                if ro == 1:
                    innerCommand = innerCommand + getChannelName(k) + "1,"
                elif ro == -1:
                    innerCommand = innerCommand + getChannelName(k) + "0,"
                k = k + 1
            delay_accu = delay_accu + 1
        else:
            delay_accu = delay_accu + 1
    
    if (delay_accu != 0):
        try:
            innerCommand = innerCommand + "d" + str(delay_accu*int(entry_square_time.get()))
        except:
            innerCommand = innerCommand + "d" + str(delay_accu*int(1))
            pass
    else:
        innerCommand = innerCommand[:-1]

    return innerCommand

def generateCommandLine(value_array):

    inner_command = generateInnerCommandLine(value_array)

    nbr_repet = "1"
    try: 
        if (entry_nbr_repet is not None):
            nbr_repet = str(int(entry_nbr_repet.get()))
    except:
        pass

    global_command = inner_command + "." + nbr_repet

    if (e4 is not None):
        e4.delete(0, tk.END)
        e4.insert(0, global_command)

    print(global_command)
    return global_command


def getChangeArray(value_array):
    #tmp_array = []
    #for col in description_array:
    #    col.insert(0, 0)
    #    tmp_array.append(col)
    tmp_array_sub = [[0] + row for row in description_array]
    tmp_array_fir = [row + [0] for row in description_array]

    #print(tmp_array)
    #print(description_array)
    return np.subtract(tmp_array_fir, tmp_array_sub)

def getChanelColor(channel):
    if(channel == 0):
        return "blue"
    if(channel == 1):
        return "green"
    if(channel == 2):
        return "red"
    if(channel == 3):
        return "orange"

def getChannelName(channel):
    if(channel == 0):
        return "A"
    if(channel == 1):
        return "B"
    if(channel == 2):
        return "C"
    if(channel == 3):
        return "D" 


def click_canva(event):
    global only_on 
    global lock_column 
    lock_column = event.widget.row
    if (description_array[event.widget.row][event.widget.col] == 1):
        only_on = 0
    else:
        only_on = 1
    event.widget.toggle_onoff()


def enter_canva(event):
    global lock_column 
    if (lock_column == event.widget.row):
        event.widget.toggle_onoff()

def show_info(event):
    global current_widget
    widget = event.widget.winfo_containing(event.x_root, event.y_root)
    if current_widget != widget:
        if current_widget:
            current_widget.event_generate("<<B1-Leave>>")
        current_widget = widget
        current_widget.event_generate("<<B1-Enter>>")

def on_enter(event):
    event.widget.configure(text="Hello, cursor!")

def entry_change_callback(sv):
    k = 0
    try:
        for t in index_label_list:
            t.config(text = str(10*k*int(entry_square_time.get())))
            k = k + 1
    except:
        for t in index_label_list:
            t.config(text = str(10*k*int(1)))
            k = k + 1
        pass
    generateCommandLine(description_array)

import time

def send_command_serial():
    gen_cmd = generateCommandLine(description_array)
    gen_cmd = "<" + gen_cmd + ">"
    seri = get_serial_obj()
    seri.write(gen_cmd.encode()) 
    print("command sent !")
    time.sleep(0.1)

def get_serial_obj():
    global ser
    if (ser is None):
        ser = serial.Serial(SERIAL_PORT, 57600)  # open serial port
    if (not ser.is_open):
        ser = serial.Serial(SERIAL_PORT, 57600)  # open serial port
    return ser

# root window
root = tk.Tk()
root.geometry("1120x500")
root.title('Login')
#mainGrid.resizable(0, 0)

confGrid = tk.Frame(root, bg='yellow', width=400, height=60, padx=3, pady=10)
confGrid.pack(side=tk.TOP)

confGrid1 = tk.Frame(confGrid, bg='yellow', width=400, height=60, padx=3, pady=3)
confGrid1.pack(side=tk.TOP)

lb1 = tk.Label(confGrid1, text="Loop period :", bg='yellow')
lb1.pack(side=tk.LEFT)

entry_loop_period = tk.Entry(confGrid1)
entry_loop_period.pack(side=tk.LEFT)
entry_loop_period.insert(0,"50")

confGrid2 = tk.Frame(confGrid, bg='yellow', width=400, height=60, padx=3, pady=3)
confGrid2.pack(side=tk.TOP)

lb2 = tk.Label(confGrid2, text="Square time :", bg='yellow')
lb2.pack(side=tk.LEFT)

sq_time_sv = tk.StringVar()
sq_time_sv.trace("w", lambda name, index, mode, sv=sq_time_sv: entry_change_callback(sq_time_sv))
entry_square_time = tk.Entry(confGrid2, textvariable=sq_time_sv)
entry_square_time.pack(side=tk.LEFT)
entry_square_time.insert(0,"1")

confGrid3 = tk.Frame(confGrid, bg='yellow', width=400, height=60, padx=3, pady=3)
confGrid3.pack(side=tk.TOP)

lb3 = tk.Label(confGrid3, text="Repetition :", bg='yellow')
lb3.pack(side=tk.LEFT)


def generateMainGrid():
    for widget in mainGrid.winfo_children():
        widget.destroy()
    for x in range(w+1):
        for y in range(h+1):
            if (y == h):
                if (x % 10 == 1):
                    lb = tk.Label(mainGrid, text=str(int(x-1)*int(entry_square_time.get())), bg='grey')
                    lb.grid(column=x, row=y, sticky=tk.W, padx=0, columnspan=5, pady=0)
                    index_label_list.append(lb)
            elif (x == 0):
                lb = tk.Label(mainGrid, text=getChannelName(y), bg='grey')
                lb.grid(column=x, row=y, sticky=tk.W, padx=0, pady=0)
            else:
                x_g = x - 1
                canva = TagCanvas(mainGrid, x_g, y, highlightthickness=1, highlightbackground="black", width=20, height=20)
                if (x_g % 10 == 0):
                    padx = 2
                else:
                    padx = 0
                canva.grid(column=x, row=y, sticky=tk.W, padx=(padx,0), pady=0)
                canva.bind("<Button>", click_canva)
                canva.bind("<B1-Motion>", show_info)
                canva.bind("<<B1-Enter>>", enter_canva)

nbr_repet_sv = tk.StringVar()
nbr_repet_sv.trace("w", lambda name, index, mode, sv=nbr_repet_sv: entry_change_callback(nbr_repet_sv))
entry_nbr_repet = tk.Entry(confGrid3, textvariable=nbr_repet_sv)
entry_nbr_repet.pack(side=tk.LEFT)
entry_nbr_repet.insert(0,"1")

mainGrid = tk.Frame(root, bg='grey', width=400, height=60, padx=3, pady=3)
mainGrid.pack(side=tk.TOP)
# configure the grid
mainGrid.columnconfigure(0, weight=1)
mainGrid.columnconfigure(1, weight=1)

generateMainGrid()

mainGrid = tk.Frame(root, bg='grey', width=400, height=60, padx=3, pady=3)
mainGrid.pack(side=tk.BOTTOM)


serialGrid = tk.Frame(root, bg='orange', width=800, height=60, padx=3, pady=10)
serialGrid.pack(side=tk.BOTTOM)

cmdLineGrid = tk.Frame(serialGrid, bg='orange', width=800, height=60, padx=3, pady=5)
cmdLineGrid.pack(side=tk.TOP)

lb4 = tk.Label(cmdLineGrid, text="Line command :", bg='orange')
lb4.pack(side=tk.LEFT)

e4 = tk.Entry(cmdLineGrid, width=750)
e4.pack(side=tk.LEFT)

execute_button = tk.Button(serialGrid, text="Execute command line", command=send_command_serial)
execute_button.pack(side=tk.BOTTOM)


generateCommandLine(description_array)

mainGrid.mainloop()
