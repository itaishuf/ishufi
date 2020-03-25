import tkinter as tk
import tkinter.filedialog
import tkinter.font
import Client
import MainApp
import os
import tkinter.messagebox
from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.master = master
        self.client = Client.Client()

        self.init_window()

    def init_window(self):
        self.master.title("Ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=GREEN)
        frame.pack(fill=tk.BOTH, expand=1)

        play_button = tk.Button(self, text='test', command=self.choose_song, bg=GREEN)
        play_button.place(relx=0.45, rely=0.55, relwidth=0.1)

    def choose_song(self):
        chosen_file = self.master.filename = tk.filedialog.askopenfilename(initialdir=str(os.getcwd()), title="Select file")
        print(chosen_file)

    def call_manager_exit(self):
        self.manager.close_frame()

    def switch_window(self, window):
        self.manager.switch_frame(window)

    def exit_window(self):
        self.quit()
        self.destroy()


def main():
    pass


if __name__ == '__main__':
    main()
