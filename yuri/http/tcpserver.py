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

    def handle_receive(self, client_socket, tcp_request):
        gc.collect()
        try:
            done, response = self._processor.handle_request(client_socket, tcp_request)
            if response and len(response) > 0:
                client_socket.write(response)
            if done:
                client_socket.close()
                return False
            else:
                self._client_socket = client_socket
                return True
        except:
            client_socket.close()
            self._client_socket = None
            return False
        gc.collect()
        logger.info('Memory allow:{}'.format(gc.mem_free()))

    def handle_accept(self, server_socket):
        client_socket, remote_addr = server_socket.accept()
        client_socket.settimeout(self._timeout)
        tcp_request = {'remote': remote_addr}
        while self.handle_receive(client_socket, tcp_request):
            pass

    def start(self):
        micropython.alloc_emergency_exception_buf(100)
        #
        # Start the listening socket.  Handle accepts asynchronously
        # in handle_accept/1
        #
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._address, self._port))
        self._server_socket.listen(0)
        self._server_socket.setsockopt(socket.SOL_SOCKET, SO_REGISTER_HANDLER, self.handle_accept)
        logger.info('Server listen on: {} , port: {}'.format(self._address, self._port))

    def stop(self):
        if self._server_socket:
            self._server_socket.close()
