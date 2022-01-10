#!/usr/bin/python3
import os, sys

def get_root(path) -> str:
    tmp = path
    if '/' in tmp:
        return tmp[:tmp.index('/')]
    return tmp


def list_file(basic, path, include):
    path += '/'
    if not os.path.exists(path):
        return

    for file in os.listdir(path):
        if os.path.isdir(path + file):
            root = (path + file).replace(basic, '')
            root = get_root(root)
            if root not in include:
                continue
            list_file(basic, path + file, include)
        elif ".py" in file:
            done = (path + file).replace(basic, '')
            print(done)


def cleanPath(path) -> str:
    tmp = path[::-1]
    index = 0
    for i in range(len(tmp)):
        if tmp[i] != '/':
            index = i
            break
    tmp = tmp[i:]
    return tmp[::-1]


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    path = sys.argv[2].replace('//', '')
    basic = sys.argv[1].replace('//', '')
    if not os.path.exists(path):
        sys.exit(1)
    if not os.path.exists(basic):
        sys.exit(1)
    include = ''
    if len(sys.argv) >= 3:
        include = sys.argv[3].replace('\'', '').split(',')
    path = cleanPath(os.path.join(path))
    basic = cleanPath(os.path.join(basic)) + '/'

    list_file(basic, path, include)
