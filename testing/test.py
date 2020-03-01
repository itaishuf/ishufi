# -*- coding: utf-8 -*-
import time
import threading


def foo(e):
    while True:
        e.wait()
        print('un pause')
        e.clear()


def main():
    e = threading.Event()
    t = threading.Thread(target=foo, args=(e,))
    t.start()
    while True:
        time.sleep(3)
        e.set()



if __name__ == '__main__':
    main()
