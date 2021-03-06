# -*- coding: utf-8 -*-
import queue
import socket
import threading
import time

import pyaudio

from Consts import *


class Client(object):
    def __init__(self):
        self.my_socket_streaming = socket.socket(socket.AF_INET,
                                                 socket.SOCK_DGRAM)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_stream_address = (IP, STREAM_PORT)
        self.server_address = (IP, PORT)
        self.p = pyaudio.PyAudio()
        self.song_q = queue.Queue()
        self.play_next_song = False
        self.paused = False
        self.song_playing = ''
        self.current_user = ''

        self.song_stack = []
        queue_t = threading.Thread(target=self.check_q)
        queue_t.start()

    def play(self):
        """
        plays the data from the server
        :return:
        """
        # gets the metadata from the server
        metadata, server_address = self.receive_streaming_msg()
        if metadata == INVALID_REQ.encode():
            return INVALID_REQ
        metadata = metadata.decode().split(DOLLAR)
        sample_rate = int(metadata[ZERO])
        channels = int(metadata[ONE])
        my_format = int(metadata[2])

        # starts getting song data from the server and initializes the stream
        new_data, server_address = self.receive_streaming_msg()
        stream = self.p.open(format=my_format, channels=channels,
                             rate=sample_rate,
                             output=True, frames_per_buffer=(MSG_SIZE / 2))
        start = time.time()
        # loop that gets new data from the server and wries it to the stream
        while new_data != FINISH:
            if new_data is not None:
                stream.write(new_data)
            try:
                new_data, server_address = self.receive_streaming_msg()
            except socket.error as e:
                print(e)
        # checks the time it took to play the song, used to check
        # if the stream is too fast or too slow
        end = time.time()
        my_time = end - start
        stream.close()
        return str(my_time)

    def download_song(self, song):
        """
        sends message to download a new song and returns the answer
        """
        to_send = DOWNLOAD_ACTION + DOLLAR + song
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        data = data[ZERO]
        if data == INVALID_REQ:
            return False, "didn't enter song"
        elif data == SUCCESS:
            return True, SUCCESS
        else:
            return False, ERROR

    def create_playlist(self, songs, playlist):
        """
        creates playlist and links the current user to it
        """
        to_send = CREATE_PL_ACTION + DOLLAR + self.current_user + DOLLAR + \
                  playlist + DOLLAR + '&'.join(songs)
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def delete_pl(self, playlist):
        """
        unlinks a playlist from this user
        """
        to_send = UNLINK_PLAYLIST + DOLLAR + self.current_user + DOLLAR + playlist
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def get_all_songs(self):
        """
        gets a list of all songs on the server
        """
        self.send_message(GET_ALL_SONGS)
        data, server_address = self.receive_msg()
        return data

    def get_songs_in_pl(self, playlist):
        """
        gets list of all songs in a certain playlist
        """
        to_send = GET_SONGS_IN_PL + DOLLAR + playlist
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def get_all_pls_of_user(self):
        """
        gets a list of all playlists linked to this user
        """
        to_send = GET_ALL_PLS_OF_USER + DOLLAR + self.current_user
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def remove_song_from_pl(self, song, pl):
        """
        removes a song from a playlist
        """
        to_send = REMOVE_SONG_FROM_PL + DOLLAR + song + DOLLAR + pl
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def add_song_to_pl(self, song, pl):
        """
        adds a song to a playlist
        """
        to_send = ADD_SONG_TO_PL + DOLLAR + song + DOLLAR + pl
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        return data

    def pause(self):
        """
        pauses the current song
        """
        self.send_message(PAUSE_ACTION)

    def un_pause(self):
        """
        resumes the current song
        """
        self.send_message(UN_PAUSE_ACTION)

    def forward(self):
        """
        skips 10 seconds int eh current song
        """
        self.send_message(FORWARD_ACTION)

    def backward(self):
        """
        goes 10 seconds back in the current song
        """
        self.send_message(BACKWARD_ACTION)

    def play_song_thread(self, lst):
        """
        threaded function that calls the stream song method,
        lowest level wrapper to the actual stream function
        """
        song = lst[ZERO]
        q = lst[ONE]
        # checks whether the current song that is playing is the same as one
        # that is requested
        # so a song wont be played from the beginning while it is playing
        if self.song_playing == song:
            # pauses/resumes the song according to its current status
            if not self.paused:
                self.paused = True
                self.pause()
                return
            else:
                self.paused = False
                self.un_pause()
                return
        elif self.song_playing != "":
            # stops the current playing song to play a different song
            # without causing issues
            self.send_message(STOP)
            time.sleep(0.4)
        self.song_playing = song
        # tells the server to start streaming and starts listening for data
        # in the client
        to_send = STREAM_ACTION + DOLLAR + song
        self.send_streaming_message(to_send)
        msg = self.play()
        # pushes a msg to the ui if the song that was requested isn't valid
        if msg == INVALID_REQ:
            q.put(INVALID_REQ)
        self.song_playing = ''
        time.sleep(0.5)
        if self.song_playing == '':
            self.play_next_song = True

    def play_song_top(self, name):
        """
        calls the thread function to stream a song
        """
        self.play_next_song = False
        self.song_stack.append(name)
        return_queue = queue.Queue()
        t_play = threading.Thread(target=self.play_song_thread,
                                  args=((name, return_queue),))
        t_play.start()
        time.sleep(0.1)
        if return_queue.empty():
            return None
        if return_queue.get() == INVALID_REQ:
            return "song doesnt exist"

    def check_q(self):
        """
        checks if a new song was added to the playing queue, plays it if no
        songs are currently playing
        """
        time.sleep(2)
        while True:
            next_song = self.song_q.get()
            if next_song != '':
                while not self.play_next_song:
                    time.sleep(ONE)
                time.sleep(ONE)
                if self.play_next_song:
                    self.play_song_top(next_song)
                    self.play_next_song = False
            time.sleep(ONE)

    def login(self, username, password):
        """
        checks if the username and password that the user submitted are correct
        """
        to_send = LOGIN_ACTION + DOLLAR + username + DOLLAR + password
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
        can_login = eval(data[ZERO])
        msg = " ".join(data[ONE:])
        return can_login, msg

    def add_user(self, username, password):
        """
        adds a new user and returns a message to the gui if it was successful
        """
        to_send = ADD_ACTION + DOLLAR + username + DOLLAR + password
        self.send_message(to_send)
        data, server_address = self.receive_msg()
        can_login = eval(data[ZERO])
        msg = SPACE.join(data[ONE:])
        if data == INVALID_REQ:
            return False, "didn't enter username or password"
        return can_login, msg

    def send_message(self, data):
        """
        sends a message to the server on the regular socket
        """
        header, data = format_msg(data)
        self.my_socket.sendto(header, self.server_address)
        self.my_socket.sendto(data, self.server_address)

    def receive_msg(self):
        """
        receives a message from the server on the regular socket
        """
        try:
            size, server_address = self.my_socket.recvfrom(HEADER_SIZE)
            data, server_address = self.my_socket.recvfrom(int(size))
            data = data.decode()
            data = data.split(DOLLAR)
            return data, server_address
        except OSError as e:
            print(e)
            return FINISH, None

    def send_streaming_message(self, data):
        """
        sends a message to the server on the streaming socket
        """
        header, data = format_msg(data)
        self.my_socket_streaming.sendto(header, self.server_stream_address)
        self.my_socket_streaming.sendto(data, self.server_stream_address)

    def receive_streaming_msg(self):
        """
        receives a message from the server on the streaming socket
        """
        try:
            size, server_address = self.my_socket_streaming.recvfrom(HEADER_SIZE)
            data, server_address = self.my_socket_streaming.recvfrom(int(size))
            return data, server_address
        except OSError as e:
            print(e)
            return FINISH, None

    def close_com(self):
        """
        closes both sockets to stop communication with the server
        """
        self.my_socket_streaming.close()
        self.my_socket.close()


def format_msg(msg):
    """
    encodes the message and returns its length and the message
    """
    if type(msg) == str:
        msg = msg.encode()
    header = str(len(msg))
    header = header.zfill(HEADER_SIZE)
    return header.encode(), msg
