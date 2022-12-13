import asyncio
import socket
import threading
from email.parser import Parser

from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_error import Http_Error
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.log_service.log_service import Logger_Service, ERROR_LOG_LEVEL

MAX_LINE = 64*1024
MAX_HEADERS = 100


class CoreHttpServer:
        def __init__(self, port,
                     logger_service: Logger_Service,
                     host='0.0.0.0'):
            self.logger_service = logger_service
            self._host = host
            self._port = port
            self._users = {}
            self.handlers: {str, BaseExecutor} = {}

        def add_handler(self, path: str, callback: BaseExecutor):
            self.handlers[path] = callback

        def serve_forever(self):
            def run():
                serv_sock = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM,

                    proto=0)

                try:
                    serv_sock.bind((self._host, self._port))
                    serv_sock.listen()

                    while True:
                        conn, _ = serv_sock.accept()
                        try:
                            th = threading.Thread(target=self.serve_client(conn))
                            th.start()
                        except Exception as e:
                            self.logger_service.send_log(ERROR_LOG_LEVEL, self.__class__.__name__, f'Client starting failed: {e}')
                finally:
                    serv_sock.close()

            th = threading.Thread(target=run, name='http_server', daemon=True)
            th.start()

        def serve_client(self, conn):
            try:
                req = self.parse_request(conn)
                resp = self.handle_request(req)
                self.send_response(conn, resp)

            except ConnectionResetError:
                conn = None
            except Exception as e:
                self.send_error(conn, e)
                self.logger_service.send_log(ERROR_LOG_LEVEL, self.__class__.__name__, f'Request parse failed: {e}')

            if conn:
                req.rfile.close()
                conn.close()

        def parse_request(self, conn):
            rfile = conn.makefile('rb')
            method, target, ver = self.parse_request_line(rfile)
            headers = self.parse_headers(rfile)
            host = headers.get('Host')
            if not host:
                raise Http_Error(400, 'Bad request',
                                 'Host header is missing')
            return Http_Request(method, target, ver, headers, rfile)

        def parse_request_line(self, rfile):
            raw = rfile.readline(MAX_LINE + 1)
            if len(raw) > MAX_LINE:
                raise Http_Error(400, 'Bad request',
                                 'Request line is too long')

            req_line = str(raw, 'iso-8859-1')
            words = req_line.split()
            if len(words) != 3:
                raise Http_Error(400, 'Bad request',
                                 'Malformed request line')

            method, target, ver = words
            if ver != 'HTTP/1.1':
                raise Http_Error(505, 'HTTP Version Not Supported')
            return method, target, ver

        def parse_headers(self, rfile):
            headers = []
            while True:
                line = rfile.readline(MAX_LINE + 1)
                if len(line) > MAX_LINE:
                    raise Http_Error(494, 'Request header too large')

                if line in (b'\r\n', b'\n', b''):
                    break

                headers.append(line)
                if len(headers) > MAX_HEADERS:
                    raise Http_Error(494, 'Too many headers')

            sheaders = b''.join(headers).decode('iso-8859-1')
            return Parser().parsestr(sheaders)

        def handle_request(self, req: Http_Request):
            path = req.path
            if path in self.handlers:
                return self.handlers[path].generate(req)

            raise Http_Error(404, 'Not found')

        def send_response(self, conn, resp):
            wfile = conn.makefile('wb')
            status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
            wfile.write(status_line.encode('iso-8859-1'))

            if resp.headers:
                for (key, value) in resp.headers:
                    header_line = f'{key}: {value}\r\n'
                    wfile.write(header_line.encode('iso-8859-1'))

            wfile.write(b'\r\n')

            if resp.body:
                wfile.write(resp.body)

            wfile.flush()
            wfile.close()

        def send_error(self, conn, err):
            try:
                status = err.status
                reason = err.reason
                body = (err.body or err.reason).encode('utf-8')
            except:
                status = 500
                reason = b'Internal Server Error'
                body = b'Internal Server Error'
            resp = Http_Response(status, reason,
                                 [('Content-Length', len(body))],
                                 body)
            self.send_response(conn, resp)



