import random
import tkinter as tk
import tkinter.font
import tkinter.messagebox

from Consts import *


class Window(tk.Frame):

    def __init__(self, master, manager):
        tk.Frame.__init__(self, master)
        self.manager = manager
        self.master = master
        self.selected_songs = []
        self.chosen_pl = ""
        self.playlist_name = None
        self.all_playlists = None
        self.songs_listbox = None
        self.my_lists = None
        self.song_label = None
        self.pl_label = None
        self.playlists_box = None

        self.init_window()

    def init_window(self):
        """
        initializes the window with all widgets and buttons
        """
        self.master.title("Ishufi")
        self.pack(fill=tk.BOTH, expand=1)

        frame = tk.Frame(master=self, bg=LIGHT_BLUE)
        frame.pack(fill=tk.BOTH, expand=1)

        create_pl_txt = tk.Label(self, text="enter playlist name",
                                 font=tk.font.Font(family="century gothic",
                                                   size="11", weight="bold"),
                                 bg=LIGHT_BLUE)
        create_pl_txt.place(relx=0.65, rely=0.65, relwidth=0.3)

        self.song_label = tk.Label(self, text="All Downloaded Songs",
                                   font=tk.font.Font(family="century gothic",
                                                     size="11", weight="bold"),
                                   bg=LIGHT_BLUE)
        self.song_label.place(relx=0.65, rely=0.05, relwidth=0.3)

        self.pl_label = tk.Label(self, text="My playlists",
                                 font=tk.font.Font(family="century gothic",
                                                   size="11", weight="bold"),
                                 bg=LIGHT_BLUE)
        self.pl_label.place(relx=0.05, rely=0.05, relwidth=0.3)

        self.playlist_name = tk.Entry(self.master,
                                      font=tk.font.Font(family='tahoma',
                                                        size='12'), bg=WHITE)
        self.playlist_name.place(relx=0.65, rely=0.7, relwidth=0.3)
        self.playlist_name.bind('<Return>', self.get_text)

        create_button = tk.Button(self, text='create playlist',
                                  command=self.create_pl, bg=WHITE)
        create_button.place(relx=0.7, rely=0.76, relwidth=0.2)

        remove_button = tk.Button(self, text='remove song from playlist',
                                  command=self.remove_song_from_pl, bg=WHITE)
        remove_button.place(relx=0.05, rely=0.5, relwidth=0.3)

        add_button = tk.Button(self, text='add song to playlist',
                               command=self.add_song_to_pl, bg=WHITE)
        add_button.place(relx=0.05, rely=0.6, relwidth=0.3)

        play_button = tk.Button(self, text='play playlist',
                                command=self.play_pl, bg=WHITE)
        play_button.place(relx=0.05, rely=0.7, relwidth=0.3)

        view_all_button = tk.Button(self, text='view all downloaded songs',
                                    command=self.fill_pl_songs, bg=WHITE)
        view_all_button.place(relx=0.65, rely=0.5, relwidth=0.3)

        delete_button = tk.Button(self, text='delete playlist',
                                  command=self.delete_pl, bg=WHITE)
        delete_button.place(relx=0.4, rely=0.1, relwidth=0.2)

        self.songs_listbox = tk.Listbox(master=self, selectmode=tk.MULTIPLE,
                                        exportselection=False)
        self.songs_listbox.place(relx=0.65, rely=0.1, relwidth=0.3)
        self.fill_pl_songs()

        self.playlists_box = tk.Listbox(master=self, selectmode=tk.SINGLE,
                                        exportselection=False)
        self.playlists_box.place(relx=0.05, rely=0.1, relwidth=0.3)
        self.fill_pls()
        self.playlists_box.bind('<<ListboxSelect>>', self.choose_pl)
        play_button.bind(RIGHT_CLICK, self.help)
        add_button.bind(RIGHT_CLICK, self.help)
        create_button.bind(RIGHT_CLICK, self.help)
        delete_button.bind(RIGHT_CLICK, self.help)
        remove_button.bind(RIGHT_CLICK, self.help)
        view_all_button.bind(RIGHT_CLICK, self.help)

    def get_text(self, event):
        """
        gets the text from both entry boxes, puts underscores instead of spaces
        """
        name = self.playlist_name.get().replace(SPACE, UNDERSCORE)
        if name == "":
            return ERROR
        return name

    def help(self, event):
        """
        opens a window with explanations about how to operate the ui
        """
        widget_name = event.widget[TEXT]
        print(widget_name)
        tk.messagebox.showinfo(TITLE, HELP_STRINGS[widget_name])
        self.master.lift()

    def delete_pl(self):
        """
        deletes the chosen playlist
        """
        msg = self.manager.client.delete_pl(self.chosen_pl)
        self.playlists_box.selection_clear(0, END)
        self.fill_pls()

    def play_pl(self):
        """
        plays the chosen playlist in shuffled order
        """
        if self.chosen_pl == "":
            return
        songs = self.manager.client.get_songs_in_pl(self.chosen_pl)
        random.shuffle(songs)
        self.manager.client.play_song_top(songs[ZERO])
        for song in songs[ONE:]:
            self.manager.client.song_q.put(song)

    def fill_pls(self):
        """
        fills the playlist listbox with all playlists
        """
        clear_listbox(self.playlists_box)
        self.all_playlists = self.manager.client.get_all_pls_of_user()
        for i in range(len(self.all_playlists)):
            self.playlists_box.insert(i, self.all_playlists[i])

    def fill_pl_songs(self, playlist=None):
        """
        fills the songs listbox with all songs if no playlist is given
        or with the songs in a certain playlist if it is given to the function
        """
        clear_listbox(self.songs_listbox)
        if playlist is None:
            songs = self.manager.client.get_all_songs()
            self.song_label[TEXT] = "All Downloaded songs"
        else:
            songs = self.manager.client.get_songs_in_pl(playlist)
        for i in range(len(songs)):
            self.songs_listbox.insert(i, songs[i])

    def choose_songs(self):
        """
        gets all the chosen songs from the songs listbox
        """
        self.selected_songs = []
        indexes = self.songs_listbox.curselection()
        for index in indexes:
            self.selected_songs.append(self.songs_listbox.get(index))

    def choose_pl(self, event=None):
        """
        fills the songs listbox and updates the chosen playlist variable
        whenever a playlist is clicked on
        by the user.
        """
        try:
            index = self.playlists_box.curselection()
            self.chosen_pl = self.playlists_box.get(index)
            self.song_label[TEXT] = "All songs in %s" % self.chosen_pl
            self.fill_pl_songs(self.chosen_pl)
            self.master.lift()
        except tk.TclError as e:
            print(e)

    def create_pl(self):
        """
        gets the name from the entry box and the songs from the listbox
        and creates a new playlist with them
        """
        name = self.get_text(None)
        if name == ERROR:
            return
        self.choose_songs()
        msg = self.manager.client.create_playlist(self.selected_songs, name)
        msg = SPACE.join(msg)
        tk.messagebox.showinfo(TITLE, msg)
        self.fill_pls()
        self.master.lift()
        self.songs_listbox.selection_clear(ZERO, END)

    def remove_song_from_pl(self):
        """
        removes the chosen song from the chosen playlist
        """
        self.songs_listbox.config(selectmode=tk.SINGLE)
        self.choose_songs()
        if self.selected_songs or self.chosen_pl is None:
            msg = self.manager.client.remove_song_from_pl(
                self.selected_songs[ZERO], self.chosen_pl)
            print(msg)

    def add_song_to_pl(self):
        """
        adds the chosen song to the chosen playlist
        """
        self.songs_listbox.config(selectmode=tk.SINGLE)
        self.choose_songs()
        if self.selected_songs or self.chosen_pl is None:
            msg = self.manager.client.add_song_to_pl(self.selected_songs[ZERO],
                                                     self.chosen_pl)
            print(msg)

    def call_manager_exit(self):
        """
        calls the manager exit function
        """
        self.manager.close_frame()

    def switch_window(self, window):
        self.manager.switch_frame(window)

    def exit_window(self):
        """
        exits the window
        """
        self.quit()
        self.destroy()


def clear_listbox(listbox):
    listbox.delete(ZERO, listbox.size())
