from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

port = 443


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Pozdrawiam dobrych chlopakow')







httpd = HTTPServer(('localhost', port), MyHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               keyfile="privkeyA.pem",
                               certfile="certA.crt",)

print(f"server listening on port {port}")
httpd.serve_forever()

# https://localhost:8887