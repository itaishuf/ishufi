# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path
from Consts import *


class ConnectionDatabase:
    def __init__(self):
        loc = str(Path.cwd()) + "\login_data.db"
        self.connection = sqlite3.connect(loc, check_same_thread=False)
        self.cursor = None

        self.create_cursor()

    def create_cursor(self):
        self.cursor = self.connection.cursor()

    def close_cursor(self):
        self.cursor.close()
        self.connection.close()

    def check_login(self, username, password):
        if username != "":
            if not self.check_if_exist(username):
                r = self.cursor.execute("SELECT password from users where username=?", (username,))
                self.connection.commit()
                for p in r:
                    if p[0] == password:
                        return True, "welcome to ISHUFI"
                    else:
                        return False, "username or password incorrect, please try again"
            else:
                return False, "user does not exist, please try again"
        else:
            return False, "please enter username"

    def check_if_exist(self, name_to_add):
        r = self.cursor.execute("SELECT username from users")
        self.connection.commit()
        for name in r:
            if name[0] == name_to_add:
                return False
        return True

    def add_user(self, new_name, new_password):
        if new_name != "":
            if self.check_if_exist(new_name):
                print("user does not exist")
                if new_password != "":
                    self.cursor.execute("insert into users (username, password) values(?, ?)", (new_name, new_password))
                    self.connection.commit()
                    return True, "welcome to ISHUFI"
                else:
                    return False, "please enter password"
            else:
                return False, "the username you chose is taken please insert a different username"
        else:
            return False, "please enter username"

    def edit_playlist(self, action, song, playlist):
        if action == ADD_ACTION:
            r = self.cursor.execute("SELECT * from playlists where name=?", (playlist,))
            self.connection.commit()
            data = []
            for i in r:
                data = i
            data = data[2:data.index('')]
            next_song_num = len(data)+1
            next_song = 'song$' + str(next_song_num)
            if song in data:
                return
            command = "UPDATE playlists SET %s = %s WHERE name = %s;" % (next_song, song, playlist)
            print(command)
            self.cursor.execute(command)

    def link_user_to_playlist(self, username, playlist):
        list_id, user_id = None, None
        r = self.cursor.execute("SELECT id from users where username=?", (username,))
        self.connection.commit()
        for i in r:
            print('found name')
            user_id = i
        rn = self.cursor.execute("SELECT id from playlists where name=?", (playlist, ))
        self.connection.commit()
        for i in rn:
            print('found list')
            list_id = i
        if list_id is None or user_id is None:
            print('didnt find')
            return
        # TODO: handle errors
        print(list_id, user_id)
        self.cursor.execute("insert into playlist_per_user (playlist, user) values(?, ?) ", (list_id[0], user_id[0]))
        self.connection.commit()

    def add_new_playlist(self, params):
        params = pad_playlist(params)
        self.cursor.execute("insert into playlists (name, song$1, song$2, song$3, song$4, song$5,"
                            " song$6, song$7, song$8, song$9, song$10, song$11, song$12, song$13,"
                            " song$14, song$15, song$16) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
                            " ?, ?, ?, ?, ?, ?)", params)
        self.connection.commit()


def pad_playlist(params):
        return params + [None]*(17-len(params))


def main():
    """
    an example insert query for python and sqlite
    """
    # opening connection
    c = ConnectionDatabase()
    c.edit_playlist(ADD_ACTION, 'rock30', 'itai')


if __name__ == '__main__':
    main()
