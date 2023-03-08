import tkinter as tk
from tkinter import ttk


w = 50
h = 4



current_widget = None
description_array = [[0 for x in range(w)] for y in range(h)]
lock_column = -1
only_on = 1

class TagCanvas(tk.Canvas):
    def __init__(self, master, col, row, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.master = master
        self.col = col
        self.row = row
        self.configure(bg='white')


    def toggle_onoff(self):
        global only_on 
        if (description_array[self.row][self.col] == 1):
            if (only_on == 0):
                description_array[self.row][self.col] = 0
                self.configure(bg='white')
        else:
            if (only_on == 1):
                description_array[self.row][self.col] = 1
                self.configure(bg=getChanelColor(self.row))
        

def getChanelColor(channel):
    if(channel == 0):
        return "blue"
    if(channel == 1):
        return "green"
    if(channel == 2):
        return "red"
    if(channel == 3):
        return "orange"
    


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


# root window
mainGrid = tk.Tk()
mainGrid.geometry("1120x500")
mainGrid.title('Login')
mainGrid.resizable(0, 0)



#mainGrid = tk.Frame(root, bg='gray2', width=400, height=60, padx=3, pady=3)
# configure the grid
mainGrid.columnconfigure(0, weight=1)
mainGrid.columnconfigure(1, weight=1)

# username
for x in range(w):
    for y in range(h+1):
        if (y == h):
            if (x % 10 == 0):
                lb = tk.Label(mainGrid, text=str(x))
                lb.grid(column=x, row=y, sticky=tk.W, padx=0, pady=0)

        else:
            canva = TagCanvas(mainGrid, x, y, highlightthickness=1, highlightbackground="black", width=20, height=20)
            if (x % 10 == 0):
                padx = 5
                print((x,y))
            else:
                padx = 0
            canva.grid(column=x, row=y, sticky=tk.W, padx=(padx,0), pady=0)
            canva.bind("<Button>", click_canva)
            canva.bind("<B1-Motion>", show_info)
            canva.bind("<<B1-Enter>>", enter_canva)


mainGrid.mainloop()