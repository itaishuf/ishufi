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
        self.name = name
        self.old_path = ''
        self.temp_path = ''
        self.new_path = ''

    def ur_lib(self):
        query_string = urllib.parse.urlencode({"search_query": self.name})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        top_result = search_results[0]
        return top_result

    def dl(self, url):
        command = 'youtube-dl -i -f mp4 -o %s.mp4 %s' % (self.name, url)
        subprocess.call(command)

    def set_paths(self):
        self.old_path = r'c:\branch\ishufi\%s.mp4' % self.name
        self.temp_path = r'c:\branch\ishufi\songs\%s.mp4' % self.name
        self.new_path = r'c:\branch\ishufi\songs\%s.wav' % self.name

    def move_to_dir(self):
        print("moving")
        os.rename(self.old_path, self.temp_path)
        command = r'ffmpeg -i %s c:\branch\ishufi\songs\%s.wav' % (self.temp_path, self.name)
        subprocess.call(command)
        os.remove(self.temp_path)

    def download(self):
        try:
            url = self.ur_lib()
            self.name = self.name.replace(' ', '_')
            self.set_paths()
            self.dl(url)
            self.move_to_dir()
            return SUCCESS
        except Exception as msg:
            print(msg)
            return ERROR


def main():
    pass


if __name__ == '__main__':
    main()
