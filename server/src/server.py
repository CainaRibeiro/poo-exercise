from http.server import HTTPServer
from routes.router import RequestHandler


def run():
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Servidor rodando na porta {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
