# -*- coding: utf-8 -*-
import socket
import pyaudio
import time
import threading
from Consts import *


class Client(object):
    def __init__(self):
        self.my_socket_streaming = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_stream_address = (IP, STREAM_PORT)
        self.server_address = (IP, PORT)
        self.p = pyaudio.PyAudio()
        self.song_playing = ""

    def play(self):
        try:
            metadata, server_address = self.receive_streaming_msg()
            print('metadata', metadata)
            metadata = metadata.decode().split('$')
            sample_rate = int(metadata[0])
            channels = int(metadata[1])
            my_format = int(metadata[2])
            new_data, server_address = self.receive_streaming_msg()
            if new_data == INVALID_REQ.encode():
                return INVALID_REQ
            p = pyaudio.PyAudio()
            stream = p.open(format=my_format, channels=channels, rate=sample_rate,
                            output=True, frames_per_buffer=4096)
            start = time.time()
            while new_data != FINISH:
                if new_data is not None:
                    stream.write(new_data)
                new_data, server_address = self.receive_streaming_msg()
            end = time.time()
            my_time = end-start
            print(my_time)
            return str(my_time)
        except socket.error as e:
            print(e)

    def download_song(self, song):
        to_send = DOWNLOAD_ACTION + "$" + song
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        data = data[0]
        if data == INVALID_REQ:
            return False, "didn't enter song"
        elif data == SUCCESS:
            return True, SUCCESS
        else:
            return False, ERROR

    def pause(self):
        self.send_message(PAUSE_ACTION)

    def un_pause(self):
        self.send_message(UN_PAUSE_ACTION)

    def forward(self):
        self.send_message(FORWARD_ACTION)

    def backward(self):
        self.send_message(BACKWARD_ACTION)

    def play_song(self, lst):
        song = lst[0]
        q = lst[1]
        print(song, self.song_playing)
        if self.song_playing == song:
            return
        elif self.song_playing != "":
            self.send_message(STOP)
            time.sleep(0.4)
        self.song_playing = song
        to_send = STREAM_ACTION + "$" + song
        self.send_streaming_message(to_send)
        msg = self.play()
        if msg == INVALID_REQ:
            q.put(INVALID_REQ)
        self.song_playing = ""

    def login(self, username, password):
        to_send = LOGIN_ACTION + "$" + username + "$" + password
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
        can_login = eval(data[0])
        msg = " ".join(data[1:])
        return can_login, msg

    def add_user(self, username, password):
        to_send = ADD_ACTION + "$" + username + "$" + password
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        data = data.decode()
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
        data = data.split('$')
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
            data = data.decode()
            data = data.split('$')
            return data, server_address
        except OSError as e:
            print(e)
            return FINISH, None

    def send_streaming_message(self, data):
        header, data = format_msg(data)
        self.my_socket_streaming.sendto(header, self.server_stream_address)
        self.my_socket_streaming.sendto(data, self.server_stream_address)

    def receive_streaming_msg(self):
        try:
            size, server_address = self.my_socket_streaming.recvfrom(5)
            data, server_address = self.my_socket_streaming.recvfrom(int(size))
            return data, server_address
        except OSError as e:
            print(e)
            return FINISH, None

    def receive_msg_not_song(self):
        try:
            size, server_address = self.my_socket_streaming.recvfrom(5)
            data, server_address = self.my_socket_streaming.recvfrom(int(size))

            data = data.decode()
            data = data.split('$')
            data = " ".join(data)
            return data, server_address
        except OSError as e:
            print(e)
            return FINISH, None

    def close_com(self):
        self.my_socket_streaming.close()
        self.my_socket.close()


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(5)
    return header.encode(), msg.encode()


def main():
    pass


if __name__ == '__main__':
    main()
