import tkinter as tk
import tkinter.font
import Client
import MainApp
import WindowManager


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
        self.master.title("ishufi1")
        self.pack(fill=tk.BOTH, expand=1)

        quit_button = tk.Button(self, text="Quit", command=self.manager.close_frame)
        quit_button.place(relx=0.4, rely=0.7, relwidth=0.2)

        continue_button = tk.Button(self, text="Continue", command=self.check_user)
        continue_button.place(relx=0.4, rely=0.6, relwidth=0.2)

        username_txt = tk.Label(self, text="Username")
        username_txt.place(relx=0.3, rely=0.03, relwidth=0.4)

        self.username_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'))
        self.username_entry.place(relx=0.3, rely=0.1, relwidth=0.4)

        password_txt = tk.Label(self, text="Password")
        password_txt.place(relx=0.3, rely=0.18, relwidth=0.4)

        self.password_entry = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'))
        self.password_entry.place(relx=0.3, rely=0.25, relwidth=0.4)
        self.password_entry.bind('<Return>', self.get_text)

    def get_text(self, event):
        username = self.username_entry.get()
        password = self.password_entry.get()
        return username, password

    def check_user(self):
        username, password = self.get_text(None)
        print(username, password)

        self.switch_window()

    def switch_window(self):
        self.manager.switch_frame(MainApp.Window)

    def exit_window(self):
        print("quit")
        self.quit()
        self.destroy()


def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
