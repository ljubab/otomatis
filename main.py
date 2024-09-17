#!/usr/bin/python3

import socketserver
from http.server import BaseHTTPRequestHandler

class HandleRequest(BaseHTTPRequestHandler):
    def do_POST(self):
        print("pong!")
        self.send_response(200)

PORT = 10045

with socketserver.TCPServer(("", PORT), HandleRequest) as httpd:
    print("It works")
    httpd.serve_forever()