import http.server
import socketserver


class CorsHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()


# Specify the server port
port: int = 8080

# Create a socket server with the custom request handler
with socketserver.TCPServer(("0.0.0.0", port), CorsHandler) as httpd:
    print(f"Server listening on port {port}...")
    httpd.serve_forever()
