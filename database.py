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

    def remove_song_from_pl(self, song, playlist):
        command = "UPDATE playlists SET %s = 0 WHERE songs = '%s'" % (playlist, song)
        return self.execute(command)

    def add_song_to_pl(self, song, playlist):
        command = "UPDATE playlists SET %s = 1 WHERE songs = '%s'" % (playlist, song)
        return self.execute(command)

    def check_if_linked(self, username, playlist):
        my_id = self.get_user_id(username)
        command = "select * from user_to_list where user='%s' and playlist='%s'" % (my_id, playlist)
        data = self.execute(command)
        return data != []

    def link_user_to_pl(self, username, playlist):
        if playlist not in self.get_column_list("playlists"):
            return
        if self.check_if_linked(username, playlist):
            return
        my_id = self.get_user_id(username)
        command = "INSERT INTO user_to_list(user, playlist) VALUES('%s', '%s')" % (my_id, playlist)
        self.execute(command)

    def get_user_id(self, username):
        command = "SELECT id FROM users WHERE username = '%s'" % username
        my_id = self.execute(command)[0]
        return my_id

    def unlink_user_to_pl(self, username, playlist):
        if playlist not in self.get_column_list("playlists"):
            return None
        if not self.check_if_linked(username, playlist):
            return None
        my_id = self.get_user_id(username)
        command = "DELETE FROM user_to_list WHERE playlist='%s' AND user='%s'" % (playlist, my_id)
        return self.execute(command)

    def delete_pl(self, playlist):
        column_list = self.get_column_list("playlists")
        if playlist in column_list:
            column_list.remove(playlist)
        columns = format_column_list(column_list)
        command = "BEGIN TRANSACTION;" \
                  "CREATE TEMPORARY TABLE t1_backup(%s); " \
                  "INSERT INTO t1_backup SELECT %s FROM %s; " \
                  "DROP TABLE %s; " \
                  "CREATE TABLE %s(%s); " \
                  "INSERT INTO %s SELECT %s FROM t1_backup; " \
                  "DROP TABLE t1_backup; " \
                  "COMMIT; " % (columns, columns, "playlists", "playlists", "playlists", columns, "playlists", columns)
        self.cursor.executescript(command)
        self.connection.commit()

    def get_column_list(self, table):
        command = "PRAGMA table_info(%s)" % table
        return self.execute(command, offset=1)

    def add_new_song(self, song):
        command = "INSERT INTO playlists(songs) VALUES('%s')" % song
        return self.execute(command)

    def init_new_playlist(self, playlist):
        command = "alter table playlists add '%s' INTEGER NOT NULL DEFAULT 0" % playlist
        return self.execute(command)

    def check_if_pl_exists(self, playlist):
        playlists = self.get_column_list("playlists")
        return playlist in playlists

    def create_new_pl(self, songs, playlist, user):
        if self.check_if_pl_exists(playlist):
            return "playlist name taken"
        self.init_new_playlist(playlist)
        for song in songs:
            self.add_song_to_pl(song, playlist)
        self.link_user_to_pl(user, playlist)
        return "playlist created successfully"

    def get_songs(self, playlist):
        command = "SELECT songs FROM playlists WHERE %s = 1" % playlist
        return self.execute(command)

    def execute(self, command, offset=0):
        try:
            r = self.cursor.execute(command)
            self.connection.commit()
        except Exception as e:
            print(e)
            return ERROR
        data = []
        for i in r:
            data.append(i[offset])
        return data

    def get_all_songs(self):
        command = "Select songs from playlists"
        return self.execute(command)

    def get_all_pls_of_user(self, username):
        my_id = self.get_user_id(username)
        command = "SELECT playlist FROM user_to_list WHERE user='%s'" % my_id
        lists = self.execute(command)
        return lists


def format_column_list(column_list):
    to_send = ""
    for x in column_list:
        to_send += x
        to_send += ', '
    return to_send[:-2]


def main():
    """
    an example insert query for python and sqlite
    """
    # opening connection
    c = ConnectionDatabase()


if __name__ == '__main__':
    main()
