# -*- coding: utf-8 -*-
import os
import re
import subprocess
import urllib.parse
import urllib.request

from Consts import *


class YoutubeDownloader(object):
    def __init__(self, name):
        self.name = name.replace(' ', '_')
        self.old_path = ''
        self.temp_path = ''
        self.new_path = ''
        self.set_paths()

    def ur_lib(self):
        query_string = urllib.parse.urlencode({"search_query": self.name})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        full_query = r'href=\"\/watch\?v=(.{11})'
        search_results = re.findall(full_query, html_content.read().decode())
        top_result = search_results[0]
        return top_result

    def dl(self, url):
        command = 'youtube-dl -i -f mp4 -o %s.mp4 %s' % (self.name, url)
        subprocess.call(command)

    def set_paths(self):
        cwd = str(os.getcwd()) + '\\'
        self.old_path = cwd + self.name + '.mp4'  # c:\ishufi\%s.mp4
        self.temp_path = cwd + 'songs\\' + self.name + '.mp4'  # c:\ishufi\songs\%s.mp4'
        self.new_path = cwd + 'songs\\' + self.name + '.wav'  # r'c:\ishufi\songs\%s.wav'

    def move_dir(self):
        print("moving")
        os.rename(self.old_path, self.temp_path)
        command = r'ffmpeg -i %s %s' % (self.temp_path, self.new_path)
        subprocess.call(command)
        os.remove(self.temp_path)

    def download(self):
        try:
            url = self.ur_lib()
            self.dl(url)
            self.move_dir()
            return SUCCESS
        except Exception as msg:
            print(msg)
            return ERROR
