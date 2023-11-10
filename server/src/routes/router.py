from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        url = urlparse(self.path)

        if url.path == '/':
            response = 'TESTE'
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('NOT FOUND'.encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))