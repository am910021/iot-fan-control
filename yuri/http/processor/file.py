import os, gc
from yuri.logger import logger
from yuri.http.share import *

CONTENT_TYPE_MAP = {
    ".html": "text/html",
    ".js": "text/javascript",
    ".css": "text/css"
}


class FileProcess:
    def __init__(self, root_path='/www', block_size=256):
        if not self.exists(root_path) or not self.is_dir(root_path):
            msg = "Root path {} is not an existing directory".format(root_path)
            raise Exception(msg)
        self._root_path = root_path
        self._block_size = BUFFER_SIZE

    #
    # callbacks
    #

    def handle_request(self, http_request):
        #
        # We only support GET
        #
        verb = http_request['verb']
        if verb != 'get':
            raise BadRequestException("Unsupported HTTP verb: {}".format(verb))
        # the relative path is the path on the HTTP request stripped of the
        # prefix used to register the file handler
        relative_path = get_relative_path(http_request)
        # the effective path is the relative path with the root path
        # prefixed, and normalized to remove '.' and '..'
        absolute_path = self.effective_path(relative_path)
        #
        # If the path is forbidden, 403 out
        #
        remote = http_request['remote']
        if not self.is_prefix(self._root_path, absolute_path):
            logger.info("FORBIDDEN {} {}".format(remote, absolute_path))
            raise ForbiddenException(absolute_path)
        #
        # If the path doesn't exist, 404 out
        #
        if not self.exists(absolute_path):
            logger.info("NOT_FOUND {} {}".format(remote, absolute_path))
            raise NotFoundException(absolute_path)
        #
        # Otherwise, generate a file listing or a file
        #
        if self.is_dir(absolute_path):
            index_path = absolute_path + "/index.html"
            if self.exists(index_path):
                logger.info("ACCESS {} {}".format(remote, index_path))
                return self.create_file_response(index_path)
            else:
                logger.info("ACCESS {} {}".format(remote, absolute_path))
                prefix = http_request['prefix']
                return self.create_dir_listing_response(absolute_path)
        else:
            logger.info("ACCESS {} {}".format(remote, absolute_path))
            return self.create_file_response(absolute_path)

    #
    # internal operations
    #

    def create_file_response(self, path):
        length, body = self.generate_file(path)
        suffix = self.get_suffix(path)
        if suffix in CONTENT_TYPE_MAP:
            content_type = CONTENT_TYPE_MAP[suffix]
        else:
            content_type = "text/plain"
        return self.create_response(200, content_type, length, body)

    def generate_file(self, path):
        gc.collect()
        return self.file_size(path), (lambda stream: self.stream_file(stream, path))

    def create_buffer(self):
        _block_size = self._block_size
        while True:
            if _block_size < 1:
                raise Exception("Unable to allocate buffer")
            try:
                return bytearray(_block_size)
            except MemoryError:
                _block_size //= 2

    def stream_file(self, stream, file):
        f = open(file, 'r')
        buf = self.create_buffer()
        while True:
            n = f.readinto(buf)
            if n:
                stream.write(buf[:n])
            else:
                break
        f.close()

    def effective_path(self, path):
        full_path = "{}/{}".format(self._root_path, path).rstrip('/')
        components = full_path.split('/')
        tmp = []
        for component in components:
            if component == '':
                pass
            elif component == "..":
                tmp = tmp[:len(tmp) - 1]
            elif component == '.':
                pass
            else:
                tmp.append(component)
        return "/{}".format('/'.join(tmp))

    @staticmethod
    def is_dir(path):
        try:
            os.listdir(path)
            return True
        except OSError:
            return False

    @staticmethod
    def exists(path):
        try:
            os.stat(path)
            return True
        except OSError:
            return False

    @staticmethod
    def create_message_response(code, message):
        data = "<html><body>{}</body></html>".format(message).encode('UTF-8')
        length = len(data)
        return FileProcess.create_response(code, "text/html", length, (lambda stream: FileProcess.stream_write(stream, data)))

    def create_dir_listing_response(self, absolute_path):
        length, body = self.generate_dir_listing(absolute_path)
        return self.create_response(200, "text/html", length, body)

    def generate_dir_listing(self, absolute_path):
        path = absolute_path[len(self._root_path):]
        if not path:
            path = '/'
        data = "<html><body><header><em>{}/{}</em><hr></header><h1>{}</h1><ul>".format(SERVER_NAME, VERSION, path)
        components = self.components(path)
        components_len = len(components)
        if components_len > 0:
            data += "<li><a href=\"{}\">..</a></li>\n".format(self.to_path(components[:components_len - 1]))
        files = os.listdir(absolute_path)
        for f in files:
            tmp = components.copy()
            tmp.append(f)
            data += "<li><a href=\"{}\">{}</a></li>\n".format(self.to_path(tmp), f)
        data += "</ul></body></html>"
        data = data.encode('UTF-8')
        return len(data), (lambda stream: FileProcess.stream_write(stream, data))

    def to_path(self, components):
        return "/{}".format("/".join(components))

    def components(self, path):
        f = lambda e: e != ''
        return self.filter(
            f, path.strip('/').split('/')
        )

    def filter(self, f, el):
        ret = []
        for e in el:
            if f(e):
                ret.append(e)
        return ret

    @staticmethod
    def stream_write(stream, data):
        return stream.write(data)

    @staticmethod
    def create_response(code, content_type, length, body):
        return {
            'code': code,
            'headers': {
                'content-type': content_type,
                #'content-length': length
            },
            'body': body
        }

    @staticmethod
    def file_size(path):
        return os.stat(path)[6]

    @staticmethod
    def get_suffix(path):
        idx = path.rfind('.')
        return "" if idx == -1 else path[idx:]

    @staticmethod
    def is_prefix(prefix, str):
        return len(prefix) <= len(str) and str[:len(prefix)] == prefix
