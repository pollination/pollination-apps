import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

IP = "127.0.0.1"
PORT = 8645


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Serve a GET request."""
        url = urlparse(self.path)
        qs = parse_qs(url.query)
        jwt = qs['token'][0]
        self.wfile.write("Success".encode('utf-8'))
        self.server.jwt = jwt


def interactive_login(url: str = 'https://auth.staging.pollination.cloud/sdk-login') -> str:
    httpd = HTTPServer((IP, PORT), RequestHandler)
    webbrowser.open_new(url)
    httpd.handle_request()
    # pylint: disable=no-member
    return httpd.jwt
