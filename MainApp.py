import tkinter as tk
import tkinter.font
import Client


class Window(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.search_box = None
        self.client = Client.Client()

        self.init_window()

    def init_window(self):
        self.master.title("ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        quit_button = tk.Button(self, text="Quit", command=exit_window)
        quit_button.place(x=180, y=250)

        play_button = tk.Button(self, text="Play", command=self.handle_client)
        play_button.place(x=180, y=200)

        self.search_box = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'))
        self.search_box.place(x=100, y=100)
        self.search_box.bind('<Return>', self.get_text)

    def get_text(self, event):
        print("getting text")
        print(self.search_box.get())

    def handle_client(self):
        self.client.handle_client("play")


def exit_window():
    print("quit")
    exit()


def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()