import socket
import miniaudio
import pyaudio
import time
MSG_SIZE = 8192
SAMPLE_RATE = 48000
STREAM_ACTION = "STREAM"
FINISH = b"finish"


class Client(object):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.device = miniaudio.PlaybackDevice()
        self.server_address = ("127.0.0.1", 8821)

    def receive_song(self):
        new_data, server_address = self.receive_msg()
        self.server_address = server_address
        while new_data != FINISH:
            yield new_data
            new_data, server_address = self.receive_msg()

        # new_data, server_address = self.receive_msg()
        # self.server_address = server_address
        # return new_data, pyaudio.paContinue

    def play_song(self):
        p = pyaudio.PyAudio()
        stream = p.open(rate=SAMPLE_RATE, channels=2, format=pyaudio.paInt16, output=True, frames_per_buffer=1024)
        # while stream.is_active():
        #     time.sleep(0)
        # stream.stop_stream()
        # stream.close()
        for i in self.receive_song():
            print(i)
            stream.write(i)
            time.sleep(1/24)
        #     stream = miniaudio.stream_memory(i)
        #     self.device.start(stream)
        #     time.sleep(MSG_SIZE/SAMPLE_RATE)
        #     self.device.stop()
        # stream.close()

    def send_req(self):
        self.send_message(STREAM_ACTION.encode())

    def handle_client(self):
        action = input("enter action: ")
        while action != "exit":
            self.send_req()
            self.play_song()
            action = input("enter action: ")

    def send_message(self, data):
        header, data = format_msg(data)
        self.my_socket.sendto(header, self.server_address)
        self.my_socket.sendto(data, self.server_address)

    def receive_msg(self):
        size, client_address = self.my_socket.recvfrom(4)
        data, client_address = self.my_socket.recvfrom(int(size))
        return data, client_address


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(4)
    msg = (header.encode(), msg)
    return msg


def main():
    client = Client()
    client.handle_client()


if __name__ == '__main__':
    main()
