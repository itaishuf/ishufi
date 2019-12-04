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
FINISH = b"finish"


class Client(object):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (IP, PORT)
        self.p = pyaudio.PyAudio()

    def play(self):
        print("receive_song")
        new_data, server_address = self.receive_msg()
        self.server_address = server_address
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=SAMPLE_RATE,
                        output=True, frames_per_buffer=4000)
        start = time.time()
        while new_data != FINISH:
            if new_data is not None:
                stream.write(new_data)
            new_data, server_address = self.receive_msg()
        end = time.time()
        print(end-start)

    def send_req(self):
        self.send_message(STREAM_ACTION.encode())

    def handle_client(self, action):
        self.send_req()
        print("starting")
        self.play()
        print("finished")

    def send_message(self, data):
        header, data = format_msg(data)
        self.my_socket.sendto(header, self.server_address)
        self.my_socket.sendto(data, self.server_address)

    def receive_msg(self):
        try:
            size, client_address = self.my_socket.recvfrom(5)
            data, client_address = self.my_socket.recvfrom(int(size))
            return data, client_address
        except OSError as e:
            print(e)
            return None, None


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
