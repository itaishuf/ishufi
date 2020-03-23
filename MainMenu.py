import tkinter as tk
import tkinter.font
import Client
import MainApp
import tkinter.messagebox
from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.master = master
        self.username_entry = None
        self.password_entry = None
        self.client = Client.Client()

        self.init_window()

    def init_window(self):
        self.master.title("Ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=GREEN)
        frame.pack(fill=tk.BOTH, expand =1)

        quit_button = tk.Button(self, text="Quit", command=self.manager_close_frame, font=tk.font.Font(family="gisha", size="10"), bg=WHITE)
        quit_button.place(relx=0.4, rely=0.75, relwidth=0.2)

        continue_button = tk.Button(self, text="Log In", command=self.check_user, font=tk.font.Font(family="gisha", size="10"), bg=WHITE)
        continue_button.place(relx=0.4, rely=0.65, relwidth=0.2)

        add_user_button = tk.Button(self, text="Register", command=self.add_user, font=tk.font.Font(family="gisha", size="10"), bg=WHITE)
        add_user_button.place(relx=0.4, rely=0.55, relwidth=0.2)

        username_txt = tk.Label(self, text="Username", font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=GREEN)
        username_txt.place(relx=0.3, rely=0.18, relwidth=0.4)

        sign_in_txt = tk.Label(self, text="Sign in", font=tk.font.Font(family='tahoma', size='20', weight="bold"), fg=PURPLE, bg=GREEN)
        sign_in_txt.place(relx=0.3, rely=0.01, relwidth=0.4)

        self.username_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=WHITE)
        self.username_entry.place(relx=0.3, rely=0.25, relwidth=0.4)

        password_txt = tk.Label(self, text="Password", font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=GREEN)
        password_txt.place(relx=0.3, rely=0.33, relwidth=0.4)

        self.password_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), show='$', bg=WHITE)
        self.password_entry.place(relx=0.3, rely=0.4, relwidth=0.4)
        self.password_entry.bind('<Return>', self.get_text)

    def get_text(self, event):
        username = self.username_entry.get()
        password = self.password_entry.get()
        return username, password

    def add_user(self):
        username, password = self.get_text(None)
        can_login, msg = self.client.add_user(username, password)
        if can_login:
            tk.messagebox.showinfo("Ishufi", msg)
            self.switch_window(MainApp.Window)
        else:
            tk.messagebox.showinfo("Ishufi", msg)

    def manager_close_frame(self):
        self.manager.close_frame()

    def check_user(self):
        username, password = self.get_text(None)
        can_login, msg = self.client.login(username, password)
        if can_login:
            self.switch_window(MainApp.Window)
        else:
            tk.messagebox.showinfo("Ishufi", msg)

    def switch_window(self, window):
        self.manager.switch_frame(window)

    def exit_window(self):
        self.quit()
        self.destroy()


def main():
    pass


if __name__ == '__main__':
    main()
