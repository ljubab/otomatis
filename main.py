#!/usr/bin/python3

import socketserver
from http.server import BaseHTTPRequestHandler
import json
import os
import subprocess

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

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

PORT = 10045

with ReusableTCPServer(("", PORT), HandleRequest) as httpd:
    print("It works")
    httpd.handle_request()

def compile(sourceCode):
    compile_command = ["g++", "-std=c++17", f"{sourceCode}.cpp", "-o", sourceCode]
    result = subprocess.run(compile_command, capture_output=True)

    if(result.stderr):
        print(result.stderr.decode("utf-8"))

def run(sourceCode):
    compile(sourceCode)

    test_cases_folder = os.listdir("testCases")
    num_of_test_cases = len([file for file in test_cases_folder if os.path.isfile(os.path.join("./testCases", file))]) // 2

    num_of_wrong_test_cases = 0

    for i in range(1, num_of_test_cases + 1):
        with open(f"testCases/{i}.in", "r") as infile:
            main_process = subprocess.Popen(
                [f"./{sourceCode}"], 
                stdin=infile, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )

            diff_process = subprocess.Popen(
                ["diff", "-wB", "-", f"testCases/{i}.out"], 
                stdin=main_process.stdout, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )

            main_process.stdout.close()
            diff_output, _ = diff_process.communicate()

            if diff_output:
                num_of_wrong_test_cases += 1
    
    print(f"Number of wrong test cases: {num_of_wrong_test_cases}")

run("main")