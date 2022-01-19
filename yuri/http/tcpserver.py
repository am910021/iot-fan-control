import gc
import micropython, socket
from yuri.http.processor import Processor
from yuri.logger import logger

SO_REGISTER_HANDLER = 20


class TCPServer:
    def __init__(self, processor: Processor, config: dict):
        self._port = config['port']
        self._address = config['address']
        self._timeout = config['timeout']
        self._server_socket = None
        self._processor = processor

    def handle_accept(self, server_socket):
        gc.collect()
        client_socket, remote = server_socket.accept()
        logger.debug('remote:{} {}'.format(remote[0], remote[1]))
        client_socket.settimeout(self._timeout)
        try:
            done, callback = self._processor.handle_request(client_socket, remote)
            if callback:
                callback()
        except:
            pass
        finally:
            client_socket.close()


    def start(self):
        micropython.alloc_emergency_exception_buf(100)
        #
        # Start the listening socket.  Handle accepts asynchronously
        # in handle_accept/1
        #
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._address, self._port))
        self._server_socket.listen(5)
        self._server_socket.setsockopt(socket.SOL_SOCKET, SO_REGISTER_HANDLER, self.handle_accept)
        logger.info('Server listen on: {} , port: {}'.format(self._address, self._port))

    def stop(self):
        if self._server_socket:
            self._server_socket.close()
