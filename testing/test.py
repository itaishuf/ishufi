# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re



def main():
    query_string = urllib.parse.urlencode({"search_query" : input()})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall('href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("http://www.youtube.com/watch?v=" + search_results[0])



if __name__ == '__main__':
    main()
