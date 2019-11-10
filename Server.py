import socket
import sys
import miniaudio
import time
PATH = r"C:\ishufi\test_song.mp3"
FINISH = b"finish"


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
        if action == "STREAM":
            self.stream_song(PATH)

    def stream_song(self, path):
        with open(path, 'rb') as song:
            data = song.read(1024)
            self.send_message(data)
            while data != b'':
                data = song.read(1024)
                self.send_message(data)
                time.sleep(0.01)
            self.send_message(FINISH)
            print(FINISH)

    def receive_msg(self):
        size, client_address = self.server_socket.recvfrom(4)
        data, client_address = self.server_socket.recvfrom(int(size))
        return data, client_address

    def send_message(self, data):
        header, data = format_msg(data)
        self.server_socket.sendto(header, self.client_address)
        self.server_socket.sendto(data, self.client_address)

    def handle_client(self):
        client_req = self.handle_req()
        self.choose_action(client_req)


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(4)
    print(msg)
    print(header)
    return header.encode(), msg


def main():
    server = Server("127.0.0.1", 8821)
    server.handle_client()


if __name__ == '__main__':
    main()
