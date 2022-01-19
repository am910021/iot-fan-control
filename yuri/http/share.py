import os

VERSION = '0.1_Alpha'
SERVER_NAME = "Yuri's_Http_Server(yHttpd)"
BUFFER_SIZE = 256


def is_dir(path):
    try:
        os.listdir(path)
        return True
    except OSError:
        return False


def exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def get_relative_path(http_request):
    return http_request['path'][len(http_request['prefix']):]


def dict_update(a: dict, b: dict):
    a.update(b)
    return a


def count_write(buff):
    return len(buff), buff


class NotFoundException(Exception):
    pass


class BadRequestException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class BufferOverflowException(Exception):
    pass
