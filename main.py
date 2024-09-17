#!/usr/bin/python3

import socketserver
from http.server import BaseHTTPRequestHandler
import json
import os

class HandleRequest(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        test_cases = post_data['tests']

        test_case_directory = f'{os.getcwd()}/testCases'
        os.mkdir(test_case_directory, 0o777)

        test_case_count = 0
        for test_case in test_cases:
            test_case_count += 1

            test_case_input_location = f'{test_case_directory}/{test_case_count}.in'
            with open(test_case_input_location, 'w') as f:
                f.write(test_case['input'])

            test_case_output_location = f'{test_case_directory}/{test_case_count}.out'
            with open(test_case_output_location, 'w') as f:
                f.write(test_case['output'])


PORT = 10045

with socketserver.TCPServer(("", PORT), HandleRequest) as httpd:
    print("It works")
    httpd.serve_forever()