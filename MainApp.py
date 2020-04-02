import tkinter as tk
import tkinter.font
from tkinter import messagebox

from PIL import Image, ImageTk

import PlaylistManager
from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.master = master
        self.search_box = None
        self.search_box_artist = None
        self.play_button = None

        load = Image.open(r"images\play1.png")
        img = load.resize((75, 75), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)

        self.play_img = render

        load = Image.open(r"images\pause3.png")
        img = load.resize((75, 75), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)

        self.pause_img = render

        self.init_window()

    def init_window(self):
        self.master.title("ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=GREEN)
        frame.pack(fill=tk.BOTH, expand=1)

        sign_in_txt = tk.Label(self, text="Search", font=tk.font.Font(family='tahoma', size='20', weight="bold"),
                               fg=PURPLE, bg=GREEN)
        sign_in_txt.place(relx=0.3, rely=0.06, relwidth=0.4)

        quit_button = tk.Button(self, text="Quit", command=self.call_manager_exit, bg=WHITE)
        quit_button.place(relx=0.425, rely=0.9, relwidth=0.15)

        download_button = tk.Button(self, text="Download", command=self.download_new_song, bg=WHITE)
        download_button.place(relx=0.425, rely=0.8, relwidth=0.15)

        add_q_button = tk.Button(self, text="Add to queue", command=self.add_to_queue, bg=WHITE)
        add_q_button.place(relx=0.2, rely=0.8, relwidth=0.2)

        make_playlist_button = tk.Button(self, text="Manage playlists", command=self.make_playlist, bg=WHITE)
        make_playlist_button.place(relx=0.6, rely=0.8, relwidth=0.2)

        self.play_button = tk.Button(self, image=self.play_img, command=self.pick_song, bg=GREEN)
        self.play_button.image = self.play_img
        self.play_button.place(relx=0.425, rely=0.55, relwidth=0.15)

        forward_button = tk.Button(self, text="forward 10s", command=self.forward, bg=WHITE)
        forward_button.place(relx=0.725, rely=0.55, relwidth=0.15)

        backward_button = tk.Button(self, text="backward 10s", command=self.backward, bg=WHITE)
        backward_button.place(relx=0.125, rely=0.55, relwidth=0.15)

        load = Image.open(r"images\next1.png")
        img = load.resize((50, 50), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)

        next_song_button = tk.Button(self, image=render, command=self.next_song, bg=WHITE)
        next_song_button.image = render
        next_song_button.place(relx=0.6, rely=0.55, relwidth=0.1)

        load = Image.open(r"images\last1.png")
        img = load.resize((50, 50), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)

        last_song_button = tk.Button(self, image=render, command=self.last_song, bg=WHITE)
        last_song_button.image = render
        last_song_button.place(relx=0.3, rely=0.55, relwidth=0.1)

        song_txt = tk.Label(self, text="Song", font=tk.font.Font(family="century gothic", size="11", weight="bold"), bg=GREEN)
        song_txt.place(relx=0.3, rely=0.22, relwidth=0.4)

        self.search_box = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=WHITE)
        self.search_box.place(relx=0.3, rely=0.3, relwidth=0.4)
        self.search_box.bind('<Return>', self.get_text)

        artist_txt = tk.Label(self, text="Artist", font=tk.font.Font(family="century gothic", size="11", weight="bold"),
                              bg=GREEN)
        artist_txt.place(relx=0.3, rely=0.38, relwidth=0.4)

        self.search_box_artist = tk.Entry(self.master, font=tk.font.Font(family='tahoma', size='12'), bg=WHITE)
        self.search_box_artist.place(relx=0.3, rely=0.45, relwidth=0.4)
        self.search_box_artist.bind('<Return>', self.get_text)

    def add_to_queue(self):
        self.manager.client.song_q.put(self.get_text(None))

    def switch_window(self, window):
        self.manager.switch_frame(window)

    def manager_close_frame(self):
        self.manager.close_frame()

    def make_playlist(self):
        self.manager.open_frame(PlaylistManager.Window, BIG)

    def next_song(self):
        self.manager.client.send_message(STOP)

    def last_song(self):
        if len(self.manager.client.song_stack) == 0:
            return
        self.manager.client.song_stack.pop()
        song = self.manager.client.song_stack[-1]
        self.manager.client.song_stack.pop()
        print("last song", song)
        self.play_song(song)

    def forward(self):
        self.manager.client.forward()

    def backward(self):
        self.manager.client.backward()

    def pause(self):
        self.manager.client.pause()

    def un_pause(self):
        self.manager.client.un_pause()

    def get_text(self, event):
        song = self.search_box.get().replace(' ', '_')
        artist = self.search_box_artist.get().replace(' ', '_')
        if song == "":
            tk.messagebox.showinfo("Ishufi", ERROR)
            return ERROR
        to_send = song + '@' + artist
        return to_send

    def download_new_song(self):
        txt = self.get_text(None)
        if txt == ERROR:
            return
        success, msg = self.manager.client.download_song(txt)
        tk.messagebox.showinfo("Ishufi", msg)

    def pick_song(self):
        name = self.get_text(None)
        if name == ERROR:
            return
        self.play_song(name)

    def play_song(self, name):
        self.change_img()
        msg = self.manager.client.play_song_top(name)
        if msg is not None:
            tk.messagebox.showinfo("Ishufi", "song doesnt exist")

    def change_img(self):
        if self.manager.client.song_playing == '':
            self.play_button["image"] = self.pause_img
        elif self.manager.client.paused:
            self.play_button["image"] = self.pause_img
        else:
            self.play_button["image"] = self.play_img


    def call_manager_exit(self):
        self.manager.client.close_com()
        self.manager.close_frame()

    def exit_window(self):
        self.destroy()
        self.quit()
