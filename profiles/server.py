#!/usr/bin/env python3
# encoding: utf-8

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header(
            'Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(data).encode())


httpd = HTTPServer(('localhost', 8003), CORSRequestHandler)
httpd.serve_forever()
