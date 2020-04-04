# -*- coding: utf-8 -*-
import queue
import socket
import threading
import time

import pyaudio

from Consts import *


class Client(object):
    def __init__(self):
        self.my_socket_streaming = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_stream_address = (IP, STREAM_PORT)
        self.server_address = (IP, PORT)
        self.p = pyaudio.PyAudio()
        self.song_q = queue.Queue()
        self.play_next_song = False
        self.paused = False
        self.song_playing = ''
        self.current_user = ''

        self.song_stack = []
        queue_t = threading.Thread(target=self.check_q)
        queue_t.start()

    def play(self):
        metadata, server_address = self.receive_streaming_msg()
        if metadata == INVALID_REQ.encode():
            return INVALID_REQ
        metadata = metadata.decode().split('$')
        sample_rate = int(metadata[0])
        channels = int(metadata[1])
        my_format = int(metadata[2])
        new_data, server_address = self.receive_streaming_msg()
        p = pyaudio.PyAudio()
        stream = p.open(format=my_format, channels=channels, rate=sample_rate,
                        output=True, frames_per_buffer=4096)
        start = time.time()
        while new_data != FINISH:
            if new_data is not None:
                stream.write(new_data)
            try:
                new_data, server_address = self.receive_streaming_msg()
            except socket.error as e:
                print(e)
        end = time.time()
        my_time = end - start
        print(my_time)
        return str(my_time)

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

    def create_playlist(self, songs, playlist):
        # creates playlist and links the current user to it
        to_send = CREATE_PL_ACTION + '$' + self.current_user + '$' + playlist + '$' + '&'.join(songs)
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def delete_pl(self, playlist):
        to_send = UNLINK_PLAYLIST + '$' + self.current_user + '$' + playlist
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def get_all_songs(self):
        self.send_message(GET_ALL_SONGS)
        data, server_address = self.receive_msg()
        return data

    def get_songs_in_pl(self, playlist):
        to_send = GET_SONGS_IN_PL + '$' + playlist
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def get_all_pls_of_user(self):
        to_send = GET_ALL_PLS_OF_USER + '$' + self.current_user
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def remove_song_from_pl(self, song, pl):
        to_send = REMOVE_SONG_FROM_PL + '$' + song + '$' + pl
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def add_song_to_pl(self, song, pl):
        to_send = ADD_SONG_TO_PL + '$' + song + '$' + pl
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def pause(self):
        self.send_message(PAUSE_ACTION)

    def un_pause(self):
        self.send_message(UN_PAUSE_ACTION)

    def forward(self):
        self.send_message(FORWARD_ACTION)

    def backward(self):
        self.send_message(BACKWARD_ACTION)

    def play_song_thread(self, lst):
        self.play_next_song = False
        song = lst[0]
        q = lst[1]
        if self.song_playing == song:
            print("playing same song")
            if not self.paused:
                self.paused = True
                self.pause()
                return
            else:
                self.paused = False
                self.un_pause()
                return
        elif self.song_playing != "":
            self.send_message(STOP)
            time.sleep(0.4)
        self.song_playing = song
        to_send = STREAM_ACTION + "$" + song
        self.send_streaming_message(to_send)
        print('playing', song)
        msg = self.play()
        if msg == INVALID_REQ:
            q.put(INVALID_REQ)
        self.song_playing = ''
        self.play_next_song = True

    def play_song_top(self, name):
        self.song_stack.append(name)
        return_queue = queue.Queue()
        t_play = threading.Thread(target=self.play_song_thread, args=((name, return_queue),))
        t_play.start()
        time.sleep(0.1)
        if return_queue.empty():
            return None
        if return_queue.get() == INVALID_REQ:
            return "song doesnt exist"

    def check_q(self):
        time.sleep(2)
        while True:
            next_song = self.song_q.get()
            if next_song != '':
                while not self.play_next_song:
                    time.sleep(1)
                print('adding', next_song)
                self.play_song_top(next_song)
            time.sleep(1)

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
        can_login = eval(data[0])
        msg = " ".join(data[1:])
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
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

    def close_com(self):
        self.my_socket_streaming.close()
        self.my_socket.close()


def format_msg(msg):
    if type(msg) == str:
        msg = msg.encode()
    header = str(len(msg))
    header = header.zfill(5)
    return header.encode(), msg
