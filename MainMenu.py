import tkinter as tk
import tkinter.font
import Window
import MainApp


class MainMenu(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("ishufi")
        self.pack(fill=tkinter.BOTH, expand=1)

        quit_button = tkinter.Button(self, text="Continue", command=continue_to_app)
        quit_button.place(x=180, y=250)

    def switch_screens(self):
        self.master.switch_frame(MainApp)


def main():
    pass

if __name__ == '__main__':
    main()
