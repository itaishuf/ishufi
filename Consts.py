MSG_SIZE = 8192
NO_LAG_MOD = 0.24095
HEADER_SIZE = 5
IP = "127.0.0.1"
PORT = 8820
STREAM_PORT = 8824
FINISH = b"finish"
EMPTY_MSG = b''

STREAM_ACTION = "STREAM"
EXIT_ACTION = "EXIT"
LOGIN_ACTION = "LOGIN"
ADD_ACTION = "ADDUSER"
REMOVE_ACTION = "REMOVE"
PAUSE_ACTION = "PAUSE"
UN_PAUSE_ACTION = 'UNPAUSE'
FORWARD_ACTION = 'FORWARD'
BACKWARD_ACTION = 'BACKWARD'
DOWNLOAD_ACTION = "DOWNLOAD"
CREATE_PL_ACTION = "CREATEPL"
GET_ALL_SONGS = "GETALLSONGS"
GET_ALL_PLS_OF_USER = "GETALLPLAYLISTSUSER"
GET_SONGS_IN_PL = "GETSONGSINPL"
REMOVE_SONG_FROM_PL = "REMOVESONGFROMPL"
ADD_SONG_TO_PL = "ADDSONGTOPL"
UNLINK_PLAYLIST = "UNLINKPL"

INVALID_REQ = "invalid"
SUCCESS = "Success"
STOP = 'STOP'
DONE = "done"
ERROR = "ERROR"

REQ_AND_PARAMS = {STREAM_ACTION: 1,
                  LOGIN_ACTION: 2,
                  EXIT_ACTION: 1,
                  ADD_ACTION: 2,
                  DOWNLOAD_ACTION: 1,
                  PAUSE_ACTION: 0,
                  UN_PAUSE_ACTION: 0,
                  FORWARD_ACTION: 0,
                  BACKWARD_ACTION: 0,
                  STOP: 0,
                  CREATE_PL_ACTION: 3,
                  GET_ALL_SONGS: 0,
                  GET_ALL_PLS_OF_USER: 1,
                  GET_SONGS_IN_PL: 1,
                  ADD_SONG_TO_PL: 2,
                  REMOVE_SONG_FROM_PL: 2,
                  UNLINK_PLAYLIST: 2}


WHITE = "#ffffff"
PURPLE = "#8A23F1"
GREEN = "#ccffea"
BIG = '600x450'
SMALL = '300x225'


"""
features
ui יפה + images
help page
better choose action


bugs
cant play after download
cant do anything while downloading
songs playing too fast/slow
"""