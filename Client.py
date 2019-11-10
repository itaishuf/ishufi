import socket
import miniaudio
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
        data = b''
        self.server_address = server_address
        # stream = miniaudio.stream_memory(new_data)
        # self.device.start(stream)
        yield new_data
        while new_data != FINISH:
            data = data + new_data
            new_data, server_address = self.receive_msg()
            # self.device.stop()
            # print("start")
            # stream = miniaudio.stream_memory(new_data)
            # self.device.start(stream)
            yield new_data

    def play_song(self):
        for i in self.receive_song():
            stream = miniaudio.stream_memory(i)
            self.device.start(stream)
            time.sleep(MSG_SIZE/SAMPLE_RATE)
            self.device.stop()

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
