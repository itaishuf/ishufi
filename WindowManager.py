import tkinter as tk
import Client
import MainApp
import MainMenu


class WindowManager(object):

    def __init__(self):
        self.active_frame_class = None
        self.active_frame = None
        self.switch_frame(MainMenu.Window)

    def switch_frame(self, frame_class):
        if self.active_frame_class is not None:
            self.close_frame()
        root = tk.Tk()
        root.geometry("400x300")
        app = frame_class(root, self)
        self.active_frame = root
        self.active_frame_class = frame_class
        root.mainloop()

    def close_frame(self, to_switch):
        print(self.active_frame_class)
        self.active_frame_class.exit_window(self.active_frame, to_switch)


def main():
    wm = WindowManager()


if __name__ == '__main__':
    main()
