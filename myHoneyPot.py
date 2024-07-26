import socket
import logging
from email_alerts import send_email

# Configure logging
logging.basicConfig(filename='honeypot_logs/honeypot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Define the honeypot settings
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 9999        # Port to listen on

def handle_client(client_socket):
    try:
        logging.info(f"Connection established from {client_socket.getpeername()}")
        send_email("Honeypot Alert", f"Connection established from {client_socket.getpeername()}")
        client_socket.send(b"Welcome to the honeypot!\n")
        while True:
            data = client_socket.recv(1024)
            if not data:
                logging.info("Connection closed by client")
                break
            logging.info(f"Received data: {data.decode()}")
            client_socket.send(b"Data received.\n")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        client_socket.close()

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    logging.info(f"Honeypot listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        logging.info(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_honeypot()
