MSG_SIZE = 8192
NO_LAG_MOD = 0.24095
HEADER_SIZE = 5
IP = "127.0.0.1"
PORT = 8820
STREAM_PORT = 8824
PATH = r"C:\ishufi\songs\abc.wav"
FINISH = b"finish"
EMPTY_MSG = b''
STREAM_ACTION = "STREAM"
EXIT_ACTION = "EXIT"
LOGIN_ACTION = "LOGIN"
ADD_ACTION = "ADD"
PAUSE_ACTION = "PAUSE"
UN_PAUSE_ACTION = 'UNPAUSE'
FORWARD_ACTION = 'FORWARD'
BACKWARD_ACTION = 'BACKWARD'
INVALID_REQ = "invalid"
SUCCESS = "Success"
STOP = 'STOP'
DOWNLOAD_ACTION = "DOWNLOAD"
REQ_AND_PARAMS = {STREAM_ACTION: 1,
                  LOGIN_ACTION: 2,
                  EXIT_ACTION: 1,
                  ADD_ACTION: 2,
                  DOWNLOAD_ACTION: 1,
                  PAUSE_ACTION: 0,
                  UN_PAUSE_ACTION: 0,
                  FORWARD_ACTION: 0,
                  BACKWARD_ACTION: 0,
                  STOP: 0}

DONE = "done"
ERROR = "ERROR"
BLUE = "#ccffea"
WHITE = "#ffffff"
PURPLE = "#8A23F1"
GREEN = "#ccffea"




"""
עברית
הצפנה לסיסמאות
תור
ui יפה

bugs

cant play after download
cant do anything while downloading
msg send on a datagream was larger then the internal msg buffer or some other network limit- happens randomly
"""