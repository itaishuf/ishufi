# -*- coding: utf-8 -*-
import os
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from Consts import *


class YoutubeDownloader(object):
    def __init__(self, name):
        self.name = name.replace(SPACE, UNDERSCORE)
        self.old_path = ''
        self.temp_path = ''
        self.new_path = ''
        self.set_paths()

    def ur_lib(self):
        """
        sends an http request to youtube to get the url for wanted song
        """
        query_string = urllib.parse.urlencode({"search_query": self.name})
        html_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string)
        full_query = r'href=\"\/watch\?v=(.{11})'
        search_results = re.findall(full_query, html_content.read().decode())
        top_result = search_results[ZERO]
        return top_result

    def dl(self, url):
        """
        downloads the wanted url using youtube dl
        """
        command = 'youtube-dl -i -f mp4 -o %s.mp4 %s' % (self.name, url)
        subprocess.call(command)

    def set_paths(self):
        """
        sets the path to save the song on the correct folder
        """
        cwd = str(os.getcwd()) + '\\'
        self.old_path = cwd + self.name + '.mp4'
        self.temp_path = cwd + 'songs\\' + self.name + '.mp4'
        self.new_path = cwd + 'songs\\' + self.name + '.wav'

    def move_dir(self):
        """
        moves the song to the correct folder and sets the format to wav
        """
        print("moving")
        os.rename(self.old_path, self.temp_path)
        command = r'ffmpeg -i %s %s' % (self.temp_path, self.new_path)
        subprocess.call(command)
        os.remove(self.temp_path)

    def check_if_exists(self):
        for filename in os.listdir(str(Path.cwd()) + '/songs'):
            if filename in self.new_path:
                return True
        return False

    def download(self):
        """
        downloads a song
        """
        try:
            if self.check_if_exists():
                return SUCCESS
            url = self.ur_lib()
            print(url, self.name)
            self.dl(url)
            self.move_dir()
            return SUCCESS
        except Exception as msg:
            print(msg)
            return ERROR
