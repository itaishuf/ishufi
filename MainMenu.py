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
        self.search_box = None
        self.client = Client.Client()

        self.init_window()

    def init_window(self):
        self.master.title("ishufi1")
        self.pack(fill=tk.BOTH, expand=1)

        quit_button = tk.Button(self, text="Quit", command=self.manager.close_frame)
        quit_button.place(x=180, y=250)

        continue_button = tk.Button(self, text="Continue", command=self.switch_window)
        continue_button.place(x=180, y=200)

    def get_text(self, event):
        print("getting text")
        print(self.search_box.get())

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
