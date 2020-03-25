# -*- coding: utf-8 -*-
import time
import threading


def foo(e):
    while True:
        e.wait()
        print('un pause')
        e.clear()


def main():
    for i in range(1, 17):
        print('song$'+ str(i) + ',', end=" ")



if __name__ == '__main__':
    main()
