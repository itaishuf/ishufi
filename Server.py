import socket
import sys
import miniaudio
import time
MSG_SIZE = 8000
SAMPLE_RATE = 48000
NO_LAG_MOD = 0.24095
HEADER_SIZE = 5
IP = "127.0.0.1"
PORT = 8821
PATH = r"C:\ishufi\test_song_trimmed.wav"
FINISH = b"finish"
EMPTY_MSG = b''
STREAM_ACTION = "STREAM"
EXIT_ACTION = "EXIT"

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

    def handle_req(self):
        data, client_address = self.receive_msg()
        data = data.decode()
        self.client_address = client_address
        return data

    def choose_action(self, action):
        if action == STREAM_ACTION:
            self.stream_song(PATH)

    def stream_song(self, path):
        print(miniaudio.get_file_info(path))
        with open(path, 'rb') as song:
            data = song.read(MSG_SIZE)
            self.send_message(data)
            while data != EMPTY_MSG:
                data = song.read(MSG_SIZE)
                self.send_message(data)
                time.sleep(MSG_SIZE * NO_LAG_MOD/SAMPLE_RATE)
            self.send_message(FINISH)
            print("finished")

    def receive_msg(self):
        size, client_address = self.server_socket.recvfrom(HEADER_SIZE)
        data, client_address = self.server_socket.recvfrom(int(size))
        return data, client_address

    def send_message(self, data):
        header, data = format_msg(data)
        self.server_socket.sendto(header, self.client_address)
        self.server_socket.sendto(data, self.client_address)

    def handle_client(self):
        try:
            while True:
                client_req = self.handle_req()
                self.choose_action(client_req)
        except socket.error as e:
            print(e)



def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(HEADER_SIZE)
    return header.encode(), msg


def main():
    server = Server(IP, PORT)
    server.handle_client()


if __name__ == '__main__':
    main()
