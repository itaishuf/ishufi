import tkinter as tk
import tkinter.font
import tkinter.messagebox
import Client
import database
import MainMenu
import MainApp


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
        quit_button = tk.Button(self.master, text="Quit", command=self.manager.close_frame)
        quit_button.place(relx=0.4, rely=0.9, relwidth=0.2)

        continue_button = tk.Button(self.master, text="Continue", command=self.add_user)
        continue_button.place(relx=0.4, rely=0.8, relwidth=0.2)

        username_txt = tk.Label(self.master, text="Username")
        username_txt.place(relx=0.3, rely=0.33, relwidth=0.4)

        sign_in_txt = tk.Label(self.master, text="Sign up", font=tk.font.Font(family='tahoma', size='18'))
        sign_in_txt.place(relx=0.3, rely=0.01, relwidth=0.4)

        self.username_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'))
        self.username_entry.place(relx=0.3, rely=0.4, relwidth=0.4)

        password_txt = tk.Label(self.master, text="Password")
        password_txt.place(relx=0.3, rely=0.48, relwidth=0.4)

        self.password_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'))
        self.password_entry.place(relx=0.3, rely=0.55, relwidth=0.4)
        self.password_entry.bind('<Return>', self.get_text)

    def get_text(self, event):
        username = self.username_entry.get()
        password = self.password_entry.get()
        return username, password

    def add_user(self):
        username, password = self.get_text(None)
        can_login, msg = self.client.add_user(username, password)
        print(can_login, msg)
        if can_login:
            tk.messagebox.showinfo("Ishufi", msg)
            self.switch_window(MainApp.Window)
        else:
            tk.messagebox.showinfo("Ishufi", msg)

    def switch_window(self, window):
        self.manager.switch_frame(window)

    def call_manager_exit(self):
        self.client.close_com()
        self.manager.close_frame()

    def exit_window(self):
        print("quit")
        self.destroy()
        self.quit()


def main():
    pass


if __name__ == '__main__':
    main()
