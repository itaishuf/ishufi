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
        self.chosen_pl = ""
        self.playlist_name = None
        self.all_songs = client.get_all_songs()
        self.all_playlists = client.get_all_pls_of_user()
        self.songs_listbox = None
        self.my_lists = None
        self.song_label = None
        self.pl_label = None
        self.playlists_box = None
        self.init_window()

    def init_window(self):
        self.master.title("Ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=GREEN)
        frame.pack(fill=tk.BOTH, expand=1)

        create_pl_txt = tk.Label(self, text="enter playlist name", font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=GREEN)
        create_pl_txt.place(relx=0.65, rely=0.65, relwidth=0.3)

        self.song_label = tk.Label(self, text="All songs", font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=GREEN)
        self.song_label.place(relx=0.65, rely=0.05, relwidth=0.3)

        self.pl_label = tk.Label(self, text="My playlists", font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=GREEN)
        self.pl_label.place(relx=0.05, rely=0.05, relwidth=0.3)

        self.playlist_name = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=WHITE)
        self.playlist_name.place(relx=0.65, rely=0.7, relwidth=0.3)
        self.playlist_name.bind('<Return>', self.get_text)

        create_button = tk.Button(self, text='create playlist', command=self.create_pl, bg=WHITE)  # TODO : add image
        create_button.place(relx=0.7, rely=0.76, relwidth=0.2)

        choose_pl_button = tk.Button(self, text='choose playlist', command=self.choose_pl, bg=WHITE)  # TODO : add image
        choose_pl_button.place(relx=0.05, rely=0.5, relwidth=0.3)

        remove_button = tk.Button(self, text='remove song from playlist', command=self.remove_song_from_pl, bg=WHITE)  # TODO : add image
        remove_button.place(relx=0.05, rely=0.6, relwidth=0.3)

        view_all_button = tk.Button(self, text='view all songs', command=self.fill_pl_songs, bg=WHITE)  # TODO:add image
        view_all_button.place(relx=0.7, rely=0.5, relwidth=0.2)

        self.songs_listbox = tk.Listbox(master=self, selectmode=tk.SINGLE)
        self.songs_listbox.place(relx=0.65, rely=0.1, relwidth=0.3)
        self.fill_all_songs()

        self.playlists_box = tk.Listbox(master=self, selectmode=tk.MULTIPLE)
        self.playlists_box.place(relx=0.05, rely=0.1, relwidth=0.3)
        for i in range(len(self.all_playlists)):
            self.playlists_box.insert(i, self.all_playlists[i])

    def get_text(self, event):
        name = self.playlist_name.get().replace(' ', '_')
        if name == "":
            return ERROR
        return name

    def fill_pls(self):
        self.clear_listbox(self.playlists_box)
        self.all_playlists = self.client.get_all_pls_of_user()
        for i in range(len(self.all_playlists)):
            self.playlists_box.insert(i, self.all_playlists[i])

    def fill_all_songs(self):
        self.clear_listbox(self.songs_listbox)
        for i in range(len(self.all_songs)):
            self.songs_listbox.insert(i, self.all_songs[i])

    def fill_pl_songs(self, playlist):
        self.clear_listbox(self.songs_listbox)
        songs = self.client.get_songs_in_pl(playlist)
        for i in range(len(songs)):
            self.songs_listbox.insert(i, songs[i])

    def choose_songs(self):
        self.songs = []
        indexes = self.songs_listbox.curselection()
        print(indexes)
        for index in indexes:
            self.songs.append(self.songs_listbox.get(index))

    def choose_pl(self):
        index = self.playlists_box.curselection()
        self.chosen_pl = self.playlists_box.get(index)
        self.choose_pl()
        self.song_label["text"] = "All songs in %s" % self.chosen_pl
        self.fill_pl_songs(self.chosen_pl)
        self.master.lift()

    def create_pl(self):
        name = self.get_text(None)
        if name == ERROR:
            return
        self.choose_songs()
        print(self.songs)
        msg = self.client.create_playlist(self.songs, name)
        msg = " ".join(msg)
        tk.messagebox.showinfo("Ishufi", msg)
        self.fill_pls()
        self.master.lift()

    def remove_song_from_pl(self):
        self.choose_songs()

    def call_manager_exit(self):
        self.manager.close_frame()

    def switch_window(self, window):
        self.manager.switch_frame(window)

    def exit_window(self):
        self.quit()
        self.destroy()

    def clear_listbox(self, listbox):
        listbox.delete(0, listbox.size())


def main():
    pass


if __name__ == '__main__':
    main()
