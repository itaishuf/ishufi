# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import youtube_dl
from tinytag import TinyTag
import time
import os
import subprocess
from pathlib import Path
DONE = "done"
ERROR = "ERROR"
SUCCESS = "Success"


def urlib(name):
    query_string = urllib.parse.urlencode({"search_query": name})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    top_results = []
    i = 0
    for item in search_results:
        if i >= 3:
            break
        top_results.append("http://www.youtube.com/watch?v=" + item)
        i += 1
    return top_results


def dl(url, name):
    filename = str(Path.cwd()) + "\\" + name + '.mp4'
    print(filename)
    ydl_opts = {"outtmpl": filename}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def move_to_dir(name, bit_rate, sample_rate, channels):
    command = r"c:\ffmpeg\bin\ffmpeg.exe -i C:/ishufi/%s.mp4 -ab %s -ac %s -ar %s -vn songs/%s.wav" % \
              (name, bit_rate, channels, sample_rate, name)
    print(command)
    print(name)
    subprocess.call(command, shell=True)
    time.sleep(0.2)
    os.remove(r"c:/ishufi/%s.mp4" % name)


def get_metadata(name):
    filename = str(Path.cwd()) + "\\" + name + '.mp4'
    tag = TinyTag.get(filename)
    bit_rate = tag.bitrate
    sample_rate = tag.samplerate
    channels = tag.channels
    return bit_rate, sample_rate, channels


def download_song(name):
    try:
        name = name.replace(' ', '_')
        url = urlib(name)
        dl(url[0], name)
        bit_rate, sample_rate, channels = get_metadata(name)
        move_to_dir(name, bit_rate, sample_rate, channels)
        return SUCCESS
    except Exception as msg:
        print(msg)
        return ERROR


def main():
    my_str = "clash royale"
    download_song(my_str)


if __name__ == '__main__':
    main()
