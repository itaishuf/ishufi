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
            self.add_song_to_playlist(song, playlist)
        elif action == REMOVE_ACTION:
            self.remove_song_from_playlist(song, playlist)

    def remove_song_from_playlist(self, song, playlist):
        command = "UPDATE playlists SET %s = 0 WHERE songs = '%s'" % (playlist, song)
        self.execute(command)

    def add_song_to_playlist(self, song, playlist):
        command = "UPDATE playlists SET %s = 1 WHERE songs = '%s'" % (playlist, song)
        self.execute(command)

    def link_user_to_playlist(self, username, playlist):
        if playlist not in self.get_column_list("playlists"):
            return
        command = "SELECT id FROM users WHERE username = '%s'" % username
        my_id = self.execute(command)[0]
        command = "INSERT INTO user_to_list(user, playlist) VALUES('%s', '%s')" % (my_id, playlist)
        self.execute(command)

    def unlink_user_to_playlist(self, username, playlist):
        if playlist not in self.get_column_list("playlists"):
            return
        command = "SELECT id FROM users WHERE username = '%s'" % username
        my_id = self.execute(command)[0]
        command = "DELETE FROM user_to_list WHERE playlist='%s' AND user='%s'" % (playlist, my_id)
        self.execute(command)

    def delete_playlist(self, playlist):
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

    def add_song(self, song, playlist):
        command = "UPDATE playlists SET %s = 1 WHERE songs = '%s'" % (playlist, song)
        self.execute(command)

    def add_new_song(self, song):
        command = "INSERT INTO playlists(songs) VALUES('%s')" % song
        self.execute(command)

    def init_new_playlist(self, playlist):
        command = "alter table playlists add '%s' INTEGER NOT NULL DEFAULT 0" % playlist
        self.execute(command)

    def create_new_playlist(self, songs, playlist):
        self.init_new_playlist(playlist)
        for song in songs:
            self.add_song(song, playlist)

    def get_songs(self, playlist):
        command = "SELECT songs FROM playlists WHERE %s = 1" % playlist
        return self.execute(command)

    def execute(self, command, offset=0):
        r = self.cursor.execute(command)
        self.connection.commit()
        data = []
        for i in r:
            data.append(i[offset])
        return data


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
    c.unlink_user_to_playlist("itai", "shira")


if __name__ == '__main__':
    main()
