import tkinter as tk
import Client
import MainMenu
from Consts import *


class WindowManager(object):

    def __init__(self):
        self.active_frame_class = []
        self.active_frame = []
        self.client = Client.Client()

    def switch_frame(self, frame_class, size):
        if self.active_frame_class:
            self.close_frame()
        root = tk.Tk()
        root.geometry(size)
        frame_class(root, self, self.client)
        self.active_frame.append(root)
        self.active_frame_class.append(frame_class)
        root.protocol("WM_DELETE_WINDOW", self.on_exit)
        root.mainloop()

    def open_frame(self, frame_class, size):
        root = tk.Tk()
        root.geometry(size)
        frame_class(root, self, self.client)
        self.active_frame.append(root)
        self.active_frame_class.append(frame_class)
        root.protocol("WM_DELETE_WINDOW", self.on_exit)
        root.mainloop()

    def close_frame(self):
        if len(self.active_frame) != 0 and len(self.active_frame_class) != 0:
            my_frame = self.active_frame.pop()
            my_frame_class = self.active_frame_class.pop()
            my_frame_class.exit_window(my_frame)
        if len(self.active_frame) == 0 and len(self.active_frame_class) == 0:
            print("no active windows")

    def on_exit(self):
        self.close_frame()


def main():
    wm = WindowManager()
    wm.switch_frame(MainMenu.Window, BIG)


if __name__ == '__main__':
    main()
