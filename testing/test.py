# -*- coding: utf-8 -*-
import pathlib

def main():
    print(pathlib.Path.cwd())
    print(pathlib.Path(__file__).resolve())



if __name__ == '__main__':
    main()
