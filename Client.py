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
EXIT_ACTION = "EXIT"
LOGIN_ACTION = "LOGIN"
INVALID_REQ = "invalid"
FINISH = b"finish"


class Client(object):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (IP, PORT)
        self.p = pyaudio.PyAudio()
        self.song_playing = False

    def play(self):
        try:
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
        except socket.error as e:
            print(e)

    # def handle_client(self, action):
    #     self.send_req()
    #     print("starting")
    #     self.play()
    #     print("finished")

    def play_song(self):
        if self.song_playing:
            return
        self.song_playing = True
        self.send_message(STREAM_ACTION)
        self.play()
        self.song_playing = False

    def login(self, username, password):
        to_send = LOGIN_ACTION + " " + username + " " + password
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
        data = data.split()
        can_login = eval(data[0])
        msg = " ".join(data[1:])
        return can_login, msg

    def send_message(self, data):
        header, data = format_msg(data)
        self.my_socket.sendto(header, self.server_address)
        self.my_socket.sendto(data, self.server_address)

    def receive_msg(self):
        try:
            size, server_address = self.my_socket.recvfrom(5)
            data, server_address = self.my_socket.recvfrom(int(size))
            return data.decode() , server_address
        except OSError as e:
            print(e)
            return FINISH, None

    def close_com(self):
        self.my_socket.close()


def format_msg(msg):
    header = str(len(msg))
    header = header.zfill(5)
    return header.encode(), msg.encode()


def main():
    pass


if __name__ == '__main__':
    main()
