import socket
import sys
import time
import database
from pathlib import Path
import os
import wave
import scipy.io.wavfile as sio
import YoutubeDownloader

MSG_SIZE = 8000
SAMPLE_RATE = 48000
NO_LAG_MOD = 0.24095
HEADER_SIZE = 5
IP = "127.0.0.1"
PORT = 8821
PATH = r"C:\ishufi\songs\abc.wav"
FINISH = b"finish"
EMPTY_MSG = b''
STREAM_ACTION = "STREAM"
EXIT_ACTION = "EXIT"
LOGIN_ACTION = "LOGIN"
ADD_ACTION = "ADD"
INVALID_REQ = "invalid"
SUCCESS = "Success"
DOWNLOAD_ACTION = "DOWNLOAD"
REQ_AND_PARAMS = {STREAM_ACTION: 1,
                  LOGIN_ACTION: 2,
                  EXIT_ACTION: 1,
                  ADD_ACTION: 2,
                  DOWNLOAD_ACTION: 1}


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
            path = self.choose_song(params)
            self.stream_song(path)
        elif action == LOGIN_ACTION:
            self.login_check(params[0], params[1])
        elif action == ADD_ACTION:
            self.add_check(params[0], params[1])
        elif action == DOWNLOAD_ACTION:
            self.download_song(params[0])

    def choose_song(self, name):
        path = str(Path.cwd())
        path += '\songs\\'
        path += name
        path += ".wav"
        if os.path.exists(path):
            return "already exists"
        else:
            return path

    def get_metadata(self, name):
        my_path = str(Path.cwd())
        my_path += '\songs\\'
        my_path += name
        my_path += ".wav"
        print('my path: ', my_path)
        bit_rate, data = sio.read(my_path)
        channels = 2
        print("here")
        print(bit_rate, channels)

    def download_song(self, song):
        msg = YoutubeDownloader.download_song(song)
        self.send_message(msg)
        self.get_metadata(song)

    def stream_song(self, path):
        # print(miniaudio.get_file_info(path))
        if path == "":
            self.send_message(INVALID_REQ)
            return
        with open(path, 'rb') as song:
            data = song.read(MSG_SIZE)
            self.send_message(data)
            while data != EMPTY_MSG:
                data = song.read(MSG_SIZE)
                self.send_message(data)
                time.sleep(MSG_SIZE * NO_LAG_MOD/SAMPLE_RATE)
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
        msg= msg.encode()
    return header.encode(), msg


def main():
    server = Server(IP, PORT)
    server.handle_client()


if __name__ == '__main__':
    main()
