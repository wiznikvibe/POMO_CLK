import time
import threading 
from tkinter import *
from tkinter import ttk



class PomodoroTimer:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x300")
        self.root.title("Study Timer NS")
        self.root.call('wm', 'iconphoto', self.root._w, PhotoImage(file='gomu.png'))

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font =("Ubuntu",16))
        self.s.configure("TButton", font=("Ubuntu",16))


        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', pady=20, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=200, height=150)
        self.tab2 = ttk.Frame(self.tabs, width=200, height=150)
        self.tab3 = ttk.Frame(self.tabs, width=200, height=150)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=("Ubuntu",40))
        self.pomodoro_timer_label.pack(pady=10)
        
        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=("Ubuntu",40))
        self.short_break_timer_label.pack(pady=10)
        
        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=("Ubuntu",40))
        self.long_break_timer_label.pack(pady=10)
        
        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0,column=0)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0,column=1)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0,column=2)


        self.pomodoro_count_label = ttk.Label(self.grid_layout, text= "Pomodoro: 0", font=("Ubuntu",16))
        self.pomodoro_count_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.pomodoros = 0 
        self.skipped = False
        self.stopped = False   
        self.running = False

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    def start_timer(self):
        
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
        self.running = True

        if timer_id == 1:
            fullseconds = 60*25
            while fullseconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullseconds, 60)
                self.pomodoro_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullseconds -= 1 
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_count_label.config(text=f"Pomodoros:{self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()
        elif timer_id == 2:
            fullseconds = 60 * 5  
            while fullseconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullseconds, 60)
                self.short_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullseconds -= 1 
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        elif timer_id == 3:
            fullseconds = 60 * 15  
            while fullseconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullseconds, 60)
                self.long_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullseconds -= 1 
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()

        else:
            print("Invalid Timer Id")

    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.pomodoro_count_label.config(text="Pomodoros: 0")
        self.running = False


    def skip_clock(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0:
            self.pomodoro_timer_label.config(text="25:00")
        elif current_tab == 1:
            self.short_break_timer_label.config(text="05:00")
        elif current_tab == 2:
            self.long_break_timer_label.config(text="15:00")

        self.stopped = True
        self.skipped = True

PomodoroTimer()