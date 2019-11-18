import socket
import miniaudio
import time
import queue
import asyncio

MSG_SIZE = 40000
SAMPLE_RATE = 48000
NO_LAG_MOD = 1.95
STREAM_ACTION = "STREAM"
FINISH = b"finish"


class Client(object):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.device = miniaudio.PlaybackDevice()
        self.server_address = ("127.0.0.1", 8822)
        self.chunk_queue = queue.Queue()

    async def receive_song(self):
        packet_index = 2
        print("receive_song")
        new_data, server_address = self.receive_msg()
        self.server_address = server_address
        data = new_data
        while new_data != FINISH:
            new_data, server_address = self.receive_msg()
            # print(len(data), packet_index, MSG_SIZE)
            if len(data) == packet_index * MSG_SIZE:
                print("put")
                self.chunk_queue.put(data)
                if packet_index < 8:
                    packet_index += 1
                else:
                    await asyncio.sleep(0.2)
                data = b''
            elif len(data) < packet_index * MSG_SIZE:
                data += new_data

    async def play_song(self):
        await asyncio.sleep(1)
        print("play_song")
        while not self.chunk_queue.empty():
            data = self.chunk_queue.get()
            stream = miniaudio.stream_memory(data)
            self.device.start(stream)
            print(len(data) * NO_LAG_MOD / SAMPLE_RATE)
            await asyncio.sleep(len(data) * NO_LAG_MOD / SAMPLE_RATE)
            self.device.stop()

    async def run(self):
        await asyncio.gather(self.receive_song(), self.play_song())

    def send_req(self):
        self.send_message(STREAM_ACTION.encode())

    def handle_client(self):
        action = input("enter action: ")
        while action != "exit":
            self.send_req()
            print("starting")
            asyncio.run(self.run())
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
