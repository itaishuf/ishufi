# -*- coding: utf-8 -*-
import scipy.io.wavfile as sio
from pathlib import Path


def get_metadata():
    my_path = "F:\project\ishufi\\testing\\dont kill my vibe kendrick lamar.wav"
    print('my path: ', my_path)
    bit_rate, data = sio.read(my_path)
    channels = 2
    print("here")
    print(bit_rate, channels)


def main():
    get_metadata()


if __name__ == '__main__':
    main()
