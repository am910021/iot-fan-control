VERSION = '0.1 Alpha'
SERVER_NAME = "Yuri's Http Server"


def get_relative_path(http_request):
    path = http_request['path']
    prefix = http_request['prefix']
    return path[len(prefix):]


class NotFoundException(Exception):
    pass


class BadRequestException(Exception):
    pass


class ForbiddenException(Exception):
    pass