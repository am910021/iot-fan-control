VERSION = '0.1_Alpha'
SERVER_NAME = "Yuri's_Http_Server(yHttpd)"


def get_relative_path(http_request):
    path = http_request['path']
    prefix = http_request['prefix']
    return path[len(prefix):]


def dict_update(a: dict, b: dict):
    a.update(b)
    return a


class NotFoundException(Exception):
    pass


class BadRequestException(Exception):
    pass


class ForbiddenException(Exception):
    pass
