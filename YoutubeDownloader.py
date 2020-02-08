# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import youtube_dl
import os
import time
import wave
from pathlib import Path
DONE = "done"
ERROR = "ERROR"


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
    filename = str(Path.cwd()) + "\\" + name + ".wav"
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'ffmpeg_location': 'C:\FFmpeg\\bin',
        'outtmpl': filename,
        'postprocessors': [{

            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def move_to_dir(name):
    time.sleep(0.1)
    path = str(Path.cwd())
    path += '\songs\\'
    path += name
    path += ".wav"
    if os.path.exists(path):
        return "already exists"
    else:
        os.replace((str(Path.cwd())+'\\'+name+".wav"), path)


def download_song(name):
    try:
        url = urlib(name)
        dl(url[0], name)
        move_to_dir(name)
        return DONE
    except Exception as msg:
        print(msg)
        return ERROR



def main():
    my_str = "clash royale"
    download_song(my_str)

if __name__ == '__main__':
    main()
