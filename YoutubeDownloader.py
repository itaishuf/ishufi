# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import wave
import os
import subprocess
from Consts import *


class YoutubeDownloader(object):
    def __init__(self, name):
        self.name = name.replace(' ', '_')
        self.old_path = r'c:\branch\ishufi\%s.mp4' % self.name
        self.temp_path = r'c:\branch\ishufi\songs\%s.mp4' % self.name
        self.new_path = r'c:\branch\ishufi\songs\%s.wav' % self.name

    def ur_lib(self):
        query_string = urllib.parse.urlencode({"search_query": self.name})
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

    def dl(self, url):
        command = 'youtube-dl -i -f mp4 -o %s.mp4 %s' % (self.name, url)
        print(command)
        subprocess.call(command)

    def move_to_dir(self):
        print("moving")
        os.rename(self.old_path, self.temp_path)
        command = r'ffmpeg -i %s c:\branch\ishufi\songs\%s.wav' % (self.temp_path, self.name)
        subprocess.call(command)
        os.remove(self.temp_path)

    def download(self):
        try:
            url = self.ur_lib()
            self.dl(url[0])
            self.move_to_dir()
            return SUCCESS
        except Exception as msg:
            print(msg)
            return ERROR


def main():
    pass


if __name__ == '__main__':
    main()
