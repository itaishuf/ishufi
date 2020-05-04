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

HELP_STRINGS = {"Log In": "Opens the app if the user credentials are correct",
                "Register": "Creates a new user and opens the app",
                "Quit": "exits the app",
                "pyimage2": "press this button start playing, to pause a song"
                            " or to resume",
                "pyimage3": "press this button start playing, to pause a song"
                            " or to resume",
                "pyimage4": "skips forward to the next song in queue",
                "pyimage5": "plays again the last played song",
                "backward 10s": "goes backwards 10 seconds in the"
                                " current playing song",
                "forward 10s": "goes forward 10 seconds in the"
                               " current playing song",
                "Add to queue": "adds the typed song to the queue",
                "Download": "downloads the typed song to the server",
                "Manage playlists": "opens the playlist manager window",
                "quit": "quits the app",
                "delete playlist": "deletes the chosen playlist",
                "remove song from playlist": "choose a song and a playlist,"
                                             " then press this button"
                                             " to remove the song from"
                                             " the playlist",
                "add song to playlist": "choose a song and a playlist,"
                                        " then press this button to add"
                                        " the song to the playlist",
                "play playlist": "play the chosen playlist",
                "view all downloaded songs": "",
                "create playlist": "choose songs from the box above, "
                                   "enter a name for the new playlist,"
                                   " then press this to create a new playlist"}


WHITE = "#ffffff"
PURPLE = "#8A23F1"
LIGHT_PURPLE = "#B577F4"
LIGHT_BLUE = "#aae1d9"
LIGHT_LIGHT_BLUE = "#d0f3ee"
BIG = '600x450'
SMALL = '300x225'
TITLE = "Ishufi"
TEXT = "text"
RIGHT_CLICK = "<Button-3>"
ZERO = 0
ONE = 1
UNDERSCORE = '_'
SPACE = " "
END = 'end'
IMAGE = "image"
PLAY = "play"
PAUSE = "pause"
ET = '@'
DOLLAR = '$'
DOESNT_EXIST = "song doesnt exist"
