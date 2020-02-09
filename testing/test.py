# -*- coding: utf-8 -*-
import scipy.io.wavfile as sio
from tinytag import TinyTag


def main():
    my_path = r'c:\ishufi\whiplash_hank_levy.mp4'
    tag = TinyTag.get(my_path)
    print(tag.samplerate, tag.bitrate)

if __name__ == '__main__':
    main()
