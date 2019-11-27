import socket
import miniaudio
import pyaudio
import time
import queue
import threading

MSG_SIZE = 16000
SAMPLE_RATE = 48000
CHANNELS = 2
NO_LAG_MOD = 0.1
STREAM_ACTION = "STREAM"
FINISH = b"finish"


class Client(object):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ("127.0.0.1", 8822)
        self.p = pyaudio.PyAudio()

    def play(self):
        print("receive_song")
        new_data, server_address = self.receive_msg()
        self.server_address = server_address
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=SAMPLE_RATE, output=True, frames_per_buffer=4000)
        start = time.time()
        while new_data != FINISH:
            stream.write(new_data)
            new_data, server_address = self.receive_msg()
        end = time.time()
        print(end-start)

    def send_req(self):
        self.send_message(STREAM_ACTION.encode())

    def handle_client(self):
        action = input("enter action: ")
        while action != "exit":
            self.send_req()
            print("starting")
            self.play()
            # self.run()
            print("finished")
            action = input("enter action: ")

    def send_message(self, data):
        header, data = format_msg(data)
        self.my_socket.sendto(header, self.server_address)
        self.my_socket.sendto(data, self.server_address)

    def receive_msg(self):
        size, client_address = self.my_socket.recvfrom(5)
        data, client_address = self.my_socket.recvfrom(int(size))
        return data, client_address


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(5)
    msg = (header.encode(), msg)
    return msg


def main():
    client = Client()
    client.handle_client()


if __name__ == '__main__':
    main()
