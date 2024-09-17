#!/usr/bin/python3

import socketserver
from http.server import SimpleHTTPRequestHandler

PORT = 10045

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("It works")
    httpd.serve_forever()