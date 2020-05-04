import tkinter as tk

import Client
import MainMenu
from Consts import *


class WindowManager(object):

    def __init__(self):
        self.active_frame_class = []  # a stack that holds all the window
        # classes that are open
        self.active_frame = []  # a stack that
        # holds all the windows that are open
        self.client = Client.Client()  # the client, links the ui to the server
        self.switch_frame(MainMenu.Window, BIG)  # starts the main menu screen

    def switch_frame(self, frame_class, size):
        """
        closes the current window and opens a new one
        :param frame_class: the class that want to be opened
        :param size: window size
        """
        if self.active_frame_class:
            self.close_frame()
        root = tk.Tk()
        root.geometry(size)
        frame_class(root, self)
        self.active_frame.append(root)
        self.active_frame_class.append(frame_class)
        root.protocol("WM_DELETE_WINDOW", self.on_exit)
        root.mainloop()

    def open_frame(self, frame_class, size):
        """
        opens a new window without closing the current one
        :param frame_class: the class that want to be opened
        :param size: window size
        """
        root = tk.Tk()
        root.geometry(size)
        frame_class(root, self)
        self.active_frame.append(root)
        self.active_frame_class.append(frame_class)
        root.protocol("WM_DELETE_WINDOW", self.on_exit)
        root.mainloop()

    def close_frame(self):
        """
        updates the active frame stack and active frame class stack.
        then closes the top most frame
        """
        if len(self.active_frame) != ZERO and len(self.active_frame_class) != ZERO:
            my_frame = self.active_frame.pop()
            my_frame_class = self.active_frame_class.pop()
            my_frame_class.exit_window(my_frame)

    def on_exit(self):
        """
        calls close frame
        """
        self.close_frame()


def main():
    wm = WindowManager()


if __name__ == '__main__':
    main()
