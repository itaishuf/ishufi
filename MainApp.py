import tkinter as tk
import tkinter.font
from tkinter import messagebox

from PIL import Image, ImageTk

import PlaylistManager
from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager  # reference to the manager
        self.master = master  # tkinter root
        self.search_box = None  # song search box declaration
        self.search_box_artist = None  # artist search box declaration
        self.play_button = None  # play button declaration

        # sets the play button image up
        load = Image.open(r"images\play1.png")
        img = load.resize((75, 75), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        self.play_img = render

        # sets the pause button image up
        load = Image.open(r"images\pause3.png")
        img = load.resize((75, 75), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        self.pause_img = render

        self.init_window()

    def init_window(self):
        """
        initializes the window with all widgets and buttons
        """
        self.master.title("ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=LIGHT_BLUE)
        frame.pack(fill=tk.BOTH, expand=1)

        search_txt = tk.Label(self, text="Search",
                              font=tk.font.Font(family='tahoma', size='20',
                                                weight="bold"),
                              fg=PURPLE, bg=LIGHT_BLUE)
        search_txt.place(relx=0.3, rely=0.06, relwidth=0.4)

        quit_button = tk.Button(self, text="Quit",
                                command=self.call_manager_exit,
                                bg=LIGHT_LIGHT_BLUE)
        quit_button.place(relx=0.425, rely=0.9, relwidth=0.15)

        download_button = tk.Button(self, text="Download",
                                    command=self.download_new_song,
                                    bg=LIGHT_LIGHT_BLUE)
        download_button.place(relx=0.425, rely=0.8, relwidth=0.15)

        add_q_button = tk.Button(self, text="Add to queue",
                                 command=self.add_to_queue,
                                 bg=LIGHT_LIGHT_BLUE)
        add_q_button.place(relx=0.2, rely=0.8, relwidth=0.2)

        make_playlist_button = tk.Button(self, text="Manage playlists",
                                         command=self.make_playlist,
                                         bg=LIGHT_LIGHT_BLUE)
        make_playlist_button.place(relx=0.6, rely=0.8, relwidth=0.2)

        self.play_button = tk.Button(self, image=self.play_img,
                                     command=self.pick_song,
                                     bg=LIGHT_LIGHT_BLUE,
                                     fg=LIGHT_LIGHT_BLUE)
        self.play_button.image = self.play_img
        self.play_button.place(relx=0.425, rely=0.55, relwidth=0.15)

        forward_button = tk.Button(self, text="forward 10s",
                                   command=self.forward, bg=LIGHT_LIGHT_BLUE)
        forward_button.place(relx=0.725, rely=0.55, relwidth=0.15)

        backward_button = tk.Button(self, text="backward 10s",
                                    command=self.backward, bg=LIGHT_LIGHT_BLUE)
        backward_button.place(relx=0.125, rely=0.55, relwidth=0.15)

        load = Image.open(r"images\next1.png")
        img = load.resize((50, 50), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)

        next_song_button = tk.Button(self, image=render,
                                     command=self.next_song,
                                     bg=LIGHT_LIGHT_BLUE,
                                     fg=LIGHT_LIGHT_BLUE)
        next_song_button.image = render
        next_song_button.place(relx=0.6, rely=0.55, relwidth=0.1)

        load = Image.open(r"images\last1.png")
        img = load.resize((50, 50), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)

        last_song_button = tk.Button(self, image=render,
                                     command=self.last_song,
                                     bg=LIGHT_LIGHT_BLUE,
                                     fg=LIGHT_LIGHT_BLUE)
        last_song_button.image = render
        last_song_button.place(relx=0.3, rely=0.55, relwidth=0.1)

        song_txt = tk.Label(self, text="Song",
                            font=tk.font.Font(family="century gothic",
                                              size="11", weight="bold"),
                            bg=LIGHT_BLUE)
        song_txt.place(relx=0.3, rely=0.22, relwidth=0.4)

        self.search_box = tk.Entry(self.master,
                                   font=tk.font.Font(family='tahoma',
                                                     size='12'), bg=WHITE)
        self.search_box.place(relx=0.3, rely=0.3, relwidth=0.4)
        self.search_box.bind('<Return>', self.get_text)

        artist_txt = tk.Label(self, text="Artist",
                              font=tk.font.Font(family="century gothic",
                                                size="11", weight="bold"),
                              bg=LIGHT_BLUE)
        artist_txt.place(relx=0.3, rely=0.38, relwidth=0.4)

        self.search_box_artist = tk.Entry(self.master,
                                          font=tk.font.Font(family='tahoma',
                                                            size='12'),
                                          bg=WHITE)
        self.search_box_artist.place(relx=0.3, rely=0.45, relwidth=0.4)
        self.search_box_artist.bind('<Return>', self.get_text)

        self.play_button.bind(RIGHT_CLICK, self.help)
        quit_button.bind(RIGHT_CLICK, self.help)
        download_button.bind(RIGHT_CLICK, self.help)
        add_q_button.bind(RIGHT_CLICK, self.help)
        make_playlist_button.bind(RIGHT_CLICK, self.help)
        forward_button.bind(RIGHT_CLICK, self.help)
        backward_button.bind(RIGHT_CLICK, self.help)
        next_song_button.bind(RIGHT_CLICK, self.help)
        last_song_button.bind(RIGHT_CLICK, self.help)

    def help(self, event):
        """
        opens a window with explanations about how to operate the ui
        """
        widget_name = event.widget[TEXT]
        widget_img = event.widget[IMAGE]
        if widget_img == '':
            value = widget_name
        else:
            value = widget_img
        tk.messagebox.showinfo(TITLE, HELP_STRINGS[value])

    def add_to_queue(self):
        """
        adds the current song to the queue
        """
        self.manager.client.song_q.put(self.get_text(None))

    def switch_window(self, window):
        """
        switches window
        """
        self.manager.switch_frame(window)

    def manager_close_frame(self):
        """
        closes this window
        """
        self.manager.close_frame()

    def make_playlist(self):
        """
        opens the playlist manager screen
        """
        self.manager.open_frame(PlaylistManager.Window, BIG)

    def next_song(self):
        """
        pushes a message to move to the next song in the queue
        """
        self.manager.client.send_message(STOP)

    def last_song(self):
        """
        starts playing the last song that was played
        """
        if len(self.manager.client.song_stack) <= ONE:
            return
        self.manager.client.song_stack.pop()
        song = self.manager.client.song_stack.pop()
        self.manager.client.play_next_song = False
        self.play_song(song)

    def forward(self):
        """
        goes forward 10 seconds in the song
        """
        self.manager.client.forward()

    def backward(self):
        """
        goes forward 10 seconds in the song
        """
        self.manager.client.backward()

    def pause(self):
        """
        pauses the current song
        """
        self.manager.client.pause()

    def un_pause(self):
        """
        resumes the current song
        """
        self.manager.client.un_pause()

    def get_text(self, event):
        """
        gets the text from both entry boxes, puts underscores instead
        of spaces and separates with @
        """
        song = self.search_box.get().replace(SPACE, UNDERSCORE)
        artist = self.search_box_artist.get().replace(SPACE, UNDERSCORE)
        if song == "":
            if self.manager.client.song_playing != "":
                return self.manager.client.song_playing
            return ERROR
        to_send = song + ET + artist
        return to_send

    def download_new_song(self):
        """
        downloads the string that the user has typed
        """
        txt = self.get_text(None)
        if txt == ERROR:
            return
        success, msg = self.manager.client.download_song(txt)
        tk.messagebox.showinfo(TITLE, msg)

    def pick_song(self):
        """
        song player highest level wrapper
        """
        name = self.get_text(None)
        if name == ERROR:
            self.change_img(mode=PLAY)
            return
        self.play_song(name)

    def play_song(self, name):
        """
        calls the client function to start the song playing process
        """
        # if self.manager.client.song_playing == "":
        self.change_img()
        self.manager.client.play_next_song = False
        msg = self.manager.client.play_song_top(name)
        if msg is not None:
            tk.messagebox.showinfo(TITLE, DOESNT_EXIST)
            self.change_img(mode=PLAY)

    def change_img(self, mode=""):
        """
        checks whether the play button should show a pause image
        or a play image and updates the image
        """
        if mode == PAUSE:
            self.play_button[IMAGE] = self.pause_img
            return
        if mode == PLAY:
            self.play_button[IMAGE] = self.play_img
            return
        if self.manager.client.song_playing == '':
            self.play_button[IMAGE] = self.pause_img
            return
        elif self.manager.client.paused:
            self.play_button[IMAGE] = self.pause_img
            return
        self.play_button[IMAGE] = self.play_img

    def call_manager_exit(self):
        """
        calls the manager exit function
        """
        self.manager.client.close_com()
        self.manager.close_frame()

    def exit_window(self):
        """
        exits the window
        """
        self.destroy()
        self.quit()
