import miniaudio
PATH = r"C:\Project\test_song.mp3"


def main():
    with open(PATH, 'rb') as song:
        data = song.read()
        a = miniaudio.mp3_get_info(data)
        data_lst = miniaudio.mp3_read_f32(data)
        print(a.duration)
        data = data[:]
        stream = miniaudio.stream_memory(data)
        device = miniaudio.PlaybackDevice()
        device.start(stream)
        input("press any key to stop")
        device.close()


if __name__ == '__main__':
    main()
