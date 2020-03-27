import tkinter as tk
import tkinter.filedialog
import tkinter.font
import Client
import MainApp
import os
import tkinter.messagebox
from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager, client):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.master = master
        self.client = client
        self.songs = []
        self.playlist_name = None
        self.all_songs = client.get_all_songs()
        self.all_playlists = client.get_all_playlists_of_user()
        self.songs_listbox = None
        self.my_lists = None
        self.init_window()

    def init_window(self):
        self.master.title("Ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=GREEN)
        frame.pack(fill=tk.BOTH, expand=1)

        song_txt = tk.Label(self, text="enter playlist name", font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=GREEN)
        song_txt.place(relx=0.65, rely=0.5, relwidth=0.3)

        self.playlist_name = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=WHITE)
        self.playlist_name.place(relx=0.65, rely=0.55, relwidth=0.3)
        self.playlist_name.bind('<Return>', self.get_text)

        create_button = tk.Button(self, text='create playlist', command=self.create_playlist, bg=WHITE) # TODO : add image
        create_button.place(relx=0.4, rely=0.15, relwidth=0.2)

        self.songs_listbox = tk.Listbox(master=self, selectmode=tk.MULTIPLE)
        self.songs_listbox.place(relx=0.65, rely=0.1, relwidth=0.3)
        for i in range(len(self.all_songs)):
            self.songs_listbox.insert(i, self.all_songs[i])

        self.my_lists = tk.Listbox(master=self, selectmode=tk.MULTIPLE)
        self.my_lists.place(relx=0.05, rely=0.1, relwidth=0.3)
        for i in range(len(self.all_songs)):
            self.songs_listbox.insert(i, self.all_songs[i])

    def get_text(self, event):
        name = self.playlist_name.get().replace(' ', '_')
        if name == "":
            return ERROR
        return name

    def choose_songs(self):
        self.songs = []
        indexes = self.songs_listbox.curselection()
        print(indexes)
        for index in indexes:
            self.songs.append(self.songs_listbox.get(index))

    def create_playlist(self):
        name = self.get_text(None)
        if name == ERROR:
            return
        self.choose_songs()
        msg = self.client.create_playlist(self.songs, name)
        msg = " ".join(msg)
        tk.messagebox.showinfo("Ishufi", msg)

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
