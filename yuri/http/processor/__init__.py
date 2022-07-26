import gc
import sys
from yuri.logger import logger
from ..share import *

logger.set_levels([0, 1, 2, 3])


class Processor:
    DEBUG_MODE = False

    def __init__(self, handlers: list, config: dict):
        self._handlers = handlers
        self._config = config
        self._debug = self._config['debug']
        Processor.DEBUG_MODE = self._debug
        logger.info('Http processor initialize finish, waiting tcp server setup.')
        if self._debug:
            logger.info('Http processor running on developer mode.')

    def handle_request(self, client_socket, tcp_request):
        http_request = dict(tcp_request)
        http_request['debug'] = self._debug
        http_request['ver'] = VERSION

        try:
            gc.collect()

            heading = self.parse_heading(client_socket.readline().decode('UTF-8'))
            http_request.update(heading)

            path = http_request['path']
            handler = None
            for prefix, h in self._handlers:
                if path.startswith(prefix):
                    # request['relative_path'] = path[len(prefix):]
                    http_request['prefix'] = prefix
                    handler = h
                    break

            headers = {}
            num_headers = 0
            len_str = 'content-length'
            while True:
                line = client_socket.readline()
                # 如果num_headers小於max_headers，就正常執行。
                if num_headers < self._config['max_headers']:
                    if not line or line == b'\r\n':
                        break
                    k, v = Processor.parse_header(line.decode('UTF-8'))
                    headers[k.lower()] = v
                    num_headers += 1
                # 如果heards大於max_headers就清空socket剩下的暫存，並發出http 400。 沒清空暫存socket會錯誤。
                else:
                    if not line or line == b'\r\n':
                        if len_str in headers:
                            client_socket.read(int(headers[len_str]))
                        raise BadRequestException("Headers size exceeds maximum allowable")
                    elif len_str in line:
                        headers = {}
                        k, v = Processor.parse_header(line.decode('UTF-8'))
                        headers[k.lower()] = v

            http_request['headers'] = headers
            #
            # 標頭封包有資料(content_length)就讀取內容(content)
            #
            content_length = 0
            if len_str in headers:
                content_length = int(headers[len_str])
            # 上傳的資料、檔案的大小超過max_content_length就清空socket剩下的暫存，並發出http 400。 沒清空暫存socket會錯誤。
            if content_length > self._config['max_content_length']:
                client_socket.read(content_length)
                raise BadRequestException("Content size exceeds maximum allowable")
            if content_length > 0:
                body = client_socket.read(content_length)
                http_request['body'] = body
            #
            # 如果handler不存在，就送出NotFoundException,http 404。
            #
            if not handler:
                raise NotFoundException("No Handler for path {}".format(path))

            #
            # 判斷是否要執行帳號/密碼驗證
            #
            if self._config['require_auth']:
                if 'authorization' not in headers:
                    return self.unauthorized_error(client_socket)
                else:
                    remote = tcp_request['remote']
                    if not self.is_authorized(headers['authorization']):
                        logger.info("UNAUTHORIZED {}".format(remote))
                        return self.unauthorized_error(client_socket)
                    else:
                        logger.info("AUTHORIZED {}".format(remote))
            #
            # 一切正常，執行最後的handle_request
            #
            return self.response(client_socket, handler.handle_request(http_request))
        except BadRequestException as e:
            sys.print_exception(e)
            return Processor.error(client_socket, 400, "Bad Request: {}".format(e), e)
        except ForbiddenException as e:
            return Processor.error(client_socket, 403, "Forbidden: {}".format(e), e)
        except NotFoundException as e:
            return Processor.error(client_socket, 404, "Not Found: {}".format(e), e)
        except BufferOverflowException as e:
            return Processor.error(client_socket, 503, "Service Unavailable: {}".format(e), e)
        except BaseException as e:
            sys.print_exception(e)
            return Processor.error(client_socket, 500, "Internal Server Error: {}".format(e), e)
        finally:
            gc.collect()

    @staticmethod
    def parse_heading(line):
        ra = line.split()
        if len(ra) < 3:
            raise BadRequestException("IndexError")
        return {'verb': ra[0].lower(), 'path': ra[1], 'protocol': ra[2]}

    @staticmethod
    def parse_header(line):
        index = line.find(": ")
        return line[:index], line[index+2:-2]

    def is_authorized(self, authorization):
        import ubinascii
        try:
            tmp = authorization.split()
            if tmp[0].lower() == "basic":
                ra = ubinascii.a2b_base64(tmp[1].strip().encode()).decode().split(':')
                return ra[0] == self._config['user'] and ra[1] == self._config['password']
            else:
                raise BadRequestException("Unsupported authorization method.")
        except:
            raise BadRequestException("authorization failed.")

    @staticmethod
    def server_name():
        return "{}/{}".format(SERVER_NAME, VERSION)

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
        elif code == 503:
            return "Service Unavailable"
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
        stream.write("{}\r\n{}\r\n".format(
            Processor.format_heading(response['code']),
            Processor.format_headers(dict_update(response['headers'], {'Server': Processor.server_name()}))
        ).encode('UTF-8'))
        #
        # Write the body, if it's present
        #
        if 'body' in response:
            body = response['body']
            if body:
                body(stream)

    def unauthorized_error(self, client_socket):
        return Processor.error(client_socket, 401, "Unauthorized", None, {'www-authenticate': "Basic realm={}".format(self._config['realm'])})

    @staticmethod
    def error(client_socket, code, error_message, e, headers={}):
        response = Processor.generate_error_response(code,
                                                     lambda stream: Processor.stream_error(stream, error_message, e),
                                                     headers)
        return Processor.response(client_socket, response)

    @staticmethod
    def stream_error(stream, error_message, e):
        stream.write(error_message)
        if e and Processor.DEBUG_MODE:
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
        return {
            'code': code,
            'headers': dict_update({
                'content-type': "text/html",
            }, headers),
            'body': lambda stream: Processor.write_html(stream,
                                                        '<html><body><header>{}/{}<hr></header>'.format(SERVER_NAME, VERSION).encode('UTF-8'),
                                                        ef,
                                                        '</body></html>'.encode('UTF-8'))
        }

    @staticmethod
    def write_html(stream, data1, ef, data2):
        stream.write(data1)
        ef(stream)
        stream.write(data2)
