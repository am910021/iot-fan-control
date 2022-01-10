import gc, sys
from yuri.logger import logger


VERSION = "0.2"
SERVER_NAME = "Yuri's Http Server"


class NotFoundException(Exception):
    pass


class BadRequestException(Exception):
    pass


class ForbiddenException(Exception):
    pass


def get_relative_path(http_request):
    path = http_request['path']
    prefix = http_request['prefix']
    return path[len(prefix):]


class Processor:
    def __init__(self, handlers:list, config: dict):
        self._handlers = handlers
        self._config = config
        self._dev = self._config['dev']

    def handle_request(self, client_socket, tcp_request):
        http_request = {
            'tcp': tcp_request,
            'dev': self._dev
        }
        try:
            gc.collect()
            #
            # parse out the heading line, to get the verb, path, and protocol
            #
            heading = self.parse_heading(client_socket.readline().decode('UTF-8'))
            http_request.update(heading)
            #
            # find the handler for the specified path.  If we don't have
            # one registered, we raise a NotFoundException, but only after
            # reading the payload.
            #
            path = http_request['path']
            handler = None
            for prefix, h in self._handlers:
                if path.startswith(prefix):
                    # request['relative_path'] = path[len(prefix):]
                    http_request['prefix'] = prefix
                    handler = h
                    break
            #
            # Parse out the headers
            #
            headers = {}
            num_headers = 0
            while True:
                line = client_socket.readline()
                if not line or line == b'\r\n':
                    break
                k, v = Processor.parse_header(line.decode('UTF-8'))
                headers[k.lower()] = v
                num_headers += 1
                if num_headers > self._config['max_headers']:
                    raise BadRequestException("Number of headers exceeds maximum allowable")
            http_request['headers'] = headers
            #
            # If the headers have a content length, then read the body
            #
            content_length = 0
            if 'content-length' in headers:
                content_length = int(headers['content-length'])
            if content_length > self._config['max_content_length']:
                raise BadRequestException("Content size exceeds maximum allowable")
            if content_length > 0:
                body = client_socket.read(content_length)
                http_request['body'] = body
            #
            # If there is no handler, then raise a NotFound exception
            #
            if not handler:
                raise NotFoundException("No Handler for path {}".format(path))

            #
            # 判斷是否要執行帳號/密碼驗證
            #
            if self._config['require_auth']:
                if 'authorization' not in headers:
                    return self.unauthorized_error(client_socket)

                remote = tcp_request['remote']
                if not self.is_authorized(headers['authorization']):
                    logger.info("UNAUTHORIZED {}".format(remote))
                    return self.unauthorized_error(client_socket)

                logger.info("AUTHORIZED {}".format(remote))

            #
            # get the response from the active handler and serialize it
            #
            response = handler.handle_request(http_request)
            return self.response(client_socket, response)
        except BadRequestException as e:
            print(1)
            return Processor.bad_request_error(client_socket, e)
        except ForbiddenException as e:
            print(2)
            return Processor.forbidden_error(client_socket, e)
        except NotFoundException as e:
            print(3)
            return Processor.not_found_error(client_socket, e)
        except BaseException as e:
            print(4)
            return Processor.internal_server_error(client_socket, e)
        except NameError as e:
            return Processor.internal_server_error(client_socket, e)
        finally:
            print(6)
            gc.collect()

    #
    # Internal operations
    #

    @staticmethod
    def parse_heading(line):
        ra = line.split()
        try:
            return {
                'verb': ra[0].lower(),
                'path': ra[1],
                'protocol': ra[2]
            }
        except IndexError:
            raise BadRequestException()

    @staticmethod
    def parse_header(line):
        ra = line.split(":")
        return ra[0].strip(), ra[1].strip()

    def is_authorized(self, authorization):
        import ubinascii
        try:
            tmp = authorization.split()
            if tmp[0].lower() == "basic":
                ra = ubinascii.a2b_base64(tmp[1].strip().encode()).decode().split(':')
                return ra[0] == self._config['user'] and ra[1] == self._config[
                    'password']
            else:
                raise BadRequestException(
                    "Unsupported authorization method: {}".format(tmp[0]))
        except Exception as e:
            raise BadRequestException(e)

    @staticmethod
    def server_name():
        return "{}/{} (running in your devices)".format(SERVER_NAME, VERSION)

    @staticmethod
    def format_heading(code):
        return "HTTP/1.1 {} {}".format(code, Processor.lookup_code(code))

    @staticmethod
    def lookup_code(code):
        if code == 200:
            return "OK"
        elif code == 400:
            return "Bad Request"
        elif code == 401:
            return "Unauthorized"
        elif code == 403:
            return "Forbidden"
        elif code == 404:
            return "Not Found"
        elif code == 500:
            return "Internal Server Error"
        else:
            return "Unknown"

    @staticmethod
    def format_headers(headers):
        ret = ""
        for k, v in headers.items():
            ret += "{}: {}\r\n".format(k, v)
        return ret

    @staticmethod
    def response(client_socket, response):
        Processor.serialize(client_socket, response)
        return True, None

    @staticmethod
    def serialize(stream, response):
        #
        # write the heading and headers
        #
        response['headers']['Server'] = Processor.server_name()
        stream.write("{}\r\n{}\r\n".format(
            Processor.format_heading(response['code']),
            Processor.format_headers(response)
        ).encode('UTF-8'))
        #
        # Write the body, if it's present
        #
        if 'body' in response:
            body = response['body']
            if body:
                body(stream)

    def unauthorized_error(self, client_socket):
        headers = {
            'www-authenticate': "Basic realm={}".format(self._config['realm'])
        }
        return Processor.error(client_socket, 401, "Unauthorized", None, headers)

    @staticmethod
    def bad_request_error(client_socket, e):
        error_message = "Bad Request {}:".format(e)
        return Processor.error(client_socket, 400, error_message, e)

    @staticmethod
    def forbidden_error(client_socket, e):
        error_message = "Forbidden {}:".format(e)
        return Processor.error(client_socket, 403, error_message, e)

    @staticmethod
    def not_found_error(client_socket, e):
        error_message = "Not Found: {}".format(e)
        return Processor.error(client_socket, 404, error_message, e)

    @staticmethod
    def internal_server_error(client_socket, e):
        # sys.print_exception(e)
        logger.error(Processor.stacktrace(e).decode())
        error_message = "Internal Server Error: {}".format(e)
        return Processor.error(client_socket, 500, error_message, e)

    @staticmethod
    def error(client_socket, code, error_message, e, headers):
        ef = lambda stream: Processor.stream_error(stream, error_message, e)
        response = Processor.generate_error_response(code, ef, headers={})
        return Processor.response(response)

    @staticmethod
    def stream_error(stream, error_message, e):
        stream.write(error_message)
        if e:
            stream.write('<pre>')
            stream.write(Processor.stacktrace(e))
            stream.write('</pre>')

    @staticmethod
    def stacktrace(e):
        import uio
        buf = uio.BytesIO()
        sys.print_exception(e, buf)
        return buf.getvalue()

    @staticmethod
    def generate_error_response(code, ef, headers={}):
        data1 = '<html><body><header>{}/{}<hr></header>'.format(SERVER_NAME, VERSION).encode('UTF-8')
        # message data in ef will go here
        data2 = '</body></html>'.encode('UTF-8')
        return {
            'code': code,
            'headers': Processor.update({
                'content-type': "text/html",
            }, headers),
            'body': lambda stream: Processor.write_html(stream, data1, ef, data2)
        }

    @staticmethod
    def write_html(stream, data1, ef, data2):
        stream.write(data1)
        ef(stream)
        stream.write(data2)
