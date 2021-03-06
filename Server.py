import glob
import os
import queue
import socket
import sys
import threading
import time
import wave
from pathlib import Path

import pyaudio

import database
from Consts import *
from YoutubeDownloader import YoutubeDownloader


class Server(object):
    def __init__(self, ip, port, stream_port):
        try:
            server_socket_streaming = socket.socket(socket.AF_INET,
                                                    socket.SOCK_DGRAM)
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket_streaming.bind((ip, stream_port))
            server_socket.bind((ip, port))
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.server_socket_streaming = server_socket_streaming
        self.server_socket = server_socket
        self.client_address = ()
        self.client_streaming_address = ()
        self.db = database.ConnectionDatabase()
        self.pause = False
        self.skip_q = queue.Queue()

    def choose_action(self, action, params, event):
        """
        chooses the correct function to call according
        to the actions dictionary
        checks if the parameters are correct
        """
        if REQ_AND_PARAMS.get(action) != len(params):
            print("invalid request")
            self.send_message(INVALID_REQ)
            return
        if action == STREAM_ACTION:
            path = choose_song(params[0])
            self.stream_song(path, event)
        elif action == LOGIN_ACTION:
            self.login_check(params[0], params[1])
        elif action == ADD_ACTION:
            self.add_check(params[0], params[1])
        elif action == DOWNLOAD_ACTION:
            self.download_song(params[0])
        elif action == PAUSE_ACTION:
            self.pause = True
            event.clear()
        elif action == UN_PAUSE_ACTION:
            self.pause = False
            event.set()
        elif action == FORWARD_ACTION:
            self.skip_q.put(FORWARD_ACTION)
        elif action == BACKWARD_ACTION:
            self.skip_q.put(BACKWARD_ACTION)
        elif action == STOP:
            self.skip_q.put(STOP)
        elif action == CREATE_PL_ACTION:
            self.create_new_pl(params)
        elif action == GET_ALL_SONGS:
            self.get_all_songs()
        elif action == GET_ALL_PLS_OF_USER:
            self.get_all_pls_of_user(params[0])
        elif action == GET_SONGS_IN_PL:
            self.get_all_songs_in_pl(params[0])
        elif action == REMOVE_SONG_FROM_PL:
            self.remove_song_from_pl(params[0], params[1])
        elif action == ADD_SONG_TO_PL:
            self.add_song_to_pl(params[0], params[1])
        elif action == UNLINK_PLAYLIST:
            self.delete_pl(params[0], params[1])

    def remove_song_from_pl(self, song, pl):
        """
        removes a song from a playlist
        """
        to_send = self.db.remove_song_from_pl(song, pl)
        if not to_send:
            to_send = SUCCESS
        self.send_message(to_send)

    def add_song_to_pl(self, song, pl):
        """
        adds a song to a playlist
        """
        to_send = self.db.add_song_to_pl(song, pl)
        if not to_send:
            to_send = SUCCESS
        self.send_message(to_send)

    def delete_pl(self, user, playlist):
        """
        deleted a playlist
        """
        to_send = self.db.unlink_user_to_pl(user, playlist)
        if to_send is None:
            self.send_message(ERROR)
        # to_send = self.db.delete_pl(playlist)
        # if to_send is None:
        #     self.send_message(ERROR)
        self.send_message(SUCCESS)

    def get_all_songs(self):
        """
        gets all songs in the database
        """
        to_send = self.db.get_all_songs()
        to_send = '$'.join(to_send)
        self.send_message(to_send)

    def get_all_pls_of_user(self, username):
        """
        gets all playlists of a certain user
        """
        to_send = self.db.get_all_pls_of_user(username)
        to_send = DOLLAR.join(to_send)
        print(to_send)
        self.send_message(to_send)

    def get_all_songs_in_pl(self, playlist):
        """
        gets a ll songs in a certain playlist
        """
        to_send = self.db.get_songs(playlist)
        to_send = DOLLAR.join(to_send)
        self.send_message(to_send)

    def create_new_pl(self, params):
        """
        creates a new playlist with the given songs
        and links it the the given user
        """
        name = params[ONE]
        user = params[ZERO]
        songs = params[2].split('&')
        msg = self.db.create_new_pl(songs, name, user)
        self.send_message(msg)

    def download_song(self, song):
        """
        downloads a song
        """
        song = song.replace(UNDERSCORE, SPACE)
        downloader = YoutubeDownloader(song)
        msg = downloader.download()
        if msg == SUCCESS:
            self.db.add_new_song(song)
        self.send_message(msg)

    def update_db(self):
        """
        makes sure the database holds only all the songs
        that are saved on the server
        """
        songs = self.db.get_all_songs()
        for song in songs:
            if choose_song(song) == ERROR:
                self.db.delete_song(song)
        files = []
        for song in glob.glob("songs\*.wav"):
            to_append = song.split('\\')[ONE][:-4]
            files.append(to_append)
        for song in files:
            if song not in songs:
                self.db.add_new_song(song)

    def stream_song(self, path, e):
        """
        sends the data from a song file chosen by the pick song method
        manages skips and pauses
        """
        if path == ERROR:
            self.send_streaming_message(INVALID_REQ)
            return
        # sends metadata
        sample_rate, channels, my_format = get_metadata(path)
        to_send = sample_rate + DOLLAR + channels + DOLLAR + my_format
        skip_amount = get_byte_num(path)
        print('to send', to_send)

        # sends a chunk each iteration of the loop
        self.send_streaming_message(to_send)
        with open(path, 'rb') as song:
            data = song.read(MSG_SIZE)
            self.send_streaming_message(data)
            while data != EMPTY_MSG:
                data = song.read(MSG_SIZE)

                # if the user wanted to pause the function will raise
                # a thread event and stop until instructed to continue
                # from outside the thread
                if self.pause:
                    e.wait()

                # checks if the song should stop playing/ go backwards/forwards
                if not self.skip_q.empty():
                    msg = self.skip_q.get()
                    if msg == FORWARD_ACTION:
                        song.read(int(skip_amount))
                    elif msg == BACKWARD_ACTION:
                        song.seek(-1 * int(skip_amount), ONE)
                    elif msg == STOP:
                        self.send_streaming_message(FINISH)
                        return
                # sends the chunk and pauses
                self.send_streaming_message(data)
                time.sleep(MSG_SIZE * NO_LAG_MOD / int(sample_rate))
            self.send_streaming_message(FINISH)

    def login_check(self, username, password):
        """
        checks if the username and password are correct
        """
        can_login, msg = self.db.check_login(username, password)
        self.send_message(str(can_login) + DOLLAR + msg)

    def add_check(self, username, password):
        """
        adds a new user
        """
        can_login, msg = self.db.add_user(username, password)
        self.send_message(str(can_login) + DOLLAR + msg)

    def receive_streaming_msg(self):
        """
        receives a message from the client on the streaming socket
        """
        size, client_streaming_address = self.server_socket_streaming.recvfrom(
            HEADER_SIZE)
        data, client_streaming_address = self.server_socket_streaming.recvfrom(
            int(size))
        data = data.decode()
        data = data.split(DOLLAR)
        self.client_streaming_address = client_streaming_address
        return data

    def send_streaming_message(self, data):
        """
        sends a message to the client on the streaming socket
        """
        header, data = format_msg(data)
        self.server_socket_streaming.sendto(header,
                                            self.client_streaming_address)
        self.server_socket_streaming.sendto(data,
                                            self.client_streaming_address)

    def receive_msg(self):
        """
        receives a message from the client on the regular socket
        """
        size, client_address = self.server_socket.recvfrom(HEADER_SIZE)
        data, client_address = self.server_socket.recvfrom(int(size))
        data = data.decode()
        data = data.split(DOLLAR)
        self.client_address = client_address
        return data

    def send_message(self, data):
        """
        sends a message to the client on the regular socket
        """
        header, data = format_msg(data)
        self.server_socket.sendto(header, self.client_address)
        self.server_socket.sendto(data, self.client_address)

    def handle_client(self):
        """
        calls the handle methods for both sockets
        """
        e = threading.Event()
        reg_t = threading.Thread(target=self.handle_reg_client, args=(e,))
        stream_t = threading.Thread(target=self.handle_stream_client,
                                    args=(e,))
        reg_t.start()
        stream_t.start()

    def handle_reg_client(self, event):
        """
        handles the regular socket
        """
        try:
            while True:
                client_req = self.receive_msg()
                self.choose_action(client_req[ZERO], client_req[ONE:], event)
        except socket.error as e:
            print(e)

    def handle_stream_client(self, event):
        """
        handles the streaming socket
        """
        try:
            while True:
                client_req = self.receive_streaming_msg()
                self.choose_action(client_req[ZERO], client_req[ONE:], event)
        except socket.error as e:
            print('stream', e)


