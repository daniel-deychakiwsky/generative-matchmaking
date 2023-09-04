#  type: ignore

import http.server
import json
import os
import socketserver


def list_files(startpath):
    file_structure = {}

    for root, _, files in os.walk(startpath)[:10]:
        path_parts = root.split(os.sep)[1:]  # Cut off the '.' part
        d = file_structure
        for part in path_parts:
            d = d.setdefault(part, {})

        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
            d[file_name] = content

    return file_structure


class CorsHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", "application/json")
        super().end_headers()

    def do_get(self):
        self.send_response(200)
        self.end_headers()

        # Directly specifying the profiles directory
        directory_structure = list_files("./profiles")
        json_structure = json.dumps(directory_structure)

        self.wfile.write(json_structure.encode("utf-8"))


# Specify the server port
port = 8080

# Create a socket server with the custom request handler
with socketserver.TCPServer(("0.0.0.0", port), CorsHandler) as httpd:
    print(f"Server listening on port {port}...")
    httpd.serve_forever()
