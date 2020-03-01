import tkinter as tk
import tkinter.font
from tkinter import messagebox
import Client
import threading
import queue
import time
from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.master = master
        self.search_box = None
        self.client = Client.Client()

        self.init_window()

    def init_window(self):
        self.master.title("ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=BLUE)
        frame.pack(fill=tk.BOTH, expand=1)

        quit_button = tk.Button(self, text="Quit", command=self.call_manager_exit, bg=LIGHT_BLUE)
        quit_button.place(relx=0.4, rely=0.75, relwidth=0.2)

        download_button = tk.Button(self, text="Download", command=self.download_new_song, bg=LIGHT_BLUE)
        download_button.place(relx=0.4, rely=0.65, relwidth=0.2)

        play_button = tk.Button(self, text="Play", command=self.pick_song, bg=LIGHT_BLUE)
        play_button.place(relx=0.4, rely=0.55, relwidth=0.2)

        pause_button = tk.Button(self, text="Pause", command=self.pause, bg=LIGHT_BLUE)
        pause_button.place(relx=0.7, rely=0.55, relwidth=0.15)

        un_pause_button = tk.Button(self, text="continue", command=self.un_pause, bg=LIGHT_BLUE)
        un_pause_button.place(relx=0.7, rely=0.65, relwidth=0.15)

        forward_button = tk.Button(self, text="forward", command=self.forward, bg=LIGHT_BLUE)
        forward_button.place(relx=0.78, rely=0.75, relwidth=0.15)

        backward_button = tk.Button(self, text="backward", command=self.backward, bg=LIGHT_BLUE)
        backward_button.place(relx=0.62, rely=0.75, relwidth=0.15)

        search_txt = tk.Label(self, text="Search", font=tk.font.Font(family="tahoma", size="18", weight="bold"), bg=BLUE, fg=PURPLE)
        search_txt.place(relx=0.3, rely=0.15, relwidth=0.4)

        self.search_box = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=LIGHT_BLUE)
        self.search_box.place(relx=0.3, rely=0.25, relwidth=0.4)
        self.search_box.bind('<Return>', self.get_text)

    def forward(self):
        self.client.forward()

    def backward(self):
        pass

    def pause(self):
        self.client.pause()

    def un_pause(self):
        self.client.un_pause()

    def get_text(self, event):
        return self.search_box.get().replace(' ', '_')

    def download_new_song(self):
        success, msg = self.client.download_song(self.get_text(None))
        print(success, msg)
        tk.messagebox.showinfo("Ishufi", msg)

    def pick_song(self):
        name = self.get_text(None)
        self.play_song(name)

    def play_song(self, name):
        return_queue = queue.Queue()
        t_play = threading.Thread(target=self.client.play_song, args=((name, return_queue),))
        t_play.start()
        time.sleep(0.1)
        if return_queue.empty():
            return
        if return_queue.get() == INVALID_REQ:
            tk.messagebox.showinfo("Ishufi", "song doesnt exist")

    def call_manager_exit(self):
        self.client.close_com()
        self.manager.close_frame()

    def exit_window(self):
        self.destroy()
        self.quit()


def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
