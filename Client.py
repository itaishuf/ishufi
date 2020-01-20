# -*- coding: utf-8 -*-
import socket
import pyaudio
import time

MSG_SIZE = 8000
SAMPLE_RATE = 48000
CHANNELS = 2
NO_LAG_MOD = 0.1
IP = "127.0.0.1"
PORT = 8821
STREAM_ACTION = "STREAM"
EXIT_ACTION = "EXIT"
LOGIN_ACTION = "LOGIN"
ADD_ACTION = "ADD"
INVALID_REQ = "invalid"
DONE = "done"
FINISH = b"finish"


class Client(object):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (IP, PORT)
        self.p = pyaudio.PyAudio()
        self.song_playing = False

    def play(self):
        try:
            new_data, server_address = self.receive_msg()
            self.server_address = server_address
            if new_data == INVALID_REQ.encode():
                return INVALID_REQ
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=SAMPLE_RATE,
                            output=True, frames_per_buffer=4000)
            start = time.time()
            while new_data != FINISH:
                if new_data is not None:
                    stream.write(new_data)
                new_data, server_address = self.receive_msg()
            end = time.time()
            my_time = end-start
            print(my_time)
            return str(my_time)
        except socket.error as e:
            print(e)


    def play_song(self, lst):
        song = lst[0]
        q = lst[1]
        if self.song_playing:
            return
        self.song_playing = True
        to_send = STREAM_ACTION + " " + song
        self.send_message(to_send)
        msg = self.play()
        print(msg)
        if msg == INVALID_REQ:
            q.put(INVALID_REQ)
        self.song_playing = False

    def login(self, username, password):
        to_send = LOGIN_ACTION + " " + username + " " + password
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        data = data.decode()
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
        data = data.split()
        can_login = eval(data[0])
        msg = " ".join(data[1:])
        return can_login, msg

    def add_user(self, username, password):
        to_send = ADD_ACTION + " " + username + " " + password
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        data = data.decode()
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
        data = data.split()
        can_login = eval(data[0])
        msg = " ".join(data[1:])
        return can_login, msg

    def send_message(self, data):
        header, data = format_msg(data)
        self.my_socket.sendto(header, self.server_address)
        self.my_socket.sendto(data, self.server_address)

    def receive_msg(self):
        try:
            size, server_address = self.my_socket.recvfrom(5)
            data, server_address = self.my_socket.recvfrom(int(size))
            return data , server_address
        except OSError as e:
            print(e)
            return FINISH, None

    def receive_msg_not_song(self, data, server_address):
        return data.decode(), server_address

    def close_com(self):
        self.my_socket.close()


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(5)
    return header.encode(), msg.encode()


def main():
    pass


if __name__ == '__main__':
    main()
