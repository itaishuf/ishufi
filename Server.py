import socket
import sys
import time
import database
from pathlib import Path
import os
import queue
import threading
import pyaudio
import wave
from YoutubeDownloader import YoutubeDownloader
from Consts import *


class Server(object):
    def __init__(self, ip, port, stream_port):
        try:
            server_socket_streaming = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket_streaming.bind((ip, stream_port))
            server_socket.bind((ip, port))
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.server_socket_streaming = server_socket_streaming
        self.server_socket = server_socket
        self.client_address = ()
        self.client_streaming_address = ()
        self.db = database.ConnectionDatabase()
        self.pause = False
        self.skip_q = queue.Queue()

    def choose_action(self, action, params, event):
        if REQ_AND_PARAMS.get(action) != len(params):
            print("invalid request")
            self.send_message(INVALID_REQ)
            return
        if action == STREAM_ACTION:
            path = choose_song(params[0])
            self.stream_song(path, event)
        elif action == LOGIN_ACTION:
            self.login_check(params[0], params[1])
        elif action == ADD_ACTION:
            self.add_check(params[0], params[1])
        elif action == DOWNLOAD_ACTION:
            self.download_song(params[0])
        elif action == PAUSE_ACTION:
            self.pause = True
            event.clear()
        elif action == UN_PAUSE_ACTION:
            self.pause = False
            event.set()
        elif action == FORWARD_ACTION:
            self.skip_q.put(FORWARD_ACTION)
        elif action == BACKWARD_ACTION:
            self.skip_q.put(BACKWARD_ACTION)
        elif action == STOP:
            self.skip_q.put(STOP)
        elif action == CREATE_PLAYLIST_ACTION:
            self.create_new_playlist(params)
        elif action == GET_ALL_SONGS:
            self.get_all_songs()
        elif action == GET_ALL_PLAYLISTS_OF_USER:
            self.get_all_playlists_of_user(params[0])

    def get_all_songs(self):
        to_send = self.db.get_all_songs()
        to_send = '$'.join(to_send)
        self.send_message(to_send)

    def get_all_playlists_of_user(self, username):
        to_send = self.db.get_all_playlists_of_user(username)
        print(to_send)
        to_send = '$'.join(to_send)
        self.send_message(to_send)

    def create_new_playlist(self, params):
        name = params[1]
        user = params[0]
        songs = params[2].split('&')
        msg = self.db.create_new_playlist(songs, name, user)
        self.send_message(msg)

    def download_song(self, song):
        song = song.replace('_', ' ')
        downloader = YoutubeDownloader(song)
        msg = downloader.download()
        self.send_message(msg)

    def stream_song(self, path, e):
        if path == ERROR:
            self.send_streaming_message(INVALID_REQ)
            return
        sample_rate, channels, my_format = get_metadata(path)
        to_send = sample_rate + "$" + channels + '$' + my_format
        skip_amount = get_byte_num(path)
        print('to send', to_send)
        self.send_streaming_message(to_send)
        with open(path, 'rb') as song:
            data = song.read(MSG_SIZE)
            self.send_streaming_message(data)
            while data != EMPTY_MSG:
                data = song.read(MSG_SIZE)
                if self.pause:
                    e.wait()
                if not self.skip_q.empty():
                    msg = self.skip_q.get()
                    if msg == FORWARD_ACTION:
                        song.read(int(skip_amount))
                    elif msg == BACKWARD_ACTION:
                        song.seek(-1*int(skip_amount), 1)
                    elif msg == STOP:
                        print('stopping')
                        self.send_streaming_message(FINISH)
                        return
                self.send_streaming_message(data)
                time.sleep(MSG_SIZE * NO_LAG_MOD/int(sample_rate))
            self.send_streaming_message(FINISH)

    def login_check(self, username, password):
        can_login, msg = self.db.check_login(username, password)
        self.send_message(str(can_login) + "$" + msg)

    def add_check(self, username, password):
        can_login, msg = self.db.add_user(username, password)
        self.send_message(str(can_login) + "$" + msg)

    def receive_streaming_msg(self):
        size, client_streaming_address = self.server_socket_streaming.recvfrom(HEADER_SIZE)
        data, client_streaming_address = self.server_socket_streaming.recvfrom(int(size))
        print('receive stream', data)
        data = data.decode()
        data = data.split("$")
        self.client_streaming_address = client_streaming_address
        return data

    def send_streaming_message(self, data):
        header, data = format_msg(data)
        self.server_socket_streaming.sendto(header, self.client_streaming_address)
        self.server_socket_streaming.sendto(data, self.client_streaming_address)

    def receive_msg(self):
        size, client_address = self.server_socket.recvfrom(HEADER_SIZE)
        data, client_address = self.server_socket.recvfrom(int(size))
        data = data.decode()
        data = data.split("$")
        self.client_address = client_address
        return data

    def send_message(self, data):
        header, data = format_msg(data)
        print('send msg', data)
        self.server_socket.sendto(header, self.client_address)
        self.server_socket.sendto(data, self.client_address)

    def handle_client(self):
        e = threading.Event()
        reg_t = threading.Thread(target=self.handle_reg_client, args=(e,))
        stream_t = threading.Thread(target=self.handle_stream_client, args=(e,))
        reg_t.start()
        stream_t.start()

    def handle_reg_client(self, event):
        try:
            while True:
                client_req = self.receive_msg()
                self.choose_action(client_req[0], client_req[1:], event)
        except socket.error as e:
            print(e)

    def handle_stream_client(self, event):
        try:
            while True:
                client_req = self.receive_streaming_msg()
                self.choose_action(client_req[0], client_req[1:], event)
        except socket.error as e:
            print(e)


def song_check(song):
    msg = choose_song(song)
    return msg != ERROR


def get_byte_num(path):
    sample, channels, my_format = get_metadata(path)
    return (int(sample) * int(my_format) * int(channels)*15) / 8


def choose_song(name):
    name = name.split('@')[0]
    path = ''
    for filename in os.listdir(str(Path.cwd())+'/songs'):
        if filename.endswith(".wav") and name in filename:
            path = str(Path.cwd()) + r'\songs\%s' % filename
    if os.path.exists(path):
        return path
    else:
        return ERROR


def get_metadata(my_path):
    with wave.open(my_path, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        my_format = pyaudio.get_format_from_width(wave_file.getsampwidth())
    return str(frame_rate), str(channels), str(my_format)


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(HEADER_SIZE)
    if type(msg) == str:
        msg = msg.encode()
    return header.encode(), msg


def main():
    server = Server(IP, PORT, STREAM_PORT)
    server.handle_client()


if __name__ == '__main__':
    main()
