import socket
import os

def send_file(conn, filename):
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            conn.send(data)
            data = file.read(1024)

def main():
    host = '192.168.56.8'  # Listen on all available interfaces
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        filename = '/home/pi/STM/output.xlsx'
        
        if os.path.exists(filename):
            conn.send(b'File exists')  # Notify the client that the file exists
            send_file(conn, filename)
            print(f"File {filename} sent successfully.")
        else:
            conn.send(b'File does not exist')  # Notify the client that the file does not exist
            print(f"File {filename} does not exist.")

        conn.close()

if __name__ == "__main__":
    main()
