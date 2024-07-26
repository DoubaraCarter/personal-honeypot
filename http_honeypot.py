from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from email_alerts import send_email

# Configure logging
logging.basicConfig(filename='honeypot_logs/http_honeypot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"Received GET request from {self.client_address}")
        send_email("HTTP Honeypot Alert", f"Received GET request from {self.client_address}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Welcome to the HTTP honeypot!")

    def log_message(self, format, *args):
        logging.info("%s - - [%s] %s\n" %
                     (self.client_address[0],
                      self.log_date_time_string(),
                      format % args))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f'Starting HTTP honeypot on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
