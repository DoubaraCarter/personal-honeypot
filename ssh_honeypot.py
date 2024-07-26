import paramiko
import logging
import socket
import threading
from email_alerts import send_email

# Configure logging
logging.basicConfig(filename='honeypot_logs/ssh_honeypot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class SSHHandler(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        logging.info(f"Attempted login with username: {username} and password: {password}")
        send_email("SSH Honeypot Alert", f"Attempted login with username: {username} and password: {password}")
        return paramiko.AUTH_FAILED

def handle_ssh_connection(client_socket):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey.generate(2048))
        server = SSHHandler()
        transport.start_server(server=server)
        channel = transport.accept()
        if channel:
            logging.info("SSH connection accepted")
            while True:
                data = channel.recv(1024)
                if not data:
                    break
                logging.info(f"Received data: {data.decode()}")
                channel.send(b"Data received.")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        client_socket.close()

def start_ssh_honeypot(port=22):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    logging.info(f"SSH honeypot listening on port {port}")

    while True:
        client_socket, _ = server.accept()
        threading.Thread(target=handle_ssh_connection, args=(client_socket,)).start()

if __name__ == "__main__":
    start_ssh_honeypot()
