# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path
import os.path


class ConnectionDatabase:
    def __init__(self):
        loc = str(Path.cwd()) + "\login_data.db"
        self.connection = sqlite3.connect(loc)
        self.cursor = None

        self.create_cursor()
    # cursor generation

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


def main():
    """
    an example insert query for python and sqlite
    """
    # opening connection
    c = ConnectionDatabase()
    s = c.add_user("aa", "11")
    print(s)
    s = c.check_login("aa", "11")
    print(s)


if __name__ == '__main__':
    main()
