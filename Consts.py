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
ADD_ACTION = "ADD"
REMOVE_ACTION = "REMOVE"
PAUSE_ACTION = "PAUSE"
UN_PAUSE_ACTION = 'UNPAUSE'
FORWARD_ACTION = 'FORWARD'
BACKWARD_ACTION = 'BACKWARD'
DOWNLOAD_ACTION = "DOWNLOAD"
CREATE_PLAYLIST_ACTION = "CREATE"
GET_ALL_SONGS = "GETALLSONGS"
GET_ALL_PLAYLISTS_OF_USER = "GETALLPLAYLISTSUSER"

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
                  CREATE_PLAYLIST_ACTION: 3,
                  GET_ALL_SONGS: 0,
                  GET_ALL_PLAYLISTS_OF_USER: 1}


BLUE = "#ccffea"
WHITE = "#ffffff"
PURPLE = "#8A23F1"
GREEN = "#ccffea"
BIG = '600x450'
SMALL = '300x225'


"""
features
עברית
הצפנה לסיסמאות
ui יפה
shuffle
playlists




bugs
cant play after download
cant do anything while downloading
msg send on a datagram was larger then the internal msg buffer or some other network limit- happens randomly
songs playing too fast/slow



code
simplify and document uses of constants
documentation
better choose action
more efficient socket action messages
"""