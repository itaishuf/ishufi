import tkinter as tk
import tkinter.font
from tkinter import messagebox
import Client
import threading
import queue
import time
INVALID_REQ = "invalid"
DONE = "done"
BLUE = "#ccffea"
LIGHT_BLUE = "#ffffff"
PURPLE = "#8A23F1"
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
        frame.pack(fill=tk.BOTH, expand =1)

        quit_button = tk.Button(self, text="Quit", command=self.call_manager_exit, bg=BLUE)
        quit_button.place(x=180, y=250)

        play_button = tk.Button(self, text="Play", command=self.pick_song, bg=BLUE)
        play_button.place(x=180, y=200)

        search_txt = tk.Label(self, text="Search", font=tk.font.Font(family="tahoma", size="18", weight="bold"), bg=BLUE, fg=PURPLE)
        search_txt.place(relx=0.3, rely=0.21, relwidth=0.4)

        self.search_box = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=LIGHT_BLUE)
        self.search_box.place(x=100, y=100)
        self.search_box.bind('<Return>', self.get_text)

    def get_text(self, event):
        return self.search_box.get()

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
        print("quit")
        self.destroy()
        self.quit()


def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
