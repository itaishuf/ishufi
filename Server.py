import socket
import sys
import time
import database
from pathlib import Path
import os
import pyaudio
import wave
from YoutubeDownloader import YoutubeDownloader
from Consts import *


class Server(object):
    def __init__(self, ip, port):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.bind((ip, port))
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.server_socket = server_socket
        self.client_address = ()
        self.db = database.ConnectionDatabase()

    def choose_action(self, action, params):
        if REQ_AND_PARAMS.get(action) != len(params):
            print("invalid request")
            self.send_message(INVALID_REQ)
            return
        if action == STREAM_ACTION:
            path = self.choose_song(params[0])
            self.stream_song(path)
        elif action == LOGIN_ACTION:
            self.login_check(params[0], params[1])
        elif action == ADD_ACTION:
            self.add_check(params[0], params[1])
        elif action == DOWNLOAD_ACTION:
            self.download_song(params[0])

    def choose_song(self, name):
        path = str(Path.cwd()) + r'\songs\%s.wav' % name
        if os.path.exists(path):
            return path
        else:
            return "doesnt exist"

    def get_metadata(self, my_path):
        with wave.open(my_path, "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            channels = wave_file.getnchannels()
            my_format = pyaudio.get_format_from_width(wave_file.getsampwidth())
        print(frame_rate, channels, my_format)
        return str(frame_rate), str(channels), str(my_format)

    def download_song(self, song):
        downloader = YoutubeDownloader(song)
        msg = downloader.download()
        self.send_message(msg)

    def stream_song(self, path):
        # print(miniaudio.get_file_info(path))
        if path == "":
            self.send_message(INVALID_REQ)
            return
        sample_rate, channels, my_format = self.get_metadata(path)
        to_send = sample_rate + "$" + channels + '$' + my_format
        self.send_message(to_send)
        with open(path, 'rb') as song:
            data = song.read(MSG_SIZE)
            self.send_message(data)
            while data != EMPTY_MSG:
                data = song.read(MSG_SIZE)
                self.send_message(data)
                time.sleep(MSG_SIZE * NO_LAG_MOD/int(sample_rate))
            self.send_message(FINISH)

    def login_check(self, username, password):
        can_login, msg = self.db.check_login(username, password)
        self.send_message(str(can_login) + "$" + msg)

    def add_check(self, username, password):
        can_login, msg = self.db.add_user(username, password)
        self.send_message(str(can_login) + "$" + msg)

    def receive_msg(self):
        size, client_address = self.server_socket.recvfrom(HEADER_SIZE)
        data, client_address = self.server_socket.recvfrom(int(size))
        data = data.decode()
        data = data.split("$")
        self.client_address = client_address
        return data

    def send_message(self, data):
        header, data = format_msg(data)
        self.server_socket.sendto(header, self.client_address)
        self.server_socket.sendto(data, self.client_address)

    def handle_client(self):
        try:
            while True:
                client_req = self.receive_msg()
                self.choose_action(client_req[0], client_req[1:])
        except socket.error as e:
            print(e)
            self.handle_client()


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(HEADER_SIZE)
    if type(msg) == str:
        msg = msg.encode()
    return header.encode(), msg


def main():
    server = Server(IP, PORT)
    server.handle_client()


if __name__ == '__main__':
    main()
