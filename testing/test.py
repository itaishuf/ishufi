import miniaudio
import queue
import time
PATH = r"C:\Project\test_song.mp3"
MSG_SIZE = 320000
SAMPLE_RATE = 48000
NO_LAG_MOD = 1.98


def prep_q():
    chunk_q = queue.Queue()
    with open(PATH, 'rb') as song:
        data = song.read(MSG_SIZE)
        while data != b'':
            chunk_q.put(data)
            data = song.read(MSG_SIZE)
    return chunk_q


def main():
    chunk_q = prep_q()
    device = miniaudio.PlaybackDevice()
    while not chunk_q.empty():
        stream = miniaudio.stream_memory(chunk_q.get())
        device.start(stream)
        print(MSG_SIZE * NO_LAG_MOD / SAMPLE_RATE)
        time.sleep(MSG_SIZE * NO_LAG_MOD / SAMPLE_RATE)
        device.stop()
    device.close()


if __name__ == '__main__':
    main()
