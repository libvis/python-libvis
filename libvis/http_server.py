#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import sys
import libvis
from pathlib import Path

p = Path(libvis.__file__)

pywebvis_path = p.parent / 'front_build'

def get_path(path):
    #if path in ['/','']:
    #    path = './index.html'
    return str(pywebvis_path) + path

def read_file(fname):
    with open(fname,'rb') as f:
        page = f.read()
    return page

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        query = urlparse(self.path).path
        self._set_headers()
        try:
            path = get_path(query)
            try:
                page = read_file(path)
            except:
                page = read_file(get_path('/index.html'))

            self.wfile.write(page)
        except Exception as e:
            self.wfile.write(bytes(str(e),'utf-8'))

    def do_HEAD(self):
        self._set_headers()

def create_server(server_class=HTTPServer, handler_class=Server, addr='', port=80):
    server_address = (addr, port)
    try:
        httpd = server_class(server_address, handler_class)
    except OSError as ose:
        print(f"HTTPServer start on {port} failed: {ose}", file=sys.stderr)
        raise
    return httpd

def run(server_class=HTTPServer, handler_class=Server, port=80):
    httpd = create_server(server_class, handler_class, port)
    httpd.serve_forever()

def start_server(port):
    run(port=port)

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
