import pathlib
import tempfile
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

IP = "127.0.0.1"
PORT = 8645

JWT_FILE = pathlib.Path('user-jwt.txt')


class RequestHandler(BaseHTTPRequestHandler):

    jwt_file = tempfile.TemporaryFile()

    def do_GET(self):
        """Serve a GET request."""
        url = urlparse(self.path)
        qs = parse_qs(url.query)
        jwt = qs['token'][0]
        JWT_FILE.write_text(jwt)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Success")
        self.server.shutdown()

    def log_message(self, format, *args):
        return


def interactive_login(url: str = 'https://auth.pollination.cloud/sdk-login') -> str:
    httpd = ThreadingHTTPServer((IP, PORT), RequestHandler)
    webbrowser.open_new(url)
    httpd.serve_forever()
    jwt = JWT_FILE.read_text()
    JWT_FILE.unlink()
    return jwt
