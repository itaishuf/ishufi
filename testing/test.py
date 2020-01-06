# -*- coding: utf-8 -*-


def main():
    str = 'abc'
    str2 = '123'
    print(str+str2)
    with open("sayarot.txt", 'r', encoding='utf-8') as txt:
        with open("flipped.txt", 'r+', encoding='utf-8') as wrt:
            wrt.truncate(0)
            data = txt.read()
            wrt.write(data[::-1])
            wrt.seek(0)
            data = wrt.readlines()
            data = data[::-1]
            wrt.seek(0)
            wrt.truncate(0)
            for line in data:
                wrt.write(line)


if __name__ == '__main__':
    main()