def song_check(song):
    """
    checks if a song is valid
    """
    msg = choose_song(song)
    return msg != ERROR


def get_byte_num(path):
    """
    gets the number of bytes that represent 10 seconds in the song
    """
    sample, channels, my_format = get_metadata(path)
    return (int(sample) * int(my_format) * int(channels) * 15) / 8


def choose_song(my_name):
    """
    chooses the file of the requested song and checks if its valid
    """
    my_name = my_name.split(ET)[ZERO]
    path = ''
    for filename in os.listdir(str(Path.cwd()) + '/songs'):
        name = filename.split('\\')[-1]
        name = name.split('.')[ZERO]
        name = name.split(ET)[ZERO]
        if filename.endswith(".wav") and my_name == name:
            path = str(Path.cwd()) + r'\songs\%s' % filename
    if os.path.exists(path):
        return path
    else:
        return ERROR


def get_metadata(my_path):
    """
    gets the metadata of the requested file
    """
    with wave.open(my_path, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        my_format = pyaudio.get_format_from_width(wave_file.getsampwidth())
    return str(frame_rate), str(channels), str(my_format)


def format_msg(msg):
    """
    encodes the message and returns its length and the message
    """
    if type(msg) == str:
        msg = msg.encode()
    header = str(len(msg))
    header = header.zfill(HEADER_SIZE)
    return header.encode(), msg


def main():
    server = Server(IP, PORT, STREAM_PORT)
    server.update_db()
    server.handle_client()


if __name__ == '__main__':
    main()
