import tkinter as tk
import tkinter.font
import tkinter.messagebox

from PIL import Image, ImageTk

import MainApp
from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.master = master
        self.username_entry = None
        self.password_entry = None

        self.init_window()

    def init_window(self):
        self.master.title("Ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=LIGHT_BLUE)
        frame.pack(fill=tk.BOTH, expand=1)
        self.master.resizable(0, 0)
        load = Image.open(r"images\logo.png")
        img = load.resize((400, 450), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)

        background = tk.Label(self, image=render, bg=LIGHT_BLUE)
        background.image = render
        background.place(x=200, rely=0)

        quit_button = tk.Button(self, text="Quit", command=self.call_manager_exit,
                                font=tk.font.Font(family="gisha", size="10"), bg=WHITE)
        quit_button.place(relx=0.1, rely=0.75, relwidth=0.13)

        log_in_button = tk.Button(self, text="Log In", command=self.check_user,
                                  font=tk.font.Font(family="gisha", size="10"), bg=WHITE)
        log_in_button.place(relx=0.1, rely=0.65, relwidth=0.13)

        add_user_button = tk.Button(self, text="Register", command=self.add_user,
                                    font=tk.font.Font(family="gisha", size="10"), bg=WHITE)
        add_user_button.place(relx=0.1, rely=0.55, relwidth=0.13)

        username_txt = tk.Label(self, text="Username",
                                font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=LIGHT_BLUE)
        username_txt.place(relx=0.08, rely=0.18, relwidth=0.2)

        sign_in_txt = tk.Label(self, text="Sign in", font=tk.font.Font(family='tahoma', size='20', weight="bold"),
                               fg=PURPLE, bg=LIGHT_BLUE)
        sign_in_txt.place(relx=0.08, rely=0.05, relwidth=0.2)

        self.username_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=WHITE)
        self.username_entry.place(relx=0.05, rely=0.25, relwidth=0.26)

        password_txt = tk.Label(self, text="Password",
                                font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=LIGHT_BLUE)
        password_txt.place(relx=0.08, rely=0.33, relwidth=0.2)

        self.password_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), show='$', bg=WHITE)
        self.password_entry.place(relx=0.05, rely=0.4, relwidth=0.26)
        self.password_entry.bind('<Return>', self.get_text)

    def get_text(self, event):
        username = self.username_entry.get()
        password = self.password_entry.get()
        return username, password

    def add_user(self):
        username, password = self.get_text(None)
        can_login, msg = self.manager.client.add_user(username, password)
        if can_login:
            tk.messagebox.showinfo("Ishufi", msg)
            self.switch_window(MainApp.Window)
        else:
            tk.messagebox.showinfo("Ishufi", msg)

    def call_manager_exit(self):
        self.manager.close_frame()

    def check_user(self):
        username, password = self.get_text(None)
        username = "itai"
        password = "123"
        can_login, msg = self.manager.client.login(username, password)
        if can_login:
            self.manager.client.current_user = username
            self.switch_window(MainApp.Window)
        else:
            tk.messagebox.showinfo("Ishufi", msg)

    def switch_window(self, window):
        self.manager.switch_frame(window, BIG)

    def exit_window(self):
        self.quit()
        self.destroy()
